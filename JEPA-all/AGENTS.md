# Agent contract: JEPA Atlas

## Mission

Maintain a technically useful public knowledge base, not a list of abstracts or an author network. Prioritize mechanisms, objectives, evaluation protocols, limitations and connections that help a researcher reason across papers.

## Canonical files and scope

Read `knowledge.json`, `schema.json` and this file before editing. Use `python kb.py search QUERY` and `python kb.py show ARXIV_ID` for retrieval. Never edit generated Markdown/JSONL or offline HTML as the primary content source. Scope currently covers the September review's 19 additions; adding a new record must not imply that the entire JEPA literature is covered.

Public site directory: `JEPA-all/` in `fokhruli/fokhruli.github.io`. No writes outside this directory. The private `World-model-all` repository is not a source of additional publishable research data merely because an agent can read it.

## Ingest one paper

1. Resolve its stable arXiv ID and inspect the primary record plus the actual article. Pin the version used. Check title changes and aliases. The two D-JEPA names and the different TD-JEPA works must not be merged.
2. Read the method and deployment setup. Identify what the encoder receives, what the target means, what the predictor estimates, how collapse is avoided, which parameters/targets receive gradients, and what inputs are still needed at test time. Do not invent uninspected details.
3. Read the result table and experimental protocol together. For each selected result store the exact task, metric, units, value, comparator, protocol, uncertainty convention and section/table locator. Separate percentages from percentage points; distinguish reward, success, RMSE, AUROC and benchmark-specific scores.
4. Preserve evidence status. `sections_checked` is selected-section review, not replication; `abstract_only` stays abstract-only until supported extraction. Use `null` and explain missing data. A reported range is not a confidence interval. Multiple cross-validation repeats are not new independent cohorts. Main single-seed runs and compact multi-seed runs are different protocols.
5. Summarize in your own words. Do not copy full abstracts, paper bodies or PDFs. Keep the source-derived brief compact and use original pedagogical interpretation only where labeled. Schematic equations must say they are schematic; exact equations need exact source locators and notation checking.
6. Keep author claims distinct from curator experiments and hypotheses. An observed result is not a guarantee. Glucose phenotype prediction is not evidence of safe dosing; model counterfactuals are not automatically identified causal effects.
7. Add concept associations sparingly. `documented_comparison` requires a primary source and locator. `curator_comparison` / `curator_tension` are reading connections, not claims that one paper cites or refutes another.
8. Run `python kb.py validate`, regenerate exports, check the rendered card and graph, and inspect the repository diff. Adding a paper alone does not grant authorization for recurring autonomous writes.

## Result selection

Choose a representative, protocol-matched comparison plus a counterexample or ablation when important. Do not cherry-pick a weak baseline when a stronger matched comparator is reported. Never pool raw metrics from different datasets or rank papers by incompatible scores. Preserve unfavorable outcomes, missing uncertainty and conflicting text/table values. Check known audits before repeating old claims.

## Update existing evidence

Do not silently replace v1 evidence with numbers from v2. Change the pinned version and affected source locators together, add an audit note explaining a material correction, and rely on Git history to retain the previous snapshot. Reconcile concurrent repository edits before committing; never force-push the website branch.

## Publication checks

Do not alter the parent homepage, custom domain, Pages settings, theme or repository visibility. Do not include secrets, private notes, unpublished experiments, identifiable patient records or personal information. Only the reviewed literature artifacts are authorized for the public visualization.

After publishing, distinguish: files committed; deployment/build succeeded; actual URL verified. Report the state supported by tool results, not an assumed successful deployment.
