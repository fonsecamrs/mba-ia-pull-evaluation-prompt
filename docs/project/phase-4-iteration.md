# Phase 4: Iterate until approval and deliver

- **Branch:** `phase-4-iteration`
- **Requirements:** OBJ-01, FR-032 to FR-038, BR-001, BR-011, BR-018, BR-019, KPI-08

## Iteration loop

1. Read the lowest metrics and the traces of the lowest-scoring examples.
2. Change only `prompts/bug_to_user_story_v2.yml`, preferably one change per iteration, to attribute its effect.
3. `pytest tests/test_prompts.py`, then push, then evaluate (push and evaluate need the owner's confirmation).
4. Validate the run (BR-018) and record it in the table below.
5. Repeat until APROVADO: every metric >= 0.8 and the average >= 0.8. One valid approved run is enough.

Hints from the metrics: Precision is in both derived metrics, so invented or off-topic content costs twice;
Clarity rewards conciseness; F1 rewards covering what the reference covers.

## Iteration log

| # | Date | Change | Helpfulness | Correctness | F1 | Clarity | Precision | Average | Status | Valid |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | First version (Phase 3) | | | | | | | | |

Discarded runs (BR-018) are listed with the reason and do not get an iteration number.

## Delivery (after approval)

1. With the owner's confirmation, create the public dataset link **once** (BR-011):
   `Client().share_dataset(dataset_name="<LANGSMITH_PROJECT>-eval")["url"]`.
2. Capture screenshots into `docs/images/`:
   - the approved scores;
   - the 15-example dataset;
   - the detailed tracing of at least 3 examples.
3. Replace `README.md` with the delivery documentation in Portuguese (FR-038). It must contain the sections
   "Técnicas Aplicadas (Fase 2)", "Resultados Finais" and "Como Executar", with a link to the original challenge statement.
4. Check that no key or private workspace link appears in the README or screenshots (NFR-003).

## Acceptance criteria

- The last valid run is APROVADO (BR-001).
- FR-032 to FR-038 met; the public link opens without workspace access.
