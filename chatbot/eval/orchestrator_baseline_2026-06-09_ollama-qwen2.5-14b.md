# Orchestrator end-to-end baseline — 2026-06-09

## Run config
- model: `ollama-qwen2.5:14b`
- queries run: 1
- PASS: 0
- INSPECT: 0  _(soft failures only — review manually)_
- FAIL: 1

Verdict key: **PASS** all assertions met · **INSPECT** only soft assertions failed (check phrasing/delegation) · **FAIL** hard assertion violated (hallucination / budget / error)

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`

## Per-query summary

| ID | verdict | delegations | tool calls | wall (s) |
|---|---|---|---|---|
| data-eng-curriculum-update | FAIL | ['AI Industry News Researcher', 'Skills Taxonomy Analyst', 'University AI Programs Researcher'] | 9 | 1497.6 |

---

## [data-eng-curriculum-update] **FAIL**

**Category:** update-mixed

**Query:**

```
I'm updating my AI/ML Master's curriculum. What are the most
in-demand data engineering skills I should make sure my program
covers, and how does Queen's University's MMAI program compare
on this dimension? Give me concrete recommendations for what to
add or strengthen.
```

**Wall time:** 1497.6s
**Tool calls:** 9
**Delegated to:** ['AI Industry News Researcher', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']

**Hard failures (FAIL):**
- wall time exceeded: 1497.6s > 600s

**Orchestrator's final answer:**

After reviewing recent market demand and peer program offerings for data engineering skills in AI/ML curricula, we advise enhancing your Master’s curriculum to include comprehensive training on top data engineering areas such as ETL processes, big data technologies, and advanced pipeline management. Queen's MMAI program currently covers foundational data science concepts but lacks detailed instruction in specialized data engineering topics.

**Concrete Recommendations:**

- **Skill Focus:** Highlight Data Pipelines (4278), DevOps (1007), Relational Databases (936), Big Data Technologies (510). These skills are highly demanded and not fully covered by Queen's MMAI program.
  - Example Courses:
    - ETL Engineering from [Course URL not found, recommend incorporating into existing data engineering or cloud technology courses]

- **Peer Programs Reference:**
  - Consider adding specialized data engineering electives as part of your curriculum. For instance, Columbia’s AI program includes specific focus on advanced topics like DevOps practices and relational databases.

- **Recent Trends (Indirect Implications):** 
  - Ensure students are equipped to handle complex data pipelines with advancements in AWS tooling for foundation model training.
  - Train them on emerging techniques for optimization of models specifically designed to run on embedded devices and how this influences broader pipeline efficiency.
  - Focus on tools and practices like Ulysses Sequence style parallelism for effective management of large datasets.

**Executive Summary:**
Your AI/ML Master's program should prioritize skills and courses focusing on data pipelines, DevOps, relational databases, big data technologies, and on-device optimizations. These updates align with industry demand and recent trends while leveraging comprehensive training compared to peers like Queen’s MMAI framework.

**Trade-off or caveat:** 
While incorporating these advanced topics will ensure your curriculum remains highly relevant and attractive to prospective students, it may require additional resources including specialized faculty expertise and technology licenses for hands-on lab experiences.

---
