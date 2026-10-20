---
paths:
  - "prompts/**/*.yml"
---

# Prompts YAML

## Arquivos

- `bug_to_user_story_v1.yml`: gerado por `src/pull_prompts.py`. Não editar à mão. Serve só como referência dos defeitos.
- `bug_to_user_story_v2.yml`: único arquivo editado nas iterações.

## Estrutura do v2

Mesma estrutura do v1, com chave raiz própria:

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

- Campos validados por `validate_prompt_structure` (em `src/utils.py`): `description`, `system_prompt` não vazio,
  `version` e `techniques_applied` com pelo menos 2 itens. A função recebe o dicionário interno, não a chave raiz.

## Variáveis de template

- Única variável: `{bug_report}` (chave de entrada do dataset), somente no `user_prompt`.
  Não repetir o relato no `system_prompt` (defeito intencional do v1).
- O `ChatPromptTemplate` interpreta o texto como f-string: chaves literais no `system_prompt`
  (JSON, rotas como `/api/uploads/{id}`, código nos exemplos) devem ser escritas como `{{` e `}}`.
- A palavra `TODO` em maiúsculas não pode aparecer no `system_prompt`: a validação faz busca literal
  e sensível a maiúsculas (ex.: "TODOS" em caixa alta reprova; "todos" passa).

## Requisitos de conteúdo

- Todo o texto do prompt em português.
- Separação System vs User: persona, instruções, regras, formato e exemplos no system; apenas o relato no user.
- Role Prompting: persona explícita iniciando com "Você é" (ex.: "Você é um Product Manager sênior ...").
- Instruções claras e específicas e regras explícitas de comportamento (o que fazer e o que não fazer).
- Few-shot obrigatório: exatamente 3 exemplos de entrada e saída (simples, médio, complexo, nessa ordem).
  Marcar cada exemplo de forma consistente com `Exemplo N`, `Entrada:` e `Saída:`; os testes dependem desses marcadores.
- Não copiar relatos nem referências do dataset para os exemplos: escrever exemplos próprios com a mesma estrutura.
- Técnicas decididas: Few-shot, Role Prompting e Chain of Thought interno (etapas de análise que o modelo segue sem
  exibir). Registrar todas em `techniques_applied`.
- Edge cases obrigatórios com instrução explícita: relato vago ou incompleto; vários problemas no mesmo relato.
- Não inventar dados ausentes no relato (valores, nomes, métricas); quando faltarem, usar descrição genérica ou
  placeholder entre colchetes, como as referências fazem (ex.: `[nome do gateway de pagamento]`).
- Detalhes do conteúdo e do formato: `specs/002-prompt-v2/spec.md`.

## Formato de saída esperado

Alinhado às `reference` de `datasets/bug_to_user_story.jsonl` (consultar o arquivo antes de alterar o formato):
- Frase de User Story: "Como um <persona>, eu quero <objetivo>, para que <benefício>."
- `Critérios de Aceitação:` em lista com `Dado que`, `Quando`, `Então` e `E`.
- Relatos médios adicionam blocos como `Contexto Técnico:` ou `Critérios Técnicos:` quando o relato traz esses dados.
- Relatos complexos (vários problemas) usam seções `=== USER STORY PRINCIPAL ===`, `=== CRITÉRIOS DE ACEITAÇÃO ===`
  (subdivididos A, B, C...), `=== CRITÉRIOS TÉCNICOS ===`, `=== CONTEXTO DO BUG ===` e `=== TASKS TÉCNICAS SUGERIDAS ===`.
- A resposta final contém apenas a User Story. Se usar CoT, verificar no tracing se o raciocínio exposto na
  resposta reduz Precision ou Clarity e, nesse caso, instruir o modelo a não exibi-lo.

## Iteração

- Métricas derivadas: Helpfulness = (Clarity + Precision) / 2; Correctness = (F1-Score + Precision) / 2.
  Precision entra nas duas derivadas.
- Analisar no tracing os exemplos com nota mais baixa antes de editar.
- Preferir uma mudança isolada por iteração, para atribuir o efeito nas métricas.
- Registrar cada iteração (mudança feita e notas obtidas) para o README e `docs/project/phase-4-iteration.md`.
- Após editar: rodar `pytest tests/test_prompts.py`, depois push, depois evaluate.