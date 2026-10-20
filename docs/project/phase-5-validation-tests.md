# Phase 5: Validation tests

- **Branch:** `phase-5-validation-tests`
- **Spec:** [004-validation-tests](../../specs/004-validation-tests/spec.md)
- **Requirements:** FR-025 to FR-031, FR-039, NFR-008
- **Execution order:** right after Phase 2 and before Phase 3, so the prompt is validated before publishing.

## Scope

1. Implement the 6 mandatory tests in `tests/test_prompts.py`, keeping the class and test names.
2. Add `test_bug_report_only_in_user_prompt` (FR-039).
3. Run `pytest tests/test_prompts.py` against the Phase 2 file and fix the prompt if a test fails.
4. Check spec 004 AC-03 once on a local, uncommitted copy of the prompt.

## Deliverables

- `tests/test_prompts.py` implemented.

## Acceptance criteria

- Spec 004 AC-01 to AC-03 met.
- From now on, every change to v2 runs the tests before the push.
