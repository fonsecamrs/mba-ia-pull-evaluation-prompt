# Phase 1: Pull the v1 prompt

- **Branch:** `phase-1-pull`
- **Spec:** [001-pull-prompt](../../specs/001-pull-prompt/spec.md)
- **Requirements:** FR-001 to FR-004, FL-01, FL-02

## Prerequisites (owner actions)

- LangSmith account and API key.
- Public Hub handle (LangSmith > Prompts > three dots next to Playground > Make Public). Permanent: choose carefully (RK-06).
- Gemini API key (already created).

## Scope

1. Create `.env` from `.env.example` (never versioned). Fill in the keys, `USERNAME_LANGSMITH_HUB` and the models of
   [ADR-001](../adr/ADR-001-llm-provider-and-models.md). Keep `LANGSMITH_PROJECT` non-empty (BR-012).
2. Create the virtual environment and install the dependencies:
   `python -m venv venv`, `venv\Scripts\activate`, `pip install -r requirements.txt`.
3. Check that the pinned packages install on the local Python 3.14 (Q-015). If not, install Python 3.12 or 3.13 and
   recreate the venv; changing `requirements.txt` needs the owner's confirmation.
4. Implement `src/pull_prompts.py` per spec 001.
5. Run `python src/pull_prompts.py` and review the regenerated `prompts/bug_to_user_story_v1.yml`.

## Deliverables

- `src/pull_prompts.py` implemented.
- `prompts/bug_to_user_story_v1.yml` regenerated from the Hub.

## Acceptance criteria

- Spec 001 AC-01 to AC-03 met.
- `git status` does not list `.env`.

## Risks

- Q-015: package incompatibility with Python 3.14.
