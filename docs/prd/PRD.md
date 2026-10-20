# PRD: Prompt Pull, Optimization, Publishing and Evaluation Pipeline

## 1. Document control

| Field | Value |
|---|---|
| Product / project | `mba-ia-pull-evaluation-prompt`: Challenge 2 of the AI MBA (Full Cycle), "Prompt Optimization and Evaluation with LangChain and LangSmith" |
| Document | Product Requirements Document (PRD) |
| Version | 0.2 |
| Status | Draft, pending approval |
| Last updated | 2026-10-19 |
| Product owner / approver | Marcos Fonseca (assumed during discovery; see Q-011) |
| Purpose | Single source of truth for the what, why and for whom of the product, with traceable and verifiable requirements that guide specs, phase documents, development and tests |

### 1.1. Sources

| Source | Use |
|---|---|
| Challenge statement (`README.md` of the base repository) | Primary source of requirements |
| [`CLAUDE.md`](../../CLAUDE.md) and rules in `.claude/rules/` | Constraints, established decisions, language and process |
| Base repository code: `src/evaluate.py`, `src/metrics.py`, `src/utils.py`, skeletons, `.env.example`, `prompts/bug_to_user_story_v1.yml`, `datasets/bug_to_user_story.jsonl` | Behavior of the ready-made components and format of the evaluation data |
| Discovery interview with the product owner (2026-10-13 to 2026-10-19) | Decisions recorded in section 17.1 |
| Official Gemini API documentation and the developer's Google AI Studio quota page (2026-10-19) | Model choice ([ADR-001](../adr/ADR-001-llm-provider-and-models.md)) |

### 1.2. Conventions

- **Confirmed:** explicitly stated in a source.
- **Existing:** behavior already implemented in the ready-made components, which must not be changed.
- **Decided:** settled by the product owner during discovery (section 17.1).
- **Assumption:** provisionally true; needs validation.
- **Pending:** missing decision or information, listed in section 17.2.

Acronyms: PRD, MVP, LLM, CLI, YAML, Hub (LangSmith Prompt Hub), F1 (harmonic mean of precision and recall), RPM / RPD (requests per minute / per day).

## 2. Executive summary

The product is a set of command-line routines that pull a low-quality prompt from the LangSmith Prompt Hub, support writing an optimized version with prompt engineering techniques, publish the optimized version to the Hub and measure its quality automatically against a fixed set of 15 examples.

The prompt turns bug reports into User Stories with acceptance criteria. The original version (`bug_to_user_story_v1`) has known defects: vague instructions, a vague persona ("an assistant"), no examples, and the bug report duplicated in the system and user prompts.

Users:
- the developer who runs the challenge;
- the challenge reviewer, who verifies the delivery.

Value: a reproducible "pull, optimize, publish, measure" cycle that turns prompt quality into numbers comparable across iterations, with public evidence.

**Main objective:** the prompt `{handle}/bug_to_user_story_v2` scores 0.8 or higher on each of the five metrics (Helpfulness, Correctness, F1-Score, Clarity, Precision) and on their average, with documented and publicly verifiable evidence.

## 3. Context and business problem

### 3.1. Current situation (facts)

- The base repository provides:
  - the evaluation dataset with 15 bug reports (5 simple, 7 medium, 3 complex, per the dataset metadata);
  - the evaluation script with the five metrics;
  - helper functions;
  - skeletons of the pull, push and test scripts.
- The seed prompt `leonanluppi/bug_to_user_story_v1` is published on the Hub. The v1 file states that its defects are intentional.
- Evaluation uses an LLM judge: F1-Score, Clarity and Precision are scored by the evaluation model; Helpfulness and Correctness are derived from them.
- The judge compares each answer with the dataset reference answer. Precision penalizes unrequested information; Clarity rewards conciseness (`src/metrics.py`).
- Any judge failure (quota, network, unparseable JSON) is recorded as score 0.0 for that example without stopping the run (`src/metrics.py`).
- Generation and judging run with temperature 0 (`src/evaluate.py`, `src/metrics.py`).

### 3.2. Pain points

| ID | Problem | Type |
|---|---|---|
| PB-01 | The v1 prompt produces low-quality User Stories: vague instructions, vague persona, no examples, duplicated input variable | Fact (stated in the v1 file) |
| PB-02 | There is no objective, repeatable and comparable way to tell whether one prompt is better than another | Fact (challenge motivation) |
| PB-03 | The reviewer has no access to the developer's private LangSmith workspace; the experiment link printed by the evaluation only opens inside the workspace | Fact |
| PB-04 | Structural requirements of the prompt (persona, examples, techniques, no pending markers) can be forgotten during iterations | Fact (reason for the mandatory tests) |

The v1 scores shown in the challenge material (0.45 to 0.52) are declared illustrative only. No measured v1 baseline will be produced (Q-005, decided).

### 3.3. Consequences

- Imprecise or incomplete User Stories lead to misunderstood requirements (assumption derived from the v1 description; not measured by the product).
- Without measurement, prompt changes are trial and error.
- Without public evidence, the reviewer cannot verify the delivery.

### 3.4. Opportunity

Apply prompt engineering techniques (mandatory Few-shot plus at least one additional technique) and an automated evaluation cycle to raise prompt quality measurably and with documentation.

### 3.5. Problem statement

