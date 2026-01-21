# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for PromptPack variable validation."""

import pytest

from promptpack.types import Variable, VariableValidation
from promptpack.variables import (
    VariableValidationError,
    validate_variable,
    validate_variables,
)


def make_variable(
    name: str = "test",
    var_type: str = "string",
    required: bool = True,
    default: object = None,
    validation: VariableValidation | None = None,
) -> Variable:
    """Helper to create a Variable for testing."""
    return Variable(
        name=name,
        type=var_type,  # type: ignore[arg-type]
        required=required,
        default=default,
        validation=validation,
    )


class TestValidateVariable:
    """Tests for validate_variable function."""

    def test_required_variable_missing(self) -> None:
        """Test error when required variable is missing."""
        var = make_variable(required=True)
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, None)
        assert "Required variable is missing" in str(exc_info.value)

    def test_required_variable_with_default(self) -> None:
        """Test required variable uses default when missing."""
        var = make_variable(required=True, default="default_value")
        result = validate_variable(var, None)
        assert result == "default_value"

    def test_optional_variable_missing(self) -> None:
        """Test optional variable returns default when missing."""
        var = make_variable(required=False, default="default_value")
        result = validate_variable(var, None)
        assert result == "default_value"

    def test_optional_variable_no_default(self) -> None:
        """Test optional variable returns None when no default."""
        var = make_variable(required=False)
        result = validate_variable(var, None)
        assert result is None

    def test_string_type_valid(self) -> None:
        """Test valid string value."""
        var = make_variable(var_type="string")
        result = validate_variable(var, "hello")
        assert result == "hello"

    def test_string_type_coercion(self) -> None:
        """Test string coercion from number."""
        var = make_variable(var_type="string")
        result = validate_variable(var, 42)
        assert result == "42"

    def test_number_type_int(self) -> None:
        """Test valid integer value."""
        var = make_variable(var_type="number")
        result = validate_variable(var, 42)
        assert result == 42

    def test_number_type_float(self) -> None:
        """Test valid float value."""
        var = make_variable(var_type="number")
        result = validate_variable(var, 3.14)
        assert result == 3.14

    def test_number_type_coercion(self) -> None:
        """Test number coercion from string."""
        var = make_variable(var_type="number")
        result = validate_variable(var, "42.5")
        assert result == 42.5

    def test_number_type_boolean_rejected(self) -> None:
        """Test boolean is not accepted as number."""
        var = make_variable(var_type="number")
        with pytest.raises(VariableValidationError):
            validate_variable(var, True)

    def test_boolean_type_valid(self) -> None:
        """Test valid boolean value."""
        var = make_variable(var_type="boolean")
        assert validate_variable(var, True) is True
        assert validate_variable(var, False) is False

    def test_boolean_type_string_coercion(self) -> None:
        """Test boolean coercion from string."""
        var = make_variable(var_type="boolean")
        assert validate_variable(var, "true") is True
        assert validate_variable(var, "false") is False
        assert validate_variable(var, "yes") is True
        assert validate_variable(var, "no") is False

    def test_object_type_valid(self) -> None:
        """Test valid object value."""
        var = make_variable(var_type="object")
        result = validate_variable(var, {"key": "value"})
        assert result == {"key": "value"}

    def test_object_type_invalid(self) -> None:
        """Test error on non-object value."""
        var = make_variable(var_type="object")
        with pytest.raises(VariableValidationError):
            validate_variable(var, "not an object")

    def test_array_type_valid(self) -> None:
        """Test valid array value."""
        var = make_variable(var_type="array")
        result = validate_variable(var, [1, 2, 3])
        assert result == [1, 2, 3]

    def test_array_type_invalid(self) -> None:
        """Test error on non-array value."""
        var = make_variable(var_type="array")
        with pytest.raises(VariableValidationError):
            validate_variable(var, "not an array")


class TestVariableValidationRules:
    """Tests for variable validation rules."""

    def test_pattern_valid(self) -> None:
        """Test valid pattern match."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(pattern=r"^[a-z]+$"),
        )
        result = validate_variable(var, "hello")
        assert result == "hello"

    def test_pattern_invalid(self) -> None:
        """Test error on pattern mismatch."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(pattern=r"^[a-z]+$"),
        )
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, "Hello123")
        assert "pattern" in str(exc_info.value)

    def test_min_length_valid(self) -> None:
        """Test valid min length."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(min_length=3),
        )
        result = validate_variable(var, "hello")
        assert result == "hello"

    def test_min_length_invalid(self) -> None:
        """Test error on min length violation."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(min_length=5),
        )
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, "hi")
        assert "too short" in str(exc_info.value)

    def test_max_length_valid(self) -> None:
        """Test valid max length."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(max_length=10),
        )
        result = validate_variable(var, "hello")
        assert result == "hello"

    def test_max_length_invalid(self) -> None:
        """Test error on max length violation."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(max_length=3),
        )
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, "hello")
        assert "too long" in str(exc_info.value)

    def test_minimum_valid(self) -> None:
        """Test valid minimum value."""
        var = make_variable(
            var_type="number",
            validation=VariableValidation(minimum=0),
        )
        result = validate_variable(var, 10)
        assert result == 10

    def test_minimum_invalid(self) -> None:
        """Test error on minimum violation."""
        var = make_variable(
            var_type="number",
            validation=VariableValidation(minimum=10),
        )
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, 5)
        assert "below minimum" in str(exc_info.value)

    def test_maximum_valid(self) -> None:
        """Test valid maximum value."""
        var = make_variable(
            var_type="number",
            validation=VariableValidation(maximum=100),
        )
        result = validate_variable(var, 50)
        assert result == 50

    def test_maximum_invalid(self) -> None:
        """Test error on maximum violation."""
        var = make_variable(
            var_type="number",
            validation=VariableValidation(maximum=10),
        )
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, 50)
        assert "above maximum" in str(exc_info.value)

    def test_enum_valid(self) -> None:
        """Test valid enum value."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(enum=["low", "medium", "high"]),
        )
        result = validate_variable(var, "medium")
        assert result == "medium"

    def test_enum_invalid(self) -> None:
        """Test error on enum violation."""
        var = make_variable(
            var_type="string",
            validation=VariableValidation(enum=["low", "medium", "high"]),
        )
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variable(var, "critical")
        assert "not in allowed values" in str(exc_info.value)


class TestValidateVariables:
    """Tests for validate_variables function."""

    def test_all_valid(self) -> None:
        """Test all variables valid."""
        variables = [
            make_variable(name="name", var_type="string"),
            make_variable(name="age", var_type="number"),
        ]
        values = {"name": "Alice", "age": 30}
        result = validate_variables(variables, values)
        assert result == {"name": "Alice", "age": 30}

    def test_applies_defaults(self) -> None:
        """Test defaults are applied for missing optional variables."""
        variables = [
            make_variable(name="name", var_type="string", required=False, default="Guest"),
        ]
        result = validate_variables(variables, {})
        assert result == {"name": "Guest"}

    def test_unknown_variable_strict(self) -> None:
        """Test error on unknown variable in strict mode."""
        variables = [make_variable(name="name")]
        with pytest.raises(VariableValidationError) as exc_info:
            validate_variables(variables, {"name": "Alice", "extra": "value"}, strict=True)
        assert "Unknown variable" in str(exc_info.value)

    def test_unknown_variable_non_strict(self) -> None:
        """Test unknown variables ignored in non-strict mode."""
        variables = [make_variable(name="name")]
        result = validate_variables(
            variables, {"name": "Alice", "extra": "value"}, strict=False
        )
        assert result == {"name": "Alice"}
