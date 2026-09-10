# Local Pilot Observations

These observations come from two repository demos, not independently verified
award-winning papers. They are examples of an AutoMCM-Pro workflow and support
only tentative process guidance.

| Pair | Local artifacts reviewed | Provenance | What it can support |
| --- | --- | --- | --- |
| P1: 2020 C, credit decisions | problem document, `latex/main.tex`, model and verification scripts, thought process | `project_demo` | data-model-output traceability and constraint-oriented verification |
| P2: 2025 A, smoke-screen deployment | problem PDF, `latex/main.tex`, model and verification scripts, thought process | `project_demo` | shared-mechanism decomposition, physics checks, and required workbook checks |

## Tentative Patterns

1. **Map questions to model units before allocating agents.** P2 groups its
   five questions into three units only where the mechanism and validation
   basis are shared. This is a useful planning check, not a license to merge
   unrelated questions.
2. **Keep the evidence chain separate from the solver.** Both pairs use
   verification scripts that recheck properties such as feasibility, physical
   relations, finite values, constraints, and sensitivity-output completeness.
   A successful solver run alone is not enough evidence.
3. **Treat required deliverables as testable outputs.** P2 verifies requested
   workbook outputs; P1 verifies policy and budget constraints. New tasks must
   derive their checks from their own stated deliverables.
4. **Plan the paper around the shared mechanism and evidence.** Both papers
   put a shared method before question-specific extensions and give sensitivity
   analysis and limitations their own sections. Their wording and layout are
   not reusable templates.

## Limits

- Two cases cannot establish a universal workflow rule.
- Both cases were produced within the same repository and share its existing
  SOP, so repeated structure may be a template artifact rather than an
  independent quality signal.
- Neither case provides independently checked award status in this workspace.
