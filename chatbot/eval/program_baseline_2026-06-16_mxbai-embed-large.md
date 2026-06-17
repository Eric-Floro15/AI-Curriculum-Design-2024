# Program RAG retrieval baseline — 2026-06-16

## Run config
- embeddings: `Ollama embeddings: model=mxbai-embed-large, host=http://localhost:11434`
- chunk_size: 1000, chunk_overlap: 100
- index docs (chunks): 67
- index built: 2026-06-16T12:41:25
- PROGRAM_RAG_MAX_DISTANCE: 0.76
- queries: 9 (8 directional, 1 negative control)
- k: 3

## Results
- **mean precision@3 = 0.88** (directional cases only — noisy at small corpus size; see no-cross-contamination below instead)
- **mean recall@3 = 1.00**
- **no cross-contamination: 7/8** directional cases retrieved ONLY chunks from the expected program
- **negative control: 1/1** passed (correctly returned zero hits)

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_program_rag_eval.py`

---

## [queens-direct] "Queen's University MMAI curriculum requirements"

- mode: directional
- expected: `['queen', 'mmai', 'smith school']`
- precision@3 = **0.67** (2/3)
- recall@3 = **1.00** (3/3)
- no cross-contamination
- matched expected: mmai, queen, smith school
- retrieved:
    - [x] distance=0.6049  fused_score=0.018333  bm25_score=9.1744  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    - [x] distance=0.7548  fused_score=0.015152  bm25_score=0.0000  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University

## [mit-direct] 'MIT 6-4 MEng Artificial Intelligence and Decision Making requirements'

- mode: directional
- expected: `['meng', 'electrical engineering', '6-4']`
- precision@3 = **1.00** (3/3)
- recall@3 = **1.00** (3/3)
- no cross-contamination
- matched expected: 6-4, electrical engineering, meng
- retrieved:
    - [x] distance=0.3276  fused_score=0.018333  bm25_score=13.5985  Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    - [x] distance=0.3717  fused_score=0.018006  bm25_score=12.6071  Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    - [x] distance=0.5014  fused_score=0.017692  bm25_score=6.6167  Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)

## [queens-by-topic] "AI master's program with business strategy courses and team leadership training"

- mode: directional
- expected: `['queen', 'mmai']`
- precision@3 = **1.00** (3/3)
- recall@3 = **1.00** (2/2)
- no cross-contamination
- matched expected: mmai, queen
- retrieved:
    - [x] distance=0.4314  fused_score=0.018333  bm25_score=9.7943  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    - [x] distance=0.5370  fused_score=0.016393  bm25_score=0.0000  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    - [x] distance=0.5815  fused_score=0.016129  bm25_score=2.1308  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University

## [mit-by-topic] 'graduate AI program requiring an engineering thesis with reinforcement learning electives'

- mode: directional
- expected: `['meng', '6-4']`
- precision@3 = **0.33** (1/3)
- recall@3 = **1.00** (2/2)
- CROSS-CONTAMINATION DETECTED — a chunk from a different program ranked inside top-k
- matched expected: 6-4, meng
- retrieved:
    - [ ] distance=0.4506  fused_score=0.016667  bm25_score=1.2919  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    - [x] distance=0.5458  fused_score=0.016393  bm25_score=0.6912  Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    - [ ] distance=0.5648  fused_score=0.016129  bm25_score=0.7219  Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University

## [cmu-direct] 'Carnegie Mellon MSAII curriculum requirements'

- mode: directional
- expected: `['msaii', 'carnegie mellon']`
- precision@3 = **1.00** (3/3)
- recall@3 = **1.00** (2/2)
- no cross-contamination
- matched expected: carnegie mellon, msaii
- retrieved:
    - [x] distance=0.5126  fused_score=0.016667  bm25_score=0.0000  Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    - [x] distance=0.5211  fused_score=0.018060  bm25_score=10.8098  Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    - [x] distance=0.5263  fused_score=0.016129  bm25_score=0.0000  Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science

## [georgia-tech-direct] 'Georgia Tech MS CS Artificial Intelligence specialization requirements'

- mode: directional
- expected: `['georgia tech', 'college of computing']`
- precision@3 = **1.00** (3/3)
- recall@3 = **1.00** (2/2)
- no cross-contamination
- matched expected: college of computing, georgia tech
- retrieved:
    - [x] distance=0.3686  fused_score=0.018306  bm25_score=13.9184  Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    - [x] distance=0.4637  fused_score=0.017796  bm25_score=14.0884  Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    - [x] distance=0.4866  fused_score=0.016972  bm25_score=7.8688  Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing

## [rotman-direct] 'University of Toronto Rotman Master of Management Analytics requirements'

- mode: directional
- expected: `['rotman', 'toronto']`
- precision@3 = **1.00** (3/3)
- recall@3 = **1.00** (2/2)
- no cross-contamination
- matched expected: rotman, toronto
- retrieved:
    - [x] distance=0.3850  fused_score=0.018333  bm25_score=26.9540  Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    - [x] distance=0.5369  fused_score=0.017981  bm25_score=8.2457  Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    - [x] distance=0.5705  fused_score=0.016129  bm25_score=0.0000  Master of Management Analytics (MMA), Rotman School of Management, University of Toronto

## [stanford-direct] 'Stanford MS CS Artificial Intelligence depth requirements'

- mode: directional
- expected: `['stanford']`
- precision@3 = **1.00** (3/3)
- recall@3 = **1.00** (1/1)
- no cross-contamination
- matched expected: stanford
- retrieved:
    - [x] distance=0.2722  fused_score=0.018306  bm25_score=6.7982  Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    - [x] distance=0.3986  fused_score=0.016393  bm25_score=1.3735  Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    - [x] distance=0.4183  fused_score=0.017796  bm25_score=7.5818  Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University

## [negative-control-uw] "University of Washington Master's in Computer Science Artificial Intelligence track requirements"

- mode: negative control (expect zero hits)
- result: **PASS (zero hits — correctly signals fall back to web search)**
- retrieved: (none)
