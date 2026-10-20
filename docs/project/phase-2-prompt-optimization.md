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

## v1 x v2 differences

Input for the README comparison (FR-033).

| Aspect | v1 | v2 | Why |
|---|---|---|---|
| Persona | "Você é um assistente" (vague) | Senior Product Manager with software engineering and QA experience | Role Prompting sets vocabulary and quality bar |
| Task | "crie uma user story" | One User Story in a defined format, in Brazilian Portuguese | Specific instructions reduce variation |
| Reasoning | None | 5 internal analysis steps (classify complexity, actor, technical data, expected behavior, format), not shown | Chain of Thought improves structure without hurting Precision and Clarity |
| Output format | Not defined | Story sentence + Dado que / Quando / Então / E criteria; extra blocks for medium reports; `=== ... ===` sections for complex ones | Mirrors the dataset references the judge compares against |
| Rules | None | Explicit do / do not list (preserve technical data, no invented facts, proportional length, no preamble) | Precision penalizes invented and off-topic content in both derived metrics |
| Edge cases | None | Vague or incomplete report; several problems in one report | FR-010 |
| Examples | None | 3 own examples: simple, medium, complex | Few-shot teaches the format of each level |
| Input variable | `{bug_report}` duplicated in system and user prompts | `{bug_report}` only in the user prompt | Removes the duplication (FR-011) |
| Metadata | No techniques listed | `techniques_applied`: few-shot, role-prompting, chain-of-thought | FR-005, BR-008 |

## Next

Phase 5 (tests) runs before Phase 3 (push), so the prompt is validated before it is published.
