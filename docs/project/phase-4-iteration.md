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
| 1 | 2026-10-20 | First version (Phase 3) | 0.93 | 0.91 | 0.90 | 0.95 | 0.91 | 0.918 | APROVADO | Yes |

Discarded runs (BR-018) are listed with the reason and do not get an iteration number. None so far.

### Iteration 1 notes

- Experiment `fonsecamrs-bug_to_user_story_v2-e38ce611`, dataset `mba-ia-pull-evaluation-prompt-eval` (created by this run).
- Validity checks: no "Erro ao avaliar", no JSON extraction failure, no quota error (BR-018).
- RK-12: no looping in any of the 15 answers; every answer starts with the story sentence; only the 3 complex
  reports used the `=== ... ===` sections.
- The judge model `gemini-3.5-flash-lite` ignores the temperature parameter ("uses fixed sampling defaults"), so the
  45 judge calls ran at the model default; the generator accepted temperature 0. See ADR-001.
- Lowest examples: 5 (F1 0.77, Precision 0.83) and 11 (Precision 0.83). Every metric average is above 0.8, so no
  further iteration is required (Q-010: one valid approved run is enough).

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
