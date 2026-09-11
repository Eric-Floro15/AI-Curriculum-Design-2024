"""compose_demo_healthcare.py — same composed-marginals method as compose_demo.py,
for the "Healthcare Delivery" sector bucket (n~1,060; EHR/Health Informatics/HIPAA/
Clinical Trials) rather than "Life Sciences" (n~368; immunology/chemistry).

Column names are kept identical to compose_demo.py's output (n_fin/lift_fin/z_fin
etc.) even though the sector is healthcare, not finance -- compose_tool.py's
composed_curriculum() reads those column names literally regardless of sector
(chatbot/tools/compose_tool.py: df["z_fin"], df["lift_fin"]), so the schema is
load-bearing, not just a naming leftover.

Output: compose_healthcare_W2026.csv -> copy to chatbot/data/ so the
composed_sector_tool's sector string "healthcare" resolves to it (mirrors how
"finance" -> compose_finance_W2026.csv, per compose_tool.py's _sector_file()
fuzzy match on the compose_<tag>_W2026.csv filename).
"""
import sys
import pandas as pd, numpy as np

# 2026-09-11 (RUN2D Item 1): see compose_demo.py's matching comment -- ONLY
# z_fin is conformed to lift_analysis.py's canonical (filtered) method;
# z_ag/z_jo/z_delta stay on the original unfiltered fw(), since they match
# a separate frozen source (skill_lift_table.csv) this task doesn't touch
# and none of RUN2D's anchors are z_ag values.
sys.path.insert(0, '.')
import lift_analysis as la

SECTOR_LABEL = 'Healthcare Delivery'
OUT_FILE = 'compose_healthcare_W2026.csv'

RUN = 'RE-ANALYSIS-2026/pipeline_runs/W2026'
M = pd.read_csv(RUN + '/skill_presence_matrix.csv', index_col=0)
attrs = pd.read_csv(RUN + '/posting_attributes.csv', low_memory=False)
n = min(len(M), len(attrs)); M = M.iloc[:n]; attrs = attrs.iloc[:n].reset_index(drop=True)
skills = list(M.columns); P = M.values.astype(bool)
sec = pd.read_csv('company_sectors_final.csv')
cmap = dict(zip(sec.company_norm, sec.sector_final))
post_sector = attrs.company_norm.map(cmap)
AG = 'Agentic Ai'; agi = skills.index(AG)
m_ag = P[:, agi]; m_fin = (post_sector == SECTOR_LABEL).values
m_joint = m_ag & m_fin; m_agnf = m_ag & (~m_fin)
def cnt(m): return P[m].sum(0).astype(float)
c_corp = P.sum(0).astype(float); c_ag = cnt(m_ag); c_fin = cnt(m_fin); c_joint = cnt(m_joint); c_agnf = cnt(m_agnf)
Nag = int(m_ag.sum()); Nfin = int(m_fin.sum()); Njoint = int(m_joint.sum()); Nagnf = int(m_agnf.sum()); Ncorp = len(P)


def fw(seg, base):
    """Original unfiltered Fightin'-Words z -- kept for z_ag/z_jo/z_delta
    only (see scope note above). NOT used for z_fin any more."""
    seg = seg.astype(float); base = base.astype(float); a0 = base
    ns, nb, na = seg.sum(), base.sum(), a0.sum()
    with np.errstate(divide='ignore', invalid='ignore'):
        d = np.log((seg + a0) / (ns + na - seg - a0)) - np.log((base + a0) / (nb + na - base - a0))
        z = d / np.sqrt(1.0 / (seg + a0) + 1.0 / (base + a0))
    return np.nan_to_num(z)


def canonical_z(seg_counts, base_counts, min_count=25):
    """lift_analysis.py's exact method -- see compose_demo.py's canonical_z
    for the full explanation. Independent-filters to n_seg >= min_count
    before computing z; excluded skills get NaN (fails any z-based cut
    safely, matching lift_analysis.py never reporting a z for them)."""
    seg_counts = np.asarray(seg_counts, float)
    base_counts = np.asarray(base_counts, float)
    keep = seg_counts >= min_count
    z = np.full(len(seg_counts), np.nan)
    if keep.any():
        z[keep] = la.fightin_words(seg_counts[keep], base_counts[keep])
    return z


