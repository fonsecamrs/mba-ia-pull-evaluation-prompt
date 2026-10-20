---
paths:
  - "tests/**/*.py"
---

# Testes de validação do prompt

- Arquivo: `tests/test_prompts.py`. Executar com `pytest tests/test_prompts.py`.
- Manter a classe `TestPrompts` e os nomes exatos dos 6 testes obrigatórios do esqueleto.
- Testes offline e determinísticos: sem chamadas a LLM, LangSmith ou rede.
- Carregar `prompts/bug_to_user_story_v2.yml` por caminho relativo ao arquivo de teste
  (`Path(__file__).parent.parent / "prompts" / ...`) e acessar a chave raiz `bug_to_user_story_v2`.
- Preferir uma fixture para carregar o YAML uma única vez.
- Mensagens de assert em português, dizendo o que falta no prompt.

## Critério de cada teste

| Teste | Verifica |
|---|---|
| `test_prompt_has_system_prompt` | `system_prompt` existe e não está vazio após `strip()` |
| `test_prompt_has_role_definition` | `system_prompt` define persona (padrão "Você é") |
| `test_prompt_mentions_format` | `system_prompt` exige formato User Story padrão ou Markdown |
| `test_prompt_has_few_shot_examples` | marcadores `Exemplo`, `Entrada:` e `Saída:` presentes, com ao menos 3 exemplos |
| `test_prompt_no_todos` | nenhum `[TODO]` em `system_prompt` e `user_prompt` |
| `test_minimum_techniques` | `techniques_applied` é lista com pelo menos 2 itens |

- Os marcadores verificados devem ser os mesmos definidos na rule de prompts. Se o formato do prompt mudar,
  atualizar o teste correspondente na mesma alteração.
- Teste adicional decidido: `test_bug_report_only_in_user_prompt` (`{bug_report}` presente no `user_prompt` e ausente
  no `system_prompt`). Detalhes: `specs/004-validation-tests/spec.md`.