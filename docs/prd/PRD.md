# PRD: Pipeline de Pull, Otimização, Publicação e Avaliação de Prompts

## 1. Identificação e controle do documento

| Campo | Valor |
|---|---|
| Produto / projeto | `mba-ia-pull-evaluation-prompt`: Desafio 2 do MBA em IA (Full Cycle), "Otimização e Avaliação de Prompts com LangChain e LangSmith" |
| Título do documento | Product Requirements Document (PRD) |
| Versão | 0.1 |
| Status | Rascunho, sem aprovação formal |
| Data da última atualização | 2026-10-13 |
| Responsável pelo produto | Pendente de definição (ver Q-011) |
| Objetivo do documento | Ser a fonte de referência do o quê, por quê e para quem do produto, com requisitos rastreáveis e verificáveis, para orientar specs, documentos de fase, desenvolvimento e testes |

### 1.1. Fontes utilizadas

| Fonte | Uso |
|---|---|
| Documento de contexto e requisitos do desafio, fornecido pelo usuário | Fonte primária de requisitos |
| [`CLAUDE.md`](../../CLAUDE.md) e rules em `.claude/rules/` | Restrições, decisões estabelecidas, idioma e processo |
| Repositório base `devfullcycle/mba-ia-pull-evaluation-prompt` (README, `.env.example`, `requirements.txt`, `src/evaluate.py`, `src/metrics.py`, `src/utils.py`, esqueletos, `prompts/bug_to_user_story_v1.yml`, `datasets/bug_to_user_story.jsonl`) | Comportamento já existente dos componentes prontos e formato dos dados de avaliação |

### 1.2. Convenções

