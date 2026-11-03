"""Planted-fabrication recall test for the five production guards (issue #6b, 2026-10-21).

No API calls. Takes the final answers of real saved multi-agent Sonnet runs (chatbot/run_records/*_full.md),
plants ONE fabrication per trial into an otherwise unmodified answer, re-runs the production guard code
(chatbot/agents/orchestrator.py, imported via guardlib with CrewAI stubbed) and records whether a NEW flag
names the planted token. Baseline = guards on the unmodified answer of the same run.

Two families of plant:
  in-scope  : fabrications the guards are designed to catch (altered/invented lift, z, posting count;
              invented course code, URL, institution; content credited to a specialist that did not run;
              false claim that a specialist was consulted).
  boundary  : realistic fabrications outside the guards' design (a grounded number moved to the wrong skill,
              an unanchored percentage, a non-'University' institution name, a paraphrased role name).
              Reported so the paper states what the guards do NOT check.
Output: recall_trials.csv (one row per trial), recall_summary.csv, baseline_flags.csv, RECALL_RESULTS.md
"""
import os, re, ast, csv, math, random, types, glob, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import guardlib
O = guardlib.O
RR = os.path.join(guardlib.ROOT, 'chatbot', 'run_records')
SEED = 20261021
TRIALS_PER_TYPE = 3   # per run, where the run offers enough targets

# Pin to the original 27 Sonnet production runs used to compute the paper's
# recall figures (§5 / Table X).  Run IDs are the 16-char timestamp from each
# filename (run_<id>_..._full.md).  Any new Sonnet run records added after
# d49fbcc (v60 Part C, 2026-11-02) are NOT part of this baseline.
_PINNED_TIMESTAMPS: frozenset = frozenset({
    '20260910T212751Z', '20260911T180715Z', '20260911T181913Z',
    '20260911T234935Z', '20260912T013020Z', '20260917T034032Z',
    '20260917T053755Z', '20260917T053944Z', '20260917T054301Z',
    '20260917T054837Z', '20260917T055234Z', '20260917T055616Z',
    '20260917T060001Z', '20260917T060114Z', '20260917T060336Z',
    '20260917T060442Z', '20260917T061729Z', '20260917T150140Z',
    '20260917T150638Z', '20260917T224824Z', '20260917T225459Z',
    '20260917T230153Z', '20260924T163704Z', '20260924T213621Z',
    '20260925T180700Z', '20261020T191818Z', '20261020T192538Z',
})

ROLES = list(O._SPECIALIST_ROLES)
ROLE_HDR = re.compile(r'^### (' + '|'.join(map(re.escape, ROLES + ['Senior Curriculum Advisor'])) + r') — step \d+\s*$', re.M)


# ---------------------------------------------------------------- parsing
def parse(path):
    t = open(path, encoding='utf-8').read()
    model = re.search(r'^\*\*Model:\*\*(.*)$', t, re.M).group(1)
    dm = re.search(r'^- \*\*Delegated to:\*\* (\[.*?\])\s*$', t, re.M)
    if 'claude-sonnet' not in model or not dm:
        return None
    q = re.search(r'^\*\*Query:\*\*\s*(.*?)\n\s*\n', t, re.M | re.S).group(1).strip()
    a0 = t.index('\n## Final Answer\n') + len('\n## Final Answer\n')
    a1 = t.index('\n## Per-Agent Tool-Call Trace')
    answer = t[a0:a1].strip('\n')
    trace = t[a1:]
    tc = re.search(r'^## Tool Calls', trace, re.M)
    if tc:
        trace = trace[:tc.start()]
    heads = list(ROLE_HDR.finditer(trace))
    steps = []
    for i, h in enumerate(heads):
        seg = trace[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(trace)]
        lines = seg.split('\n')
        fences = [k for k, ln in enumerate(lines) if ln.strip() == '```' or ln.strip().startswith('```')]
        body = '\n'.join(lines[fences[0] + 1: fences[-1]]) if len(fences) >= 2 else seg
        steps.append({'role': h.group(1), 'output': types.SimpleNamespace(output=body)})
    return dict(file=os.path.basename(path), query=q, delegated=ast.literal_eval(dm.group(1)),
                answer=answer, steps=steps)


def run_guards(answer, r):
    out = []
    for g, fl in [('attribution', O._detect_fabrication_flags(answer, r['delegated'])),
                  ('numeric', O._detect_numeric_fabrication_flags(answer, r['steps'], r['delegated'])),
                  ('content', O._detect_content_attribution_flags(answer, r['query'], r['steps'], r['delegated'])),
                  ('delegation_claim', O._detect_delegation_claim_flags(answer, r['delegated']))]:
        out += [(g, f) for f in fl]
    return out


