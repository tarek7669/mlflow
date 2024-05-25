import time
import uuid
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from mlflow.entities import Evaluation as EvaluationEntity
from mlflow.entities import Metric
from mlflow.evaluation.evaluation import Evaluation, Feedback
from mlflow.evaluation.utils import (
    dataframes_to_evaluations,
    evaluations_to_dataframes,
    read_evaluations_dataframe,
    read_feedback_dataframe,
    read_metrics_dataframe,
)
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INTERNAL_ERROR, RESOURCE_DOES_NOT_EXIST
from mlflow.tracking.client import MlflowClient
from mlflow.tracking.fluent import _get_or_start_run


def log_evaluation(
    *,
    inputs: Dict[str, Any],
    outputs: Dict[str, Any],
    inputs_id: Optional[str] = None,
    request_id: Optional[str] = None,
    ground_truths: Optional[Dict[str, Any]] = None,
    feedback: Optional[Union[List[Feedback], List[Dict[str, Any]]]] = None,
    metrics: Optional[Union[List[Metric], Dict[str, float]]] = None,
    run_id: Optional[str] = None,
):
    """
    Logs an evaluation to an MLflow Run.

    Args:
      inputs (Dict[str, Any]): Input fields used by the model to compute outputs.
      outputs (Dict[str, Any]): Outputs computed by the model.
      inputs_id (Optional[str]): Unique identifier for the evaluation `inputs`. If not specified,
          a unique identifier is generated by hashing the inputs.
      request_id (Optional[str]): ID of an MLflow Trace corresponding to the inputs and outputs.
          If specified, displayed in the MLflow UI to help with root causing issues and identifying
          more granular areas for improvement when reviewing the evaluation and adding feedback.
      ground_truths (Optional[Dict[str, Any]]): Ground truths corresponding to one or more of the
          evaluation `outputs`. Helps root cause issues when reviewing the evaluation and adding
          feedback.
      feedback (Optional[Union[List[Feedback], List[Dict[str, Any]]]]): Feedback on the evaluation,
          e.g., relevance of documents retrieved by a RAG model to a user input query, as assessed
          by an LLM Judge.
      metrics (Optional[Union[List[Metric], Dict[str, float]]]): Numerical metrics for the
          evaluation, e.g., "number of input tokens", "number of output tokens".
      run_id (Optional[str]): ID of the MLflow Run to log the evaluation. If unspecified, the
          current active run is used.
    """
    if feedback and isinstance(feedback[0], dict):
        if not all(isinstance(fb, dict) for fb in feedback):
            raise ValueError(
                "If `feedback` contains a dictionary, all elements must be dictionaries."
            )
        feedback = [Feedback.from_dictionary(fb) for fb in feedback]

    if metrics and isinstance(metrics, dict):
        metrics = [
            Metric(key=k, value=v, timestamp=time.time() * 1000, step=0) for k, v in metrics.items()
        ]

    evaluation = Evaluation(
        inputs=inputs,
        outputs=outputs,
        inputs_id=inputs_id,
        request_id=request_id,
        ground_truths=ground_truths,
        feedback=feedback,
        metrics=metrics,
    )

    log_evaluations(evaluations=[evaluation], run_id=run_id)


def log_evaluations(*, evaluations: List[Evaluation], run_id: Optional[str] = None):
    """
    Logs one or more evaluations to an MLflow Run.

    Args:
      evaluations (List[Evaluation]): List of one or more MLflow Evaluation objects.
      run_id (Optional[str]): ID of the MLflow Run to log the evaluation. If unspecified, the
          current active run is used.
    """
    run_id = run_id if run_id is not None else _get_or_start_run().info.run_id
    evaluation_entities = [
        evaluation._to_entity(run_id=run_id, evaluation_id=uuid.uuid4().hex)
        for evaluation in evaluations
    ]
    evaluations_df, metrics_df, feedback_df = evaluations_to_dataframes(evaluation_entities)
    MlflowClient().log_table(run_id=run_id, data=evaluations_df, artifact_file="_evaluations.json")
    MlflowClient().log_table(run_id=run_id, data=metrics_df, artifact_file="_metrics.json")
    MlflowClient().log_table(run_id=run_id, data=feedback_df, artifact_file="_feedback.json")
    return evaluation_entities


