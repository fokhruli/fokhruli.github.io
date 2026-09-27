# JEPA Atlas

A contribution-centered, evidence-linked knowledge base for JEPA literature. The first edition covers the **19 papers from the September 26, 2026 additions**, not every entry in the upstream awesome list. Author and institutional networks are deliberately omitted.

## Read

Open `index.html` through a local HTTP server or the hosted `/JEPA-all/` site. Browse the paper library, focus the concept graph, compare up to four records, or follow a reading path. Each paper has a permanent `#paper=ARXIV_ID` link.

```bash
python -m http.server 8000
# Open http://localhost:8000
```

For a single-file viewer that opens without a server:

```bash
python kb.py offline
# Open JEPA-Atlas-offline.html
```

Primary-source links still need internet access; the offline viewer itself does not. The viewer stores only comparison selections in browser local storage. It has no tracking, backend, API key, external font, CDN or model dependency.

## Data model

`knowledge.json` is the only canonical content source. Its `papers` array uses arXiv identifiers as stable IDs and retains aliases for renamed or colliding acronyms. It records:

- The problem, plain-language intuition, technical mechanism and abbreviated objective/pipeline.
- Training signals versus deployment inputs.
- Result records with task, metric, value, units, comparator, protocol, uncertainty and a source locator.
- Limitations, curator-proposed experiments, review status and curation audits.

`concepts` provide a readable technical vocabulary. Paper-to-concept links are curated topic associations, **not citations or statements of methodological equivalence**. `relations` distinguish documented comparisons (source required) from curator comparisons or tensions. `paths` define question-led reading sequences.

All summarized results are **author-reported, not independently reproduced**. `sections_checked` means selected method/result sections were inspected, not that the entire paper was audited. `abstract_only` is intentionally visible. Missing uncertainty is `null`, never zero. Different tasks and protocols are not converted into a leaderboard. Equations use normalized/abbreviated notation, not a claim to reproduce all derivation details.

## Maintain and retrieve

Python 3.10+ and a modern browser are sufficient. The maintainer uses the standard library only.

```bash
python kb.py validate
python kb.py search "privileged"
python kb.py show 2608.24044
python kb.py export
python kb.py offline
```

`export` generates `COMPILATION.md`, independent Markdown files in `generated/papers/`, and `generated/papers.jsonl`. These exports can be indexed by a retrieval system, but are not separately editable sources. Browser export buttons create JSON, JSONL and Markdown directly from the loaded data.

To add a reviewed record, copy an existing paper into a new JSON file, replace all of its content and evidence, then run:

```bash
python kb.py add new-paper.json
python kb.py validate
python kb.py export
```

The `add` command refuses duplicate IDs and invalid source/graph references. It does not read papers, verify claims, update concept memberships or publish for you. Update relevant concepts, relationships, reading paths, scope and review-date metadata deliberately. See `AGENTS.md` and `schema.json`.

## Publishing

The requested URL is served by the isolated `JEPA-all/` folder in `fokhruli/fokhruli.github.io`. No new GitHub project repository is required. Keep all changes inside that folder. Do not change the parent site's `CNAME`, homepage, theme, build settings or visibility.

After source edits, validate, regenerate exports and commit together. The online viewer reads `knowledge.json`; the single-file offline edition must be regenerated after content/code changes. Hosting a commit and verifying that GitHub Pages serves it are separate checks.

Only public literature and original summaries belong here. Do not publish private repository history, personal data, unreleased experiments, credentials or full-text paper copies.

## Provenance and design

The initial paper set comes from the 19 additions to `AbdelStark/awesome-jepa` curated on September 26, 2026. Canonical primary links and source versions appear in every record. The separation of knowledge creation and graph visualization was inspired by `sgottsch/research_institute_kg`; no source code was copied from that project. This site instead uses a dependency-free static viewer suitable for GitHub Pages.

The graph is a technical reading aid, not an automated causal or citation graph. Future extraction agents must preserve evidence boundaries rather than make the graph denser with unverified edges.