# ---------------------------------------------------------------- helpers
def paragraph_slots(answer):
    """Offsets of blank-line boundaries outside tables/fences (where a new paragraph can be inserted)."""
    slots, infence = [], False
    pos = 0
    lines = answer.split('\n')
    for i, ln in enumerate(lines):
        if ln.strip().startswith('```'):
            infence = not infence
        pos += len(ln) + 1
        if (not infence and ln.strip() == '' and i > 2 and i + 1 < len(lines)
                and not lines[i - 1].lstrip().startswith('|') and not lines[i + 1].lstrip().startswith('|')):
            slots.append(pos)
    return slots


def insert_para(answer, text, rng):
    slots = paragraph_slots(answer)
    p = rng.choice(slots[: max(1, int(len(slots) * 0.85))]) if slots else len(answer)
    return answer[:p] + text + '\n\n' + answer[p:]


def fmt_like(raw, val):
    d = len(raw.split('.')[1]) if '.' in raw else 0
    return f'{val:.{d}f}'


def pool_for(r, kind):
    gt = O._build_consulted_text(r['steps'], r['delegated'])
    pool = [v for _, v, k, _, _ in O._extract_market_numbers(gt) if k == kind]
    for m in O._TABLE_CELL_NUM_RE.finditer(gt):
        try:
            pool.append(O._normalize_market_num(m.group(1)))
        except ValueError:
            pass
    return pool, gt


def ungrounded_value(raw, val, pool, rng):
    for _ in range(200):
        nv = val * rng.uniform(1.15, 1.6) + rng.uniform(0.3, 2.0)
        s = fmt_like(raw, nv)
        f = float(s)
        if all(abs(f - g) > max(1e-6 * abs(g), 1e-6) for g in pool) and \
           not any(math.floor(g) == f or round(g) == f for g in pool) and s != raw:
            return s
    return None


def grounded_targets(r, kind):
    """Number occurrences in the answer of `kind` that are grounded (so altering them is a clean test)."""
    pool, _ = pool_for(r, kind)
    tg = []
    for raw, val, k, s, e in O._extract_market_numbers(r['answer']):
        if k != kind:
            continue
        tol = O._MARKET_NUM_KINDS[k][2]
        if any(abs(val - g) <= max(tol * abs(g), tol) for g in pool):
            tg.append((raw, val, s, e))
    return tg, pool


# ---------------------------------------------------------------- plant generators
# each returns list of (plant_type, family, planted_answer, token_that_a_flag_must_name, note)
def plants_numeric_alter(r, rng, kind, ptype):
    tg, pool = grounded_targets(r, kind)
    rng.shuffle(tg)
    out = []
    for raw, val, s, e in tg[:TRIALS_PER_TYPE]:
        nv = ungrounded_value(raw, val, pool, rng)
        if nv is None:
            continue
        a = r['answer'][:s] + nv + r['answer'][e:]
        out.append((ptype, 'in-scope', a, nv, f'{raw}->{nv}'))
    return out


def plants_numeric_insert(r, rng):
    poolL, gt = pool_for(r, 'lift')
    poolZ, _ = pool_for(r, 'z-score')
    out = []
    for _ in range(TRIALS_PER_TYPE):
        L = ungrounded_value('1.00', rng.uniform(3, 20), poolL, rng)
        Z = ungrounded_value('1.0', rng.uniform(2.5, 9), poolZ, rng)
        sent = f'Prompt evaluation also stands out, with a {L}× lift (z = {Z}) over AI postings generally.'
        out.append(('invented lift + z (inserted)', 'in-scope', insert_para(r['answer'], sent, rng), L, f'{L}x, z={Z}'))
    return out


def plants_swap(r, rng):
    """Boundary: replace a grounded lift with a DIFFERENT grounded lift from the same run (number moved to the wrong skill)."""
    tg, pool = grounded_targets(r, 'lift')
    rng.shuffle(tg)
    out = []
    for raw, val, s, e in tg[:TRIALS_PER_TYPE]:
        others = sorted({g for g in pool if abs(g - val) > 0.5 and g >= 1.5})
        if not others:
            continue
        g = rng.choice(others)
        nv = fmt_like(raw, g) if abs(float(fmt_like(raw, g)) - g) < 1e-9 else f'{g:g}'
        out.append(('grounded lift moved to wrong skill', 'boundary', r['answer'][:s] + nv + r['answer'][e:], nv, f'{raw}->{nv}'))
    return out


