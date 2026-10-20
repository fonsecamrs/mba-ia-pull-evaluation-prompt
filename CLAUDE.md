# CLAUDE.md

Desafio 2 do MBA em IA (Full Cycle): pull, otimização, push e avaliação de prompts com LangChain e LangSmith.
Meta: o prompt `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2` atingir >= 0.8 em CADA uma das 5 métricas
(Helpfulness, Correctness, F1-Score, Clarity, Precision) e também na média. Média alta com uma métrica abaixo de 0.8 reprova.

## Stack

- Python 3.10+, `langchain-core`, `langsmith` (Client: Prompt Hub, datasets, experimentos), prompts em YAML, `pytest`.
- Versões fixadas em `requirements.txt`. Não usar `langchain.hub` (removido na v1 do LangChain): pull/push via `langsmith.Client`.
- LLM configurado só por `.env`: `LLM_PROVIDER` (`google` ou `openai`), `LLM_MODEL` (resposta) e `EVAL_MODEL` (avaliação).
  Provedor, modelos e plano (Gemini gratuito) decididos em `docs/adr/ADR-001-llm-provider-and-models.md`.
- Este projeto não usa banco de dados.

## Comandos

Executar sempre a partir da raiz do repositório: os scripts usam caminhos relativos e importam `utils` de `src/`.

```bash
python3 -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/pull_prompts.py     # leonanluppi/bug_to_user_story_v1 -> prompts/bug_to_user_story_v1.yml
python src/push_prompts.py     # prompts/bug_to_user_story_v2.yml -> {handle}/bug_to_user_story_v2 (público)
python src/evaluate.py         # experimento no LangSmith com as 5 métricas
pytest tests/test_prompts.py   # validação estrutural do prompt v2 (offline)
```

## Fluxo de trabalho

1. Pull do v1 -> 2. editar `prompts/bug_to_user_story_v2.yml` -> 3. pytest -> 4. push -> 5. evaluate -> repetir 2 a 5 (3 a 5 iterações esperadas).
- `evaluate.py` avalia a versão publicada no Hub, não o arquivo local: toda alteração no v2 exige novo push antes de avaliar.
- Execução com "Erro ao avaliar" na saída (cota, rede) é descartada e repetida sem mudar o prompt; não conta como iteração (BR-018).
- Modelos fixos a partir da primeira avaliação; trocar só registrando nova linha de base (BR-019).
- O handle do Hub (`USERNAME_LANGSMITH_HUB`) só existe após tornar um prompt público na UI do LangSmith (Make Public). É definitivo.
- Diagnóstico de notas baixas: usar o tracing do LangSmith, exemplo a exemplo.

## Escopo de implementação

Implementar apenas:
- `src/pull_prompts.py` e `src/push_prompts.py`: corpo das funções do esqueleto, mantendo nomes e assinaturas.
- `prompts/bug_to_user_story_v2.yml`: criado do zero.
- `tests/test_prompts.py`: os 6 testes obrigatórios (mais testes são permitidos).
- `README.md`, `docs/` e `specs/`.

Não alterar (prontos, fazem parte da avaliação do desafio):
- `src/evaluate.py`, `src/metrics.py`, `src/utils.py`
- `datasets/bug_to_user_story.jsonl`
- `prompts/bug_to_user_story_v1.yml` (gerado apenas pelo pull)

Para subir as notas, iterar somente no `bug_to_user_story_v2.yml`. Nunca ajustar dataset, métricas, threshold ou o script de avaliação.
Reutilizar os helpers de `src/utils.py` (`load_yaml`, `save_yaml`, `check_env_vars`, `print_section_header`,
`validate_prompt_structure`, `get_llm`, `get_eval_llm`) em vez de reimplementá-los.

## Restrições: pedir confirmação explícita antes de

- Commitar segredos ou chaves de API. `.env` nunca é versionado; variáveis novas entram em `.env.example` sem valor.
- Editar arquivos de configuração de ambientes não locais.
- Fixar em código provedor ou nome de modelo de LLM. Usar `get_llm`/`get_eval_llm` e as variáveis do `.env`.
- Executar `push_prompts.py` (publica no Hub) ou `evaluate.py` (consome cota de API e cria experimento).
- Alterar `requirements.txt` ou adicionar dependências.
- Executar `share_dataset`: cada nova execução muda o link público já registrado no README.