- **Confirmado:** consta explicitamente em uma das fontes.
- **Existente:** comportamento já implementado nos componentes prontos do repositório base, que não devem ser alterados.
- **Premissa / hipótese:** considerado verdadeiro provisoriamente; precisa de validação.
- **Pendente:** decisão ou informação ausente, registrada em [Questões em aberto](#17-questões-em-aberto-e-decisões-pendentes).

Siglas: PRD (Product Requirements Document), MVP (Minimum Viable Product), LLM (Large Language Model), CLI (Command Line Interface), YAML (formato de arquivo de dados), Hub (LangSmith Prompt Hub), F1 (média harmônica entre precisão e cobertura).

## 2. Resumo executivo

O produto é um conjunto de rotinas de linha de comando que obtém um prompt de baixa qualidade publicado no LangSmith Prompt Hub, permite produzir uma versão otimizada desse prompt com técnicas de engenharia de prompt, publica a versão otimizada no Hub e mede sua qualidade de forma automatizada contra um conjunto fixo de 15 exemplos.

O prompt em questão transforma relatos de bugs em User Stories com critérios de aceitação. A versão original (`bug_to_user_story_v1`) tem defeitos conhecidos: instruções vagas, ausência de exemplos, ausência de persona e o relato de bug duplicado no prompt de sistema e no de usuário.

Usuários principais:
- o desenvolvedor que executa o desafio;
- o avaliador do desafio, que verifica a entrega.

O valor entregue é um ciclo reprodutível de "obter, otimizar, publicar e medir" que transforma a qualidade de um prompt em números comparáveis entre iterações, com evidências públicas.

**Objetivo principal da primeira versão:** o prompt `{handle}/bug_to_user_story_v2` obter nota maior ou igual a 0.8 em cada uma das cinco métricas (Helpfulness, Correctness, F1-Score, Clarity, Precision) e na média. A entrega também precisa estar documentada e com evidências verificáveis por terceiros.

## 3. Contexto e problema de negócio

### 3.1. Cenário atual (fatos)

- O repositório base já fornece:
  - o dataset de avaliação com 15 relatos de bugs (5 simples, 7 médios e 3 complexos, conforme os metadados do dataset);
  - o script de avaliação com as cinco métricas;
  - funções auxiliares;
  - esqueletos dos scripts de pull, push e testes.
- O prompt semente `leonanluppi/bug_to_user_story_v1` está publicado no Hub. O próprio arquivo v1 declara que seus problemas são intencionais.
- A avaliação é feita por LLM juiz: F1-Score, Clarity e Precision são julgadas por um modelo de avaliação. Helpfulness e Correctness são derivadas dessas três.
- O provedor e os modelos de LLM não são fixados pelo desafio. Devem ser escolhidos conforme a documentação oficial vigente do provedor.

### 3.2. Dores identificadas

| ID | Problema | Tipo |
|---|---|---|
| PB-01 | O prompt v1 gera User Stories de baixa qualidade por instruções vagas, falta de exemplos, falta de persona e duplicação da variável de entrada | Fato (declarado no arquivo v1) |
| PB-02 | Não há como afirmar que um prompt é melhor que outro sem medição objetiva, repetível e comparável entre iterações | Fato (motivação do desafio) |
| PB-03 | O avaliador da entrega não tem acesso ao workspace privado do LangSmith do desenvolvedor; o link de experimento impresso pela avaliação só abre para quem tem acesso ao workspace | Fato |
| PB-04 | Requisitos estruturais do prompt (persona, exemplos, técnicas, ausência de pendências) podem ser esquecidos durante as iterações | Fato (motivo dos testes obrigatórios) |

As notas do v1 exibidas no material do desafio (0.45 a 0.52) são declaradas como **apenas ilustrativas**. Não existe linha de base medida do v1 (ver Q-005).

### 3.3. Consequências do problema

- User Stories imprecisas ou incompletas levam a requisitos mal compreendidos pelo time de desenvolvimento. Hipótese de contexto: a descrição do v1 cita "tarefas para desenvolvedores", mas o impacto não é medido pelo produto.
- Sem medição, ajustes no prompt são feitos por tentativa e erro, sem saber se melhoraram ou pioraram o resultado.
- Sem evidências públicas, a entrega não pode ser verificada pelo avaliador.

### 3.4. Oportunidade

Aplicar técnicas de engenharia de prompt (Few-shot obrigatório e ao menos uma técnica adicional) e um ciclo de avaliação automatizado para elevar a qualidade do prompt de forma mensurável e documentada.

### 3.5. Declaração do problema

O prompt `bug_to_user_story_v1` não produz User Stories com a qualidade exigida. Falta ao desenvolvedor um ciclo reprodutível para versionar, publicar e medir prompts que comprove, com evidências verificáveis por terceiros, que a versão otimizada atinge nota mínima de 0.8 em todas as métricas.

## 4. Visão do produto e proposta de valor

- **Visão:** tratar prompts como artefatos versionados e mensuráveis, cuja qualidade é demonstrada por avaliação automatizada e não por percepção subjetiva.
- **Proposta de valor:** com poucos comandos, o desenvolvedor obtém o prompt base, publica versões otimizadas e recebe notas objetivas por métrica e por exemplo, com histórico de experimentos comparável no LangSmith.
- **Benefícios esperados:**
  - qualidade do prompt comprovada por métricas;
  - iterações comparáveis lado a lado;
  - conformidade estrutural verificada automaticamente;
  - entrega auditável por link público.
- **Objetivos do produto:**

| ID | Objetivo |
|---|---|
| OBJ-01 | O prompt v2 publicado atinge nota maior ou igual a 0.8 em cada uma das cinco métricas e na média |
| OBJ-02 | Disponibilizar um ciclo reprodutível de obtenção, publicação versionada e avaliação de prompts |
| OBJ-03 | Verificar automaticamente que o prompt v2 atende aos requisitos estruturais de engenharia de prompt do desafio |
| OBJ-04 | Disponibilizar documentação e evidências públicas que permitam ao avaliador verificar e reproduzir a entrega |

## 5. Público-alvo e personas

Não há dados demográficos ou comportamentais nas fontes. Foram definidos perfis funcionais.

| ID | Perfil | Objetivos | Necessidades | Dificuldades | Uso do produto | Origem |
|---|---|---|---|---|---|---|
| P1 | Desenvolvedor do desafio (operador) | Atingir aprovação em todas as métricas e entregar o desafio | Obter o prompt base, publicar versões, medir notas e comparar iterações | Limites de requisições de planos gratuitos de LLM; variação das notas de LLM juiz; escolha de modelos sem orientação fixa | Executa pull, edita o v2, executa testes, push e avaliação; gera o link público e documenta | Confirmado |
| P2 | Avaliador do desafio | Verificar se a entrega cumpre os requisitos | Ver técnicas aplicadas, notas maiores ou iguais a 0.8, dataset, execuções e traces sem acesso ao workspace privado; reproduzir a execução | Link de experimento privado não abre para terceiros | Lê o README, acessa o link público do dataset e inspeciona o repositório | Confirmado (entregáveis e evidências exigidos) |
| P3 | Time de produto e desenvolvimento que recebe relatos de bugs (beneficiário indireto) | Receber User Stories claras a partir de relatos | User Story com persona, objetivo, benefício e critérios de aceitação | Não identificadas nas fontes | Não interage com o produto; consome a saída do prompt | Hipótese, derivada da descrição do prompt v1; não validada |

## 6. Objetivos e critérios de sucesso

### 6.1. Métricas de resultado

Fonte de dados para KPI-01 a KPI-06: saída de `src/evaluate.py` e feedback gravado no experimento do LangSmith. Prazo de avaliação: pendente (ver Q-010).

| ID | Indicador | Objetivo | Método de cálculo | Meta |
|---|---|---|---|---|
| KPI-01 | Helpfulness | OBJ-01 | Média, nos 15 exemplos, de (Clarity + Precision) / 2 por exemplo | >= 0.8 |
| KPI-02 | Correctness | OBJ-01 | Média, nos 15 exemplos, de (F1-Score + Precision) / 2 por exemplo | >= 0.8 |
| KPI-03 | F1-Score | OBJ-01 | Média nos 15 exemplos de 2·P·R / (P + R), com P e R atribuídos pelo LLM juiz | >= 0.8 |
| KPI-04 | Clarity | OBJ-01 | Média nos 15 exemplos da nota do LLM juiz (organização, linguagem direta, ausência de ambiguidade, concisão) | >= 0.8 |
| KPI-05 | Precision | OBJ-01 | Média nos 15 exemplos da nota do LLM juiz (sem alucinações, foco no pedido, correção em relação à referência) | >= 0.8 |
| KPI-06 | Média geral | OBJ-01 | Média aritmética de KPI-01 a KPI-05 | >= 0.8 |

### 6.2. Métricas operacionais

| ID | Indicador | Objetivo | Método de cálculo | Fonte | Meta |
|---|---|---|---|---|---|
| KPI-07 | Testes de validação estrutural aprovados | OBJ-03 | Testes aprovados / testes executados | Saída do `pytest` | 6 de 6 testes obrigatórios aprovados |
| KPI-08 | Iterações até a aprovação | OBJ-02 | Número de ciclos editar, publicar e avaliar até atingir OBJ-01 | Experimentos no LangSmith | Sem meta. O material indica que 3 a 5 iterações são esperadas, como referência e não como compromisso |
| KPI-09 | Completude das evidências | OBJ-04 | Itens de evidência presentes / itens exigidos (FR-036) | Link público e README | 100% dos itens exigidos |

## 7. Escopo do produto

| ID | Grupo funcional | Descrição | Necessidade atendida | Capacidades | Usuários | Prioridade | Dependências |
|---|---|---|---|---|---|---|---|
| G1 | Obtenção do prompt base | Trazer o prompt semente do Hub para o repositório | PB-01 (analisar o ponto de partida) | Validar configuração, obter o prompt, salvar localmente em YAML, informar falhas | P1 | Must Have | Conta e chave do LangSmith; prompt semente disponível |
| G2 | Prompt otimizado v2 | Manter a versão otimizada em arquivo versionado | PB-01 | Persona, instruções, regras, Few-shot, técnica adicional, edge cases, separação sistema e usuário, formato de saída, metadados | P1 | Must Have | G1 (análise do v1) |
| G3 | Publicação versionada | Publicar o v2 no Hub como público, com metadados | PB-02, PB-03 | Ler, validar, publicar com identificador versionado, informar resultado | P1 | Must Have | G2; handle público do Hub |
| G4 | Avaliação de qualidade | Medir o v2 publicado contra o dataset | PB-02 | Experimento por execução, 5 métricas por exemplo, status de aprovação, link do experimento | P1 | Must Have (existente, não implementar) | G3; chaves e modelos de LLM configurados |
| G5 | Validação estrutural automatizada | Verificar requisitos estruturais do v2 | PB-04 | 6 verificações obrigatórias executáveis por um comando | P1, P2 | Must Have | G2 |
| G6 | Documentação e evidências da entrega | Permitir ao avaliador verificar e reproduzir | PB-03 | README com seções obrigatórias, link público do dataset, screenshots, repositório público em fork | P1, P2 | Must Have | G4 com aprovação |

Todos os grupos são Must Have porque o material do desafio os define como entregáveis obrigatórios. Não há, nas fontes, funcionalidades opcionais que justifiquem Should Have ou Could Have, exceto as indicadas em 8.2.

## 8. MVP e não objetivos (Non-Goals)

### 8.1. MVP

O MVP corresponde à entrega completa do desafio: grupos G1 a G6, com os requisitos funcionais de prioridade Must Have.

O MVP deve permitir avaliar:
- se o v2 atinge OBJ-01 (KPI-01 a KPI-06);
- se o v2 atende aos requisitos estruturais (KPI-07);
- se a entrega é verificável por terceiros (KPI-09).

Requisitos mínimos de uso:
- credenciais do LangSmith e do provedor de LLM configuradas;
- handle público do Hub existente;
- modelos de resposta e de avaliação definidos.

### 8.2. Itens fora do MVP, permitidos pelas fontes

| Item | Classificação | Fundamento |
|---|---|---|
| Testes de validação adicionais aos 6 obrigatórios | Should Have | O material pede "no mínimo" 6 testes |
| Exibição do endereço do prompt publicado ao final do push | Should Have | A dica de implementação do esqueleto retorna esse endereço; o material pede verificar a publicação no dashboard |

### 8.3. Não objetivos

- Alterar o dataset, as métricas, o limite de aprovação, o script de avaliação ou as funções auxiliares para melhorar notas.
- Avaliar outros prompts além de `{handle}/bug_to_user_story_v2` (o script de avaliação existente avalia somente esse prompt).
- Fixar provedor ou modelo de LLM no código.
- Utilizar banco de dados.
- Gerar User Stories para uso operacional real. O produto mede a qualidade do prompt; não é uma ferramenta de produção para times de produto (P3 é beneficiário apenas indireto).

## 9. Requisitos funcionais

Prioridades conforme a seção 7. Ator "Sistema" designa as rotinas do produto.

### 9.1. G1: Obtenção do prompt base

**FR-001: Validar configuração antes da obtenção**
- Descrição: antes de contatar o Hub, o sistema verifica se as credenciais do LangSmith estão configuradas.
- Justificativa: evitar falhas sem diagnóstico (PB-02).
- Ator: P1 / Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-014.
- Critérios de aceitação:
  - com credencial ausente, o sistema lista as variáveis faltantes em português;
  - o sistema encerra com status de falha e não contata o Hub.
- Dependências: nenhuma.

**FR-002: Obter o prompt semente do Hub**
- Descrição: o sistema obtém o prompt `leonanluppi/bug_to_user_story_v1` do LangSmith Prompt Hub.
- Justificativa: PB-01.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-013, BR-015.
- Critérios de aceitação: com credenciais válidas, o sistema obtém as mensagens de sistema e de usuário do prompt semente.
- Dependências: FR-001.

**FR-003: Persistir o prompt base localmente**
- Descrição: o sistema salva o prompt obtido em `prompts/bug_to_user_story_v1.yml`, em YAML, contendo o prompt de sistema, o prompt de usuário e os metadados disponíveis.
- Justificativa: permitir análise local do ponto de partida.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma além do formato YAML (restrição R-03).
- Critérios de aceitação:
  - após a execução, o arquivo existe e é um YAML válido;
  - o arquivo contém os textos de sistema e de usuário iguais aos do prompt obtido.
- Dependências: FR-002.

**FR-004: Informar falha na obtenção**
- Descrição: se a obtenção falhar, o sistema informa o motivo em português e encerra com status de falha.
- Justificativa: diagnóstico para P1.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: com erro de rede, credencial inválida ou prompt inexistente, a mensagem descreve o erro e o status de saída indica falha.
- Dependências: FR-002.

### 9.2. G2: Prompt otimizado v2

**FR-005: Manter o prompt v2 em arquivo versionado com metadados**
- Descrição: o prompt otimizado existe em `prompts/bug_to_user_story_v2.yml`.
- Justificativa: PB-01, OBJ-03.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-008.
- Critérios de aceitação: o arquivo contém descrição, prompt de sistema, prompt de usuário, versão, tags e a lista de técnicas aplicadas.
- Dependências: nenhuma.

**FR-006: Definir persona no prompt de sistema**
- Descrição: o prompt de sistema define explicitamente o papel assumido pelo modelo (ex.: "Você é um Product Manager").
- Justificativa: requisito de Role Prompting e teste obrigatório.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: o prompt de sistema contém uma definição de persona verificável por FR-027.
- Dependências: FR-005.

**FR-007: Conter instruções claras e regras explícitas de comportamento**
- Descrição: o prompt de sistema descreve a tarefa de forma específica e lista regras explícitas do que o modelo deve e não deve fazer.
- Justificativa: corrigir instruções vagas do v1 (PB-01).
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: o prompt de sistema contém uma seção identificável de regras de comportamento.
- Dependências: FR-005.

**FR-008: Conter exemplos de entrada e saída (Few-shot)**
- Descrição: o prompt de sistema contém exemplos de relato de bug (entrada) e da User Story esperada (saída).
- Justificativa: técnica obrigatória (BR-008).
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-008.
- Critérios de aceitação: o prompt contém ao menos um par entrada e saída identificável. A quantidade mínima não está definida nas fontes; o material recomenda 2 a 3 exemplos (ver Q-012).
- Dependências: FR-005.

**FR-009: Aplicar ao menos uma técnica adicional**
- Descrição: além de Few-shot, o prompt aplica ao menos uma das técnicas: Chain of Thought, Tree of Thought, Skeleton of Thought, ReAct ou Role Prompting.
- Justificativa: BR-008.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-008.
- Critérios de aceitação:
  - a lista de técnicas aplicadas contém Few-shot e ao menos uma técnica da lista;
  - a aplicação da técnica é identificável no texto do prompt.
- Dependências: FR-005.

**FR-010: Tratar casos de borda**
- Descrição: o prompt instrui o comportamento esperado diante de relatos que fogem do caso típico.
- Justificativa: requisito do prompt otimizado.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: o prompt contém instruções explícitas para casos de borda. A lista mínima de casos de borda não está definida nas fontes (ver Q-013).
- Dependências: FR-005.

**FR-011: Separar prompt de sistema e prompt de usuário**
- Descrição: instruções, persona, regras e exemplos ficam no prompt de sistema. O relato de bug é recebido exclusivamente no prompt de usuário.
- Justificativa: corrigir a duplicação do v1 (PB-01).
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-009.
- Critérios de aceitação:
  - a variável de entrada aparece apenas no prompt de usuário;
  - o prompt de sistema não referencia a variável de entrada.
- Dependências: FR-005.

**FR-012: Exigir formato de saída de User Story**
- Descrição: o prompt exige que a saída siga o formato de User Story padrão ou Markdown.
- Justificativa: teste obrigatório; alinhamento com as respostas de referência do dataset.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-016.
- Critérios de aceitação: o prompt de sistema menciona explicitamente o formato de saída exigido. A escolha entre User Story padrão e Markdown está pendente (ver Q-006).
- Dependências: FR-005.

**FR-013: Não conter pendências de edição**
- Descrição: o prompt não contém marcadores de pendência.
- Justificativa: PB-04.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: o texto do prompt não contém `[TODO]`, nem a sequência `TODO` em maiúsculas no prompt de sistema.
- Dependências: FR-005.

**FR-014: Redigir o conteúdo do prompt em português**
- Descrição: o texto do prompt enviado ao LLM está em português.
- Justificativa: regra de idioma do projeto; o dataset está em português.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: instruções, regras e exemplos estão em português.
- Dependências: FR-005.

### 9.3. G3: Publicação versionada

**FR-015: Ler o prompt v2 local**
- Descrição: o sistema lê o prompt de `prompts/bug_to_user_story_v2.yml`.
- Justificativa: OBJ-02.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: com arquivo ausente ou YAML inválido, o sistema informa o erro em português e encerra com status de falha, sem publicar.
- Dependências: FR-005.

**FR-016: Validar o prompt antes de publicar**
- Descrição: o sistema valida a estrutura do prompt antes da publicação.
- Justificativa: PB-04.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-008.
- Critérios de aceitação:
  - prompt sem descrição, sem prompt de sistema, com prompt de sistema vazio, sem versão, com pendências ou com menos de 2 técnicas não é publicado;
  - todos os erros encontrados são listados.
- Dependências: FR-015.

**FR-017: Publicar com identificador versionado**
- Descrição: o sistema publica o prompt no Hub com o identificador `{handle}/bug_to_user_story_v2`.
- Justificativa: OBJ-02; pré-requisito da avaliação.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-005.
- Critérios de aceitação: após a publicação, o prompt é localizável no Hub por esse identificador.
- Dependências: FR-016.

**FR-018: Publicar como público**
- Descrição: o prompt publicado fica com visibilidade pública.
- Justificativa: PB-03.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-006.
- Critérios de aceitação: o prompt é acessível por usuário sem acesso ao workspace.
- Dependências: FR-017.

**FR-019: Registrar metadados na publicação**
- Descrição: a publicação inclui tags, descrição e técnicas utilizadas.
- Justificativa: requisito do desafio.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: tags, descrição e técnicas são visíveis no Hub para o prompt publicado. A forma de exibir as técnicas está pendente (ver Q-014).
- Dependências: FR-017.

**FR-020: Informar o resultado da publicação**
- Descrição: o sistema informa sucesso ou falha. Em caso de falha por handle inexistente, orienta a criar o handle tornando um prompt público na interface do LangSmith.
- Justificativa: diagnóstico para P1.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-005.
- Critérios de aceitação:
  - o status de saída indica sucesso ou falha;
  - a mensagem é em português.
- Dependências: FR-017.

### 9.4. G4: Avaliação de qualidade (existente)

Os requisitos FR-021 a FR-024 descrevem o comportamento já implementado em `src/evaluate.py`. Não devem ser implementados nem alterados (BR-003). Servem para verificação e rastreabilidade.

**FR-021: Avaliar o prompt publicado como experimento**
- Descrição: o sistema obtém do Hub o prompt `{handle}/bug_to_user_story_v2` e o executa contra os 15 exemplos do dataset de avaliação. Cada execução gera um experimento ligado ao dataset.
- Justificativa: PB-02.
- Ator: Sistema.
- Prioridade: Must Have (existente).
- Regras de negócio: BR-007, BR-012.
- Critérios de aceitação: cada execução cria um novo experimento com 15 execuções do prompt.
- Dependências: FR-017.

**FR-022: Calcular e registrar cinco métricas por exemplo**
- Descrição: para cada exemplo, o sistema calcula F1-Score, Clarity e Precision por LLM juiz, deriva Helpfulness e Correctness e grava as cinco notas como feedback no experimento.
- Justificativa: PB-02.
- Ator: Sistema.
- Prioridade: Must Have (existente).
- Regras de negócio: BR-002.
- Critérios de aceitação: cada exemplo do experimento tem as cinco notas, entre 0.0 e 1.0.
- Dependências: FR-021.

**FR-023: Determinar o status de aprovação**
- Descrição: o sistema exibe as médias das cinco métricas e a média geral, e indica APROVADO ou REPROVADO. Em caso de reprovação, lista as métricas abaixo do limite.
- Justificativa: OBJ-01.
- Ator: Sistema.
- Prioridade: Must Have (existente).
- Regras de negócio: BR-001.
- Critérios de aceitação: o status segue BR-001.
- Dependências: FR-022.

**FR-024: Exibir o endereço do experimento**
- Descrição: ao final, o sistema exibe o endereço do experimento no LangSmith.
- Justificativa: diagnóstico e comparação de iterações.
- Ator: Sistema.
- Prioridade: Must Have (existente).
- Regras de negócio: nenhuma.
- Critérios de aceitação: o endereço é exibido quando o experimento é criado.
- Dependências: FR-021.

### 9.5. G5: Validação estrutural automatizada

**FR-025: Executar a validação estrutural por um único comando**
- Descrição: as verificações estruturais do prompt v2 são executadas por um único comando de testes.
- Justificativa: PB-04, OBJ-03.
- Ator: P1, P2.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação:
  - o comando executa as 6 verificações FR-026 a FR-031;
  - o comando informa o resultado de cada uma.
- Dependências: FR-005.

**FR-026: Verificar a existência do prompt de sistema**
- Descrição: verifica que o prompt de sistema existe e não está vazio.
- Justificativa: teste obrigatório `test_prompt_has_system_prompt`.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: falha se o campo estiver ausente ou contiver apenas espaços.
- Dependências: FR-025.

**FR-027: Verificar a definição de persona**
- Descrição: verifica que o prompt define uma persona.
- Justificativa: teste obrigatório `test_prompt_has_role_definition`.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: falha se não houver definição de persona no prompt de sistema.
- Dependências: FR-025, FR-006.

**FR-028: Verificar a exigência de formato**
- Descrição: verifica que o prompt exige formato Markdown ou User Story padrão.
- Justificativa: teste obrigatório `test_prompt_mentions_format`.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: falha se o prompt não mencionar o formato exigido.
- Dependências: FR-025, FR-012.

**FR-029: Verificar a presença de exemplos Few-shot**
- Descrição: verifica que o prompt contém exemplos de entrada e saída.
- Justificativa: teste obrigatório `test_prompt_has_few_shot_examples`.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: falha se não houver exemplos de entrada e saída identificáveis.
- Dependências: FR-025, FR-008.

**FR-030: Verificar a ausência de pendências**
- Descrição: verifica que o prompt não contém `[TODO]`.
- Justificativa: teste obrigatório `test_prompt_no_todos`.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: falha se `[TODO]` estiver presente.
- Dependências: FR-025, FR-013.

**FR-031: Verificar o número mínimo de técnicas**
- Descrição: verifica, pelos metadados do YAML, que ao menos 2 técnicas foram listadas.
- Justificativa: teste obrigatório `test_minimum_techniques`.
- Ator: Sistema.
- Prioridade: Must Have.
- Regras de negócio: BR-008.
- Critérios de aceitação: falha se a lista de técnicas tiver menos de 2 itens.
- Dependências: FR-025.

### 9.6. G6: Documentação e evidências da entrega

**FR-032: Documentar as técnicas aplicadas**
- Descrição: o README contém a seção "Técnicas Aplicadas (Fase 2)".
- Justificativa: entregável obrigatório; necessidade de P2.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: a seção lista as técnicas escolhidas e, para cada uma, a justificativa e um exemplo prático de aplicação.
- Dependências: FR-009.

**FR-033: Documentar os resultados finais**
- Descrição: o README contém a seção "Resultados Finais".
- Justificativa: entregável obrigatório.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-011.
- Critérios de aceitação: a seção contém o link público do dataset de avaliação com os experimentos, screenshots com as notas maiores ou iguais a 0.8 e a comparação entre v1 e v2 (o que mudou e por quê).
- Dependências: FR-023, FR-035.

**FR-034: Documentar como executar**
- Descrição: o README contém a seção "Como Executar".
- Justificativa: necessidade de reprodução por P2.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: a seção contém pré-requisitos, dependências e os comandos de cada fase do projeto.
- Dependências: nenhuma.

**FR-035: Disponibilizar link público do dataset de avaliação**
- Descrição: um endereço público do dataset de avaliação, que expõe os experimentos executados contra ele, é gerado e registrado.
- Justificativa: PB-03.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-011.
- Critérios de aceitação: o endereço abre para um usuário sem acesso ao workspace.
- Dependências: FR-021.

**FR-036: Tornar visíveis as evidências exigidas**
- Descrição: pelo link público ou por screenshots, ficam visíveis: o dataset com 15 exemplos, as execuções do v2 com notas maiores ou iguais a 0.8 e o tracing detalhado de ao menos 3 exemplos.
- Justificativa: PB-03, OBJ-04.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: nenhuma.
- Critérios de aceitação: os três itens são verificáveis por P2.
- Dependências: FR-035.

**FR-037: Entregar em repositório público derivado do repositório base**
- Descrição: a entrega é um repositório público no GitHub, fork do repositório base.
- Justificativa: entregável obrigatório.
- Ator: P1.
- Prioridade: Must Have.
- Regras de negócio: BR-017.
- Critérios de aceitação: o repositório é público, é fork de `devfullcycle/mba-ia-pull-evaluation-prompt` e contém o código implementado, o v2 completo e o README atualizado.
- Dependências: G1 a G5.

## 10. Histórias de usuário

**US-001: Obter o prompt base**
- História: Como desenvolvedor do desafio, quero obter localmente o prompt v1 publicado no Hub, para analisar seus defeitos e usá-lo como ponto de partida da otimização.
- Necessidade: PB-01.
- Prioridade: Must Have.
- Requisitos: FR-001 a FR-004.
- Critérios de aceitação:
  - o arquivo do v1 é criado com o conteúdo do Hub;
  - falhas são informadas com status de falha.
- Dependências: credenciais do LangSmith.

**US-002: Manter um prompt otimizado versionado**
- História: Como desenvolvedor do desafio, quero manter o prompt v2 em arquivo com persona, regras, exemplos, técnica adicional e tratamento de casos de borda, para gerar User Stories de melhor qualidade que o v1.
- Necessidade: PB-01.
- Prioridade: Must Have.
- Requisitos: FR-005 a FR-014.
- Critérios de aceitação: o arquivo atende a FR-005 a FR-014 e passa nas verificações FR-026 a FR-031.
- Dependências: US-001.

**US-003: Validar o prompt antes de publicar**
- História: Como desenvolvedor do desafio, quero validar automaticamente a estrutura do prompt v2, para garantir que ele atende aos requisitos mínimos do desafio antes de publicá-lo.
- Necessidade: PB-04.
- Prioridade: Must Have.
- Requisitos: FR-025 a FR-031.
- Critérios de aceitação: um único comando executa as 6 verificações e indica o resultado de cada uma.
- Dependências: US-002.

**US-004: Publicar o prompt otimizado**
- História: Como desenvolvedor do desafio, quero publicar o v2 no Hub como público, com identificador versionado e metadados, para que ele possa ser avaliado e consultado.
- Necessidade: PB-02, PB-03.
- Prioridade: Must Have.
- Requisitos: FR-015 a FR-020.
- Critérios de aceitação:
  - prompt inválido não é publicado;
  - prompt válido fica público como `{handle}/bug_to_user_story_v2` com metadados.
- Dependências: US-002; handle do Hub.

**US-005: Medir a qualidade do prompt publicado**
- História: Como desenvolvedor do desafio, quero avaliar o v2 publicado com cinco métricas objetivas, para saber se ele atinge o critério de aprovação.
- Necessidade: PB-02.
- Prioridade: Must Have.
- Requisitos: FR-021 a FR-024.
- Critérios de aceitação: a execução exibe as cinco notas, a média e o status conforme BR-001.
- Dependências: US-004.

**US-006: Iterar até a aprovação**
- História: Como desenvolvedor do desafio, quero editar, republicar e reavaliar o v2 e comparar os experimentos, para atingir nota maior ou igual a 0.8 em todas as métricas.
- Necessidade: PB-02.
- Prioridade: Must Have.
- Requisitos: FR-005 a FR-024.
- Critérios de aceitação:
  - cada ciclo gera um novo experimento comparável no LangSmith;
  - o último ciclo atinge BR-001.
- Dependências: US-004, US-005.

**US-007: Verificar a entrega sem acesso ao workspace**
- História: Como avaliador do desafio, quero acessar um link público com o dataset, as execuções e os traces, para verificar as notas sem acesso ao workspace do desenvolvedor.
- Necessidade: PB-03.
- Prioridade: Must Have.
- Requisitos: FR-035, FR-036.
- Critérios de aceitação: o link abre sem autenticação no workspace e mostra os itens de FR-036.
- Dependências: US-006.

**US-008: Compreender e reproduzir a solução**
- História: Como avaliador do desafio, quero ler no README as técnicas aplicadas, os resultados e as instruções de execução, para avaliar a solução e reproduzi-la.
- Necessidade: PB-03.
- Prioridade: Must Have.
- Requisitos: FR-032 a FR-034, FR-037.
- Critérios de aceitação: o README contém as três seções obrigatórias com o conteúdo exigido, e o repositório atende a FR-037.
- Dependências: US-006, US-007.

## 11. Critérios de aceitação em Gherkin

```gherkin
# language: pt
Funcionalidade: Obtenção do prompt base (FR-001 a FR-004)

  Cenário: Obter o prompt semente com credenciais válidas
    Dado que as credenciais do LangSmith estão configuradas
    E o prompt "leonanluppi/bug_to_user_story_v1" está disponível no Hub
    Quando o desenvolvedor executa a obtenção do prompt base
    Então o arquivo "prompts/bug_to_user_story_v1.yml" é criado em YAML válido
    E o arquivo contém os textos de sistema e de usuário do prompt obtido
    E a execução termina com status de sucesso

  Cenário: Credencial ausente
    Dado que a chave de API do LangSmith não está configurada
    Quando o desenvolvedor executa a obtenção do prompt base
    Então o sistema lista em português as variáveis faltantes
    E o Hub não é contatado
    E a execução termina com status de falha

  Cenário: Falha ao contatar o Hub
    Dado que as credenciais estão configuradas
    E o Hub não responde ou recusa a requisição
    Quando o desenvolvedor executa a obtenção do prompt base
    Então o sistema informa o motivo da falha em português
    E a execução termina com status de falha
```

```gherkin
# language: pt
Funcionalidade: Validação estrutural do prompt v2 (FR-025 a FR-031)

  Cenário: Prompt v2 conforme
    Dado que o prompt v2 possui prompt de sistema não vazio
    E define uma persona
    E exige formato de User Story padrão ou Markdown
    E contém exemplos de entrada e saída
    E não contém "[TODO]"
    E lista ao menos 2 técnicas nos metadados
    Quando o desenvolvedor executa a validação estrutural
    Então as 6 verificações são aprovadas

  Cenário: Prompt v2 com uma única técnica listada
    Dado que os metadados do prompt v2 listam apenas 1 técnica
    Quando o desenvolvedor executa a validação estrutural
    Então a verificação de número mínimo de técnicas falha
    E o resultado indica qual verificação falhou

  Cenário: Prompt v2 com pendência esquecida
    Dado que o prompt v2 contém o marcador "[TODO]"
    Quando o desenvolvedor executa a validação estrutural
    Então a verificação de ausência de pendências falha
```

```gherkin
# language: pt
Funcionalidade: Publicação do prompt v2 (FR-015 a FR-020)

  Cenário: Publicar prompt válido
    Dado que o prompt v2 local é válido
    E o handle público do Hub existe e está configurado
    Quando o desenvolvedor executa a publicação
    Então o prompt fica disponível no Hub como "{handle}/bug_to_user_story_v2"
    E o prompt é público
    E tags, descrição e técnicas utilizadas ficam registradas
    E a execução termina com status de sucesso

  Cenário: Bloquear publicação de prompt inválido
    Dado que o prompt v2 local não possui o campo de versão
    E lista menos de 2 técnicas
    Quando o desenvolvedor executa a publicação
    Então nenhum prompt é publicado
    E todos os erros de validação são listados em português
    E a execução termina com status de falha

  Cenário: Handle do Hub inexistente
    Dado que o prompt v2 local é válido
    E o handle configurado não existe no Hub
    Quando o desenvolvedor executa a publicação
    Então a publicação falha
    E o sistema orienta a criar o handle tornando um prompt público na interface do LangSmith

  Cenário: Arquivo do prompt v2 ausente
    Dado que o arquivo "prompts/bug_to_user_story_v2.yml" não existe
    Quando o desenvolvedor executa a publicação
    Então o sistema informa que o arquivo não foi encontrado
    E nenhum prompt é publicado
```

```gherkin
# language: pt
Funcionalidade: Avaliação do prompt publicado (FR-021 a FR-024, BR-001)

  Cenário: Aprovação com todas as métricas no limite ou acima
    Dado que o prompt v2 foi publicado
    E as médias obtidas são Helpfulness 0.85, Correctness 0.80, F1-Score 0.80, Clarity 0.90 e Precision 0.80
    Quando o desenvolvedor executa a avaliação
    Então o status exibido é "APROVADO"

  Cenário: Reprovação com média alta e uma métrica abaixo do limite
    Dado que o prompt v2 foi publicado
    E as médias obtidas são Helpfulness 0.95, Correctness 0.87, F1-Score 0.79, Clarity 0.95 e Precision 0.95
    Quando o desenvolvedor executa a avaliação
    Então o status exibido é "REPROVADO"
    E a métrica "f1_score" é listada como abaixo de 0.8

  Cenário: Alteração local não publicada
    Dado que o desenvolvedor alterou o prompt v2 local
    E não executou a publicação após a alteração
    Quando o desenvolvedor executa a avaliação
    Então a versão avaliada é a última publicada no Hub, e não a alteração local

  Cenário: Prompt v2 ainda não publicado
    Dado que não existe "{handle}/bug_to_user_story_v2" no Hub
    Quando o desenvolvedor executa a avaliação
    Então o sistema informa que o prompt não foi encontrado
    E orienta a executar a publicação
```

```gherkin
# language: pt
Funcionalidade: Evidências públicas da entrega (FR-035, FR-036)

  Cenário: Avaliador acessa as evidências
    Dado que o link público do dataset de avaliação foi gerado e registrado no README
    E o avaliador não tem acesso ao workspace do desenvolvedor
    Quando o avaliador abre o link
    Então o dataset de avaliação com 15 exemplos é exibido
    E as execuções do prompt v2 com notas maiores ou iguais a 0.8 são visíveis
    E o tracing de ao menos 3 exemplos pode ser inspecionado
```

## 12. Requisitos não funcionais

| ID | Categoria | Requisito | Critério de avaliação | Origem |
|---|---|---|---|---|
| NFR-001 | Reprodutibilidade | A geração e a avaliação são executadas com temperatura 0, e os modelos escolhidos devem aceitar esse valor | Execução da avaliação sem erro de parâmetro de temperatura | Confirmado (`.env.example`; existente no código) |
| NFR-002 | Configurabilidade | Provedor (Google ou OpenAI), modelo de resposta e modelo de avaliação são configuráveis sem alteração de código | Trocar o provedor ou o modelo exige apenas alterar a configuração de ambiente | Confirmado |
| NFR-003 | Segurança de credenciais | Credenciais ficam apenas na configuração de ambiente local, não são versionadas e não aparecem no README, nos screenshots ou na saída das rotinas | Inspeção do repositório e das evidências sem ocorrência de chaves | Confirmado (`CLAUDE.md`) |
| NFR-004 | Segurança de conteúdo de terceiros | A obtenção de prompts de terceiros identificados por `owner/nome` é autorizada explicitamente apenas para o prompt semente do desafio, de origem conhecida | Nenhum outro prompt de terceiros é obtido pelo produto | Confirmado |
| NFR-005 | Compatibilidade | O produto executa em Python 3.10 ou superior | Execução bem-sucedida em Python 3.10+ | Confirmado no documento de contexto; divergência com o README base (Q-003) |
| NFR-006 | Operação sob limites de cota | A avaliação opera dentro de limites baixos de requisições por minuto de planos gratuitos, executando os exemplos sequencialmente. Cada exemplo consome 4 chamadas ao LLM (1 de geração e 3 de julgamento); cada avaliação completa, 60 chamadas | Avaliação completa sem erros de limite de requisições. Os limites vigentes do provedor não estão definidos (Q-004) | Existente (código); valores de cota pendentes |
| NFR-007 | Observabilidade | Cada execução da avaliação é rastreável no LangSmith, com trace por exemplo e as cinco notas registradas como feedback | Experimento exibe 15 execuções com traces e feedback | Confirmado / existente |
| NFR-008 | Testabilidade | A validação estrutural executa sem acesso a rede e sem consumo de LLM | Testes executam com a rede desabilitada | Confirmado (`CLAUDE.md`) |
| NFR-009 | Manutenibilidade | O código é legível, limpo e simples, segundo o Zen do Python | Revisão de código | Confirmado (`CLAUDE.md`) |
| NFR-010 | Usabilidade e idioma | Mensagens ao usuário e erros exibidos em português; identificadores, comentários e logs em inglês | Inspeção das mensagens e do código | Confirmado (`CLAUDE.md`) |
| NFR-011 | Reprodutibilidade da entrega | As rotinas são executadas a partir da raiz do repositório, com os comandos documentados no README | Um terceiro reproduz o fluxo seguindo apenas o README | Confirmado |

Tempo de execução máximo das rotinas: não há fundamento nas fontes para definir meta. Não foi especificado.

## 13. Regras de negócio

| ID | Nome | Descrição | Condição | Resultado | Requisitos |
|---|---|---|---|---|---|
| BR-001 | Critério de aprovação | A aprovação exige cada uma das cinco métricas maior ou igual a 0.8 e a média das cinco maior ou igual a 0.8 | Ao final de cada avaliação | APROVADO somente se ambas as condições forem atendidas; caso contrário, REPROVADO | FR-023 |
| BR-002 | Métricas derivadas | Helpfulness = (Clarity + Precision) / 2; Correctness = (F1-Score + Precision) / 2, calculadas por exemplo | A cada exemplo avaliado | Precision influencia as duas métricas derivadas | FR-022 |
| BR-003 | Imutabilidade dos instrumentos de avaliação | Dataset, métricas, limite de aprovação, script de avaliação e funções auxiliares não podem ser alterados | Sempre | Melhorias de nota só podem vir do prompt | FR-021 a FR-024 |
| BR-004 | Objeto da otimização | Somente o prompt v2 pode ser alterado para melhorar as notas | Durante as iterações | Alterações em outros artefatos não contam como otimização | FR-005 a FR-014 |
| BR-005 | Identificação do prompt publicado | O identificador é `{handle}/bug_to_user_story_v2`. O handle é criado ao tornar um prompt público pela primeira vez na interface do LangSmith e é definitivo após confirmado | Antes da primeira publicação | Sem handle, a publicação não é possível | FR-017, FR-020 |
| BR-006 | Visibilidade pública | O prompt v2 publicado deve ser público | Na publicação | Prompt acessível a terceiros | FR-018 |
| BR-007 | Fonte da avaliação | A avaliação usa a versão publicada no Hub, não o arquivo local | A cada avaliação | Alterações locais só são avaliadas após nova publicação | FR-021 |
| BR-008 | Técnicas obrigatórias | Few-shot é obrigatório, mais ao menos uma técnica entre CoT, Tree of Thought, Skeleton of Thought, ReAct e Role Prompting. Os metadados devem listar ao menos 2 técnicas | Na criação e na validação do v2 | Prompt fora da regra é rejeitado pela validação | FR-008, FR-009, FR-016, FR-031 |
| BR-009 | Variável de entrada | A única entrada do prompt é o relato de bug, recebido no prompt de usuário | Na definição do v2 | O relato não aparece duplicado no prompt de sistema | FR-011 |
| BR-010 | Escolha de modelos | Os modelos não são fixados pelo desafio; devem ser escolhidos pela documentação oficial vigente do provedor. O modelo de avaliação pode ser o mesmo ou um mais capaz | Na configuração | Escolha registrada na configuração de ambiente | NFR-002 |
| BR-011 | Link público de evidências | O link público é obtido compartilhando o dataset de avaliação, o que expõe os experimentos. Um novo compartilhamento muda o link | Ao gerar evidências | O link deve ser gerado uma vez e registrado | FR-033, FR-035 |
| BR-012 | Dataset de avaliação | O dataset de avaliação no LangSmith é nomeado `{LANGSMITH_PROJECT}-eval` e é criado a partir dos 15 exemplos locais, ou reutilizado se já existir | Na avaliação | O nome do projeto de tracing não pode ficar vazio | FR-021 |
| BR-013 | Prompt semente | O prompt de origem é `leonanluppi/bug_to_user_story_v1` | Na obtenção | Nenhum outro prompt de origem é usado | FR-002 |
| BR-014 | Pré-condição de configuração | Rotinas que acessam serviços externos exigem credenciais configuradas | Antes de acessar serviços externos | Execução interrompida com lista de variáveis faltantes | FR-001 |
| BR-015 | Autorização explícita para prompt de terceiros | A obtenção de prompt identificado por `owner/nome` exige autorização explícita, por se tratar de objeto serializado de terceiros | Na obtenção do prompt semente | Obtenção autorizada apenas para o prompt semente | FR-002, NFR-004 |
| BR-016 | Formato da User Story | A saída esperada segue o padrão das referências do dataset: frase "Como um ..., eu quero ..., para que ..." seguida de "Critérios de Aceitação" no formato Dado / Quando / Então / E. Relatos médios e complexos incluem seções adicionais de contexto técnico e tarefas | Na definição do formato de saída do v2 | Saída comparável às referências pelo LLM juiz | FR-012 |
| BR-017 | Forma de entrega | A entrega é um repositório público no GitHub que seja fork do repositório base | Na entrega | Repositório fora dessa forma não atende ao entregável | FR-037 |

BR-016 descreve o formato observado nas respostas de referência do dataset (fato). Que o v2 deva reproduzi-lo integralmente é uma premissa (PR-03): é o meio esperado de maximizar F1-Score e Precision, mas não está escrito como regra no material do desafio.

## 14. Fluxos principais de utilização

**FL-01: Preparação do ambiente**
- Objetivo: deixar o ambiente apto a executar as rotinas.
- Condições iniciais: repositório fork clonado; conta no LangSmith; chave do provedor de LLM.
- Etapas:
  1. Criar o handle público no LangSmith, tornando um prompt público na interface.
  2. Configurar o ambiente a partir do modelo de variáveis (credenciais, projeto, handle, provedor, modelos).
  3. Criar o ambiente virtual e instalar as dependências.
- Resultado: rotinas executáveis.
- Exceções: modelo que não aceita temperatura 0 (NFR-001).
- Requisitos: BR-005, BR-010, NFR-001, NFR-002, NFR-005.

**FL-02: Obtenção do prompt base**
- Objetivo: ter o v1 localmente.
- Condições iniciais: FL-01 concluído.
- Etapas: executar a obtenção e analisar o arquivo gerado.
- Resultado: `prompts/bug_to_user_story_v1.yml` criado.
- Exceções: credenciais ausentes ou falha no Hub.
- Requisitos: FR-001 a FR-004.

**FL-03: Otimização e validação local**
- Objetivo: produzir um v2 estruturalmente válido.
- Condições iniciais: FL-02 concluído.
- Etapas:
  1. Editar o v2.
  2. Executar a validação estrutural.
  3. Corrigir as falhas.
- Resultado: 6 verificações aprovadas.
- Exceções: verificações reprovadas retornam à etapa de edição.
- Requisitos: FR-005 a FR-014, FR-025 a FR-031.

**FL-04: Publicação**
- Objetivo: disponibilizar o v2 no Hub.
- Condições iniciais: FL-03 concluído; handle existente.
- Etapas: executar a publicação e verificar o prompt no Hub.
- Resultado: prompt público com metadados.
- Exceções: validação reprovada; handle inexistente.
- Requisitos: FR-015 a FR-020.

**FL-05: Avaliação e iteração**
- Objetivo: atingir BR-001.
- Condições iniciais: FL-04 concluído.
- Etapas:
  1. Executar a avaliação.
  2. Se REPROVADO, analisar as métricas baixas e os traces por exemplo.
  3. Retornar a FL-03 e FL-04.
  4. Repetir até APROVADO.
- Resultado: experimento aprovado.
- Exceções:
  - limite de requisições do provedor;
  - falha de chamada ao LLM juiz, que resulta em nota 0.0 no exemplo e reduz a média (RK-02).
- Requisitos: FR-021 a FR-024, BR-001, BR-007.

**FL-06: Geração de evidências e entrega**
- Objetivo: permitir a verificação por P2.
- Condições iniciais: FL-05 aprovado.
- Etapas:
  1. Gerar uma única vez o link público do dataset.
  2. Capturar os screenshots.
  3. Escrever as seções do README.
  4. Publicar o repositório.
- Resultado: entrega verificável.
- Exceções: novo compartilhamento muda o link (BR-011).
- Dependência pendente: local dos screenshots (Q-007).
- Requisitos: FR-032 a FR-037.

## 15. Dependências, restrições e premissas

### 15.1. Dependências

| ID | Dependência |
|---|---|
| D-01 | Conta no LangSmith com chave de API e acesso ao Prompt Hub, a datasets e a experimentos |
| D-02 | Handle público do LangSmith Hub |
| D-03 | Disponibilidade pública do prompt semente `leonanluppi/bug_to_user_story_v1` |
| D-04 | Chave de API do provedor de LLM (Google Gemini ou OpenAI) e modelos disponíveis |
| D-05 | Repositório base `devfullcycle/mba-ia-pull-evaluation-prompt` com os componentes prontos |
| D-06 | Acesso à internet para obtenção, publicação e avaliação |

### 15.2. Restrições

| ID | Restrição |
|---|---|
| R-01 | Linguagem Python 3.10+ |
| R-02 | Framework LangChain; plataforma de avaliação e gestão de prompts LangSmith |
| R-03 | Formato de prompts em YAML |
| R-04 | Estrutura obrigatória de diretórios e arquivos do desafio |
| R-05 | Componentes prontos e dataset não podem ser alterados (BR-003) |
| R-06 | Entrega como fork público (BR-017) |
| R-07 | Regras de idioma do `CLAUDE.md` |
| R-08 | Processo de versionamento: commits só com autorização explícita, Conventional Commits em português e uma branch por fase |

### 15.3. Premissas

| ID | Premissa |
|---|---|
| PR-01 | O prompt semente permanecerá disponível no Hub durante o desenvolvimento |
| PR-02 | A cota do provedor escolhido é suficiente para as iterações necessárias (3 a 5 esperadas, cerca de 60 chamadas por avaliação) |
| PR-03 | Reproduzir no v2 o formato das referências do dataset (BR-016) contribui para atingir as metas de F1-Score e Precision |
| PR-04 | Uma única execução de avaliação com status APROVADO é suficiente para a entrega (ver Q-010) |

### 15.4. Riscos e mitigações

| ID | Risco | Mitigação |
|---|---|---|
| RK-01 | Limite de requisições ou cota do plano gratuito interrompe a avaliação | Avaliação sequencial (existente); escolher modelo e plano com cota compatível; espaçar as execuções |
| RK-02 | Falha de chamada ou de interpretação do LLM juiz gera nota 0.0 no exemplo e derruba a média | Inspecionar o feedback e os traces por exemplo antes de alterar o prompt; repetir a avaliação quando a falha for de infraestrutura |
| RK-03 | Variação das notas entre execuções por julgamento de LLM | Temperatura 0 (NFR-001); registrar as notas de cada iteração; ver Q-010 |
| RK-04 | Modelo escolhido descontinuado ou sem suporte a temperatura 0 | Escolher pela documentação oficial vigente (BR-010) |
| RK-05 | Ajuste excessivo do prompt ao dataset (exemplos copiados das referências) | Usar exemplos Few-shot próprios, não retirados do dataset |
| RK-06 | Escolha definitiva de um handle inadequado | Escolher o handle com cuidado antes de confirmar (BR-005) |
| RK-07 | Repositório atual do desenvolvedor fora do formato de entrega (não é fork e está vazio) | Criar fork do repositório base (Q-001) |
| RK-08 | Link público alterado por novo compartilhamento após registro no README | Gerar uma única vez e registrar (BR-011) |

## 16. Fora do escopo

| Item | Motivo | Relação com versões futuras |
|---|---|---|
| Alteração do dataset, das métricas, do limite ou do script de avaliação | Proibido pelo desafio (BR-003) | Nenhuma prevista |
| Avaliação automatizada do v1 ou de outros prompts | O script existente avalia somente o v2 e não pode ser alterado | Pendente de decisão (Q-005) |
| Métricas adicionais existentes no módulo de métricas e não utilizadas pela avaliação (Tone, Acceptance Criteria, User Story Format, Completeness) | Não fazem parte do critério de aprovação | Não prevista nas fontes |
| Fixação de provedor ou modelo no código | Proibido (BR-010, NFR-002) | Nenhuma |
| Banco de dados | Não utilizado no projeto | Nenhuma |
| Uso operacional das User Stories geradas por times de produto | O produto mede a qualidade do prompt; não é ferramenta de produção | Não prevista |

## 17. Questões em aberto e decisões pendentes

| ID | Questão | Motivo | Impacto | Afeta | Próxima ação |
|---|---|---|---|---|---|
| Q-001 | O repositório `fonsecamrs/mba-prompt-evaluator-challenge-2` está vazio e não é fork do repositório base. Qual repositório será usado na entrega? | Contradição entre o repositório criado e o entregável exigido | Entrega não conforme se mantido | FR-037, BR-017 | Criar fork do repositório base e decidir o nome |
| Q-002 | O `CLAUDE.md` define documentação em `docs/` em inglês; este PRD foi solicitado em português do Brasil | Contradição entre fontes | Inconsistência de idioma na documentação | Este PRD, NFR-010, R-07 | Decidir se o PRD é exceção ou se o `CLAUDE.md` deve ser atualizado |
| Q-003 | Versão mínima do Python: 3.10+ (documento de contexto) ou 3.9+ (README do repositório base) | Contradição entre fontes | Compatibilidade do ambiente | NFR-005, R-01 | Confirmar 3.10+, adotado provisoriamente |
| Q-004 | Provedor de LLM, modelo de resposta, modelo de avaliação e limites de cota vigentes | Não definidos; o desafio exige consulta à documentação oficial | Custo, cota, duração e notas obtidas | NFR-001, NFR-006, BR-010 | Consultar a documentação do provedor e registrar a decisão em ADR |
| Q-005 | A comparação v1 x v2 no README exige notas medidas do v1? | O material pede "o que mudou e por quê"; as notas do v1 no material são ilustrativas, e o script de avaliação não avalia o v1 | Conteúdo da seção Resultados Finais | FR-033 | Confirmar com o critério de correção do desafio |
| Q-006 | O formato exigido é "User Story padrão" ou "Markdown"? O teste aceita qualquer um; as referências do dataset usam texto com seções, sem cabeçalhos Markdown | Ambiguidade | Notas de F1-Score e Precision; critério de FR-028 | FR-012, FR-028, BR-016 | Definir na spec do prompt e validar com a primeira avaliação |
| Q-007 | Local de armazenamento dos screenshots no repositório | Não definido | Organização da entrega | FR-033, FL-06 | Decidir antes de FL-06 |
| Q-008 | Padrão de nome das branches por fase | Não definido no `CLAUDE.md` | Processo de versionamento | R-08 | Definir com o desenvolvedor |
| Q-009 | Prazo de entrega do desafio | Ausente nas fontes | Planejamento das iterações | KPI-08 | Consultar o calendário do MBA |
| Q-010 | A aprovação precisa ser estável em execuções repetidas, ou basta uma execução aprovada? | Notas de LLM juiz podem variar entre execuções | Critério de conclusão do MVP | BR-001, PR-04, RK-03 | Confirmar com o critério de correção |
| Q-011 | Responsável pelo produto e aprovação formal deste PRD | Ausente nas fontes | Governança do documento | Seção 1, seção 18 | Indicar o responsável e o aprovador |
| Q-012 | Quantidade mínima de exemplos Few-shot | O material recomenda 2 a 3 exemplos, mas não exige quantidade | Critério de FR-008 e FR-029 | FR-008, FR-029 | Definir na spec do prompt |
| Q-013 | Lista mínima de casos de borda que o prompt deve tratar | O requisito existe, mas os casos não são enumerados nas fontes | Verificabilidade de FR-010 | FR-010 | Definir na spec do prompt |
| Q-014 | Forma de exibir as técnicas utilizadas nos metadados do Hub (tags, descrição ou outro campo) | O requisito existe, mas o meio não é definido | Verificabilidade de FR-019 | FR-019 | Definir na spec de publicação |

## 18. Evolução do produto e versionamento do PRD

Diretrizes:
- Atualizar este documento quando houver mudança relevante em requisitos, escopo, objetivos ou critérios de sucesso.
- Registrar toda alteração significativa no histórico abaixo, com justificativa.
- Ao alterar um requisito, atualizar na mesma revisão as histórias, regras, critérios de aceitação e a matriz de rastreabilidade relacionados.
- Não reutilizar identificadores removidos; marcar requisitos descontinuados como "Removido" em vez de apagá-los.
- Revisar as métricas de sucesso apenas com justificativa registrada.
- Registrar como nova versão qualquer decisão que altere o MVP.
- Ao resolver uma questão da seção 17, registrar a decisão e atualizar os requisitos afetados.

### 18.1. Histórico de versões

| Data | Versão | Alteração | Justificativa |
|---|---|---|---|
| 2026-10-13 | 0.1 | Criação do documento | Consolidação inicial dos requisitos do desafio, do `CLAUDE.md` e do repositório base. Sem aprovação formal |

## 19. Matriz de rastreabilidade

### 19.1. Objetivos, problemas e indicadores

| Objetivo | Problemas | Indicadores | Grupos |
|---|---|---|---|
| OBJ-01 | PB-01, PB-02 | KPI-01 a KPI-06, KPI-08 | G2, G3, G4 |
| OBJ-02 | PB-02 | KPI-08 | G1, G3, G4 |
| OBJ-03 | PB-04 | KPI-07 | G2, G5 |
| OBJ-04 | PB-03 | KPI-09 | G6 |

### 19.2. Requisitos, histórias e critérios

| Grupo | Requisitos funcionais | Histórias | Regras de negócio | Requisitos não funcionais | Critérios Gherkin |
|---|---|---|---|---|---|
| G1 | FR-001 a FR-004 | US-001 | BR-013, BR-014, BR-015 | NFR-003, NFR-004, NFR-010 | Obtenção do prompt base |
| G2 | FR-005 a FR-014 | US-002, US-006 | BR-004, BR-008, BR-009, BR-016 | NFR-010 | Validação estrutural |
| G3 | FR-015 a FR-020 | US-004, US-006 | BR-005, BR-006, BR-008 | NFR-003, NFR-010 | Publicação do prompt v2 |
| G4 | FR-021 a FR-024 | US-005, US-006 | BR-001, BR-002, BR-003, BR-007, BR-010, BR-012 | NFR-001, NFR-002, NFR-006, NFR-007 | Avaliação do prompt publicado |
| G5 | FR-025 a FR-031 | US-003 | BR-008 | NFR-008 | Validação estrutural |
| G6 | FR-032 a FR-037 | US-007, US-008 | BR-011, BR-017 | NFR-003, NFR-011 | Evidências públicas da entrega |

### 19.3. Requisitos sem justificativa clara

Nenhum requisito funcional foi identificado sem problema ou objetivo associado. Seguem como requisitos de processo, sem objetivo de produto associado:
- NFR-005: restrição técnica do desafio;
- NFR-009: padrão de qualidade de código.