CODE_PREFIX = ['CSC', 'STAT', 'MIE', 'CS', 'MMAI', 'DSCI', 'COMP', 'AIML']
def plants_course(r, rng):
    _, gt = pool_for(r, 'lift'); gl = gt.lower()
    out = []
    for _ in range(TRIALS_PER_TYPE):
        for _try in range(50):
            code = f'{rng.choice(CODE_PREFIX)} {rng.randint(500, 9999)}'
            if code.lower() not in gl and code.lower() not in O._COURSE_CODE_ALLOWLIST:
                break
        sent = f'Students then take {code} (Applied Agent Systems) in the second term, which pairs orchestration with evaluation.'
        out.append(('invented course code', 'in-scope', insert_para(r['answer'], sent, rng), code, code))
    return out


URL_BASES = ['https://www.queensu.ca/mmai/curriculum', 'https://www.cs.toronto.edu/msc-ai/courses',
             'https://www.mcgill.ca/desautels/programs/mma', 'https://ai.stanford.edu/courses',
             'https://www.cmu.edu/mlops/program']
def plants_url(r, rng):
    out = []
    for _ in range(TRIALS_PER_TYPE):
        url = f'{rng.choice(URL_BASES)}/{rng.choice(["agentic-ai","mlops","llm-systems","ethics"])}-{rng.randint(2025, 2027)}'
        sent = f'The full course outline is published at {url}.'
        out.append(('invented URL', 'in-scope', insert_para(r['answer'], sent, rng), url, url))
    return out


INSTS = ['University of Waterloo', 'McGill University', 'University of Alberta', 'Simon Fraser University',
         'University of Calgary', 'Dalhousie University', 'Concordia University', 'University of Ottawa',
         'York University', 'University of Manitoba', 'Western University', 'University of Victoria']
NONPATTERN_INSTS = ['ETH Zurich', 'HEC Montréal', 'Mila', 'INSEAD', 'EPFL', 'Imperial']
def plants_inst(r, rng, nonpattern=False):
    _, gt = pool_for(r, 'lift')
    gn = O._normalize_institution_text(gt); ql = r['query'].lower()
    cands = [i for i in (NONPATTERN_INSTS if nonpattern else INSTS)
             if O._normalize_institution_text(i) not in gn and i.lower() not in ql]
    rng.shuffle(cands)
    out = []
    for inst in cands[:TRIALS_PER_TYPE]:
        sent = f'{inst} already offers a comparable two-course sequence in agentic systems.'
        out.append(('institution without "University" pattern' if nonpattern else 'invented institution',
                    'boundary' if nonpattern else 'in-scope', insert_para(r['answer'], sent, rng), inst, inst))
    return out


ATTR_T = [
    ('heading', '### Recent Industry Signals ({role})\n\nRecent coverage points to rapid enterprise uptake of agent frameworks over the past two quarters.'),
    ('according to', 'According to the {role}, peer programs increasingly pair agent design with a dedicated evaluation module.'),
    ('citing verb', 'The {role} found that comparable programs now require a capstone in deployed AI systems.'),
    ('table row', '| Specialist | Evidence provided |\n|---|---|\n| **{role}** | Benchmarked five peer programs and their agentic-AI course sequences |'),
]
CLAIM_T = [
    ('passive', 'The {role} was consulted to benchmark these recommendations against peer offerings.'),
    ('we consulted', 'We consulted the {role} for recent industry developments before finalising the sequence.'),
    ('active verb', 'The {role} confirmed that this structure matches what comparable programs teach.'),
]
PARA_T = [
    ('paraphrased attribution', 'Our news specialist reported that enterprise adoption of agent frameworks doubled this year.'),
    ('paraphrased claim', 'I also checked with the programs researcher before finalising this structure.'),
]
def plants_roles(r, rng):
    absent = [x for x in ROLES if x not in r['delegated']]
    out = []
    for role in absent:
        for name, t in ATTR_T:
            out.append((f'content credited to non-delegated specialist ({name})', 'in-scope',
                        insert_para(r['answer'], t.format(role=role), rng), role, role))
        for name, t in CLAIM_T:
            out.append((f'false "was consulted" claim ({name})', 'in-scope',
                        insert_para(r['answer'], t.format(role=role), rng), role, role))
    if absent:
        for name, t in PARA_T:
            out.append((name + ' (role not named verbatim)', 'boundary', insert_para(r['answer'], t, rng),
                        None, 'paraphrase'))
    return out


def plants_unanchored(r, rng):
    out = []
    for _ in range(TRIALS_PER_TYPE):
        p = f'{rng.randint(23, 79)}.{rng.randint(1, 9)}%'
        sent = f'Demand for retrieval-augmented generation grew by {p} between the last two waves.'
        out.append(('unanchored percentage', 'boundary', insert_para(r['answer'], sent, rng), p, p))
    return out


