import sys
import pandas as pd, numpy as np

# 2026-09-11 (RUN2D Item 1): the SECTOR-lift z (z_fin -- what sector_wrap()
# actually surfaces and what the anchor check validates) is now computed
# via lift_analysis.py's own fightin_words (the paper-canonical routine
# every frozen table, incl. the headline agentic-segment z's, already
# uses) instead of a second, hand-rolled copy that disagreed with it by
# ~2% on the finance anchors (RUN2C finding: the old fw() below ran
# fightin_words over the FULL ~962-skill vector; lift_analysis.py filters
# to n>=25 first, which changes the informative-prior's normalising
# total). Import, not replicate: lift_analysis.py's fightin_words is a
# plain, side-effect-free function (confirmed importable, no argparse/
# main execution on import).
#
# Scope note: z_ag/z_jo/z_delta are DELIBERATELY left on the original fw()
# below, not conformed. They already match a DIFFERENT frozen source
# (chatbot/data/skill_lift_table.csv, the "agentic core" skill_lift_tool
# reads -- itself generated over W2026 with an unfiltered fightin_words,
# e.g. Large Language Models z=9.56 exact) -- conforming them to
# lift_analysis.py's filtered method was tried and shifts them away from
# that match (LLM z_ag: 9.56 -> 9.22) for no anchor-check benefit, since
# none of RUN2D's 6 anchors are z_ag values and the "core" list never
# reads this file's z_ag column at all (it reads skill_lift_table.csv
# directly, an entirely separate pipeline). Conforming only what's
# actually anchored/tested is the minimal, correct fix.
sys.path.insert(0, '.')
import lift_analysis as la

RUN='RE-ANALYSIS-2026/pipeline_runs/W2026'
M=pd.read_csv(RUN+'/skill_presence_matrix.csv', index_col=0)
attrs=pd.read_csv(RUN+'/posting_attributes.csv', low_memory=False)
n=min(len(M),len(attrs)); M=M.iloc[:n]; attrs=attrs.iloc[:n].reset_index(drop=True)
skills=list(M.columns); P=M.values.astype(bool)
sec=pd.read_csv('company_sectors_final.csv')
cmap=dict(zip(sec.company_norm,sec.sector_final))
post_sector=attrs.company_norm.map(cmap)
AG='Agentic Ai'; agi=skills.index(AG)
m_ag=P[:,agi]; m_fin=(post_sector=='Finance & Insurance').values
m_joint=m_ag&m_fin; m_agnf=m_ag&(~m_fin)
def cnt(m): return P[m].sum(0).astype(float)
c_corp=P.sum(0).astype(float); c_ag=cnt(m_ag); c_fin=cnt(m_fin); c_joint=cnt(m_joint); c_agnf=cnt(m_agnf)
Nag=int(m_ag.sum());Nfin=int(m_fin.sum());Njoint=int(m_joint.sum());Nagnf=int(m_agnf.sum());Ncorp=len(P)


def fw(seg,base):
    """Original unfiltered Fightin'-Words z -- kept for z_ag/z_jo/z_delta
    only (see scope note above). NOT used for z_fin any more."""
    seg=seg.astype(float); base=base.astype(float); a0=base
    ns,nb,na=seg.sum(),base.sum(),a0.sum()
    with np.errstate(divide='ignore',invalid='ignore'):
        d=np.log((seg+a0)/(ns+na-seg-a0))-np.log((base+a0)/(nb+na-base-a0))
        z=d/np.sqrt(1.0/(seg+a0)+1.0/(base+a0))
    return np.nan_to_num(z)


