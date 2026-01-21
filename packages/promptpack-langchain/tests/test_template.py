# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for PromptPackTemplate."""

import pytest
from promptpack import parse_promptpack_string
from promptpack_langchain import PromptPackTemplate


@pytest.fixture
def sample_pack_json() -> str:
    """Sample PromptPack JSON for testing."""
    return """{
  "id": "test-pack",
  "name": "Test Pack",
  "version": "1.0.0",
  "template_engine": {"version": "v1", "syntax": "{{variable}}"},
  "prompts": {
    "support": {
      "id": "support",
      "name": "Support Bot",
      "version": "1.0.0",
      "system_template": "You are a {{role}} for {{company}}. {{fragment:guidelines}}",
      "variables": [
        {"name": "role", "type": "string", "required": true},
        {"name": "company", "type": "string", "required": true}
      ],
      "parameters": {
        "temperature": 0.7,
        "max_tokens": 1500
      },
      "model_overrides": {
        "gpt-4": {
          "system_template_prefix": "[GPT-4 Mode] ",
          "parameters": {"temperature": 0.5}
        }
      }
    },
    "simple": {
      "id": "simple",
      "name": "Simple Bot",
      "version": "1.0.0",
      "system_template": "You are a simple assistant."
    }
  },
  "fragments": {
    "guidelines": "Be helpful and professional."
  }
}"""


@pytest.fixture
def pack(sample_pack_json: str):
    """Parse the sample pack."""
    return parse_promptpack_string(sample_pack_json)


class TestPromptPackTemplate:
    """Tests for PromptPackTemplate."""

    def test_from_promptpack(self, pack) -> None:
        """Test creating a template from a pack."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        assert template.prompt.id == "support"
        assert "role" in template.input_variables
        assert "company" in template.input_variables

    def test_from_promptpack_not_found(self, pack) -> None:
        """Test error when prompt not found."""
        with pytest.raises(ValueError) as exc_info:
            PromptPackTemplate.from_promptpack(pack, "nonexistent")
        assert "nonexistent" in str(exc_info.value)

    def test_format(self, pack) -> None:
        """Test formatting the template."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        result = template.format(role="support agent", company="Acme")
        assert "support agent" in result
        assert "Acme" in result
        assert "Be helpful and professional" in result

    def test_format_prompt(self, pack) -> None:
        """Test format_prompt returns PromptValue."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        result = template.format_prompt(role="agent", company="TestCo")
        assert "agent" in result.text
        assert "TestCo" in result.text

    def test_model_override_template(self, pack) -> None:
        """Test model-specific template override."""
        template = PromptPackTemplate.from_promptpack(pack, "support", model_name="gpt-4")
        result = template.format(role="agent", company="TestCo")
        assert "[GPT-4 Mode]" in result

    def test_get_parameters(self, pack) -> None:
        """Test getting LLM parameters."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        params = template.get_parameters()
        assert params["temperature"] == 0.7
        assert params["max_tokens"] == 1500

    def test_get_parameters_with_override(self, pack) -> None:
        """Test model-specific parameter override."""
        template = PromptPackTemplate.from_promptpack(pack, "support", model_name="gpt-4")
        params = template.get_parameters()
        assert params["temperature"] == 0.5  # Override
        assert params["max_tokens"] == 1500  # Base

    def test_simple_prompt_no_variables(self, pack) -> None:
        """Test prompt with no variables."""
        template = PromptPackTemplate.from_promptpack(pack, "simple")
        assert template.input_variables == []
        result = template.format()
        assert "simple assistant" in result

    def test_to_chat_prompt_template(self, pack) -> None:
        """Test conversion to ChatPromptTemplate."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        chat_template = template.to_chat_prompt_template(role="agent", company="TestCo")
        assert chat_template is not None