## Fases e branches

As fases seguem a numeração dos requisitos do desafio. Cada fase tem branch própria (`phase-N-<nome>`, igual ao nome
do documento sem `.md`) e documento em `docs/project/`. Ordem de execução: 0, 1, 2, 5, 3, 4 (testes antes do push).

| Fase | Entrega | Documento |
|---|---|---|
| 0 | Discovery: PRD, ADR, specs e documentos de fase | — (branch `phase-0-discovery`) |
| 1 | Pull do prompt v1 | `phase-1-pull.md` |
| 2 | Prompt otimizado v2 | `phase-2-prompt-optimization.md` |
| 3 | Push ao Hub e primeira avaliação | `phase-3-push-evaluation.md` |
| 4 | Iterações até todas as métricas >= 0.8 | `phase-4-iteration.md` |
| 5 | Testes de validação | `phase-5-validation-tests.md` |

## Git e commits

- Nunca commitar automaticamente: apresentar arquivos alterados e mensagem proposta e aguardar autorização explícita.
- Criar uma branch nova ao iniciar cada fase, no padrão `phase-N-<nome>` (ver "Fases e branches").
- Conventional Commits com descrição em português: `<tipo>: <descrição>`.
- Tipos permitidos:
  - `feat`: nova funcionalidade
  - `fix`: correção de bug ou erro
  - `docs`: somente documentação
  - `style`: formatação sem efeito no comportamento
  - `refactor`: mudança de código sem corrigir bug nem adicionar funcionalidade
  - `perf`: melhoria de desempenho
  - `test`: adicionar ou corrigir testes
  - `chore`: build, configuração de ferramentas ou pacotes (ex.: `.gitignore`)
- Repositório de entrega: `fonsecamrs/mba-ia-pull-evaluation-prompt`, fork público de `devfullcycle/mba-ia-pull-evaluation-prompt`.

## Idioma

- Inglês: `specs/`, `docs/` (incluindo `docs/project/`), nomes de arquivos, classes, funções e variáveis,
  comentários e docstrings novos, mensagens de log.
- Português: mensagens de commit, mensagens de erro e saída de CLI exibidas ao usuário, conteúdo dos prompts
  enviados ao LLM, `README.md`.
- Não traduzir docstrings e mensagens já existentes no código base.

## Código

- Legível, limpo e simples, seguindo o Zen do Python (PEP 20). Detalhes na rule de estilo Python.

## Documentação

- Enxuta: criar apenas o necessário para orientar a implementação.
- Requisitos e regras de negócio (o quê): `docs/prd/PRD.md`. Detalhe por funcionalidade: `specs/`.
  Decisões arquiteturais: `docs/adr/`. Como implementar cada fase: `docs/project/`. Imagens do README: `docs/images/`.
- Convenções de PRD, specs, ADRs, documentos de fase e seções obrigatórias do README: rule de documentação.

## Rules específicas

Carregadas automaticamente por `paths` ao ler ou editar arquivos correspondentes.
Antes de CRIAR um arquivo novo nesses caminhos, ler a rule correspondente.

| Rule | Aplica-se a |
|---|---|
| `.claude/rules/prompts/prompt-yaml.md` | `prompts/**/*.yml` |
| `.claude/rules/python/code-style.md` | `src/**/*.py`, `tests/**/*.py` |
| `.claude/rules/python/langsmith-scripts.md` | `src/pull_prompts.py`, `src/push_prompts.py` |
| `.claude/rules/tests/prompt-tests.md` | `tests/**/*.py` |
| `.claude/rules/docs/documentation.md` | `README.md`, `docs/**/*.md`, `specs/**/*.md` |

## Manutenção deste arquivo

- Máximo de 200 linhas. Ao ultrapassar, não remover informação importante: extrair instruções específicas
  para `.claude/rules/` (um arquivo por assunto, subdiretórios quando fizer sentido, `paths` com globs no frontmatter).
- Manter aqui só instruções gerais e de maior abrangência; referenciar as rules novas na tabela acima sem duplicar seu conteúdo.