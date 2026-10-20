"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml

DICAS DE IMPLEMENTAÇÃO:

- O pull é feito pelo cliente do LangSmith:

      from langsmith import Client
      client = Client()
      prompt = client.pull_prompt(
          "leonanluppi/bug_to_user_story_v1",
          dangerously_pull_public_prompt=True,
      )

- O parâmetro `dangerously_pull_public_prompt=True` é obrigatório sempre que o
  identificador tem dono explícito ("owner/nome"). O LangSmith bloqueia esse pull
  por padrão porque um prompt do Hub é um objeto LangChain serializado, que pode
  vir de terceiros. Aqui o prompt é o do desafio, então o risco é conhecido.

- O retorno é um ChatPromptTemplate. Para extrair o conteúdo das mensagens,
  use a serialização nativa do LangChain (`prompt.messages`, e o atributo
  `.prompt.template` de cada mensagem).

- Use `save_yaml` de utils.py para gravar o resultado no arquivo .yml.
"""

import os
import sys
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langsmith import Client
from langsmith.schemas import Prompt
from langsmith.utils import LangSmithConnectionError, LangSmithError, LangSmithNotFoundError
from utils import load_yaml, save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_IDENTIFIER = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = Path("prompts/bug_to_user_story_v1.yml")
ROOT_KEY = "bug_to_user_story_v1"

MESSAGE_ROLES = {
    SystemMessagePromptTemplate: "system",
    HumanMessagePromptTemplate: "user",
}


def extract_messages(prompt: ChatPromptTemplate) -> dict[str, str]:
    """Return the system and user templates of the pulled prompt, keyed by role."""
    messages = {}
    for message in prompt.messages:
        role = MESSAGE_ROLES.get(type(message))
        if role:
            messages[role] = message.prompt.template

    missing = {"system", "user"} - messages.keys()
    if missing:
        raise ValueError(f"O prompt não tem mensagem do tipo: {', '.join(sorted(missing))}")
    return messages


def load_current_metadata() -> dict[str, Any]:
    """Return the metadata of the existing v1 file, used when the Hub has none."""
    if not OUTPUT_PATH.exists():
        return {}
    data = load_yaml(str(OUTPUT_PATH)) or {}
    return data.get(ROOT_KEY, {})


def build_prompt_data(messages: dict[str, str], hub_prompt: Prompt, current: dict[str, Any]) -> dict[str, Any]:
    """Build the YAML content: texts always from the Hub, metadata from the Hub when it has any."""
    # The Hub tags each prompt with its object type, which says nothing about the content.
    hub_tags = [tag for tag in hub_prompt.tags if tag != ChatPromptTemplate.__name__]

    data = {
        "description": hub_prompt.description or current.get("description", ""),
        "system_prompt": messages["system"],
        "user_prompt": messages["user"],
        "version": "v1",
    }
    if "created_at" in current:
        data["created_at"] = current["created_at"]
    data["tags"] = hub_tags or current.get("tags", [])
    return data


def pull_prompts_from_langsmith():
    """Pull the seed prompt from the Hub and save it as YAML. Return True on success."""
    client = Client()
    print(f"Puxando prompt do LangSmith Hub: {PROMPT_IDENTIFIER}")

    try:
        # Pulling an owner/name prompt needs explicit consent; the seed prompt is a known challenge source.
        prompt = client.pull_prompt(PROMPT_IDENTIFIER, dangerously_pull_public_prompt=True)
        hub_prompt = client.get_prompt(PROMPT_IDENTIFIER)
    except LangSmithNotFoundError:
        print(f"❌ Prompt não encontrado no LangSmith Hub: {PROMPT_IDENTIFIER}")
        return False
    except LangSmithConnectionError as e:
        print(f"❌ Não foi possível conectar ao LangSmith: {e}")
        return False
    except LangSmithError as e:
        print(f"❌ Erro ao acessar o LangSmith: {e}")
        print("Verifique se LANGSMITH_API_KEY no .env é uma chave válida.")
        return False

    try:
        messages = extract_messages(prompt)
    except ValueError as e:
        print(f"❌ {e}")
        return False

    data = build_prompt_data(messages, hub_prompt, load_current_metadata())
    if not save_yaml({ROOT_KEY: data}, str(OUTPUT_PATH)):
        return False

    print(f"✓ Prompt salvo em {OUTPUT_PATH}")
    return True


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    return 0 if pull_prompts_from_langsmith() else 1


if __name__ == "__main__":
    sys.exit(main())
