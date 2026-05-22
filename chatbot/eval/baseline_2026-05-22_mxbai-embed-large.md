# RAG retrieval baseline — 2026-05-22

## Run config
- embeddings: `Ollama embeddings: model=mxbai-embed-large, host=http://localhost:11434`
- chunk_size: 2000, chunk_overlap: 0
- index docs: 871
- index built: 2026-05-22T17:03:33
- queries: 10
- k: 5

## Results
- **mean precision@5 = 0.64**
- **mean recall@5 = 0.30**

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_rag_eval.py`

---

## [cloud-infra] 'What cloud infrastructure skills are most in demand?'

- expected: `['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'kubernetes']`
- filter: none
- precision@5 = **1.00** (5/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['cloud']
- retrieved:
    - [x] Cloud Infrastructure
    - [x] Cloud Computing
    - [x] Cloud Certifications
    - [x] Cloud Deployment
    - [x] Cloud Automation Scripting

## [data-engineering] 'Data engineering tools like Spark and Kafka'

- expected: `['spark', 'kafka', 'hadoop', 'etl', 'data pipeline', 'airflow', 'databricks']`
- filter: none
- precision@5 = **0.40** (2/5)
- recall@5 = **0.29** (2/7)
- matched expected: ['hadoop', 'kafka']
- retrieved:
    - [x] Kafka
    - [x] Hadoop
    - [ ] Big Data Technologies
    - [ ] Hive
    - [ ] Data Integration

## [soft-skills-ml] 'Soft skills for machine learning practitioners'

- expected: `['communication', 'collaboration', 'problem solving', 'leadership', 'teamwork', 'critical thinking', 'stakeholder', 'learning agility', 'decision making']`
- filter: `{'level1': 'soft'}`
- precision@5 = **0.80** (4/5)
- recall@5 = **0.44** (4/9)
- matched expected: ['decision making', 'learning agility', 'stakeholder', 'teamwork']
- retrieved:
    - [ ] Continuous Learning
    - [x] Learning Agility
    - [x] Stakeholder Management
    - [x] Decision Making
    - [x] Teamwork

## [mlops] 'MLOps and model deployment skills'

- expected: `['mlops', 'model deployment', 'docker', 'kubernetes', 'ci/cd', 'model monitoring']`
- filter: none
- precision@5 = **0.80** (4/5)
- recall@5 = **0.33** (2/6)
- matched expected: ['mlops', 'model deployment']
- retrieved:
    - [x] Model Deployment
    - [x] Mlops Tools
    - [ ] Ml Solutions Deployment
    - [x] Mlops
    - [x] Mlops Best Practices

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
- recall@5 = **0.33** (2/6)
- matched expected: ['natural language', 'nlp']
- retrieved:
    - [x] Natural Language Processing
    - [x] Nlp
    - [x] Natural Language Understanding
    - [x] Nlp Techniques
    - [ ] Speech Recognition

## [computer-vision] 'Computer vision and image processing'

- expected: `['computer vision', 'opencv', 'image processing', 'image recognition', 'cnn']`
- filter: none
- precision@5 = **0.40** (2/5)
- recall@5 = **0.40** (2/5)
- matched expected: ['cnn', 'computer vision']
- retrieved:
    - [x] Computer Vision
    - [x] Cnn
    - [ ] Multimodal Systems
    - [ ] Multimodal Learning
    - [ ] Unsupervised Learning

## [data-viz] 'Data visualization and business intelligence tools'

- expected: `['tableau', 'power bi', 'visualization', 'dashboard', 'matplotlib', 'ggplot']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['visualization']
- retrieved:
    - [x] Business Intelligence Visualization Tool
    - [x] Visualization Tools
    - [x] Data Visualization
    - [ ] Bi Tools
    - [ ] Analytics Tools

## [programming] 'Programming languages used in data science'

- expected: `['python', 'r programming', 'sql', 'scala', 'java']`
- filter: none
- precision@5 = **0.20** (1/5)
- recall@5 = **0.20** (1/5)
- matched expected: ['sql']
- retrieved:
    - [ ] Data Science
    - [x] Sql
    - [ ] Programming Languages
    - [ ] Data Querying Languages
    - [ ] Matlab

## [gen-ai] 'Generative AI and large language model skills'

- expected: `['generative ai', 'llm', 'large language', 'prompt engineering', 'rag', 'fine-tuning', 'gpt']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.43** (3/7)
- matched expected: ['generative ai', 'large language', 'llm']
- retrieved:
    - [x] Large Language Models
    - [x] Generative Ai
    - [ ] Genai
    - [ ] Gans
    - [x] Llms