The `bug_to_user_story_v1` prompt does not produce User Stories of the required quality. The developer lacks a reproducible cycle to version, publish and measure prompts that proves, with evidence verifiable by third parties, that the optimized version reaches at least 0.8 on every metric.

## 4. Product vision and value proposition

- **Vision:** treat prompts as versioned, measurable artifacts whose quality is demonstrated by automated evaluation, not subjective perception.
- **Value proposition:** with a few commands, the developer pulls the base prompt, publishes optimized versions and gets objective scores per metric and per example, with an experiment history comparable in LangSmith.

| ID | Objective |
|---|---|
| OBJ-01 | The published v2 prompt scores >= 0.8 on each of the five metrics and on their average |
| OBJ-02 | Provide a reproducible cycle of pulling, versioned publishing and evaluation of prompts |
| OBJ-03 | Automatically verify that the v2 prompt meets the challenge's structural prompt engineering requirements |
| OBJ-04 | Provide documentation and public evidence that allow the reviewer to verify and reproduce the delivery |

## 5. Target users and personas

No demographic data exists in the sources; functional profiles were defined.

| ID | Profile | Goals | Needs | Difficulties | Product use | Origin |
|---|---|---|---|---|---|---|
| P1 | Challenge developer (operator) | Pass all metrics and deliver the challenge | Pull the base prompt, publish versions, measure scores, compare iterations | Free-tier quotas; LLM-judge score variation; model choice without fixed guidance | Runs pull, edits v2, runs tests, push and evaluation; creates the public link; documents | Confirmed |
| P2 | Challenge reviewer | Verify that the delivery meets the requirements | See techniques, scores >= 0.8, dataset, runs and traces without workspace access; reproduce the run | Private experiment link does not open for third parties | Reads the README, opens the public dataset link, inspects the repository | Confirmed |
| P3 | Product and development team receiving bug reports (indirect beneficiary) | Get clear User Stories from reports | User Story with persona, goal, benefit and acceptance criteria | Not identified | Does not interact with the product | Assumption from the v1 description |

## 6. Success criteria

### 6.1. Outcome metrics

Data source for KPI-01 to KPI-06: output of `src/evaluate.py` and the feedback recorded in the LangSmith experiment. A single valid approved run is enough (BR-018, Q-010).

| ID | Indicator | Objective | Calculation | Target |
|---|---|---|---|---|
| KPI-01 | Helpfulness | OBJ-01 | Mean over the 15 examples of (Clarity + Precision) / 2 | >= 0.8 |
| KPI-02 | Correctness | OBJ-01 | Mean over the 15 examples of (F1-Score + Precision) / 2 | >= 0.8 |
| KPI-03 | F1-Score | OBJ-01 | Mean over the 15 examples of 2·P·R / (P + R), P and R scored by the judge | >= 0.8 |
| KPI-04 | Clarity | OBJ-01 | Mean over the 15 examples of the judge score (organization, plain language, no ambiguity, conciseness) | >= 0.8 |
| KPI-05 | Precision | OBJ-01 | Mean over the 15 examples of the judge score (no hallucinations, focus, correctness against the reference) | >= 0.8 |
| KPI-06 | Overall average | OBJ-01 | Arithmetic mean of KPI-01 to KPI-05 | >= 0.8 |

### 6.2. Operational metrics

| ID | Indicator | Objective | Calculation | Source | Target |
|---|---|---|---|---|---|
| KPI-07 | Structural validation tests passing | OBJ-03 | Passed / executed | `pytest` output | 6 of 6 mandatory tests (plus any additional test) |
| KPI-08 | Iterations until approval | OBJ-02 | Valid edit-publish-evaluate cycles until OBJ-01; runs discarded under BR-018 do not count | LangSmith experiments | No target; 3 to 5 iterations expected as reference |
| KPI-09 | Evidence completeness | OBJ-04 | Evidence items present / items required (FR-036) | Public link and README | 100% |

## 7. Product scope

All groups are Must Have: the challenge defines them as mandatory deliverables.

| ID | Group | Description | Need | Users | Dependencies |
|---|---|---|---|---|---|
| G1 | Base prompt pull | Bring the seed prompt from the Hub into the repository | PB-01 | P1 | LangSmith account and key; seed prompt available |
| G2 | Optimized v2 prompt | Keep the optimized version in a versioned file | PB-01 | P1 | G1 (v1 analysis) |
| G3 | Versioned publishing | Publish v2 to the Hub as public, with metadata | PB-02, PB-03 | P1 | G2; public Hub handle |
| G4 | Quality evaluation | Measure the published v2 against the dataset | PB-02 | P1 | G3; LLM keys and models (Existing, do not implement) |
| G5 | Automated structural validation | Check structural requirements of v2 | PB-04 | P1, P2 | G2 |
| G6 | Delivery documentation and evidence | Let the reviewer verify and reproduce | PB-03 | P1, P2 | G4 approved |

## 8. MVP and non-goals

### 8.1. MVP

The MVP is the full challenge delivery: groups G1 to G6 with their Must Have requirements. It must allow checking OBJ-01 (KPI-01 to KPI-06), the structural requirements (KPI-07) and third-party verifiability (KPI-09).

Minimum usage requirements: LangSmith and LLM provider credentials configured, a public Hub handle, generation and evaluation models defined ([ADR-001](../adr/ADR-001-llm-provider-and-models.md)).

### 8.2. Should Have items allowed by the sources

