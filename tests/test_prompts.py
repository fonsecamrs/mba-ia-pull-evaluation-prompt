"""
Testes automatizados para validação de prompts.
"""
import re
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
ROOT_KEY = "bug_to_user_story_v2"
MIN_EXAMPLES = 3
MIN_TECHNIQUES = 2

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="module")
def prompt() -> dict:
    """v2 prompt data, loaded once for all tests."""
    return load_prompts(PROMPT_PATH)[ROOT_KEY]

@pytest.fixture(scope="module")
def system_prompt(prompt: dict) -> str:
    return prompt.get("system_prompt") or ""

class TestPrompts:
    def test_prompt_has_system_prompt(self, system_prompt: str):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert system_prompt.strip(), "O prompt não tem 'system_prompt' ou ele está vazio."

    def test_prompt_has_role_definition(self, system_prompt: str):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert re.search(r"^Você é ", system_prompt, re.MULTILINE), (
            "O system_prompt não define uma persona: falta uma frase iniciada por 'Você é'."
        )

    def test_prompt_mentions_format(self, system_prompt: str):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        # A bare "Markdown" match is not enough: the v2 prompt only mentions it to forbid Markdown headings.
        assert re.search(r"user story", system_prompt, re.IGNORECASE), (
            "O system_prompt não menciona o formato User Story."
        )
        assert re.search(r"Como um .+, eu quero .+, para que", system_prompt), (
            "O system_prompt não descreve o modelo padrão 'Como um ..., eu quero ..., para que ...'."
        )

    def test_prompt_has_few_shot_examples(self, system_prompt: str):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        markers = {
            "Exemplo N": len(re.findall(r"Exemplo \d", system_prompt)),
            "Entrada:": system_prompt.count("Entrada:"),
            "Saída:": system_prompt.count("Saída:"),
        }
        missing = [marker for marker, count in markers.items() if count < MIN_EXAMPLES]
        assert not missing, (
            f"O system_prompt precisa de {MIN_EXAMPLES} exemplos Few-shot; "
            f"marcadores insuficientes: {', '.join(missing)} (encontrados: {markers})."
        )

    def test_prompt_no_todos(self, prompt: dict):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        for field in ("system_prompt", "user_prompt"):
            assert "[TODO]" not in (prompt.get(field) or ""), f"O campo '{field}' ainda contém [TODO]."

    def test_minimum_techniques(self, prompt: dict):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied")
        assert isinstance(techniques, list), "O campo 'techniques_applied' deve ser uma lista."
        assert len(techniques) >= MIN_TECHNIQUES, (
            f"São necessárias pelo menos {MIN_TECHNIQUES} técnicas em 'techniques_applied'; "
            f"encontradas: {len(techniques)}."
        )

    def test_bug_report_only_in_user_prompt(self, prompt: dict, system_prompt: str):
        """Checks that the bug report variable is received only in the user prompt (FR-011)."""
        assert "{bug_report}" in (prompt.get("user_prompt") or ""), (
            "O user_prompt precisa conter a variável {bug_report}."
        )
        assert "{bug_report}" not in system_prompt, (
            "O system_prompt não pode conter {bug_report}: o relato deve vir apenas no user_prompt."
        )

    def test_prompt_passes_structure_validation(self, prompt: dict):
        """Checks the same validation that push_prompts.py runs before publishing."""
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, f"O prompt não passa na validação estrutural: {errors}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