def log_evaluations_df(
    *,
    run_id: str,
    evaluations_df: pd.DataFrame,
    input_cols: List[str],
    output_cols: List[str],
    inputs_id_col: Optional[str] = None,
    ground_truth_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Logs one or more evaluations from a DataFrame to an MLflow Run.

    Args:
      run_id (str): ID of the MLflow Run to log the Evaluations.
      evaluations_df (pd.DataFrame): Pandas DataFrame containing the evaluations to log.
          Must contain the columns specified in `input_cols`, `output_cols`, and
          `ground_truth_cols`.
          Additionally, evaluation information will be read from the following optional columns,
          if specified (see documentation for the log_evaluations() API):
              - "inputs_id": Unique identifier for evaluation inputs.
              - "request_id": ID of an MLflow trace corresponding to the evaluation inputs and
                  outputs.
              - "metrics": Numerical evaluation metrics, represented as a list of MLflow Metric
                  objects or as a dictionary.
      input_cols (List[str]): Names of columns containing input fields for evaluation.
      output_cols (List[str]): Names of columns containing output fields for evaluation.
      inputs_id_col (Optional[str]): Name of the column containing unique identifiers for the
          inputs. If not specified, a unique identifier is generated by hashing the inputs.
      ground_truth_cols (Optional[List[str]]): Names of columns containing ground truths for
          evaluation.

    Returns:
      pd.DataFrame: The specified evaluations DataFrame, with an additional "evaluation_id" column
          containing the IDs of the logged evaluations.
    """
    # Extract columns for Evaluation objects
    eval_data = evaluations_df[input_cols + output_cols]
    ground_truth_data = evaluations_df[ground_truth_cols] if ground_truth_cols else None

    # Create a list of Evaluation objects
    evaluations = []
    for _, row in eval_data.iterrows():
        inputs = row[input_cols].to_dict()
        outputs = row[output_cols].to_dict()
        ground_truths = row[ground_truth_cols].to_dict() if ground_truth_data is not None else None
        inputs_id = row[inputs_id_col] if inputs_id_col else None
        evaluations.append(
            Evaluation(
                inputs=inputs,
                outputs=outputs,
                inputs_id=inputs_id,
                ground_truths=ground_truths,
            )
        )

    # Log evaluations
    evaluation_entities = log_evaluations(evaluations=evaluations, run_id=run_id)

    # Add evaluation_id column to main DataFrame for the result
    evaluations_df["evaluation_id"] = [
        eval_entity.evaluation_id for eval_entity in evaluation_entities
    ]

    return evaluations_df


def log_feedback(
    *,
    evaluation_id: str,
    feedback: Union[Feedback, List[Feedback], Dict[str, Any], List[Dict[str, Any]]],
    run_id: Optional[str] = None,
):
    """
    Logs feedback to an existing Evaluation.

    Args:
        evaluation_id (str): The ID of the evaluation.
        feedback (Union[Feedback, List[Feedback], Dict[str, Any], List[Dict[str, Any]]]):
            An MLflow Feedback object, a dictionary representation of MLflow Feedback objects,
            or a list of these objects / dictionaries.
        run_id (Optional[str]): ID of the MLflow Run to log the feedback. If unspecified, the
            current active run is used.
    """
    run_id = run_id if run_id is not None else _get_or_start_run().info.run_id
    # Fetch the evaluation from the run to verify that it exists
    get_evaluation(run_id=run_id, evaluation_id=evaluation_id)
    client = MlflowClient()

    if isinstance(feedback, dict):
        feedback = [Feedback.from_dictionary(feedback)]
    elif isinstance(feedback, list) and any(isinstance(fb, dict) for fb in feedback):
        if not all(isinstance(fb, dict) for fb in feedback):
            raise ValueError(
                "If `feedback` contains a dictionary, all elements must be dictionaries."
            )
        feedback = [Feedback.from_dictionary(fb) for fb in feedback]
    feedback = [fb._to_entity(evaluation_id=evaluation_id) for fb in feedback]

    feedback_file = client.download_artifacts(run_id=run_id, path="_feedback.json")
    feedback_df = pd.read_json(feedback_file, orient="split")
    for feedback_item in feedback:
        feedback_df = _add_feedback_to_df(
            feedback_df=feedback_df, feedback=feedback_item, evaluation_id=evaluation_id
        )

    with client._log_artifact_helper(run_id, "_feedback.json") as tmp_path:
        feedback_df.to_json(tmp_path, orient="split")


def _add_feedback_to_df(
    feedback_df: pd.DataFrame, feedback: Feedback, evaluation_id: str
) -> pd.DataFrame:
    """
    Adds or updates feedback in the DataFrame.

    Args:
        feedback_df (pd.DataFrame): The DataFrame containing existing feedback.
        feedback (Feedback): The new feedback to add or update.
        evaluation_id (str): The ID of the evaluation.

    Returns:
        pd.DataFrame: The updated DataFrame with the new or updated feedback.
    """
    # Check if feedback already exists
    existing_feedback_index = feedback_df[
        (feedback_df["evaluation_id"] == evaluation_id)
        & (feedback_df["name"] == feedback.name)
        & (feedback_df["source"] == feedback.source.to_dictionary())
    ].index

    feedback_dict = feedback.to_dictionary()
    feedback_dict["evaluation_id"] = evaluation_id

    if not existing_feedback_index.empty:
        # Update existing feedback
        feedback_df.loc[existing_feedback_index, feedback_dict.keys()] = feedback_dict.values()
    else:
        # Append new feedback
        feedback_df = feedback_df.append(feedback_dict, ignore_index=True)

    return feedback_df


def get_evaluation(run_id: str, evaluation_id: str) -> EvaluationEntity:
    """
    Retrieves an Evaluation object from an MLflow Run.

    Args:
        run_id (str): ID of the MLflow Run containing the evaluation.
        evaluation_id (str): The ID of the evaluation.

    Returns:
        Evaluation: The Evaluation object.
    """

    def _contains_evaluation_artifacts(client: MlflowClient, run_id: str) -> bool:
        return (
            any(file.path == "_evaluations.json" for file in client.list_artifacts(run_id))
            and any(file.path == "_metrics.json" for file in client.list_artifacts(run_id))
            and any(file.path == "_feedback.json" for file in client.list_artifacts(run_id))
        )

    client = MlflowClient()
    if not _contains_evaluation_artifacts(client, run_id):
        raise MlflowException(
            "The specified run does not contain any evaluations. "
            "Please log evaluations to the run before retrieving them.",
            error_code=RESOURCE_DOES_NOT_EXIST,
        )

    evaluations_file = client.download_artifacts(run_id=run_id, path="_evaluations.json")
    evaluations_df = read_evaluations_dataframe(evaluations_file)

    evaluation_row = evaluations_df[evaluations_df["evaluation_id"] == evaluation_id]
    if evaluation_row.empty:
        raise MlflowException(
            f"The specified evaluation ID '{evaluation_id}' does not exist in the run '{run_id}'.",
            error_code=RESOURCE_DOES_NOT_EXIST,
        )

    # Extract metrics and feedback
    metrics_file = client.download_artifacts(run_id=run_id, path="_metrics.json")
    metrics_df = read_metrics_dataframe(metrics_file)
    # metrics_list = metrics_df[metrics_df["evaluation_id"] == evaluation_id].to_dict(
    #     orient="records"
    # )
    # evaluation_dict["metrics"] = metrics_list

    feedback_file = client.download_artifacts(run_id=run_id, path="_feedback.json")
    feedback_df = read_feedback_dataframe(feedback_file)
    # feedback_list = feedback_df[feedback_df["evaluation_id"] == evaluation_id].to_dict(
    #     orient="records"
    # )
    # evaluation_dict["feedback"] = feedback_list

    evaluations: List[Evaluation] = dataframes_to_evaluations(
        evaluations_df=evaluations_df, metrics_df=metrics_df, feedback_df=feedback_df
    )
    if len(evaluations) != 1:
        raise MlflowException(
            f"Expected to find a single evaluation with ID '{evaluation_id}', but found "
            f"{len(evaluations)} evaluations.",
            error_code=INTERNAL_ERROR,
        )

    return evaluations[0]