| Item | Basis |
|---|---|
| Additional validation tests beyond the 6 mandatory ones (FR-039) | The challenge asks for "at least" 6 tests |
| Printing the published prompt URL at the end of the push (FR-020) | The skeleton hint returns that URL |

### 8.3. Non-goals

- Changing the dataset, metrics, threshold, evaluation script or helpers to improve scores.
- Evaluating prompts other than `{handle}/bug_to_user_story_v2`.
- Hard-coding the LLM provider or model.
- Using a database.
- Generating User Stories for real operational use.

## 9. Functional requirements

Actor "System" means the product routines. All requirements are Must Have unless stated otherwise.

### 9.1. G1: Base prompt pull

| ID | Requirement | Acceptance criteria | Rules | Depends on |
|---|---|---|---|---|
| FR-001 | Before contacting the Hub, the system checks that the LangSmith credentials are configured | With a missing variable, the system lists the missing variables in Portuguese, does not contact the Hub and exits with failure status | BR-014 | — |
| FR-002 | The system pulls `leonanluppi/bug_to_user_story_v1` from the Hub | With valid credentials, the system gets the system and user messages of the seed prompt | BR-013, BR-015 | FR-001 |
| FR-003 | The system saves the pulled prompt to `prompts/bug_to_user_story_v1.yml`, with system prompt, user prompt and available metadata | The file exists, is valid YAML and its system and user texts equal those of the pulled prompt | R-03 | FR-002 |
| FR-004 | On pull failure, the system reports the reason in Portuguese and exits with failure status | Network error, invalid credential or missing prompt produce a descriptive message and failure status | — | FR-002 |

### 9.2. G2: Optimized v2 prompt

Detailed in [spec 002](../../specs/002-prompt-v2/spec.md).

| ID | Requirement | Acceptance criteria | Rules | Depends on |
|---|---|---|---|---|
| FR-005 | The optimized prompt lives in `prompts/bug_to_user_story_v2.yml` with metadata | The file has description, system prompt, user prompt, version, creation date, tags and the list of applied techniques | BR-008 | — |
| FR-006 | The system prompt defines the persona explicitly | The system prompt contains a persona sentence starting with "Você é" (Role Prompting) | BR-008 | FR-005 |
| FR-007 | The system prompt describes the task specifically and lists explicit behavior rules (do and do not) | The system prompt contains an identifiable rules section | — | FR-005 |
| FR-008 | The system prompt contains Few-shot examples | Exactly 3 own examples (simple, medium, complex), each marked `Exemplo N`, `Entrada:` and `Saída:`; none copied from the dataset | BR-008, BR-020 | FR-005 |
| FR-009 | The prompt applies Role Prompting and Chain of Thought in addition to Few-shot | `techniques_applied` lists few-shot, role prompting and chain of thought; the CoT analysis steps are identifiable in the text and the reasoning is not shown in the answer | BR-008 | FR-005 |
| FR-010 | The prompt instructs behavior for edge cases | Explicit instructions for: (a) vague or incomplete report, with no invented data; (b) several problems in one report, using the complex format | — | FR-005 |
| FR-011 | Persona, instructions, rules and examples are in the system prompt; the bug report is received only in the user prompt | `{bug_report}` appears only in the user prompt | BR-009 | FR-005 |
| FR-012 | The prompt requires the User Story output format of the dataset references, varying by report complexity | The system prompt names the required format explicitly ("User Story") and describes it per complexity level | BR-016 | FR-005 |
| FR-013 | The prompt has no pending-edit markers | No `[TODO]` anywhere and no uppercase `TODO` in the system prompt | — | FR-005 |
| FR-014 | The prompt text sent to the LLM is in Portuguese | Instructions, rules and examples are in Portuguese | — | FR-005 |

### 9.3. G3: Versioned publishing

Detailed in [spec 003](../../specs/003-push-prompt/spec.md).

| ID | Requirement | Acceptance criteria | Rules | Depends on |
|---|---|---|---|---|
| FR-015 | The system reads the prompt from `prompts/bug_to_user_story_v2.yml` | Missing file or invalid YAML: error in Portuguese, failure status, nothing published | — | FR-005 |
| FR-016 | The system validates the prompt structure before publishing | A prompt without description, without or with empty system prompt, without version, with pending markers or with fewer than 2 techniques is not published; all errors are listed | BR-008 | FR-015 |
| FR-017 | The system publishes the prompt as `{handle}/bug_to_user_story_v2` | After publishing, the prompt is found on the Hub by that identifier | BR-005 | FR-016 |
| FR-018 | The published prompt is public | The prompt opens for a user without workspace access | BR-006 | FR-017 |
| FR-019 | Publishing records tags, description and applied techniques | Tags, description and techniques are visible on the Hub (techniques in tags and description, pending confirmation of available fields: Q-014) | — | FR-017 |
| FR-020 | The system reports success or failure; on a missing handle, it explains how to create one via Make Public in the LangSmith UI. Should Have: print the published prompt URL | Exit status reflects the result; messages in Portuguese | BR-005 | FR-017 |

### 9.4. G4: Quality evaluation (Existing)

FR-021 to FR-024 describe behavior already implemented in `src/evaluate.py`. They must not be implemented or changed (BR-003); they exist for verification and traceability.

