# Spec 002: Optimized prompt v2

- **Requirements:** FR-005 to FR-014, BR-004, BR-008, BR-009, BR-016, BR-020
- **File:** `prompts/bug_to_user_story_v2.yml` (the only file changed during iterations)
- **Related:** [ADR-001](../../docs/adr/ADR-001-llm-provider-and-models.md), [spec 004](../004-validation-tests/spec.md)

## Goal

Turn a bug report into a User Story whose format and level of detail match the dataset references, so the LLM judge
scores >= 0.8 on every metric.

## How the judge scores (facts from `src/metrics.py`)

- All three judges see the bug report, the generated answer and the reference answer.
- **F1-Score:** precision (correct and relevant information) and recall (reference information present).
- **Clarity:** organization, plain language, no ambiguity, **conciseness** (no redundancy).
- **Precision:** no hallucinations, **focus** (no unrequested information), factual correctness against the reference.
- Precision feeds both derived metrics, so invented or off-topic content costs twice.

Consequence: the answer must cover what the reference covers, in the same structure, without extra sections or
invented facts, with length proportional to the report.

## YAML structure

```yaml
bug_to_user_story_v2:
  description: "..."
  system_prompt: |
    ...
  user_prompt: "{bug_report}"
  version: "v2"
  created_at: "YYYY-MM-DD"
  tags: ["bug-analysis", "user-story", "product-management"]
  techniques_applied: ["few-shot", "role-prompting", "chain-of-thought"]
```

- `{bug_report}` appears only in `user_prompt` (FR-011).
- Literal braces in `system_prompt` (JSON, routes such as `/api/items/{id}`, code) are written `{{` and `}}`:
  the text is parsed as an f-string template.
- Uppercase `TODO` must not appear in `system_prompt`, not even inside words such as "TODOS"; `[TODO]` must not appear anywhere.
- All prompt text is in Portuguese (FR-014).

## System prompt content

Recommended section order (an iteration variable, see Phase 4):

1. **Persona (Role Prompting):** a sentence starting with "Você é", e.g. a senior Product Manager experienced in
   turning bug reports into User Stories with testable acceptance criteria.
2. **Task:** turn the received report into one User Story in the format below.
3. **Internal analysis (Chain of Thought):** steps the model follows silently before answering:
   1. count the distinct problems and classify the report as simple, medium or complex;
   2. identify the affected user (or the system, see rules);
   3. list the technical data present in the report (endpoints, HTTP codes, logs, values, steps, severity);
   4. derive the expected correct behavior for each problem;
   5. pick the output format for the complexity level.

   Explicit instruction: do not show this analysis; answer only with the User Story.
4. **Output format** (below), explicitly named "User Story".
5. **Behavior rules** (do and do not).
6. **Edge cases** (below).
7. **Examples (Few-shot)**.

## Output format (BR-016)

Observed in the 15 references of `datasets/bug_to_user_story.jsonl`. Plain text with `- ` bullets, no Markdown
headings (`#`), no bold, no code fences, no preamble such as "Aqui está".

| Level | When | Structure |
|---|---|---|
| Simple | One problem, short report, no technical data | Story sentence + `Critérios de Aceitação:` with about 4 to 6 bullets |
| Medium | One problem with technical data (steps, logs, endpoints, HTTP codes, metrics, severity) | Simple structure + 1 or 2 complementary blocks named after their content |
| Complex | Several distinct problems in one report | Opening story sentence + `=== ... ===` sections |

**Story sentence:** `Como um <persona>, eu quero <objetivo>, para que <benefício>.` When the actor is a machine or a
control (integration, webhook, permission check), the references use `Como o sistema ...`.

**Acceptance criteria:** bullets starting with `Dado que`, `Quando`, `Então`, `E`.

**Medium complementary blocks seen in the references:** `Contexto Técnico:`, `Critérios Técnicos:`, `Contexto do Bug:`,
`Contexto de Segurança:`, `Critérios Adicionais para <perfil>:`, `Critérios de Prevenção:`,
`Critérios de Acessibilidade:`, `Exemplo de Cálculo:`.

**Complex sections, in order:**

```text
<story sentence>

=== USER STORY PRINCIPAL ===
Título: ...
Descrição:
Como um ..., eu quero ..., para que ...

=== CRITÉRIOS DE ACEITAÇÃO ===
A. <Área> - <objetivo>:
- Dado que ... / Quando ... / Então ... / E ...
B. ...

=== CRITÉRIOS TÉCNICOS ===
<grouped bullets per area>

=== CONTEXTO DO BUG ===
Severidade: ...
Impacto: ...
Problemas Identificados: ...

=== TASKS TÉCNICAS SUGERIDAS ===
1. [ÁREA] ...
```

One subsection per problem in `CRITÉRIOS DE ACEITAÇÃO` (A, B, C...). One reference also adds `=== MÉTRICAS DE SUCESSO ===`;
it is optional.

## Behavior rules

- Do: preserve literally the technical data from the report (endpoints, codes, values, error messages).
- Do: write criteria that describe the expected correct behavior implied by the report.
- Do not: invent data absent from the report (names, values, metrics, tools).
- Do not: add features, sections or recommendations unrelated to the reported problems.
- Do not: show the analysis, comments about the task or text outside the User Story.

## Edge cases (FR-010)

| Case | Expected behavior |
|---|---|
| Vague or incomplete report | Write the story from what is stated; for missing data use a generic description or a bracketed placeholder, as the references do (e.g. `[nome do gateway de pagamento]`); never invent values |
| Several problems in one report | Use the complex format, one acceptance criteria subsection per problem |

## Few-shot examples (FR-008, BR-020)

- Exactly 3 examples: simple, medium, complex, in this order.
- Markers, consistent across examples (tests depend on them):
  `Exemplo 1`, `Exemplo 2`, `Exemplo 3`, each followed by `Entrada:` and `Saída:`.
- Own reports and answers: never copy reports or references from the dataset. Prefer domains or bugs absent from the
  dataset to avoid over-fitting (RK-05).
- Each `Saída:` follows exactly the format of its level, so the examples also teach the format.
- The complex example keeps the full section structure but can be shorter than the dataset references, to limit prompt size.

## Acceptance criteria

| ID | Criterion | Verified by |
|---|---|---|
| AC-01 | YAML is valid, root key `bug_to_user_story_v2`, all fields of the structure present | Spec 004; `validate_prompt_structure` |
| AC-02 | Persona sentence starting with "Você é" | `test_prompt_has_role_definition` |
| AC-03 | The format is named explicitly ("User Story") and described for the three levels | `test_prompt_mentions_format`; review |
| AC-04 | 3 examples with the markers above | `test_prompt_has_few_shot_examples` |
| AC-05 | `techniques_applied` = few-shot, role-prompting, chain-of-thought; CoT steps present and marked as not shown | `test_minimum_techniques`; review |
| AC-06 | `{bug_report}` only in `user_prompt` | Additional test (FR-039) |
| AC-07 | No `[TODO]`; no uppercase `TODO` in `system_prompt` | `test_prompt_no_todos`; `validate_prompt_structure` |
| AC-08 | Both edge cases instructed | Review |
| AC-09 | In the first evaluation traces, answers contain only the User Story, with the format matching each example's complexity and no looping | Trace review (Phase 3) |

## Open points

- Section order, example length and wording are tuned during Phase 4 iterations, one change per iteration.
