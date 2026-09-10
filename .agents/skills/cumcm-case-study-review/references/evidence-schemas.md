# Evidence Card Schemas

Read this reference only when producing machine-readable case-study artifacts.
JSONL files contain one UTF-8 JSON object per non-empty line.

## Paper Card

Required fields are `paper_id`, `family`, `provenance`, `artifacts`,
`visually_checked_pages`, `facts`, `interpretation`, `not_transferable`, and
`evidence_level`. Every fact includes an artifact path and page or field
location.

## Artifact Card

Required fields are `artifact_id`, `type`, `path`, `producer`, `consumers`,
`schema_or_interface`, `units`, `quality_findings`, `verification`, and
`confidence`. For an output template, also record sheet/table names, row and
column semantics, precision, dynamic dimensions, and unresolved ambiguity.

## Paper-Artifact Link

Required fields are `paper_id`, `artifact_id`, `relationship`, `evidence`, and
`match_status`. `match_status` is one of `verified`, `topic_level`,
`conflicting`, or `unknown`. A README without identity/input/output checks
cannot produce `verified`.

## Pattern Card

Required fields are `pattern_id`, `candidate_rule`, `mechanism`,
`supporting_cases`, `families`, `counterexamples`, `applicability`,
`failure_modes`, `cost`, `acceptance_test`, and `evidence_level`.

Do not mark a pattern E4 until a separate replay record identifies the tested
case, baseline, changed behavior, regression result, and negative-transfer
check.
