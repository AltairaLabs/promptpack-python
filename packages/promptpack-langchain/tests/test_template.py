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
      "validators": [
        {
          "type": "banned_words",
          "enabled": true,
          "fail_on_violation": false,
          "params": {"words": ["bad", "evil"]}
        }
      ],
      "model_overrides": {
        "gpt-4": {
          "system_template_prefix": "[GPT-4 Mode] ",
          "parameters": {"temperature": 0.5}
        },
        "claude-3": {
          "system_template_suffix": " Be concise.",
          "parameters": {"temperature": 0.8}
        },
        "gpt-4-turbo": {
          "system_template": "You are a GPT-4 Turbo assistant."
        }
      }
    },
    "simple": {
      "id": "simple",
      "name": "Simple Bot",
      "version": "1.0.0",
      "system_template": "You are a simple assistant."
    },
    "with_defaults": {
      "id": "with_defaults",
      "name": "Bot with Defaults",
      "version": "1.0.0",
      "system_template": "You are a {{role}} assistant.",
      "variables": [
        {"name": "role", "type": "string", "required": false, "default": "helpful"}
      ]
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

    def test_model_override_suffix(self, pack) -> None:
        """Test model-specific template with suffix."""
        template = PromptPackTemplate.from_promptpack(pack, "support", model_name="claude-3")
        result = template.format(role="agent", company="TestCo")
        assert "Be concise." in result
        assert "Be helpful and professional" in result

    def test_model_override_full_template(self, pack) -> None:
        """Test model-specific full template replacement."""
        template = PromptPackTemplate.from_promptpack(pack, "support", model_name="gpt-4-turbo")
        result = template.format(role="agent", company="TestCo")
        assert result == "You are a GPT-4 Turbo assistant."

    def test_no_model_override(self, pack) -> None:
        """Test using base template when model has no override."""
        template = PromptPackTemplate.from_promptpack(pack, "support", model_name="unknown-model")
        result = template.format(role="agent", company="TestCo")
        assert "[GPT-4 Mode]" not in result
        assert "agent" in result

    def test_prompt_type(self, pack) -> None:
        """Test prompt type property."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        assert template._prompt_type == "promptpack"

    def test_default_variables(self, pack) -> None:
        """Test variables with default values."""
        template = PromptPackTemplate.from_promptpack(pack, "with_defaults")
        # Default values should not be in input_variables
        assert "role" not in template.input_variables
        result = template.format()
        assert "helpful" in result

    def test_override_default_value(self, pack) -> None:
        """Test overriding default value."""
        template = PromptPackTemplate.from_promptpack(pack, "with_defaults")
        result = template.format(role="friendly")
        assert "friendly" in result

    def test_get_parameters_empty(self, pack) -> None:
        """Test getting parameters from prompt without any."""
        template = PromptPackTemplate.from_promptpack(pack, "simple")
        params = template.get_parameters()
        assert params == {}

    def test_available_prompts_in_error(self, pack) -> None:
        """Test error message shows available prompts."""
        with pytest.raises(ValueError) as exc_info:
            PromptPackTemplate.from_promptpack(pack, "nonexistent")
        error_msg = str(exc_info.value)
        assert "support" in error_msg
        assert "simple" in error_msg

    @pytest.mark.asyncio
    async def test_aformat_prompt(self, pack) -> None:
        """Test async format_prompt."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        result = await template.aformat_prompt(role="agent", company="TestCo")
        assert "agent" in result.text
        assert "TestCo" in result.text

    def test_to_chat_prompt_template_without_vars(self, pack) -> None:
        """Test conversion to ChatPromptTemplate without variables."""
        template = PromptPackTemplate.from_promptpack(pack, "support")
        chat_template = template.to_chat_prompt_template()
        # Should include the template with placeholders
        assert chat_template is not None


class TestPromptPackTemplateIntegration:
    """Integration tests for PromptPackTemplate."""

    def test_full_workflow(self) -> None:
        """Test complete workflow from JSON to formatted output."""
        pack_json = """{
          "id": "workflow-test",
          "name": "Workflow Test",
          "version": "1.0.0",
          "template_engine": {"version": "v1", "syntax": "{{variable}}"},
          "prompts": {
            "main": {
              "id": "main",
              "name": "Main Prompt",
              "version": "1.0.0",
              "system_template": "Role: {{role}}. Task: {{task}}. Guidelines: {{fragment:rules}}",
              "variables": [
                {"name": "role", "type": "string", "required": true},
                {"name": "task", "type": "string", "required": true}
              ],
              "parameters": {"temperature": 0.5, "max_tokens": 1000}
            }
          },
          "fragments": {
            "rules": "Follow best practices."
          }
        }"""

        pack = parse_promptpack_string(pack_json)
        template = PromptPackTemplate.from_promptpack(pack, "main")

        # Verify metadata
        assert template.input_variables == ["role", "task"]
        params = template.get_parameters()
        assert params["temperature"] == 0.5

        # Verify formatting
        result = template.format(role="assistant", task="help users")
        assert "Role: assistant" in result
        assert "Task: help users" in result
        assert "Follow best practices" in result
