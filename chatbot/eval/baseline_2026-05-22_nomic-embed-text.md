# RAG retrieval baseline — 2026-05-22

## Run config
- embeddings: `Ollama embeddings: model=nomic-embed-text, host=http://localhost:11434`
- chunk_size: 2000, chunk_overlap: 0
- index docs: 871
- index built: 2026-05-22T15:55:44
- queries: 10
- k: 5

## Results
- **mean precision@5 = 0.36**
- **mean recall@5 = 0.26**

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_rag_eval.py`

---

## [cloud-infra] 'What cloud infrastructure skills are most in demand?'

- expected: `['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'kubernetes']`
- precision@5 = **0.80** (4/5)
- recall@5 = **0.33** (2/6)
- matched expected: ['azure', 'cloud']
- retrieved:
    - [x] Cloud Automation Scripting
    - [x] Azure Certifications
    - [x] Cloud Certifications
    - [x] Cloud Deployment
    - [ ] Serverless

## [data-engineering] 'Data engineering tools like Spark and Kafka'

- expected: `['spark', 'kafka', 'hadoop', 'etl', 'data pipeline', 'airflow', 'databricks']`
- precision@5 = **0.00** (0/5)
- recall@5 = **0.00** (0/7)
- matched expected: —
- retrieved:
    - [ ] Autocad Civil 3D
    - [ ] Reporting Tools
    - [ ] Ci/Cd Tools
    - [ ] Orchestration Tools
    - [ ] Cad software

## [soft-skills-ml] 'Soft skills for machine learning practitioners'

- expected: `['communication', 'collaboration', 'problem solving', 'leadership', 'teamwork', 'critical thinking']`
- precision@5 = **0.00** (0/5)
- recall@5 = **0.00** (0/6)
- matched expected: —
- retrieved:
    - [ ] Model Training
    - [ ] Ml Frameworks
    - [ ] Mlops Tools
    - [ ] Model Architecture Design
    - [ ] Distributed Training

## [mlops] 'MLOps and model deployment skills'

- expected: `['mlops', 'model deployment', 'docker', 'kubernetes', 'ci/cd', 'model monitoring']`
- precision@5 = **0.00** (0/5)
- recall@5 = **0.00** (0/6)
- matched expected: —
- retrieved:
    - [ ] Foundation Models
    - [ ] Analytical Modeling
    - [ ] Model Development
    - [ ] Supervised Fine-Tuning
    - [ ] Machine Learning Projects

## [stats-math] 'Statistical methods and mathematical foundations for machine learning'

- expected: `['statistics', 'probability', 'linear algebra', 'regression', 'calculus', 'hypothesis testing']`
- precision@5 = **0.00** (0/5)
- recall@5 = **0.00** (0/6)
- matched expected: —
- retrieved:
    - [ ] Reinforcement Learning (Rl)
    - [ ] Model Architecture Design
    - [ ] Distributed Training
    - [ ] Reinforcement Learning
    - [ ] Ml Frameworks

## [nlp] 'Natural language processing skills'

- expected: `['nlp', 'natural language', 'llm', 'transformer', 'text mining', 'language model']`
- precision@5 = **0.80** (4/5)
- recall@5 = **0.67** (4/6)
- matched expected: ['llm', 'natural language', 'nlp', 'transformer']
- retrieved:
    - [x] Nlp Techniques
    - [x] Llm Architectures
    - [x] Natural Language Understanding
    - [x] Transformer Models
    - [ ] Machine Translation

## [computer-vision] 'Computer vision and image processing'

- expected: `['computer vision', 'opencv', 'image processing', 'image recognition', 'cnn']`
- precision@5 = **0.40** (2/5)
- recall@5 = **0.40** (2/5)
- matched expected: ['cnn', 'computer vision']
- retrieved:
    - [x] Cnn
    - [ ] Gpu
    - [x] Computer Vision
    - [ ] Neural/Deep Learning Methods
    - [ ] Deep Learning Frameworks

## [data-viz] 'Data visualization and business intelligence tools'

- expected: `['tableau', 'power bi', 'visualization', 'dashboard', 'matplotlib', 'ggplot']`
- precision@5 = **0.60** (3/5)
- recall@5 = **0.33** (2/6)
- matched expected: ['power bi', 'visualization']
- retrieved:
    - [x] Power Bi
    - [x] Powerbi
    - [ ] Quicksight
    - [ ] Looker
    - [x] Visualization Tools

## [programming] 'Programming languages used in data science'

- expected: `['python', 'r programming', 'sql', 'scala', 'java']`
- precision@5 = **0.60** (3/5)
- recall@5 = **0.60** (3/5)
- matched expected: ['java', 'python', 'sql']
- retrieved:
    - [x] Java/Kotlin
    - [ ] Scripting Languages
    - [x] Sql
    - [x] Python
    - [ ] Rust

## [gen-ai] 'Generative AI and large language model skills'

- expected: `['generative ai', 'llm', 'large language', 'prompt engineering', 'rag', 'fine-tuning', 'gpt']`
- precision@5 = **0.40** (2/5)
- recall@5 = **0.29** (2/7)
- matched expected: ['llm', 'rag']
- retrieved:
    - [ ] Foundation Models
    - [x] Retrieval-Augmented Generation (Rag)
    - [x] Llm Architectures
    - [ ] Distributed Training
    - [ ] Multimodal Learning
