# Phase 2: Optimized prompt v2

- **Branch:** `phase-2-prompt-optimization`
- **Spec:** [002-prompt-v2](../../specs/002-prompt-v2/spec.md)
- **Requirements:** FR-005 to FR-014, BR-008, BR-009, BR-016, BR-020

## Scope

1. Analyze the defects of `prompts/bug_to_user_story_v1.yml`: vague instructions, vague persona, no examples,
   `{bug_report}` duplicated in the system prompt.
2. Create `prompts/bug_to_user_story_v2.yml` from scratch, following spec 002:
   - persona (Role Prompting);
   - task and internal analysis steps (Chain of Thought, not shown in the answer);
   - output format per complexity level, mirroring the dataset references;
   - behavior rules and the two edge cases;
   - 3 own Few-shot examples (simple, medium, complex).
3. Read the dataset references before writing the format section, without copying them into the prompt.

## Deliverables

- `prompts/bug_to_user_story_v2.yml`.
- A short note of the v1 x v2 differences, reused later in the README comparison (FR-033).

## Acceptance criteria

- Spec 002 AC-01 to AC-08 met (AC-09 is checked in Phase 3).
- `validate_prompt_structure` returns no errors for the file.

## Next

Phase 5 (tests) runs before Phase 3 (push), so the prompt is validated before it is published.