| ID | Requirement | Acceptance criteria | Rules |
|---|---|---|---|
| FR-021 | The system pulls `{handle}/bug_to_user_story_v2` from the Hub and runs it against the 15 dataset examples as a new experiment | Each run creates an experiment with 15 prompt runs | BR-007, BR-012 |
| FR-022 | For each example, the system computes F1-Score, Clarity and Precision with the LLM judge, derives Helpfulness and Correctness and records the five scores as feedback | Each example has five scores between 0.0 and 1.0 | BR-002 |
| FR-023 | The system shows the five averages and the overall average and prints APROVADO or REPROVADO, listing metrics below the threshold | Status follows BR-001 | BR-001 |
| FR-024 | The system prints the experiment URL | URL printed when the experiment is created | — |

### 9.5. G5: Automated structural validation

Detailed in [spec 004](../../specs/004-validation-tests/spec.md).

| ID | Requirement | Acceptance criteria | Depends on |
|---|---|---|---|
| FR-025 | Structural checks run with a single test command | The command runs FR-026 to FR-031 and reports each result | FR-005 |
| FR-026 | `test_prompt_has_system_prompt`: system prompt exists and is not empty | Fails if missing or whitespace only | FR-025 |
| FR-027 | `test_prompt_has_role_definition`: the prompt defines a persona | Fails without a "Você é" persona sentence in the system prompt | FR-006 |
| FR-028 | `test_prompt_mentions_format`: the prompt requires User Story or Markdown format | Fails if the required format is not mentioned | FR-012 |
| FR-029 | `test_prompt_has_few_shot_examples`: the prompt has input/output examples | Fails with fewer than 3 examples marked `Exemplo`, `Entrada:`, `Saída:` | FR-008 |
| FR-030 | `test_prompt_no_todos`: no `[TODO]` | Fails if `[TODO]` appears in the system or user prompt | FR-013 |
| FR-031 | `test_minimum_techniques`: at least 2 techniques in the YAML metadata | Fails if `techniques_applied` has fewer than 2 items | BR-008 |
| FR-039 | Should Have. Additional test: `{bug_report}` is in the user prompt and not in the system prompt | Fails if the variable is missing from the user prompt or present in the system prompt | FR-011 |

### 9.6. G6: Delivery documentation and evidence

| ID | Requirement | Acceptance criteria | Rules | Depends on |
|---|---|---|---|---|
| FR-032 | The README has the section "Técnicas Aplicadas (Fase 2)" | Lists the techniques, the rationale and a practical example of each in v2 | — | FR-009 |
| FR-033 | The README has the section "Resultados Finais" | Contains the public dataset link, screenshots (stored in `docs/images/`) with scores >= 0.8, a qualitative v1 x v2 comparison (what changed and why) and the history of valid iterations with their scores | BR-011 | FR-023, FR-035 |
| FR-034 | The README has the section "Como Executar" | Contains prerequisites, dependencies and the commands of each phase | — | — |
| FR-035 | A public URL of the evaluation dataset, exposing the experiments run against it, is created once and recorded | The URL opens for a user without workspace access | BR-011 | FR-021 |
| FR-036 | Through the public link or screenshots, the following are visible: the 15-example dataset, the v2 runs with scores >= 0.8 and the detailed tracing of at least 3 examples | All three items are verifiable by P2 | — | FR-035 |
| FR-037 | The delivery is a public GitHub repository forked from the base repository | `fonsecamrs/mba-ia-pull-evaluation-prompt` is public, a fork of `devfullcycle/mba-ia-pull-evaluation-prompt`, and contains the implemented code, the complete v2 and the updated README | BR-017 | G1 to G5 |
| FR-038 | The delivery README replaces the challenge statement | The README contains the delivery documentation and links to the original statement in the base repository | — | FR-032 to FR-034 |

## 10. User stories

| ID | Story | Requirements | Acceptance criteria |
|---|---|---|---|
| US-001 | As the challenge developer, I want to pull the v1 prompt from the Hub, to analyze its defects and use it as the starting point | FR-001 to FR-004 | The v1 file is created with the Hub content; failures exit with failure status |
| US-002 | As the challenge developer, I want a versioned v2 prompt with persona, rules, examples, additional technique and edge cases, to generate better User Stories than v1 | FR-005 to FR-014 | The file meets FR-005 to FR-014 and passes FR-026 to FR-031 |
| US-003 | As the challenge developer, I want to validate the v2 structure automatically, to be sure it meets the minimum requirements before publishing | FR-025 to FR-031, FR-039 | A single command runs the checks and reports each result |
| US-004 | As the challenge developer, I want to publish v2 to the Hub as public with metadata, so it can be evaluated and consulted | FR-015 to FR-020 | Invalid prompt is not published; valid prompt is public as `{handle}/bug_to_user_story_v2` with metadata |
| US-005 | As the challenge developer, I want to evaluate the published v2 with five objective metrics, to know whether it meets the approval criterion | FR-021 to FR-024 | The run shows the five scores, the average and the status per BR-001 |
| US-006 | As the challenge developer, I want to edit, republish and re-evaluate v2 and compare experiments, to reach >= 0.8 on all metrics | FR-005 to FR-024 | Each valid cycle creates a comparable experiment; the last one meets BR-001 |
| US-007 | As the reviewer, I want a public link with the dataset, runs and traces, to verify the scores without workspace access | FR-035, FR-036 | The link opens without workspace authentication and shows the FR-036 items |
| US-008 | As the reviewer, I want to read in the README the techniques, results and run instructions, to assess and reproduce the solution | FR-032 to FR-034, FR-037, FR-038 | The README has the three mandatory sections and the repository meets FR-037 |