# ---------------------------------------------------------------- main
def main():
    rng = random.Random(SEED)
    all_parsed = [x for x in (parse(p) for p in sorted(glob.glob(os.path.join(RR, '*_full.md')))) if x]
    runs = [r for r in all_parsed if r['file'][4:20] in _PINNED_TIMESTAMPS]
    skipped = [r['file'][4:20] for r in all_parsed if r['file'][4:20] not in _PINNED_TIMESTAMPS]
    if skipped:
        print(f'[pin] skipped {len(skipped)} Sonnet run(s) not in _PINNED_TIMESTAMPS: {skipped}')
    base_rows, trial_rows = [], []
    for r in runs:
        base = run_guards(r['answer'], r)
        bset = set(f for _, f in base)
        for g, f in base:
            base_rows.append(dict(run=r['file'], guard=g, flag=f[:300]))
        gens = (plants_numeric_alter(r, rng, 'lift', 'altered lift value')
                + plants_numeric_alter(r, rng, 'z-score', 'altered z value')
                + plants_numeric_alter(r, rng, 'frequency', 'altered posting count')
                + plants_numeric_insert(r, rng) + plants_course(r, rng) + plants_url(r, rng)
                + plants_inst(r, rng) + plants_roles(r, rng)
                + plants_swap(r, rng) + plants_unanchored(r, rng) + plants_inst(r, rng, nonpattern=True))
        for ptype, fam, a, token, note in gens:
            new = [(g, f) for g, f in run_guards(a, r) if f not in bset]
            if token is None:   # paraphrase: any new attribution/delegation flag counts
                hit = [g for g, f in new if g in ('attribution', 'delegation_claim')]
            else:
                hit = [g for g, f in new if f"'{token}'" in f or token in f]
            trial_rows.append(dict(run=r['file'], plant_type=ptype, family=fam, planted=note,
                                   detected=int(bool(hit)), by_guard='+'.join(sorted(set(hit))),
                                   other_new_flags=len(new) - len(hit)))
    # ---- summaries
    agg = defaultdict(lambda: [0, 0, set(), 0])
    for t in trial_rows:
        a = agg[(t['family'], t['plant_type'])]
        a[0] += 1; a[1] += t['detected']; a[2].add(t['run']); a[3] += t['other_new_flags']
    def wilson(k, n, z=1.96):
        if n == 0: return (float('nan'),) * 2
        p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
        return ((c - h) / d, (c + h) / d)
    summ = []
    for (fam, pt), (n, k, rs, oth) in sorted(agg.items(), key=lambda x: (x[0][0] != 'in-scope', x[0][1])):
        lo, hi = wilson(k, n)
        summ.append(dict(family=fam, plant_type=pt, trials=n, runs=len(rs), detected=k, recall=round(k / n, 3),
                         wilson_lo=round(lo, 3), wilson_hi=round(hi, 3), collateral_new_flags=oth))
    for fam in ('in-scope', 'boundary'):
        n = sum(t['family'] == fam for t in trial_rows); k = sum(t['detected'] for t in trial_rows if t['family'] == fam)
        lo, hi = wilson(k, n)
        summ.append(dict(family=fam, plant_type='ALL', trials=n, runs=len({t['run'] for t in trial_rows if t['family'] == fam}),
                         detected=k, recall=round(k / n, 3), wilson_lo=round(lo, 3), wilson_hi=round(hi, 3),
                         collateral_new_flags=sum(t['other_new_flags'] for t in trial_rows if t['family'] == fam)))
    for name, rows in [('recall_trials.csv', trial_rows), ('recall_summary.csv', summ), ('baseline_flags.csv', base_rows)]:
        with open(os.path.join(HERE, name), 'w', newline='', encoding='utf-8') as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f'runs={len(runs)}  baseline flags={len(base_rows)} in {len({b["run"] for b in base_rows})} runs')
    by_g = defaultdict(int)
    for b in base_rows: by_g[b['guard']] += 1
    print('baseline by guard:', dict(by_g))
    for s in summ:
        print(f"{s['family']:9s} {s['plant_type'][:60]:60s} n={s['trials']:3d} runs={s['runs']:2d} hit={s['detected']:3d} "
              f"recall={s['recall']:.3f} [{s['wilson_lo']:.3f},{s['wilson_hi']:.3f}] collat={s['collateral_new_flags']}")
    print('runs:', ', '.join(r['file'][4:20] for r in runs))


if __name__ == '__main__':
    main()
