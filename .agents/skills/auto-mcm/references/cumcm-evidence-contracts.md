# CUMCM Evidence Contracts

Read this reference only for a CUMCM run. Paths below are relative to
`CUMCM_Workspace/` unless absolute.

## `memory/problem_fingerprint.json`

Record `problem_id`, `mechanisms`, `geometry_or_data_structure`,
`state_variables`, `decision_variables`, `constraints`, `inputs`, `outputs`,
`uncertainties`, and `validation_opportunities`. These are observations and
candidates, not a solver prescription.

## `memory/problem_graph.json`

```json
{
  "questions": [
    {"id": "Q1", "deliverables": ["result1"], "model_unit": "M1"},
    {"id": "Q2", "deliverables": ["result2"], "model_unit": "M1"},
    {"id": "Q3", "deliverables": ["result3"], "model_unit": "M1"},
    {"id": "Q4", "deliverables": ["result4"], "model_unit": "M2"}
  ],
  "model_units": [
    {
      "id": "M1",
      "questions": ["Q1", "Q2", "Q3"],
      "depends_on": [],
      "purpose": "shared state engine",
      "states": ["state_a"],
      "inputs": ["input_a"],
      "outputs": ["state_history"],
      "validation_profile": ["initial_condition", "grid_convergence"]
    },
    {
      "id": "M2",
      "questions": ["Q4"],
      "depends_on": ["M1"],
      "purpose": "geometry-varying variant",
      "states": ["state_a"],
      "inputs": ["state_history", "geometry_history"],
      "outputs": ["result4"],
      "validation_profile": ["coordinate_mapping", "balance_check"]
    }
  ],
  "question_to_model": {"Q1": "M1", "Q2": "M1", "Q3": "M1", "Q4": "M2"}
}
```

The example demonstrates shared-state grouping only. A dissimilar problem may
have one unit per question or another justified graph.

## `memory/artifact_contract.json`

```json
{
  "contest": "CUMCM",
  "problem_id": "year_problem",
  "inputs": [
    {
      "id": "input1",
      "path": "data/input.xlsx",
      "must_exist": true,
      "schema": {"sheets": ["Sheet1"], "columns": ["time", "value"]},
      "units": {"time": "s", "value": "problem unit"},
      "processing": ["interpolation method and boundary behavior"]
    }
  ],
  "deliverables": [
    {
      "id": "result1",
      "path": "output/result1.xlsx",
      "required": true,
      "schema": {"sheets": ["Sheet1"], "precision_decimals": 4},
      "source_evidence": ["problem.pdf#page=3"],
      "validation": ["sheet names", "row/column semantics", "no placeholders"]
    }
  ],
  "ambiguities": [
    {
      "id": "A1",
      "location": "problem.pdf#page=3",
      "description": "unresolved output convention",
      "status": "open"
    }
  ]
}
```

An open ambiguity produces WARN and must appear in the checkpoint. Resolve it
only with problem text, template structure, or human confirmation; record the
decision and evidence before changing `status` to `resolved`.

## `memory/evidence_ledger.json`

```json
{
  "entries": [
    {
      "id": "C-Q1-01",
      "claim": "question-one result and unit",
      "core": true,
      "status": "verified",
      "questions": ["Q1"],
      "deliverables": ["result1"],
      "evidence_locations": [
        "state/model1_results.json:value",
        "state/verify_model1.txt:V-PDE-03",
        "output/result1.xlsx:Sheet1!B2"
      ]
    }
  ]
}
```

Every required question and deliverable needs coverage. Core entries require
`status=verified` and at least one exact evidence location. Non-core draft
entries are allowed but produce WARN and cannot be used in the abstract.

## Validation Record

For every selected check, report `check_id`, model unit, failure source,
threshold, threshold basis, observed value, PASS/FAIL, and evidence location.
Select checks by model structure. Do not copy a percentage from an example
without a scale, data-quality, tolerance, or convergence basis.