## 11. Acceptance criteria in Gherkin

```gherkin
Feature: Base prompt pull (FR-001 to FR-004)

  Scenario: Pull the seed prompt with valid credentials
    Given the LangSmith credentials are configured
    And the prompt "leonanluppi/bug_to_user_story_v1" is available on the Hub
    When the developer runs the pull
    Then "prompts/bug_to_user_story_v1.yml" is created as valid YAML
    And it contains the system and user texts of the pulled prompt
    And the run exits with success status

  Scenario: Missing credential
    Given the LangSmith API key is not configured
    When the developer runs the pull
    Then the system lists the missing variables in Portuguese
    And the Hub is not contacted
    And the run exits with failure status

  Scenario: Hub failure
    Given the credentials are configured
    And the Hub does not respond or rejects the request
    When the developer runs the pull
    Then the system reports the reason in Portuguese
    And the run exits with failure status
```

```gherkin
Feature: v2 structural validation (FR-025 to FR-031, FR-039)

  Scenario: Compliant v2 prompt
    Given the v2 prompt has a non-empty system prompt
    And defines a persona
    And requires the User Story format
    And contains 3 input/output examples
    And has no "[TODO]"
    And lists at least 2 techniques in its metadata
    When the developer runs the structural validation
    Then all checks pass

  Scenario: Only one technique listed
    Given the v2 metadata lists a single technique
    When the developer runs the structural validation
    Then the minimum techniques check fails
    And the result names the failing check

  Scenario: Forgotten pending marker
    Given the v2 prompt contains "[TODO]"
    When the developer runs the structural validation
    Then the no-pending-markers check fails
```

```gherkin
Feature: v2 publishing (FR-015 to FR-020)

  Scenario: Publish a valid prompt
    Given the local v2 prompt is valid
    And the public Hub handle exists and is configured
    When the developer runs the push
    Then the prompt is available on the Hub as "{handle}/bug_to_user_story_v2"
    And the prompt is public
    And tags, description and techniques are recorded
    And the run exits with success status

  Scenario: Block an invalid prompt
    Given the local v2 prompt has no version field
    And lists fewer than 2 techniques
    When the developer runs the push
    Then nothing is published
    And all validation errors are listed in Portuguese
    And the run exits with failure status

  Scenario: Missing Hub handle
    Given the local v2 prompt is valid
    And the configured handle does not exist on the Hub
    When the developer runs the push
    Then publishing fails
    And the system explains how to create the handle via Make Public in the LangSmith UI

  Scenario: Missing v2 file
    Given "prompts/bug_to_user_story_v2.yml" does not exist
    When the developer runs the push
    Then the system reports that the file was not found
    And nothing is published
```

```gherkin
Feature: Evaluation of the published prompt (FR-021 to FR-024, BR-001, BR-018)

  Scenario: Approval with every metric at or above the threshold
    Given the v2 prompt is published
    And the averages are Helpfulness 0.85, Correctness 0.80, F1-Score 0.80, Clarity 0.90 and Precision 0.80
    When the developer runs the evaluation
    Then the status shown is "APROVADO"

  Scenario: Rejection with a high average and one metric below the threshold
    Given the v2 prompt is published
    And the averages are Helpfulness 0.95, Correctness 0.87, F1-Score 0.79, Clarity 0.95 and Precision 0.95
    When the developer runs the evaluation
    Then the status shown is "REPROVADO"
    And "f1_score" is listed as below 0.8

  Scenario: Unpublished local change
    Given the developer changed the local v2 prompt
    And did not run the push afterwards
    When the developer runs the evaluation
    Then the evaluated version is the last one published on the Hub

  Scenario: v2 not yet published
    Given "{handle}/bug_to_user_story_v2" does not exist on the Hub
    When the developer runs the evaluation
    Then the system reports that the prompt was not found
    And tells the developer to run the push

  Scenario: Run invalidated by an infrastructure error
    Given an evaluation run printed "Erro ao avaliar" for at least one example
    When the developer reviews the run
    Then the run is discarded and not counted as an iteration
    And the evaluation is repeated without changing the prompt
```

```gherkin
Feature: Public delivery evidence (FR-035, FR-036)

  Scenario: Reviewer opens the evidence
    Given the public dataset link was created and recorded in the README
    And the reviewer has no access to the developer workspace
    When the reviewer opens the link
    Then the 15-example evaluation dataset is shown
    And the v2 runs with scores >= 0.8 are visible
    And the tracing of at least 3 examples can be inspected
```

## 12. Non-functional requirements

