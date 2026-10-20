"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from langsmith.utils import (
    LangSmithConflictError,
    LangSmithConnectionError,
    LangSmithError,
    LangSmithUserError,
)
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

PROMPT_PATH = "prompts/bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"
INPUT_VARIABLE = "{bug_report}"

HANDLE_HELP = (
    "Confira se USERNAME_LANGSMITH_HUB no .env é o seu handle público do Hub.\n"
    "Se você ainda não tem um handle, crie-o no LangSmith:\n"
    "  Prompts > três pontinhos ao lado de Playground > Make Public > Choose your public handle"
)


def build_tags(prompt_data: dict) -> list[str]:
    """Return the YAML tags followed by the applied techniques, without duplicates."""
    tags = prompt_data.get("tags", []) + prompt_data.get("techniques_applied", [])
    return list(dict.fromkeys(tags))


def build_description(prompt_data: dict) -> str:
    techniques = ", ".join(prompt_data["techniques_applied"])
    return f"{prompt_data['description'].rstrip('.')}. Técnicas: {techniques}."


def build_readme(prompt_data: dict) -> str:
    """Return the Markdown shown on the public Hub page of the prompt."""
    techniques = "\n".join(f"- {technique}" for technique in prompt_data["techniques_applied"])
    return (
        f"# {PROMPT_KEY}\n\n"
        f"{prompt_data['description'].rstrip('.')}.\n\n"
        f"## Técnicas aplicadas\n\n{techniques}\n\n"
        f"## Entrada\n\nVariável `{INPUT_VARIABLE}`: o relato de bug, recebido na mensagem do usuário.\n\n"
        f"Versão: {prompt_data['version']}"
    )


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]),
        ("user", prompt_data["user_prompt"]),
    ])

    print(f"Publicando prompt no LangSmith Hub: {prompt_name}")
    try:
        url = Client().push_prompt(
            prompt_name,
            object=prompt,
            is_public=True,
            description=build_description(prompt_data),
            readme=build_readme(prompt_data),
            tags=build_tags(prompt_data),
        )
    # Raised before publishing when there is no handle or it belongs to another account.
    except (LangSmithUserError, ValueError) as e:
        print(f"❌ Não foi possível publicar com o handle informado: {e}")
        print(HANDLE_HELP)
        return False
    except LangSmithConflictError as e:
        print(f"❌ O Hub recusou o commit por conflito: {e}")
        print("Se o arquivo local não mudou desde o último push, não há nada novo para publicar.")
        return False
    except LangSmithConnectionError as e:
        print(f"❌ Não foi possível conectar ao LangSmith: {e}")
        return False
    except LangSmithError as e:
        print(f"❌ Erro ao publicar no LangSmith: {e}")
        print("Verifique se LANGSMITH_API_KEY no .env é uma chave válida.")
        return False

    print("✓ Prompt publicado como público")
    print(f"   {url}")
    return True


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    _, errors = validate_prompt_structure(prompt_data)

    # The evaluation feeds each bug report through this variable (BR-009).
    if INPUT_VARIABLE not in (prompt_data.get("user_prompt") or ""):
        errors.append(f"user_prompt precisa conter a variável {INPUT_VARIABLE}")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    data = load_yaml(PROMPT_PATH)
    if data is None:
        return 1

    prompt_data = data.get(PROMPT_KEY) if isinstance(data, dict) else None
    if not prompt_data:
        print(f"❌ Chave raiz '{PROMPT_KEY}' não encontrada em {PROMPT_PATH}")
        return 1

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ O prompt não passou na validação e não foi publicado:")
        for error in errors:
            print(f"   - {error}")
        return 1
    print("✓ Prompt validado")

    prompt_name = f"{os.getenv('USERNAME_LANGSMITH_HUB')}/{PROMPT_KEY}"
    return 0 if push_prompt_to_langsmith(prompt_name, prompt_data) else 1


if __name__ == "__main__":
    sys.exit(main())
