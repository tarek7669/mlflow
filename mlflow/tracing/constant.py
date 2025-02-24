# NB: These keys are placeholders and subject to change
class TraceMetadataKey:
    INPUTS = "mlflow.traceInputs"
    OUTPUTS = "mlflow.traceOutputs"
    SOURCE_RUN = "mlflow.sourceRun"


class TraceTagKey:
    TRACE_NAME = "mlflow.traceName"
    EVAL_REQUEST_ID = "eval.requestId"


# A set of reserved attribute keys
class SpanAttributeKey:
    EXPERIMENT_ID = "mlflow.experimentId"
    REQUEST_ID = "mlflow.traceRequestId"
    INPUTS = "mlflow.spanInputs"
    OUTPUTS = "mlflow.spanOutputs"
    SPAN_TYPE = "mlflow.spanType"
    FUNCTION_NAME = "mlflow.spanFunctionName"
    START_TIME_NS = "mlflow.spanStartTimeNs"
    # these attributes are for standardized chat messages and tool definitions
    # in CHAT_MODEL and LLM spans. they are used for rendering the rich chat
    # display in the trace UI, as well as downstream consumers of trace data
    # such as evaluation
    CHAT_MESSAGES = "mlflow.chat.messages"
    CHAT_TOOLS = "mlflow.chat.tools"
    # This attribute is used to populate `intermediate_outputs` property of a trace data
    # representing intermediate outputs of the trace. This attribute is not empty only on
    # the root span of a trace created by the `mlflow.log_trace` API. The `intermediate_outputs`
    # property of the normal trace is generated by the outputs of non-root spans.
    INTERMEDIATE_OUTPUTS = "mlflow.trace.intermediate_outputs"


# All storage backends are guaranteed to support key values up to 250 characters
MAX_CHARS_IN_TRACE_INFO_METADATA_AND_TAGS = 250
TRUNCATION_SUFFIX = "..."

# Trace request ID must have the prefix "tr-" appended to the OpenTelemetry trace ID
TRACE_REQUEST_ID_PREFIX = "tr-"

# Schema version of traces and spans.
TRACE_SCHEMA_VERSION = 2

# Key for the trace schema version in the trace. This key is also used in
# Databricks model serving to be careful when modifying it.
TRACE_SCHEMA_VERSION_KEY = "mlflow.trace_schema.version"


STREAM_CHUNK_EVENT_NAME_FORMAT = "mlflow.chunk.item.{index}"
STREAM_CHUNK_EVENT_VALUE_KEY = "mlflow.chunk.value"
