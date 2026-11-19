# CloudVision AI — Agent Working Rules

> Version: 1.0 | Phase 1: Project Initialization | Language: 繁體中文（專業術語保留英文）
> Scope: All files within this repository. User-confirmed requirements take precedence; never invent execution results.

## 1. Purpose and success criteria

CloudVision AI is an educational LLM Wiki on **AI-based Cloud and Shadow Detection in Satellite Imagery**. Ingest at least **five** verified academic papers and/or official technical documents; maintain a traceable Markdown Wiki; and use **the Wiki as the sole factual knowledge source for an 8–15-page interactive HTML teaching presentation** (target 10–12 pages).

This project evaluates reproducible knowledge work, not the training of a new cloud detection model. Do not depict teaching demonstrations as measured model inference.

## 2. Audience, language, content scope

- Tiered instruction: beginner-friendly explanations first, optional advanced technical material second.
- Main language: Traditional Chinese; include English technical terms at first mention.
- M01: 衛星影像與雲影問題 / Optical satellite imagery and observation quality.
- M02: 厚雲、薄雲、雲影、地形陰影與清晰像元.
- M03: 多光譜資訊、可見光、NIR、SWIR 與光譜特徵.
- M04: 傳統演算法、Fmask 與品質遮罩.
- M05: AI / CNN / U-Net / Semantic Segmentation, datasets and labels.
- M06: Precision, Recall, IoU, confusion matrix and clear-pixel applications.
- Make no universal accuracy ranking from results obtained on different datasets or sensors.

## 3. Source-of-truth hierarchy and permissions

1. `raw/` contains immutable source PDFs/documents. Never overwrite originals; do not store personal or confidential data. Record licenses and redistribution restrictions.
2. `sources.md` lists Source IDs, bibliographic metadata, DOI/URL, type, file path, access date and ingest status. Unknown fields must be marked 未確認, not fabricated.
3. `wiki/` contains curated knowledge derived from those sources; `wiki/index.md` is the entry point and `wiki/log.md` is append-only operational history.
4. `cards/` contains slide evidence derived **only from retrieved Wiki entries**, with provenance links all the way to `sources.md`.
5. `drafts/` and `deck.html` use approved cards and drafts. No additional external facts or scientific claims are introduced during rendering.

Original documents may be used to verify Wiki claims; slide generation must retrieve Wiki-derived knowledge instead of bypassing the Wiki.

## 4. Required metadata and traceability

For every source: stable `SRC-###`, title, authors/organization, year, DOI or URL, document version (if any), original path, access date, license or distribution note, ingest state.

For every significant Wiki entry: stable `W-M##-###`, bilingual title, beginner explanation, advanced explanation, supporting Source IDs with section/page **when verified**, related Wiki IDs, disagreements/conditions, validation state.

For every evidence card: stable `CARD-###`, supported claim, supporting Wiki IDs, source identifiers, confirmed page/section, teaching objective, proposed slide reference and review status. Slides must declare their cards/Wiki references. An unavailable passage/page must never be invented.

In conflicting studies, preserve differences and compare sensors, datasets, geographic contexts, assumptions and metrics. Flag unresolved contradictions rather than presenting them as facts.

## 5. Ingest procedure (incremental)

1. Before ingestion, register the actual file/source in `sources.md`; record parsing limitations and reuse rights.
2. Begin with 1–2 sources. Extract and inspect text; where PDF has tables or figures, review them instead of guessing from extraction.
3. Extract supported concepts and claims. Search for related/duplicate Wiki entries before adding new ones.
4. Create or update Wiki entries; preserve precise source connections; update `wiki/index.md` and append an actual operation to `wiki/log.md`.
5. Run structural Lint and semantic checks; register warnings/failures. Do not mark a source `ingested` until extraction, synthesis, indexing, provenance checks and review are complete.
6. After passing the batch, create a Git commit. Repeat until >=5 sources are genuinely ingested. File placement alone does **not** count as ingestion.

## 6. Query procedure

- Start at `wiki/index.md`, then read matching Wiki entries and recorded citations.
- Answers state relevant Wiki IDs and sources. If evidence is missing, say **資料不足** and return a gap report.
- Never silently fill missing knowledge using model memory or un-ingested external sources when building slides.

## 7. Wiki Lint and semantic validation

