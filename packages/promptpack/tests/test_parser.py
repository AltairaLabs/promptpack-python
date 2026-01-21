# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for PromptPack parser."""

from pathlib import Path

import pytest
from promptpack import parse_promptpack, parse_promptpack_string
from promptpack.parser import PromptPackParseError


@pytest.fixture
def sample_pack_path() -> Path:
    """Get path to sample pack fixture."""
    return Path(__file__).parent / "fixtures" / "sample.pack.json"


@pytest.fixture
def sample_pack_content(sample_pack_path: Path) -> str:
    """Get sample pack content."""
    return sample_pack_path.read_text()


def test_parse_promptpack_from_file(sample_pack_path: Path) -> None:
    """Test parsing a PromptPack from a file."""
    pack = parse_promptpack(sample_pack_path)

    assert pack.id == "customer-support"
    assert pack.name == "Customer Support Pack"
    assert pack.version == "1.0.0"
    assert len(pack.prompts) == 2
    assert "support" in pack.prompts
    assert "sales" in pack.prompts


def test_parse_promptpack_from_string(sample_pack_content: str) -> None:
    """Test parsing a PromptPack from a string."""
    pack = parse_promptpack_string(sample_pack_content)

    assert pack.id == "customer-support"
    assert len(pack.prompts) == 2


def test_parse_promptpack_file_not_found() -> None:
    """Test error when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        parse_promptpack("/nonexistent/path.json")


def test_parse_promptpack_invalid_json() -> None:
    """Test error on invalid JSON."""
    with pytest.raises(PromptPackParseError) as exc_info:
        parse_promptpack_string("not valid json")

    assert "Invalid JSON" in str(exc_info.value)


def test_parse_promptpack_validation_error() -> None:
    """Test error on schema validation failure."""
    invalid_pack = '{"id": "test"}'  # Missing required fields

    with pytest.raises(PromptPackParseError) as exc_info:
        parse_promptpack_string(invalid_pack)

    assert "validation failed" in str(exc_info.value)
    assert exc_info.value.errors is not None
    assert len(exc_info.value.errors) > 0


def test_prompt_access(sample_pack_content: str) -> None:
    """Test accessing prompts from a pack."""
    pack = parse_promptpack_string(sample_pack_content)

    support = pack.get_prompt("support")
    assert support is not None
    assert support.id == "support"
    assert support.name == "Support Bot"

    nonexistent = pack.get_prompt("nonexistent")
    assert nonexistent is None


def test_tool_access(sample_pack_content: str) -> None:
    """Test accessing tools from a pack."""
    pack = parse_promptpack_string(sample_pack_content)

    lookup = pack.get_tool("lookup_order")
    assert lookup is not None
    assert lookup.name == "lookup_order"
    assert "order" in lookup.description.lower()

    nonexistent = pack.get_tool("nonexistent")
    assert nonexistent is None


def test_fragment_access(sample_pack_content: str) -> None:
    """Test accessing fragments from a pack."""
    pack = parse_promptpack_string(sample_pack_content)

    guidelines = pack.get_fragment("guidelines")
    assert guidelines is not None
    assert "helpful" in guidelines.lower()

    nonexistent = pack.get_fragment("nonexistent")
    assert nonexistent is None


def test_tools_for_prompt(sample_pack_content: str) -> None:
    """Test getting tools for a specific prompt."""
    pack = parse_promptpack_string(sample_pack_content)

    tools = pack.get_tools_for_prompt("support")
    tool_names = [t.name for t in tools]

    assert "lookup_order" in tool_names
    assert "create_ticket" in tool_names
    # dangerous_tool should be excluded due to blocklist
    assert "dangerous_tool" not in tool_names


def test_variable_access(sample_pack_content: str) -> None:
    """Test accessing variables from a prompt."""
    pack = parse_promptpack_string(sample_pack_content)
    prompt = pack.get_prompt("support")
    assert prompt is not None

    role_var = prompt.get_variable("role")
    assert role_var is not None
    assert role_var.required is True
    assert role_var.type == "string"

    customer_var = prompt.get_variable("customer_name")
    assert customer_var is not None
    assert customer_var.required is False
    assert customer_var.default == "Guest"
