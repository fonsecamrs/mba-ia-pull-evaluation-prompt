---
paths:
  - "src/pull_prompts.py"
  - "src/push_prompts.py"
---

# Scripts de pull e push no LangSmith

## Pull (`src/pull_prompts.py`)

- Variáveis exigidas: no mínimo `LANGSMITH_API_KEY`.
- Usar `Client().pull_prompt("leonanluppi/bug_to_user_story_v1", dangerously_pull_public_prompt=True)`.
  O parâmetro é obrigatório para identificadores `owner/nome`; usar apenas com prompts de origem conhecida.
- O retorno é um `ChatPromptTemplate`: extrair o texto de cada mensagem por `prompt.messages[i].prompt.template`,
  identificando system e user pelo tipo da mensagem.
- Gravar com `save_yaml` em `prompts/bug_to_user_story_v1.yml`, na estrutura do arquivo original:
  chave raiz `bug_to_user_story_v1` com `description`, `system_prompt`, `user_prompt`, `version` e `tags`.

## Push (`src/push_prompts.py`)

- Variáveis exigidas: `LANGSMITH_API_KEY` e `USERNAME_LANGSMITH_HUB`.
- Ler `prompts/bug_to_user_story_v2.yml` com `load_yaml` e acessar a chave raiz `bug_to_user_story_v2`.
- Validar antes do push (`validate_prompt`, podendo delegar a `validate_prompt_structure`); se houver erros,
  listar todos e encerrar com código `1` sem publicar.
- Montar `ChatPromptTemplate.from_messages([("system", system_prompt), ("user", user_prompt)])`.
- Publicar com `client.push_prompt(f"{username}/bug_to_user_story_v2", object=prompt, is_public=True,
  description=..., tags=[...])` e imprimir a URL retornada.
- Metadados obrigatórios no push: tags, descrição e técnicas utilizadas (de `techniques_applied`).
  Conferir na assinatura de `Client.push_prompt` da versão instalada de `langsmith` quais parâmetros existem
  para isso antes de usar algum além de `description` e `tags`.
- Erro de handle inexistente ou não encontrado: orientar o usuário a criar o handle via Make Public na UI.

## Evidências

- Dataset de avaliação criado pelo `evaluate.py`: `{LANGSMITH_PROJECT}-eval` (15 exemplos).
- Link público: `Client().share_dataset(dataset_name="<LANGSMITH_PROJECT>-eval")["url"]`.
  Executar uma única vez, com confirmação do usuário; o link muda a cada novo compartilhamento.
- O link impresso pelo `evaluate.py` é privado do workspace e não serve como evidência pública.