def prof(cseg, cbase, Ns, Nb, z_fn=fw):
    ps = cseg / Ns; pb = cbase / Nb; lift = np.where(pb > 0, ps / pb, np.nan)
    return lift, z_fn(cseg, cbase)
lift_ag, z_ag = prof(c_ag, c_corp, Nag, Ncorp)
lift_fin, z_fin = prof(c_fin, c_corp, Nfin, Ncorp, z_fn=canonical_z)
lift_jo, z_jo = prof(c_joint, c_corp, Njoint, Ncorp)
lift_dl, z_dl = prof(c_joint, c_agnf, Njoint, Nagnf)
df = pd.DataFrame({'skill': skills, 'n_ag': c_ag.astype(int), 'lift_ag': lift_ag, 'z_ag': z_ag,
  'n_fin': c_fin.astype(int), 'lift_fin': lift_fin, 'z_fin': z_fin,
  'n_joint': c_joint.astype(int), 'lift_jo': lift_jo, 'z_jo': z_jo, 'lift_delta': lift_dl, 'z_delta': z_dl})
df = df[df.skill.str.lower() != 'agentic ai'].copy()
df['lift_comp'] = df.lift_ag * df.lift_fin
df.to_csv(OUT_FILE, index=False)
print('=== sector=%s | N: corpus=%d agentic=%d sector=%d joint(ag&sector)=%d ag_not_sector=%d ===' % (
    SECTOR_LABEL, Ncorp, Nag, Nfin, Njoint, Nagnf))
llm = df[df.skill.str.lower().str.startswith('large language')].iloc[0]
print('VERIFY LLM agentic marginal: lift=%.2f z=%.2f (should match compose_finance_W2026.csv exactly -- same agentic marginal, sector-independent)' % (llm.lift_ag, llm.z_ag))
adopt_lift = (c_fin[agi] / Nfin) / (c_corp[agi] / Ncorp); adopt_z = z_fin[agi]
print('ADOPTION: agentic-AI demand in %s vs corpus: lift=%.2f z=%.2f (n_sector_agentic=%d)' % (SECTOR_LABEL, adopt_lift, adopt_z, int(c_fin[agi])))
def show(d, cols, title, k=12):
    print('\n=== %s ===' % title)
    print(d[cols].head(k).to_string(index=False, float_format=lambda x: '%.2f' % x))
core = df[df.z_ag >= 2].sort_values('z_ag', ascending=False)
show(core, ['skill', 'n_ag', 'lift_ag', 'z_ag', 'lift_fin', 'z_fin'], 'AGENTIC CORE (top by z_ag) -- is it emphasized in healthcare too?', 12)
adds = df[(df.n_joint >= 8)].sort_values('z_delta', ascending=False)
show(adds, ['skill', 'n_joint', 'lift_delta', 'z_delta', 'lift_fin', 'z_fin'], 'PANEL B DELTA: what healthcare ADDS within agentic (interaction)', 10)
comp = df[((df.z_ag >= 2) | (df.z_fin >= 2)) & (df.lift_ag >= 1) & (df.lift_fin >= 1)].sort_values('lift_comp', ascending=False)
show(comp, ['skill', 'lift_ag', 'z_ag', 'lift_fin', 'z_fin', 'lift_comp', 'lift_jo', 'z_jo'], 'COMPOSED agentic-in-healthcare curriculum (rank by lift_ag x lift_fin)', 15)

# Verification sanity check: EHR / Health Informatics / HIPAA / Clinical Trials
print('\n=== SANITY CHECK: healthcare-distinctive skills ===')
check_terms = ['ehr', 'health informatics', 'hipaa', 'clinical trial', 'electronic health']
for _, r in df.iterrows():
    key = r.skill.lower()
    if any(t in key for t in check_terms):
        print('  %-40s n_fin=%-5d lift_fin=%6.2f z_fin=%6.2f lift_comp=%6.2f' % (
            r.skill, r.n_fin, r.lift_fin, r.z_fin, r.lift_comp))