- Check Source IDs and Wiki IDs are unique and exist, links resolve, and indexed entries exist.
- Detect dangling references, missing required fields, unbacked numbers, near-duplicate entries and unresolved contradictions.
- Separately check semantic fidelity against original sources, especially tables, numerical comparisons and opposite causal claims.
- A machine passing link checks does not establish factual correctness. Record both automated and independent review outcomes.

## 8. Graph and separation of duties

Planned graph: Source Ingest → Wiki Build/Lint → Wiki Query → Coverage Gate → Evidence Cards → Outline → **Human Outline Approval** → Slide Drafts → Fidelity Gate → HTML Render → Render Gate → Report.

Each node has defined inputs, output artifacts, pass/fail checks, and only the permissions required for its task. Evidence creation cannot introduce external claims. Drafting can see approved outline and cards; rendering may change presentation/layout only, **not vetted scientific wording or numerical values**. Checking nodes report issues and do not covertly mutate artifacts.

On errors, return to nearest responsible node:
- Parsing failure → Ingest; missing coverage → Query, or Ingest if no source exists.
- Bad source link/evidence → Evidence Card or Wiki Build.
- Misleading/incorrect slide wording → only affected draft.
- Layout/interaction issues → HTML render.

A local repair loop may run at most **three correction attempts** for an issue; halt early if all gates pass, or stop with a truthful blocker report if evidence is insufficient, an unresolved conflict is material, or retry budget is exhausted. Never disable validation just to pass.

## 9. HTML deck requirements

- 8–15 navigable slides, target 10–12; beginner-friendly order, expandable advanced explanations.
- Original imagery / overlay / cloud-shadow mask toggle where properly sourced or explicitly identified as simulated illustration.
- Previous/next and keyboard navigation, responsive layout, visible Wiki/source references.
- Images must have valid reuse rights/attribution. Do not falsely label illustrative images as real satellite or model outputs.
- Ensure no visible overflow, broken buttons, unresolved source links or unsupported numbers.

## 10. Verification and independent review

- Automatic checks: files, identifiers, citations, slide count, HTML navigation and interactive behaviors, layout overflow where browser testing available.
- Independent content review: in a fresh review context using only draft/deck and supporting source evidence; check fidelity, coverage and any misleading claims.
- Human acceptance: approve outline, key scientific claims, and final publication.
- Preserve test commands, actual output, timestamp, failing node, corrections, attempt count and final result in `report.md` and/or `wiki/log.md`.

## 11. Git, publishing and security

- Git commits at clear milestones: initialization, first ingest, subsequent ingest, wiki lint, workflow, first deck, tested deck.
- Do not commit restricted source PDFs to a public GitHub repository. `.gitignore` protects `raw/` by default; only explicit lawful exceptions may be published.
- GitHub Pages may expose the HTML deck, attribution and public Wiki excerpts, not proprietary source files.
- Do not make changes outside the repository without explicit permission.

## 12. Definition of Done

- [ ] >=5 successfully ingested sources with verified metadata and traceable claims.
- [ ] Searchable, indexed Markdown Wiki with recorded Query and Lint runs.
- [ ] 8–15-slide working HTML presentation using Wiki-linked evidence only.
- [ ] Working Graph/Loop with real checks, routing and maximum-three-retry policy.
- [ ] At least one authentic execution log, test report, and reflection about actual failures and any checks moved earlier.
- [ ] Independent content review and human acceptance recorded.
- [ ] Public deliverable accessible and Git history retained.

**Phase 1 restriction:** only initialize project files and verify scaffold. Do **not** claim ingest, workflow execution, HTML rendering or final validation has occurred.

## 13. Phase 3 operational implementation (2026-11-19)

- Run `.agents/workflows/graph.py` using Python standard library for index-led Wiki Query, ID-based Coverage Check, immutable-excerpt Evidence Cards, deterministic provenance Fidelity Check, and proposed Outline.
- The source text of evidence cards must match the current Wiki entry byte-for-byte at the section-content level. The scientific correctness of the Wiki against the underlying PDFs is **not** mechanically certified.
- Query matching uses a human-authored plan with selected Wiki IDs, not vector retrieval; `match_score` is informational.
- Retry limit is three **per failing item**; after exhausting evidence retrieval, stop rather than producing unsourced slides.
- Use `.agents/workflows/README.md` for concrete commands, error-injection test cases, and honest known limitations.
- Do not proceed to slide drafts, HTML or claim human approval until explicitly authorized.
