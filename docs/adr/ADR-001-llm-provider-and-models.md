# ADR-001: LLM provider and models

- **Status:** Accepted
- **Date:** 2026-10-19
- **Requirements:** BR-010, BR-019, NFR-001, NFR-002, NFR-006, RK-01, RK-11, RK-12

## Context

The challenge does not fix the LLM. `src/utils.py` supports `google` and `openai`, configured only through `.env`
(`LLM_PROVIDER`, `LLM_MODEL` for generation, `EVAL_MODEL` for the judge). Constraints:

- The product owner chose Google Gemini on the **free tier**.
- One evaluation run makes 60 sequential calls: 15 generation calls and 45 judge calls (3 judges per example).
- Generation and judging use temperature 0, fixed in the evaluation code, which cannot change (BR-003).
- A failed judge call becomes score 0.0 silently (RK-11), so quota errors directly distort scores.
- Free-tier limits apply **per project and per model**; daily quotas reset at midnight Pacific time.
  The official docs no longer publish the numbers; they are shown only in Google AI Studio.

Free-tier text models available to a new account, and their limits measured in the owner's AI Studio on 2026-10-19:

| Model | RPM | TPM | RPD | Notes |
|---|---|---|---|---|
| `gemini-3.8-flash` | 5 | 250K | 20 | Most capable free Flash model |
| `gemini-3.6-flash` | — | — | 0 | No free text quota (listed only under Maps grounding) |
| `gemini-3.5-flash-lite` | 15 | 250K | 500 | Newer and pricier Lite model, assumed more capable than 3.1 |
| `gemini-3.1-flash-lite` | 15 | 250K | 500 | Low-cost model |

Paid-only models (`gemini-4-argon`, `gemini-3.1-pro-preview`) and restricted ones (2.5 family) were not considered.
Preview models were avoided because of their stricter limits.

## Options considered

| Option | Generation | Judge | Runs per day | Outcome |
|---|---|---|---|---|
| A | `gemini-3.5-flash-lite` | `gemini-3.8-flash` | 0 (judge needs 45 of 20 RPD) | Rejected |
| B | `gemini-3.8-flash` | `gemini-3.8-flash` | 0 (60 of 20 RPD) | Rejected |
| C | `gemini-3.8-flash` | `gemini-3.6-flash` | 0 (no free quota) | Rejected |
| **D** | `gemini-3.1-flash-lite` | `gemini-3.5-flash-lite` | ~11 (judge: 45 of 500) | **Chosen** |
| E | `gemini-3.5-flash-lite` | `gemini-3.5-flash-lite` | ~8 (60 of 500) | Fallback |
| F | `gemini-3.5-flash-lite` | `gemini-3.1-flash-lite` | ~11 | Rejected: judge less capable than the generator |

## Decision

```dotenv
LLM_PROVIDER=google
LLM_MODEL=gemini-3.1-flash-lite
EVAL_MODEL=gemini-3.5-flash-lite
```

- Splitting generation and judge across two models splits the per-minute quota, lowering the risk of silent 0.0 scores (RK-11).
- The judge gets the more capable model, making scores more reliable.
- Models stay fixed from the first evaluation on (BR-019).

## Consequences

- About 11 evaluation runs per day, enough for the expected 3 to 5 iterations plus repeated runs (BR-018).
- If the generator proves too weak to reach 0.8, switch to option E by changing `LLM_MODEL` only, and record a new baseline (BR-019).
- RK-12: the Gemini 3 developer guide recommends keeping temperature at the default 1.0, warning of looping or degraded
  quality below it. Temperature 0 is imposed by the evaluation code and accepted; the traces of the 3 complex examples
  are checked in the first run. Checked on 2026-10-20: no looping.
- Found in the first run (2026-10-20): `gemini-3.5-flash-lite` ignores the temperature parameter
  (`langchain-google-genai` warns that the model "uses fixed sampling defaults"), so the judge runs at the model
  default instead of 0. Judge scores may vary more between runs (RK-03). Accepted: one valid approved run is enough
  (Q-010), and the generator (`gemini-3.1-flash-lite`) does accept temperature 0.
- On the free tier, Google may use submitted content to improve its products (to confirm in the current terms).
  Impact is nil: the dataset is fictitious and contains no personal data.
- Limits and model availability change often. Re-check them in AI Studio before Phase 3; a change in quotas or the
  discontinuation of a model reopens this ADR.
- Moving to the paid tier is a future decision, taken only if quotas block the iterations.

## Sources

- [Gemini models](https://ai.google.dev/gemini-api/docs/models)
- [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini 3 developer guide (temperature)](https://ai.google.dev/gemini-api/docs/interactions/gemini-3)
