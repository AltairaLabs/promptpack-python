# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for PromptPack to LangChain tool conversion."""

import pytest

from promptpack import parse_promptpack_string
from promptpack_langchain import convert_tool, convert_tools


@pytest.fixture
def sample_pack_json() -> str:
    """Sample PromptPack JSON with tools."""
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
      "system_template": "You are a support bot.",
      "tools": ["lookup_order", "create_ticket"],
      "tool_policy": {
        "blocklist": ["dangerous_tool"]
      }
    }
  },
  "tools": {
    "lookup_order": {
      "name": "lookup_order",
      "description": "Look up order by ID",
      "parameters": {
        "type": "object",
        "properties": {
          "order_id": {"type": "string", "description": "Order ID"}
        },
        "required": ["order_id"]
      }
    },
    "create_ticket": {
      "name": "create_ticket",
      "description": "Create a support ticket",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {"type": "string", "description": "Ticket title"},
          "priority": {"type": "string", "description": "Priority level"}
        },
        "required": ["title"]
      }
    },
    "dangerous_tool": {
      "name": "dangerous_tool",
      "description": "A blocked tool"
    }
  }
}"""


@pytest.fixture
def pack(sample_pack_json: str):
    """Parse the sample pack."""
    return parse_promptpack_string(sample_pack_json)


class TestConvertTool:
    """Tests for convert_tool function."""

    def test_basic_conversion(self, pack) -> None:
        """Test basic tool conversion."""
        tool_def = pack.get_tool("lookup_order")
        assert tool_def is not None

        tool = convert_tool(tool_def)
        assert tool.name == "lookup_order"
        assert tool.description == "Look up order by ID"

    def test_with_handler(self, pack) -> None:
        """Test tool with custom handler."""
        tool_def = pack.get_tool("lookup_order")
        assert tool_def is not None

        def handler(order_id: str) -> str:
            return f"Order: {order_id}"

        tool = convert_tool(tool_def, handler=handler)
        result = tool.invoke({"order_id": "123"})
        assert result == "Order: 123"

    def test_without_handler_raises(self, pack) -> None:
        """Test tool without handler raises on invoke."""
        tool_def = pack.get_tool("lookup_order")
        assert tool_def is not None

        tool = convert_tool(tool_def)
        with pytest.raises(NotImplementedError):
            tool.invoke({"order_id": "123"})

    def test_args_schema(self, pack) -> None:
        """Test argument schema generation."""
        tool_def = pack.get_tool("create_ticket")
        assert tool_def is not None

        tool = convert_tool(tool_def)

        # Check schema has the right fields
        schema = tool.args_schema
        assert schema is not None
        # Pydantic model should have fields
        assert hasattr(schema, "model_fields")


class TestConvertTools:
    """Tests for convert_tools function."""

    def test_all_tools(self, pack) -> None:
        """Test converting all tools."""
        tools = convert_tools(pack)
        names = [t.name for t in tools]
        assert "lookup_order" in names
        assert "create_ticket" in names
        assert "dangerous_tool" in names  # Not filtered when no prompt

    def test_tools_for_prompt(self, pack) -> None:
        """Test converting tools for a specific prompt."""
        tools = convert_tools(pack, "support")
        names = [t.name for t in tools]
        assert "lookup_order" in names
        assert "create_ticket" in names
        assert "dangerous_tool" not in names  # Blocklisted

    def test_with_handlers(self, pack) -> None:
        """Test converting with handlers."""
        handlers = {
            "lookup_order": lambda order_id: f"Found: {order_id}",
        }
        tools = convert_tools(pack, handlers=handlers)

        lookup_tool = next(t for t in tools if t.name == "lookup_order")
        result = lookup_tool.invoke({"order_id": "456"})
        assert result == "Found: 456"
