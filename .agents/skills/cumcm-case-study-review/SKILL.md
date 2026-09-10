---
name: cumcm-case-study-review
description: >
  Review user-provided CUMCM problem-paper pairs to extract evidence-backed,
  reusable modeling-workflow patterns. Use before a modeling task only when
  local reference pairs are available; do not use it to copy papers, claims,
  wording, code, or numerical conclusions.
---

# CUMCM Case-Study Review

Turn a frozen local corpus of historical problem-paper pairs into traceable
process guidance for a later modeling task. The outcome is an evidence report,
not a reproduction of a reference paper.

## Scope And Inputs

Before extraction, record a corpus snapshot: local paths, file counts, sizes,
timestamps or hashes when available, and missing artifacts. Do not modify the
source corpus. For every pair, identify the problem statement, paper,
attachments, code source, and provenance. Distinguish
`official_award_verified`, `organizer_showcase`, `author_claimed`, and
`project_demo`. Never call a paper "best" or "optimal" without verifiable award
evidence supplied by the user.

Read [the review protocol](references/review-protocol.md) before reviewing a
corpus. Read [the evidence schemas](references/evidence-schemas.md) when
writing machine-readable cards. Use the PDF and spreadsheet skills where their
artifacts require them.

For the repository's two built-in demos, read
[the local pilot observations](references/local-pilot-observations.md). Treat
them only as `project_demo` evidence; they are not a substitute for a supplied
historical award corpus.

## Required Output

Write `CUMCM_Workspace/memory/case_study_review.md` with:

1. A corpus table: pair id, year/problem, provenance, accessible artifacts,
   snapshot id, and limitations.
2. A problem-to-model map for each pair. Group questions only when they share
   the same state variables, mechanism, interface, and validation basis.
3. Reusable patterns, each citing exact local evidence locations and an
   `E0`--`E4` level.
4. Counterexamples, rejected patterns, and uncertainty.
5. A task-specific checklist framed as checks, never a forced model choice.

Store `paper_cards.jsonl`, `artifact_cards.jsonl`,
`paper_artifact_links.jsonl`, and `pattern_catalog.json` under
`CUMCM_Workspace/memory/case_studies/`. Every card separates observed fact,
interpretation, candidate rule, and current-task applicability.

## Evidence Rules

- OCR text is a locator, not formula or table truth. Visually inspect the
  original page for formulas, tables, diagrams, low-confidence symbols, and
  any claim used in a rule. Record the page and inspection method.
- A code README proves only that a source description exists. Treat code as
  paper-matched only when identity, version, license, inputs, and outputs are
  verified; otherwise mark the link `topic_level` or `unknown`.
- `E0`: locator or unverified extraction; `E1`: one visually checked case;
  `E2`: repeated evidence inside one family; `E3`: at least three independent
  cases across two families plus a counterexample check; `E4`: an E3 rule that
  improves independent replay cases. Only E3 or E4 may become a default
  workflow rule. E4 requires replay evidence, not reviewer confidence.
- When original pages are unavailable, preserve the observation as E0 and do
  not infer missing formulas or table values.

## Guardrails

- Do not copy prose, tables, figures, references, code, numerical results, or
  unverified claims from the reference papers.
- Do not treat project demos as award-winning evidence.
- Do not make a pattern mandatory from fewer than three independent,
  provenance-identified pairs spanning at least two problem families.
- Do not prescribe the current problem's physics or numerical method from a
  corpus without a direct mechanism match. Keep workflow analogies and domain
  equations separate.
- A reference paper cannot replace literature research, numerical verification,
  sensitivity analysis, or compliance checks for the current task.
- Preserve the current problem's deliverables and constraints even when a
  historical pair used different ones.