| ID | Category | Requirement | Evaluation criterion | Origin |
|---|---|---|---|---|
| NFR-001 | Reproducibility | Generation and evaluation run with temperature 0 (Existing). The Gemini 3.x guide recommends the default 1.0 and warns that lower values may cause looping or degraded quality; this is accepted because the evaluation code cannot change (RK-12) | Evaluation runs without temperature errors; first run traces checked for looping | Existing; [ADR-001](../adr/ADR-001-llm-provider-and-models.md) |
| NFR-002 | Configurability | Provider, generation model and evaluation model are set only in the environment configuration | Changing provider or model only requires editing `.env` | Confirmed |
| NFR-003 | Credential security | Credentials live only in the local `.env`, are never versioned and never appear in the README, screenshots or routine output | Repository and evidence contain no keys | Confirmed |
| NFR-004 | Third-party content safety | Pulling a third-party `owner/name` prompt is explicitly allowed only for the challenge seed prompt | No other third-party prompt is pulled | Confirmed |
| NFR-005 | Compatibility | The product runs on Python 3.10 or later | Successful run on Python 3.10+; compatibility of the pinned packages with the local Python 3.14 is checked in Phase 1 | Confirmed (challenge statement) |
| NFR-006 | Quota operation | The evaluation runs sequentially within the free-tier quotas: 60 LLM calls per run (15 generation, 45 judge). Measured limits on 2026-10-19: 15 RPM and 500 RPD per model, about 11 runs per day with the chosen models | Runs complete without quota errors; otherwise BR-018 applies | Existing; [ADR-001](../adr/ADR-001-llm-provider-and-models.md) |
| NFR-007 | Observability | Each evaluation run is traceable in LangSmith, with a trace per example and the five scores as feedback | The experiment shows 15 runs with traces and feedback | Existing |
| NFR-008 | Testability | Structural validation runs without network access and without LLM usage | Tests pass with the network disabled | Confirmed |
| NFR-009 | Maintainability | Code is readable, clean and simple, following the Zen of Python | Code review | Confirmed |
| NFR-010 | Usability and language | User messages and errors in Portuguese; identifiers, comments and logs in English | Inspection | Confirmed |
| NFR-011 | Delivery reproducibility | Routines run from the repository root with the commands documented in the README | A third party reproduces the flow following only the README | Confirmed |

No maximum run time is defined: the sources give no basis for one.

## 13. Business rules

| ID | Name | Description | Requirements |
|---|---|---|---|
| BR-001 | Approval criterion | Approval requires each of the five metrics >= 0.8 and their average >= 0.8; otherwise REPROVADO | FR-023 |
| BR-002 | Derived metrics | Per example: Helpfulness = (Clarity + Precision) / 2; Correctness = (F1-Score + Precision) / 2. Precision affects both | FR-022 |
| BR-003 | Immutable evaluation instruments | Dataset, metrics, threshold, evaluation script and helpers cannot be changed | FR-021 to FR-024 |
| BR-004 | Optimization target | Only the v2 prompt may change to improve scores | FR-005 to FR-014 |
| BR-005 | Published prompt identifier | `{handle}/bug_to_user_story_v2`. The handle is created the first time a prompt is made public in the LangSmith UI and is permanent once confirmed | FR-017, FR-020 |
| BR-006 | Public visibility | The published v2 prompt must be public | FR-018 |
| BR-007 | Evaluation source | The evaluation uses the version published on the Hub, not the local file | FR-021 |
| BR-008 | Techniques | Few-shot is mandatory, plus at least one of CoT, Tree of Thought, Skeleton of Thought, ReAct, Role Prompting; metadata lists at least 2 techniques. Decided set: Few-shot, Role Prompting, Chain of Thought | FR-008, FR-009, FR-016, FR-031 |
| BR-009 | Input variable | The only input is the bug report, received in the user prompt as `{bug_report}` | FR-011 |
| BR-010 | Model choice | Models are not fixed by the challenge; they are chosen from the provider's current official documentation and recorded in [ADR-001](../adr/ADR-001-llm-provider-and-models.md) | NFR-002 |
| BR-011 | Public evidence link | The public link comes from sharing the evaluation dataset, which exposes its experiments. Sharing again changes the link, so it is created once, with the owner's confirmation, and recorded | FR-033, FR-035 |
| BR-012 | Evaluation dataset | Named `{LANGSMITH_PROJECT}-eval`, created from the 15 local examples or reused if it exists; the project name cannot be empty | FR-021 |
| BR-013 | Seed prompt | The source prompt is `leonanluppi/bug_to_user_story_v1` | FR-002 |
| BR-014 | Configuration precondition | Routines that access external services require credentials and stop listing the missing variables | FR-001 |
| BR-015 | Explicit consent for third-party prompts | Pulling an `owner/name` prompt requires explicit consent (`dangerously_pull_public_prompt=True`), granted only for the seed prompt | FR-002, NFR-004 |
| BR-016 | User Story format | The output follows the dataset references: "Como um ..., eu quero ..., para que ..." sentence, "Critérios de Aceitação:" in Dado que / Quando / Então / E; medium reports add technical blocks; complex reports use `=== ... ===` sections (spec 002) | FR-012 |
| BR-017 | Delivery form | Public GitHub repository forked from the base repository | FR-037 |
| BR-018 | Invalid runs | A run with a score caused by an infrastructure error (quota, network, unparseable judge output, shown as "Erro ao avaliar") is discarded, repeated without prompt changes and not counted as an iteration; the reason is recorded | KPI-08, FR-023 |
| BR-019 | Fixed models | Generation and evaluation models stay fixed from the first evaluation on. A change is allowed only by recording a new baseline, because scores across different models are not comparable | NFR-002, KPI-08 |
| BR-020 | Own examples | Few-shot examples are written for the prompt; reports and references from the dataset are never copied into the prompt | FR-008 |

## 14. Main flows

**FL-01: Environment setup**
- Steps:
  1. Create the LangSmith account and API key.
  2. Create the public Hub handle by making a prompt public in the UI.
  3. Create the Gemini API key.
  4. Fill `.env` from `.env.example` (credentials, project, handle, provider, models per ADR-001).
  5. Create the virtual environment and install the dependencies.
