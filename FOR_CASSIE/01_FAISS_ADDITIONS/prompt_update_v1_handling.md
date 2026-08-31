# Handling V1 vs V2 taxonomy content in the skills index

## Why this exists

Your existing skills index almost certainly already has V1 taxonomy
content in it (`Grouped_Skills_Categorized_Updated.xlsx`, built before V2
existed) — untagged, no version metadata. This bundle adds V2 taxonomy
content (`v2_taxonomy_skills.jsonl`) tagged `taxonomy_version: V2,
status: current`.

We deliberately did **not** re-embed the V1 descriptions to sit alongside
V2 with an "outdated" tag. Re-adding V1 content as a second, separately-
tagged copy risks the same retrieval-crowding problem you already found
and fixed once in the news corpus (VentureBeat-style near-duplicate
chunks eating retrieval slots that should've gone to something else) —
here it'd be two near-identical descriptions of the same skill competing
for the same top-k slot, and FAISS ranks by embedding similarity, not by
version tag, so a metadata tag alone doesn't stop that from happening.

## What we're recommending instead

Handle it at the prompt layer, not the data layer — same pattern as the
institution-name sanity check you already added to the University
Programs agent. Add something like this to the Skills Taxonomy Analyst
agent's backstory/instructions:

> When you retrieve skill taxonomy entries, some will be tagged
> `taxonomy_version: V2, status: current` — these are the current,
> authoritative descriptions. Entries without a `taxonomy_version` tag
> are from an older taxonomy version and may use outdated category
> labels or terminology. If both a V2-tagged and an untagged entry
> surface for the same skill, prefer the V2-tagged one and don't
> mention the untagged one unless asked specifically about how the
> taxonomy has changed over time.

This avoids touching your existing index at all — no risk of breaking
anything already working, no duplicate-content crowding risk, and it's a
one-line change you can revert instantly if it doesn't behave as
expected.

## If you'd rather have a fully clean, explicitly-tagged index instead

That's a reasonable thing to want (e.g. if you want the chatbot to be
able to answer "how has the taxonomy changed" queries directly from
retrieval rather than just "trust me, V2 is newer"). But doing it
properly means rebuilding the skills index from scratch with both V1 and
V2 explicitly tagged from the start, rather than appending — a bigger
job than this bundle is set up for. Worth flagging as an option, not
something we're pushing you toward by default. Let Eric know if you want
to go this route and we can help scope it.
