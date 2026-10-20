# Phase 3: Push to the Hub and first evaluation

- **Branch:** `phase-3-push-evaluation`
- **Spec:** [003-push-prompt](../../specs/003-push-prompt/spec.md)
- **Requirements:** FR-015 to FR-024, BR-005 to BR-007, BR-018, BR-019

## Prerequisites

- Phases 1, 2 and 5 done; `pytest tests/test_prompts.py` passing.
- Model limits re-checked in AI Studio ([ADR-001](../adr/ADR-001-llm-provider-and-models.md)).

## Scope

1. Check the `Client.push_prompt` signature in the installed `langsmith` and close Q-014.
2. Implement `src/push_prompts.py` per spec 003.
3. With the owner's confirmation, run `python src/push_prompts.py` and check the prompt on the Hub (public, tags, description).
4. With the owner's confirmation, run `python src/evaluate.py` (first evaluation, about 60 LLM calls).
5. Validate the run:
   - if the output shows "Erro ao avaliar", discard the run and repeat it (BR-018);
   - inspect the traces of the 3 complex examples for looping or degraded output (RK-12) and the format of each level
     (spec 002 AC-09).
6. Record the result as iteration 1 in [phase 4](phase-4-iteration.md).

## Deliverables

- `src/push_prompts.py` implemented.
- v2 public on the Hub.
- First valid evaluation recorded.

## Acceptance criteria

- Spec 003 AC-01 to AC-04 met.
- One valid experiment exists in LangSmith with 15 runs and five scores per example.
- From this run on, the models are fixed (BR-019).