- Result: routines runnable.
- Exceptions: package incompatible with the local Python version (NFR-005).

**FL-02: Base prompt pull**: run the pull and analyze the generated file. Exceptions: missing credentials, Hub failure. Requirements: FR-001 to FR-004.

**FL-03: Optimization and local validation**: edit v2, run the structural validation, fix failures. Requirements: FR-005 to FR-014, FR-025 to FR-031, FR-039.

**FL-04: Publishing**: run the push and check the prompt on the Hub. Exceptions: failed validation, missing handle. Requirements: FR-015 to FR-020.

**FL-05: Evaluation and iteration**
- Steps:
  1. Run the evaluation.
  2. Check the output for "Erro ao avaliar"; if present, apply BR-018.
  3. If REPROVADO, analyze the low metrics and the per-example traces.
  4. Return to FL-03 and FL-04, preferably one change per iteration.
  5. Repeat until APROVADO.
- Requirements: FR-021 to FR-024, BR-001, BR-007, BR-018, BR-019.

**FL-06: Evidence and delivery**
- Steps:
  1. Create the public dataset link once (BR-011).
  2. Capture screenshots into `docs/images/`.
  3. Replace the README with the delivery documentation.
  4. Push the repository.
- Requirements: FR-032 to FR-038.

## 15. Dependencies, constraints, assumptions and risks

### 15.1. Dependencies

| ID | Dependency |
|---|---|
| D-01 | LangSmith account with API key and access to the Prompt Hub, datasets and experiments |
| D-02 | Public LangSmith Hub handle |
| D-03 | Public availability of the seed prompt `leonanluppi/bug_to_user_story_v1` |
| D-04 | Google Gemini API key on the free tier, with the models of ADR-001 available |
| D-05 | Fork `fonsecamrs/mba-ia-pull-evaluation-prompt` with the ready-made components |
| D-06 | Internet access for pull, push and evaluation |

### 15.2. Constraints

| ID | Constraint |
|---|---|
| R-01 | Python 3.10+ |
| R-02 | LangChain framework; LangSmith for prompt management and evaluation |
| R-03 | Prompts in YAML |
| R-04 | Mandatory directory and file structure of the challenge |
| R-05 | Ready-made components and dataset cannot change (BR-003) |
| R-06 | Delivery as a public fork (BR-017) |
| R-07 | Language rules of `CLAUDE.md` |
| R-08 | Versioning process: commits only with explicit authorization, Conventional Commits in Portuguese, one branch per phase named `phase-N-<name>` |

### 15.3. Assumptions

| ID | Assumption |
|---|---|
| PR-01 | The seed prompt stays available on the Hub during development |
| PR-02 | The free-tier quota (about 11 runs per day) is enough for the expected 3 to 5 iterations plus repeated runs |
| PR-03 | Mirroring the reference format (BR-016) helps reach the F1-Score and Precision targets |

### 15.4. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| RK-01 | Free-tier rate or daily quota interrupts the evaluation | Sequential evaluation (Existing); generation and judge on different models to split the quota (ADR-001); space out runs |
| RK-02 | A judge call or parsing failure yields 0.0 for the example and lowers the average | Check the output and traces before changing the prompt; BR-018 |
| RK-03 | Scores vary between runs because of the LLM judge | Temperature 0; fixed models (BR-019); record each iteration's scores |
| RK-04 | Chosen model discontinued or without temperature 0 support | Re-check the official documentation before Phase 3 (ADR-001) |
| RK-05 | Over-fitting the prompt to the dataset | Own Few-shot examples (BR-020) |
| RK-06 | Permanent choice of an unsuitable handle | Choose carefully before confirming; recommendation: same as the GitHub username |
| RK-08 | Public link changed by a new share after being recorded in the README | Create it once and record it (BR-011) |
| RK-09 | Free-tier daily limit allows few runs per day | No fixed deadline; plan one change per iteration; paid tier is a future decision |
| RK-10 | Git conflicts confuse the developer during setup | Closed: fork cloned without conflicts on 2026-10-13 |
| RK-11 | A quota error becomes 0.0 silently instead of stopping the run | Check for "Erro ao avaliar" before analyzing scores; BR-018 |
| RK-12 | Temperature 0 on Gemini 3.x models may cause looping or degraded quality, especially on the long complex outputs | Inspect the traces of the 3 complex examples in the first run; record the finding |

RK-07 (delivery repository not a fork) was closed on 2026-10-13: the fork `fonsecamrs/mba-ia-pull-evaluation-prompt` was created.

## 16. Out of scope

| Item | Reason |
|---|---|
| Changing the dataset, metrics, threshold or evaluation script | Forbidden (BR-003) |
| Automated evaluation of v1 or other prompts | The existing script evaluates only v2 and cannot change; the v1 x v2 comparison is qualitative (Q-005) |
| Extra metrics present in `metrics.py` but unused (Tone, Acceptance Criteria, User Story Format, Completeness) | Not part of the approval criterion |
| Hard-coding provider or model | Forbidden (BR-010, NFR-002) |
| Database | Not used |
| Authentication, authorization, APIs, deploy | No users, services or servers in the product |
| Operational use of the generated User Stories | The product measures prompt quality only |

## 17. Decisions and open questions

### 17.1. Decisions recorded during discovery

