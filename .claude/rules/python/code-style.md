---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Estilo de código Python

- Seguir o Zen do Python (PEP 20): explícito, simples, legível, sem abstrações desnecessárias.
- Funções pequenas com uma responsabilidade. Manter type hints nas assinaturas, como no esqueleto.
- Identificadores, comentários e docstrings novos em inglês. Comentar o porquê, não o óbvio.
- Saída de CLI e mensagens de erro ao usuário em português; mensagens de `logging` em inglês.
- Scripts mantêm o padrão do esqueleto: `main()` retorna `0` (sucesso) ou `1` (falha) e o módulo termina com
  `sys.exit(main())`.
- Validar variáveis de ambiente no início com `check_env_vars` e encerrar com código `1` se faltar alguma.
- Capturar exceções específicas quando possível; nunca silenciar erro sem mensagem.
- Segredos só via `.env` (`python-dotenv`). Nunca imprimir valores de chaves de API.
- Caminhos de arquivo relativos à raiz do repositório (os scripts são executados a partir dela).