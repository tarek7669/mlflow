import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";
import { apiReferencePrefix } from "./docusaurusConfigUtils";

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  docsSidebar: [
    {
      type: 'doc',
      id: 'index',
      className: 'sidebar-top-level-category',
    },
    {
      type: 'category',
      label: 'Getting Started',
      className: 'sidebar-top-level-category',
      items: [
        {
          type: 'doc',
          id: 'getting-started/intro-quickstart/index',
          label: 'Quickstart',
        },
        {
          type: 'doc',
          id: 'getting-started/running-notebooks/index',
        },
        {
          type: 'doc',
          id: 'getting-started/databricks-trial/index',
        },
        {
          type: 'category',
          label: 'More Tutorials',
          items: [
            {
              type: 'doc',
              label: 'Hyperparameter Tuning Tutorial',
              id: 'getting-started/quickstart-2/index',
            },
            {
              type: 'category',
              label: 'Model Registry Tutorial',
              items: [
                {
                  type: 'autogenerated',
                  dirName: 'getting-started/registering-first-model',
                }
              ]
            },
            {
              type: 'doc',
              id: 'getting-started/tracking-server-overview/index',
            }
          ]
        }
      ],
      link: {
        type: 'doc',
        id: 'getting-started/index',
      }
    },
    {
      type: 'category',
      label: 'Machine Learning 🧠',
      className: 'sidebar-top-level-category',
      collapsed: false,
      items: [
        {
          type: 'category',
          label: 'LLM / GenAI',
          items: [
            {
              type: 'doc',
              label: 'Overview',
              id: 'llms/index',
            },
            {
              type: 'category',
              label: 'Integrations',
              items: [
                {
                  type: 'category',
                  label: 'OpenAI',
                  items: [
                    {
                      type: 'autogenerated',
                      dirName: 'llms/openai',
                    }
                  ],
                  link: {
                    type: 'doc',
                    id: 'llms/openai/index',
                  }
                },
                {
                  type: 'category',
                  label: 'LangChain',
                  items: [
                    {
                      type: 'autogenerated',
                      dirName: 'llms/langchain',
                    }
                  ],
                  link: {
                    type: 'doc',
                    id: 'llms/langchain/index',
                  }
                },
                {
                  type: 'doc',
                  id: 'llms/dspy/index',
                  label: 'DSPy',
                },
                {
                  type: 'doc',
                  id: 'llms/llama-index/index',
                  label: 'LlamaIndex',
                },
                {
                  type: 'category',
                  label: 'Transformers',
                  items: [
                    {
                      type: 'autogenerated',
                      dirName: 'llms/transformers',
                    }
                  ],
                  link: {
                    type: 'doc',
                    id: 'llms/transformers/index',
                  }
                },
                {
                  type: 'category',
                  label: 'Sentence Transformers',
                  items: [
                    {
                      type: 'autogenerated',
                      dirName: 'llms/sentence-transformers',
                    }
                  ],
                  link: {
                    type: 'doc',
                    id: 'llms/sentence-transformers/index',
                  }
                },
                {
                  type: 'link',
                  href: '/tracing/integrations/',
                  label: 'More',
                },
              ],
            },
            {
              type: 'link',
              label: 'Tracing (Observability)',
              href: '/tracing/',
            },
            {
              type: 'category',
              label: 'Evaluation',
              link: {
                type: 'doc',
                id: 'llms/llm-evaluate/index',
              },
              items: [
                {
                  type: 'autogenerated',
                  dirName: 'llms/llm-evaluate',
                },
              ],
            },
            {
              type: 'category',
              label: 'ChatModel',
              items: [
                {
                  type: 'doc',
                  id: 'llms/chat-model-intro/index',
                  label: 'What is ChatModel?',
                },
                {
                  type: 'doc',
                  id: 'llms/chat-model-guide/index',
                  label: 'Advanced Guide',
                },
                {
                  type: 'doc',
                  id: 'llms/custom-pyfunc-for-llms/index',
                  label: 'More Customization',
                }
              ]
            },
            {
              type: 'category',
              label: 'RAG',
              items: [
                {
                  'type': 'doc',
                  'id': 'llms/rag/index',
                  'label': 'What is RAG?'
                },
                {
                  'type': 'doc',
                  'id': 'llms/rag/notebooks/index',
                }
              ]
            },
            {
              type: 'doc',
              label: 'Prompt Engineering',
              id: 'llms/prompt-engineering/index',
            },
          ],
          link: {
            type: 'doc',
            id: 'llms/index',
          }
        },
        {
          type: 'category',
          label: 'Deep Learning',
          items: [
            {
              type: 'autogenerated',
              dirName: 'deep-learning',
            },
          ],
          link: {
            type: 'doc',
            id: 'deep-learning/index',
          }
        },
        {
          type: 'category',
          label: 'Traditional ML',
          items: [
            {
              type: 'autogenerated',
              dirName: 'traditional-ml',
            },
          ],
          link: {
            type: 'doc',
            id: 'traditional-ml/index',
          }
        },
      ],
    },
    {
      type: 'category',
      label: 'Build 🔨 ',
      className: 'sidebar-top-level-category',
      collapsed: false,
      items: [
        {
          type: 'category',
          label: 'MLflow Tracking',
          items: [
            {
              type: 'doc',
              id: 'tracking/index',
            },
            /* Using link instead of doc to avoid duplicated select state in sidebar */
            {
              type: 'link',
              href: '/getting-started/intro-quickstart/',
              label: 'Quickstart',
            },
            {
              type: 'doc',
              id: 'tracking/autolog/index',
            },
            {
              type: 'category',
              label: 'Tracking Server',
              items: [
                {
                  type: 'doc',
                  id: 'tracking/artifacts-stores/index',
                },
                {
                  type: 'doc',
                  id: 'tracking/backend-stores/index',
                },
                {
                  type: 'category',
                  label: 'Tutorials',
                  items: [
                    {
                      type: 'autogenerated',
                      dirName: 'tracking/tutorials',
                    }
                  ],
                }
              ],
              link: {
                type: 'doc',
                id: 'tracking/server/index',
              }
            },
            {
              type: 'category',
              label: 'Searching Runs & Experiments',
              items: [
                {
                  type: 'doc',
                  id: 'search-runs/index',
                },
                {
                  type: 'doc',
                  id: 'search-experiments/index',
                }
              ]
            },
            {
              type: 'doc',
              id: 'system-metrics/index',
            }
          ],
          link: {
            type: 'doc',
            id: 'tracking/index',
          },
        },
        {
          type: 'category',
          label: 'MLflow Model',
          items: [
            {
              type: 'autogenerated',
              dirName: 'model',
            },
          ],
        },
        {
          type: 'doc',
          id: 'recipes/index'
        }
      ]
    },
    {
      type: 'category',
      label: 'Evaluate & Monitor 📊',
      className: 'sidebar-top-level-category',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'model-evaluation/index',
          label: 'MLflow Evaluation',
        },
        {
          type: 'category',
          label: 'MLflow Tracing (Observability)',
          items: [
            {
              type: 'autogenerated',
              dirName: 'tracing',
            },
          ],
          link: {
            type: 'doc',
            id: 'tracing/index',
          }
        },
        {
          type: 'doc',
          id: 'dataset/index',
          label: 'MLflow Dataset',
        },
      ]
    },
    {
      type: 'category',
      label: 'Deploy 🚀',
      className: 'sidebar-top-level-category',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'model-registry/index',
        },
        {
          type: 'category',
          label: 'MLflow Serving',
          items: [
            {
              type: 'autogenerated',
              dirName: 'deployment',
            }
          ]
        },
        {
          type: 'category',
          label: 'MLflow AI Gateway',
          link: {
            type: 'doc',
            id: 'llms/deployments/index',
          },
          items: [
            {
              type: 'autogenerated',
              dirName: 'llms/deployments',
            }
          ],
        },
      ]
    },
    {
      type: 'category',
      label: 'Team Collaboration 👥',
      className: 'sidebar-top-level-category',
      collapsed: true,
      items: [
        {
          type: 'link',
          href: '/tracking/#tracking-setup',
          label: 'Self-Hosting'
        },
        {
          type: 'link',
          href: '/#running-mlflow-anywhere',
          label: 'Managed Services'
        },
        {
          type: 'doc',
          id: 'auth/index',
          label: 'Access Control',
        },
        {
          type: 'doc',
          id: 'projects/index',
          label: 'MLflow Projects',
        },
      ]
    },
    {
      type: 'category',
      label: 'API References',
      className: 'sidebar-top-level-category',
      collapsed: true,
      items: [
        {
          type: 'link',
          label: 'Python API',
          href: `${apiReferencePrefix()}api_reference/python_api/index.html`,
        },
        {
          type: 'link',
          label: 'Java API',
          href: `${apiReferencePrefix()}api_reference/java_api/index.html`,
        },
        {
          type: 'link',
          label: 'R API',
          href: `${apiReferencePrefix()}api_reference/R-api.html`,
        },
        {
          type: 'link',
          label: 'REST API',
          href: `${apiReferencePrefix()}api_reference/rest-api.html`,
        },
        {
          type: 'link',
          label: 'CLI',
          href: `${apiReferencePrefix()}cli.html`,
        }
      ]
    },
    {
      type: 'category',
      label: 'More',
      collapsed: true,
      className:'sidebar-top-level-category',
      items: [
        {
          type: 'link',
          label: 'Contributing',
          href: 'https://github.com/mlflow/mlflow/blob/master/CONTRIBUTING.md',
        },
        {
          type: 'link',
          label: 'MLflow Blogs',
          href: 'https://mlflow.org/blog/index.html',
        },
        {
          type: 'doc',
          id: 'plugins/index',
        },
      ]
    },
  ]
};

export default sidebars;
