---
paths:
  - "README.md"
  - "docs/**/*.md"
  - "specs/**/*.md"
---

# Documentação

## Princípios

- Enxuta: apenas o necessário para orientar a implementação. Não repetir o que já está no código.
- Nunca registrar segredos, chaves de API ou links privados do workspace do LangSmith.
- Decisão ainda não tomada é registrada como pendente, nunca inventada.

## Estrutura

| Arquivo | Conteúdo | Idioma |
|---|---|---|
| `docs/prd/PRD.md` | Requisitos do produto com IDs. Fonte da verdade do o quê | Inglês |
| `specs/NNN-<feature>/spec.md` | Fluxos, exceções, critérios de aceite e casos de teste, referenciando IDs do PRD | Inglês |
| `docs/adr/ADR-NNN-<title>.md` | Apenas decisões arquiteturais relevantes (contexto, decisão, consequências, status) | Inglês |
| `docs/project/phase-<N>-<name>.md` | Como implementar a fase: escopo, entregas, critérios de aceite | Inglês |
| `README.md` | Documentação de entrega do desafio | Português |

- Numeração `NNN` com três dígitos (`001`, `002`). Nomes de arquivo em inglês, kebab-case.

## README.md (seções obrigatórias da entrega)

### Técnicas Aplicadas (Fase 2)
- Técnicas escolhidas, justificativa de cada uma e exemplo prático de aplicação no prompt v2.

### Resultados Finais
- Link público do dataset de avaliação com os experimentos (gerado por `share_dataset`).
- Screenshots das avaliações com todas as métricas >= 0.8 (local de armazenamento das imagens: confirmar com o usuário).
- Comparação v1 vs v2: o que mudou e por quê, incluindo o histórico das iterações e suas notas.

### Como Executar
- Pré-requisitos (Python 3.10+, conta LangSmith com handle público, chave de API do provedor de LLM).
- Configuração do `.env` a partir do `.env.example`, sem expor valores.
- Comandos de cada fase: venv, instalação, pull, push, evaluate e pytest.

## Evidências no LangSmith (devem estar visíveis pelo link ou screenshots)

- Dataset de avaliação com 15 exemplos.
- Execuções do prompt v2 com notas >= 0.8.
- Tracing detalhado de pelo menos 3 exemplos.