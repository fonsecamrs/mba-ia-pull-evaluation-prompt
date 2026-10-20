# Spec 001: Pull the seed prompt

- **Requirements:** FR-001 to FR-004, BR-013, BR-014, BR-015, NFR-003, NFR-004, NFR-010
- **File:** `src/pull_prompts.py` (implement the skeleton bodies; keep names and signatures)

## Goal

Bring `leonanluppi/bug_to_user_story_v1` from the LangSmith Hub into `prompts/bug_to_user_story_v1.yml`, as the
reference of the defects to fix in v2.

## Preconditions

- `.env` with `LANGSMITH_API_KEY` (the only variable required by this script).
- Run from the repository root: `python src/pull_prompts.py`.

## Main flow

1. `main()` prints a header with `print_section_header`.
2. `check_env_vars(["LANGSMITH_API_KEY"])`; on failure, return `1` without contacting the Hub (FR-001).
3. `pull_prompts_from_langsmith()`:
   1. `Client().pull_prompt("leonanluppi/bug_to_user_story_v1", dangerously_pull_public_prompt=True)` (BR-015).
   2. Read the text of each message of the returned `ChatPromptTemplate` through `prompt.messages[i].prompt.template`,
      identifying system and user by the message type (FR-002).
   3. Build the dictionary and save it with `save_yaml` (FR-003).
4. Print the saved path and return `0`.

## Output file

```yaml
bug_to_user_story_v1:
  description: "..."
  system_prompt: |
    ...
  user_prompt: "{bug_report}"
  version: "v1"
  tags: [...]
```

- `system_prompt` and `user_prompt` must equal the Hub texts.
- `description` and `tags` come from the Hub metadata when available. Where the installed `langsmith` exposes them
  is checked during implementation; if they are not exposed, keep the values of the current file.

## Exceptions

| Situation | Behavior |
|---|---|
| Missing variable | List of missing variables in Portuguese (`check_env_vars`), exit `1` |
| Network error, invalid key, prompt not found | Message in Portuguese with the reason, exit `1` (FR-004) |
| File cannot be written | `save_yaml` message, exit `1` |

Catch specific exceptions where the library exposes them; never swallow an error without a message.

## Acceptance criteria

- AC-01: with a valid key, the file is regenerated, is valid YAML and its texts equal the Hub prompt.
- AC-02: without `LANGSMITH_API_KEY`, nothing is contacted and the exit code is `1`.
- AC-03: no key value is printed.

## Test cases (manual: they need network access, so they stay out of the offline suite)

| ID | Setup | Expected |
|---|---|---|
| TC-01 | Valid `.env` | Exit `0`; `git diff prompts/bug_to_user_story_v1.yml` shows only formatting or comment differences |
| TC-02 | `LANGSMITH_API_KEY` empty | Missing variable listed; exit `1` |
| TC-03 | Invalid key | Error message in Portuguese; exit `1` |

## Notes

- The base repository's v1 file has a header comment explaining the intentional defects. `save_yaml` does not
  preserve comments, so the regenerated file loses it. This is accepted: the file is only a reference and is never
  edited by hand.
