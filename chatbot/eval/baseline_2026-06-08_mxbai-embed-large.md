# RAG retrieval baseline — 2026-06-08

## Run config
- embeddings: `Ollama embeddings: model=mxbai-embed-large, host=http://localhost:11434`
- chunk_size: 2000, chunk_overlap: 0
- index docs: 871
- index built: 2026-05-22T17:03:33
- queries: 10
- k: 5

## Results
- **mean precision@5 = 0.68**
- **mean recall@5 = 0.37**

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_rag_eval.py`

---

## [cloud-infra] 'What cloud infrastructure skills are most in demand?'

- expected: `['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'kubernetes']`
- filter: none
- precision@5 = **1.00** (5/5)
- recall@5 = **0.33** (2/6)
- matched expected: ['aws', 'cloud']
- retrieved:
    - [x] Cloud Certifications
    - [x] Cloud Automation Scripting
    - [x] Cloud Infrastructure
    - [x] Cloud Computing
    - [x] Aws Solutions

## [data-engineering] 'Data engineering tools like Spark and Kafka'

- expected: `['spark', 'kafka', 'hadoop', 'etl', 'data pipeline', 'airflow', 'databricks']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.43** (3/7)
- matched expected: ['hadoop', 'kafka', 'spark']
- retrieved:
    - [x] Kafka
    - [x] Hadoop
    - [ ] Big Data Technologies
    - [ ] Hive
    - [x] Spark Mllib

## [soft-skills-ml] 'Soft skills for machine learning practitioners'

- expected: `['communication', 'collaboration', 'problem solving', 'leadership', 'teamwork', 'critical thinking', 'stakeholder', 'learning agility', 'decision making']`
- filter: `{'level1': 'soft'}`
- precision@5 = **0.80** (4/5)
- recall@5 = **0.44** (4/9)
- matched expected: ['critical thinking', 'decision making', 'learning agility', 'stakeholder']
- retrieved:
    - [ ] Continuous Learning
    - [x] Learning Agility
    - [x] Stakeholder Management
    - [x] Critical Thinking
    - [x] Decision Making

## [mlops] 'MLOps and model deployment skills'

- expected: `['mlops', 'model deployment', 'docker', 'kubernetes', 'ci/cd', 'model monitoring']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['mlops']
- retrieved:
    - [x] Mlops Tools
    - [x] Mlops
    - [ ] Ml Solutions Deployment
    - [x] Mlops Best Practices
    - [ ] Mlflow

## [stats-math] 'Statistical methods and mathematical foundations for machine learning'

- expected: `['statistics', 'statistical', 'probability', 'linear algebra', 'regression', 'calculus', 'hypothesis testing', 'quantitative', 'mathematics']`
- filter: `{'level2_contains': 'statistic'}`
- precision@5 = **0.80** (4/5)
- recall@5 = **0.22** (2/9)
- matched expected: ['statistical', 'statistics']
- retrieved:
    - [x] Statistical Methodologies
    - [x] Statistical Analysis
    - [x] Statistics
    - [x] Statistical/Mathematical software
    - [ ] Causal Inference

## [nlp] 'Natural language processing skills'

- expected: `['nlp', 'natural language', 'llm', 'transformer', 'text mining', 'language model']`
- filter: none
- precision@5 = **0.80** (4/5)
- recall@5 = **0.50** (3/6)
- matched expected: ['natural language', 'nlp', 'transformer']
- retrieved:
    - [x] Natural Language Processing
    - [x] Nlp
    - [x] Natural Language Understanding
    - [ ] Speech Recognition
    - [x] Transformers

## [computer-vision] 'Computer vision and image processing'

- expected: `['computer vision', 'opencv', 'image processing', 'image recognition', 'cnn']`
- filter: none
- precision@5 = **0.40** (2/5)
- recall@5 = **0.40** (2/5)
- matched expected: ['cnn', 'computer vision']
- retrieved:
    - [x] Computer Vision
    - [x] Cnn
    - [ ] Neural/Deep Learning Methods
    - [ ] Multimodal Systems
    - [ ] Multimodal Learning

## [data-viz] 'Data visualization and business intelligence tools'

- expected: `['tableau', 'power bi', 'visualization', 'dashboard', 'matplotlib', 'ggplot']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['visualization']
- retrieved:
    - [x] Visualization Tools
    - [x] Business Intelligence Visualization Tool
    - [x] Data Visualization
    - [ ] Analytical Tools
    - [ ] Bi Tools

## [programming] 'Programming languages used in data science'

- expected: `['python', 'r programming', 'sql', 'scala', 'java']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.60** (3/5)
- matched expected: ['java', 'scala', 'sql']
- retrieved:
    - [ ] Programming Languages
    - [x] Scala
    - [ ] Data Science
    - [x] Sql
    - [x] Java/Kotlin

## [gen-ai] 'Generative AI and large language model skills'

- expected: `['generative ai', 'llm', 'large language', 'prompt engineering', 'rag', 'fine-tuning', 'gpt']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.43** (3/7)
- matched expected: ['generative ai', 'large language', 'rag']
- retrieved:
    - [x] Generative Ai
    - [x] Large Language Models
    - [ ] Genai
    - [ ] Transformers
    - [x] Retrieval-Augmented Generation (Rag)