def canonical_z(seg_counts, base_counts, min_count=25):
    """lift_analysis.py's EXACT method: independent-filter skills to
    n_seg(=seg_counts) >= min_count BEFORE computing z (its own
    `keep = df.n_seg >= args.min_count; df = df[keep]` happens before
    `z = fightin_words(df.n_seg.values, df.n_base.values)`), so the
    informative prior's normalising total matches what lift_analysis.py
    itself would report for these skills. Skills failing the filter get
    NaN -- lift_analysis.py never reports a z for them either (excluded
    before significance testing, per Bourgon et al.'s independent-
    filtering argument its own docstring cites) -- NaN comparisons (e.g.
    `z >= 2`) fail safely, so they can never pass a z-based cut downstream.
    """
    seg_counts = np.asarray(seg_counts, float)
    base_counts = np.asarray(base_counts, float)
    keep = seg_counts >= min_count
    z = np.full(len(seg_counts), np.nan)
    if keep.any():
        z[keep] = la.fightin_words(seg_counts[keep], base_counts[keep])
    return z


def prof(cseg,cbase,Ns,Nb,z_fn=fw):
    ps=cseg/Ns; pb=cbase/Nb; lift=np.where(pb>0,ps/pb,np.nan); return lift, z_fn(cseg,cbase)
lift_ag,z_ag=prof(c_ag,c_corp,Nag,Ncorp)
lift_fin,z_fin=prof(c_fin,c_corp,Nfin,Ncorp,z_fn=canonical_z)
lift_jo,z_jo=prof(c_joint,c_corp,Njoint,Ncorp)
lift_dl,z_dl=prof(c_joint,c_agnf,Njoint,Nagnf)
df=pd.DataFrame({'skill':skills,'n_ag':c_ag.astype(int),'lift_ag':lift_ag,'z_ag':z_ag,
  'n_fin':c_fin.astype(int),'lift_fin':lift_fin,'z_fin':z_fin,
  'n_joint':c_joint.astype(int),'lift_jo':lift_jo,'z_jo':z_jo,'lift_delta':lift_dl,'z_delta':z_dl})
df=df[df.skill.str.lower()!='agentic ai'].copy()
df['lift_comp']=df.lift_ag*df.lift_fin
df.to_csv('compose_finance_W2026.csv',index=False)
print('=== N: corpus=%d agentic=%d finance=%d joint(ag∩fin)=%d ag_not_fin=%d ==='%(Ncorp,Nag,Nfin,Njoint,Nagnf))
llm=df[df.skill.str.lower().str.startswith('large language')].iloc[0]
print('VERIFY LLM agentic marginal: lift=%.2f z=%.2f (CS1 said 6.17 / 9.36)'%(llm.lift_ag,llm.z_ag))
adopt_lift=(c_fin[agi]/Nfin)/(c_corp[agi]/Ncorp); adopt_z=z_fin[agi]
print('ADOPTION: agentic-AI demand in finance vs corpus: lift=%.2f z=%.2f (n_fin_agentic=%d)'%(adopt_lift,adopt_z,int(c_fin[agi])))
def show(d,cols,title,k=12):
    print('\n=== %s ==='%title)
    print(d[cols].head(k).to_string(index=False,float_format=lambda x:'%.2f'%x))
core=df[df.z_ag>=2].sort_values('z_ag',ascending=False)
show(core,['skill','n_ag','lift_ag','z_ag','lift_fin','z_fin'],'AGENTIC CORE (top by z_ag) — is it emphasized in finance too?',12)
adds=df[(df.n_joint>=8)].sort_values('z_delta',ascending=False)
show(adds,['skill','n_joint','lift_delta','z_delta','lift_fin','z_fin'],'PANEL B DELTA: what finance ADDS within agentic (interaction)',10)
comp=df[((df.z_ag>=2)|(df.z_fin>=2))&(df.lift_ag>=1)&(df.lift_fin>=1)].sort_values('lift_comp',ascending=False)
show(comp,['skill','lift_ag','z_ag','lift_fin','z_fin','lift_comp','lift_jo','z_jo'],'COMPOSED agentic-in-finance curriculum (rank by lift_ag x lift_fin)',15)
