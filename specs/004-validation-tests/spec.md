# Spec 004: Structural validation tests

- **Requirements:** FR-025 to FR-031, FR-039, NFR-008
- **File:** `tests/test_prompts.py` (keep the `TestPrompts` class and the exact names of the 6 skeleton tests)
- **Command:** `pytest tests/test_prompts.py`

## Goal

Check offline, deterministically and without LLM or network access, that `prompts/bug_to_user_story_v2.yml` meets the
structural requirements of [spec 002](../002-prompt-v2/spec.md).

## Setup

- Load the YAML once with a fixture, by a path relative to the test file:
  `Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"`, root key `bug_to_user_story_v2`.
- Reuse the skeleton's `load_prompts` helper.
- Assertion messages in Portuguese, saying what is missing in the prompt.

## Tests

| Test | Checks | Requirement |
|---|---|---|
| `test_prompt_has_system_prompt` | `system_prompt` exists and is not empty after `strip()` | FR-026 |
| `test_prompt_has_role_definition` | `system_prompt` contains a persona sentence starting with "Você é" | FR-027 |
| `test_prompt_mentions_format` | `system_prompt` mentions "User Story" or "Markdown" (case-insensitive) | FR-028 |
| `test_prompt_has_few_shot_examples` | At least 3 occurrences each of `Exemplo`, `Entrada:` and `Saída:` in `system_prompt` | FR-029 |
| `test_prompt_no_todos` | No `[TODO]` in `system_prompt` or `user_prompt` | FR-030 |
| `test_minimum_techniques` | `techniques_applied` is a list with at least 2 items | FR-031 |
| `test_bug_report_only_in_user_prompt` (additional) | `{bug_report}` is in `user_prompt` and not in `system_prompt` | FR-039 |

Optional additional test: `validate_prompt_structure(prompt)` returns `(True, [])`, which also covers uppercase `TODO`.

## Rules

- Markers checked here are the ones defined in spec 002. If the prompt format changes, update the tests in the same change.
- The tests check the real v2 file; they never mock or rewrite it.

## Acceptance criteria

- AC-01: `pytest tests/test_prompts.py` passes with the final v2 file.
- AC-02: the suite runs with the network disabled.
- AC-03: removing a technique, an example or the persona from a local copy makes the corresponding test fail with a
  clear message (checked manually once, without committing the broken copy).
