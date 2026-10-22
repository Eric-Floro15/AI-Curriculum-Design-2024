# RAG retrieval baseline — 2026-10-22

## Run config
- embeddings: `Ollama embeddings: model=mxbai-embed-large, host=http://localhost:11434`
- chunk_size: 5000, chunk_overlap: 0
- index docs: 962
- index built: 2026-10-22T15:12:22
- queries: 10
- k: 5

## Results
- **mean precision@5 = 0.48**
- **mean recall@5 = 0.25**

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_rag_eval.py`

---

## [cloud-infra] 'What cloud infrastructure skills are most in demand?'

- expected: `['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'kubernetes']`
- filter: none
- precision@5 = **0.80** (4/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['cloud']
- retrieved:
    - [x] Cloud Certifications
    - [x] Cloud Security
    - [x] Cloud Automation Scripting
    - [ ] Terraform
    - [x] Cloud Computing

## [data-engineering] 'Data engineering tools like Spark and Kafka'

- expected: `['spark', 'kafka', 'hadoop', 'etl', 'data pipeline', 'airflow', 'databricks']`
- filter: none
- precision@5 = **0.40** (2/5)
- recall@5 = **0.29** (2/7)
- matched expected: ['kafka', 'spark']
- retrieved:
    - [x] Kafka
    - [x] Spark Mllib
    - [ ] Debezium
    - [ ] Modern Data Stack
    - [ ] Data Engineering

## [soft-skills-ml] 'Soft skills for machine learning practitioners'

- expected: `['communication', 'collaboration', 'problem solving', 'leadership', 'teamwork', 'critical thinking', 'stakeholder', 'learning agility', 'decision making']`
- filter: `{'level1': 'soft'}`
- precision@5 = **0.40** (2/5)
- recall@5 = **0.22** (2/9)
- matched expected: ['decision making', 'learning agility']
- retrieved:
    - [x] Decision Making
    - [ ] Data Storytelling
    - [x] Learning Agility
    - [ ] Continuous Learning
    - [ ] Team Player

## [mlops] 'MLOps and model deployment skills'

- expected: `['mlops', 'model deployment', 'docker', 'kubernetes', 'ci/cd', 'model monitoring']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.50** (3/6)
- matched expected: ['mlops', 'model deployment', 'model monitoring']
- retrieved:
    - [x] Mlops
    - [x] Model Monitoring
    - [ ] LLMOps
    - [x] Model Deployment
    - [ ] Model Serving

## [stats-math] 'Statistical methods and mathematical foundations for machine learning'

- expected: `['statistics', 'statistical', 'probability', 'linear algebra', 'regression', 'calculus', 'hypothesis testing', 'quantitative', 'mathematics']`
- filter: `{'level2_contains': 'statistic'}`
- precision@5 = **0.60** (3/5)
- recall@5 = **0.11** (1/9)
- matched expected: ['statistical']
- retrieved:
    - [x] Statistical Methodologies
    - [x] Statistical Sampling
    - [ ] Linear Mixed-Effects Model
    - [x] Statistical/Mathematical software
    - [ ] Survival Analysis

## [nlp] 'Natural language processing skills'

- expected: `['nlp', 'natural language', 'llm', 'transformer', 'text mining', 'language model']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['natural language']
- retrieved:
    - [x] Natural Language Processing
    - [ ] NLTK
    - [x] Natural Language Understanding
    - [x] Natural Language Generation
    - [ ] spaCy

## [computer-vision] 'Computer vision and image processing'

- expected: `['computer vision', 'opencv', 'image processing', 'image recognition', 'cnn']`
- filter: none
- precision@5 = **0.60** (3/5)
- recall@5 = **0.60** (3/5)
- matched expected: ['computer vision', 'image processing', 'opencv']
- retrieved:
    - [x] Image Processing
    - [x] Computer Vision
    - [x] OpenCV
    - [ ] Optical Character Recognition
    - [ ] Medical Imaging

## [data-viz] 'Data visualization and business intelligence tools'

- expected: `['tableau', 'power bi', 'visualization', 'dashboard', 'matplotlib', 'ggplot']`
- filter: none
- precision@5 = **0.40** (2/5)
- recall@5 = **0.17** (1/6)
- matched expected: ['visualization']
- retrieved:
    - [x] Visualization Tools
    - [ ] Analytical Tools
    - [x] Data Visualization
    - [ ] Bi Tools
    - [ ] Business Intelligence

## [programming] 'Programming languages used in data science'

- expected: `['python', 'r programming', 'sql', 'scala', 'java']`
- filter: none
- precision@5 = **0.00** (0/5)
- recall@5 = **0.00** (0/5)
- matched expected: —
- retrieved:
    - [ ] R
    - [ ] Programming Languages
    - [ ] Data Science
    - [ ] Matlab
    - [ ] Data Querying Languages

## [gen-ai] 'Generative AI and large language model skills'

- expected: `['generative ai', 'llm', 'large language', 'prompt engineering', 'rag', 'fine-tuning', 'gpt']`
- filter: none
- precision@5 = **0.40** (2/5)
- recall@5 = **0.29** (2/7)
- matched expected: ['generative ai', 'large language']
- retrieved:
    - [x] Generative Ai
    - [ ] Diffusion Models
    - [ ] Gemini
    - [x] Large Language Models
    - [ ] Gans
