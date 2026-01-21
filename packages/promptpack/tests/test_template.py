# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for PromptPack template engine."""

import pytest

from promptpack.template import TemplateEngine, TemplateError


@pytest.fixture
def engine() -> TemplateEngine:
    """Create a template engine with test fragments."""
    return TemplateEngine(
        syntax="{{variable}}",
        fragments={
            "greeting": "Hello, {{name}}!",
            "nested": "Start: {{fragment:greeting}} End.",
        },
    )


def test_basic_substitution(engine: TemplateEngine) -> None:
    """Test basic variable substitution."""
    template = "Hello, {{name}}! Welcome to {{company}}."
    result = engine.render(template, {"name": "Alice", "company": "Acme"})
    assert result == "Hello, Alice! Welcome to Acme."


def test_substitution_with_numbers(engine: TemplateEngine) -> None:
    """Test substitution with numeric values."""
    template = "Count: {{count}}, Price: {{price}}"
    result = engine.render(template, {"count": 42, "price": 19.99})
    assert result == "Count: 42, Price: 19.99"


def test_substitution_with_boolean(engine: TemplateEngine) -> None:
    """Test substitution with boolean values."""
    template = "Active: {{active}}, Enabled: {{enabled}}"
    result = engine.render(template, {"active": True, "enabled": False})
    assert result == "Active: true, Enabled: false"


def test_substitution_with_list(engine: TemplateEngine) -> None:
    """Test substitution with list values."""
    template = "Items: {{items}}"
    result = engine.render(template, {"items": ["a", "b", "c"]})
    assert result == 'Items: ["a", "b", "c"]'


def test_substitution_with_dict(engine: TemplateEngine) -> None:
    """Test substitution with dict values."""
    template = "Config: {{config}}"
    result = engine.render(template, {"config": {"key": "value"}})
    assert result == 'Config: {"key": "value"}'


def test_substitution_with_none(engine: TemplateEngine) -> None:
    """Test substitution with None value."""
    template = "Value: {{value}}!"
    result = engine.render(template, {"value": None})
    assert result == "Value: !"


def test_missing_variable_strict(engine: TemplateEngine) -> None:
    """Test error on missing variable in strict mode."""
    template = "Hello, {{name}}!"
    with pytest.raises(TemplateError) as exc_info:
        engine.render(template, {})
    assert "Undefined variable" in str(exc_info.value)


def test_missing_variable_non_strict(engine: TemplateEngine) -> None:
    """Test non-strict mode leaves undefined variables."""
    template = "Hello, {{name}}!"
    result = engine.render(template, {}, strict=False)
    assert result == "Hello, {{name}}!"


def test_fragment_resolution(engine: TemplateEngine) -> None:
    """Test fragment reference resolution."""
    template = "{{fragment:greeting}}"
    result = engine.render(template, {"name": "Bob"})
    assert result == "Hello, Bob!"


def test_fragment_in_template(engine: TemplateEngine) -> None:
    """Test fragment embedded in larger template."""
    template = "Start: {{fragment:greeting}} End."
    result = engine.render(template, {"name": "Charlie"})
    assert result == "Start: Hello, Charlie! End."


def test_missing_fragment_strict(engine: TemplateEngine) -> None:
    """Test error on missing fragment in strict mode."""
    template = "{{fragment:nonexistent}}"
    with pytest.raises(TemplateError) as exc_info:
        engine.render(template, {})
    assert "Undefined fragment" in str(exc_info.value)


def test_missing_fragment_non_strict(engine: TemplateEngine) -> None:
    """Test non-strict mode leaves undefined fragments."""
    template = "{{fragment:nonexistent}}"
    result = engine.render(template, {}, strict=False)
    assert result == "{{fragment:nonexistent}}"


def test_extract_variables(engine: TemplateEngine) -> None:
    """Test variable extraction from template."""
    template = "Hello, {{name}}! Welcome to {{company}}. {{name}} again."
    variables = engine.extract_variables(template)
    assert variables == {"name", "company"}


def test_extract_variables_with_fragments(engine: TemplateEngine) -> None:
    """Test variable extraction excludes fragment references."""
    template = "{{name}} - {{fragment:greeting}}"
    variables = engine.extract_variables(template)
    assert variables == {"name"}


def test_extract_fragments(engine: TemplateEngine) -> None:
    """Test fragment extraction from template."""
    template = "{{fragment:greeting}} and {{fragment:goodbye}}"
    fragments = engine.extract_fragments(template)
    assert fragments == {"greeting", "goodbye"}


def test_no_substitution_needed(engine: TemplateEngine) -> None:
    """Test template with no variables."""
    template = "Just plain text."
    result = engine.render(template, {})
    assert result == "Just plain text."


def test_multiple_occurrences(engine: TemplateEngine) -> None:
    """Test variable appearing multiple times."""
    template = "{{name}} says hello to {{name}}."
    result = engine.render(template, {"name": "Alice"})
    assert result == "Alice says hello to Alice."


def test_adjacent_variables(engine: TemplateEngine) -> None:
    """Test adjacent variables."""
    template = "{{first}}{{last}}"
    result = engine.render(template, {"first": "John", "last": "Doe"})
    assert result == "JohnDoe"
