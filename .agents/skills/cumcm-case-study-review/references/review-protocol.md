# Historical Pair Review Protocol

## Evidence Extraction

Freeze the corpus before reading it. Record a snapshot identifier and the
availability of the problem, paper, page images, OCR/layout data, attachments,
code, and provenance metadata. If files continue changing, postpone synthesis
or mark the snapshot incomplete.

For each pair, record only observations traceable to named artifacts:

| Lens | Extract | Do not extract |
| --- | --- | --- |
| Problem structure | deliverables, dependencies, shared mechanisms, data and output constraints | the paper's final numeric answer |
| Modeling architecture | state and decision variables, objective, constraints, subproblem grouping | a model choice as a universal template |
| Evidence chain | validation type, baselines, robustness tests, result-to-claim links | unsupported claims of correctness |
| Communication | section purpose, figure/table role, appendix evidence strategy | sentences, captions, or visual assets |
| Delivery | file schema, rounding, reproducibility artifacts, format compliance | source code or workbook content |

For each item, keep four fields distinct: `fact`, `interpretation`,
`rule_candidate`, and `not_transferable`. OCR locates evidence. Formula, table,
diagram, and low-confidence content must be checked against the original page
before it can exceed E0; record the checked page and do not silently repair OCR.

## Comparison Method

Build a matrix across pairs. A reusable pattern needs a concrete benefit,
explicit supporting evidence, and a boundary describing when it does not
apply. Record disagreements rather than resolving them by majority vote.

An acceptable rule asks the current agent to verify whether questions share a
state model. It does not order the agent to reuse a historical equation or
solver.

## Provenance And Evidence Strength

Provenance and evidence strength are separate:

- `official_award_verified`: verified award provenance.
- `organizer_showcase`: organizer-provided showcase, without assumed ranking.
- `author_claimed`: useful only after checking the artifacts themselves.
- `project_demo`: workflow audit evidence, never contest-ranking evidence.

| Level | Meaning | Permitted use |
| --- | --- | --- |
| E0 | OCR locator, missing original page, or unverified linkage | search lead only |
| E1 | one artifact-level fact visually checked | case observation |
| E2 | repeated evidence within one problem family | family hypothesis |
| E3 | three independent cases across two families and a counterexample check | default workflow candidate |
| E4 | E3 plus successful independent replay/ablation | validated workflow default |

At least three independent pairs over two problem families are needed before a
pattern becomes a default recommendation. A paper's provenance never upgrades
an unverified observation by itself.

## Artifact Lineage

For every attachment or code source, record its producer, consumer, schema or
interface, units, transformation, expected output, and match confidence. README
existence alone is not proof that code implements the paper. A paper-code link
may be `verified`, `topic_level`, `conflicting`, or `unknown`.

## Applying And Replaying The Review

Compare each observation with the current problem's mechanism, required
outputs, data support, and scoring constraints. Convert it into a falsifiable
task check. Any implementation still follows the main AutoMCM-Pro verification
and review gates.

Before promoting E3 to E4, replay the rule on a mechanism-related case and a
dissimilar counterexample. Report new failures/warnings, manual repair time,
and negative transfer. Failed replay demotes the rule to guidance.
