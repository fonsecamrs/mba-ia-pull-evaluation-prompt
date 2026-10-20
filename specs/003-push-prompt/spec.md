# Spec 003: Push the v2 prompt

- **Requirements:** FR-015 to FR-020, BR-005, BR-006, BR-008, NFR-003, NFR-010
- **File:** `src/push_prompts.py` (implement the skeleton bodies; keep names and signatures)

## Goal

Publish `prompts/bug_to_user_story_v2.yml` to the Hub as the public prompt `{handle}/bug_to_user_story_v2`, with
metadata, so `src/evaluate.py` can evaluate it (BR-007).

## Preconditions

- `.env` with `LANGSMITH_API_KEY` and `USERNAME_LANGSMITH_HUB` (the public handle, BR-005).
- `pytest tests/test_prompts.py` passing (Phase 5 runs before Phase 3).
- Run from the repository root: `python src/push_prompts.py`. Each run publishes a new commit of the prompt on the Hub
  and needs the owner's confirmation (`CLAUDE.md`).

## Main flow

1. `main()` prints a header and checks the variables with `check_env_vars`; on failure, return `1`.
2. `load_yaml("prompts/bug_to_user_story_v2.yml")` and read the root key `bug_to_user_story_v2` (FR-015).
3. `validate_prompt(prompt_data)`, delegating to `validate_prompt_structure` from `src/utils.py` and adding a check that
   `user_prompt` exists and contains `{bug_report}`. On errors, print all of them and return `1` without publishing (FR-016).
4. `push_prompt_to_langsmith(prompt_name, prompt_data)`:
   1. `ChatPromptTemplate.from_messages([("system", system_prompt), ("user", user_prompt)])`.
   2. `Client().push_prompt(f"{username}/bug_to_user_story_v2", object=prompt, is_public=True, description=..., tags=...)`.
   3. Print the returned URL (FR-020).
5. Return `0` on success, `1` on failure.

## Metadata (FR-019, Q-014)

- `description`: the YAML `description`, followed by the applied techniques.
- `tags`: the YAML `tags` plus each item of `techniques_applied`, without duplicates.
- Checked in Phase 1: `Client.push_prompt` in `langsmith` 0.13.0 also accepts `readme`, `commit_tags` and
  `commit_description`. Deciding whether the techniques also go into `readme` closes Q-014 in Phase 3.

## Exceptions

| Situation | Behavior |
|---|---|
| Missing variable | List of missing variables, exit `1` |
| Missing file or invalid YAML | `load_yaml` message, exit `1`, nothing published |
| Missing root key | Message in Portuguese naming the expected key, exit `1` |
| Validation errors | All errors listed in Portuguese, exit `1` |
| Handle not found or not public | Explain how to create it: LangSmith > Prompts > three dots next to Playground > Make Public > Choose your public handle; exit `1` |
| Other Hub errors | Message in Portuguese with the reason, exit `1` |

## Acceptance criteria

- AC-01: a valid prompt becomes public on the Hub as `{handle}/bug_to_user_story_v2`, with description and tags.
- AC-02: an invalid prompt is never published and every error is listed.
- AC-03: the published system and user texts equal the YAML.
- AC-04: no key value is printed.

## Test cases (manual: they publish to the Hub)

| ID | Setup | Expected |
|---|---|---|
| TC-01 | Valid v2, existing handle | Exit `0`; URL printed; the Hub shows the prompt as public with tags |
| TC-02 | Copy of v2 without `version` and with one technique (temporary file, not committed) | Both errors listed; exit `1`; no new Hub commit |
| TC-03 | `USERNAME_LANGSMITH_HUB` with a non-existent handle | Make Public guidance; exit `1` |