| ID | Question | Decision | Date |
|---|---|---|---|
| Q-001 | Delivery repository | Public fork `fonsecamrs/mba-ia-pull-evaluation-prompt`, original name kept | 2026-10-13 |
| Q-002 | Documentation language | `docs/` in English, including this PRD | 2026-10-13 |
| Q-003 | Minimum Python version | 3.10+ (challenge statement); local environment has 3.14 | 2026-10-13 |
| Q-004 | Provider, models, quotas | Gemini free tier: generation `gemini-3.1-flash-lite`, judge `gemini-3.5-flash-lite` ([ADR-001](../adr/ADR-001-llm-provider-and-models.md)) | 2026-10-19 |
| Q-005 | v1 x v2 comparison | Qualitative comparison plus the history of v2 iterations; no measured v1 baseline | 2026-10-19 |
| Q-006 | Output format | Mirror the dataset references, by complexity (BR-016) | 2026-10-19 |
| Q-007 | Screenshot location | `docs/images/` (the base `.gitignore` ignores `screenshots/`) | 2026-10-19 |
| Q-008 | Branch naming | `phase-N-<name>`, matching the phase document names | 2026-10-19 |
| Q-009 | Deadline | No fixed deadline | 2026-10-13 |
| Q-010 | Approval stability | One valid approved run is enough | 2026-10-19 |
| Q-012 | Number of Few-shot examples | 3: simple, medium, complex | 2026-10-19 |
| Q-013 | Mandatory edge cases | Vague or incomplete report; several problems in one report | 2026-10-19 |
| — | Database | None | 2026-10-13 |
| — | Discovery scope | Challenge only, lean documentation | 2026-10-13 |
| — | Additional techniques | Role Prompting and internal Chain of Thought | 2026-10-19 |
| — | Invalid runs and fixed models | BR-018 and BR-019 | 2026-10-19 |
| — | README | Replaces the challenge statement (FR-038) | 2026-10-19 |

### 17.2. Open questions

| ID | Question | Impact | Next action |
|---|---|---|---|
| Q-011 | Product owner and PRD approver: Marcos Fonseca is assumed | Document governance | Confirm when approving this version |
| Q-014 | How to show the techniques on the Hub: tags and description (recommended) or another field | FR-019 verifiability | Check `Client.push_prompt` in the installed `langsmith` during Phase 3 |
| Q-015 | Compatibility of the pinned packages with Python 3.14 | Environment setup | Check during the Phase 1 install; fallback: install Python 3.12 or 3.13 |

## 18. Product evolution and PRD versioning

- Update this document on relevant changes to requirements, scope, objectives or success criteria, and record them below.
- When a requirement changes, update its stories, rules, criteria and traceability in the same revision.
- Never reuse removed identifiers; mark discontinued items as "Removed".
- Record as a new version any decision that changes the MVP.

### 18.1. Version history

| Date | Version | Change | Reason |
|---|---|---|---|
| 2026-10-13 | 0.1 | Document created (Portuguese) | Initial consolidation of the challenge requirements, `CLAUDE.md` and the base repository |
| 2026-10-19 | 0.2 | Translated to English; Q-001 to Q-010, Q-012 and Q-013 resolved; requirements tables condensed; FR-008 to FR-010, FR-012, FR-019, FR-029, FR-033 detailed; FR-038, FR-039, BR-018 to BR-020, RK-09 to RK-12, Q-015 added; RK-07 and RK-10 closed; PB-01 corrected (vague persona, not missing) | Discovery interview and reading of the base repository code |

## 19. Traceability matrix

### 19.1. Objectives, problems and indicators

| Objective | Problems | Indicators | Groups |
|---|---|---|---|
| OBJ-01 | PB-01, PB-02 | KPI-01 to KPI-06, KPI-08 | G2, G3, G4 |
| OBJ-02 | PB-02 | KPI-08 | G1, G3, G4 |
| OBJ-03 | PB-04 | KPI-07 | G2, G5 |
| OBJ-04 | PB-03 | KPI-09 | G6 |

### 19.2. Requirements, stories, specs and phases

| Group | Functional requirements | Stories | Business rules | NFRs | Spec | Phase |
|---|---|---|---|---|---|---|
| G1 | FR-001 to FR-004 | US-001 | BR-013, BR-014, BR-015 | NFR-003, NFR-004, NFR-010 | [001](../../specs/001-pull-prompt/spec.md) | 1 |
| G2 | FR-005 to FR-014 | US-002, US-006 | BR-004, BR-008, BR-009, BR-016, BR-020 | NFR-010 | [002](../../specs/002-prompt-v2/spec.md) | 2, 4 |
| G3 | FR-015 to FR-020 | US-004, US-006 | BR-005, BR-006, BR-008 | NFR-003, NFR-010 | [003](../../specs/003-push-prompt/spec.md) | 3 |
| G4 | FR-021 to FR-024 | US-005, US-006 | BR-001, BR-002, BR-003, BR-007, BR-010, BR-012, BR-018, BR-019 | NFR-001, NFR-002, NFR-006, NFR-007 | — (Existing) | 3, 4 |
| G5 | FR-025 to FR-031, FR-039 | US-003 | BR-008 | NFR-008 | [004](../../specs/004-validation-tests/spec.md) | 5 |
| G6 | FR-032 to FR-038 | US-007, US-008 | BR-011, BR-017 | NFR-003, NFR-011 | — | 4 |
