# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Variable validation utilities for PromptPack."""

from __future__ import annotations

import re
from typing import Any

from promptpack.types import Variable


class VariableValidationError(Exception):
    """Error raised when variable validation fails."""

    def __init__(self, variable_name: str, message: str):
        super().__init__(f"Variable '{variable_name}': {message}")
        self.variable_name = variable_name


def validate_variable(variable: Variable, value: Any) -> Any:
    """Validate a single variable value against its definition.

    Args:
        variable: The variable definition.
        value: The value to validate.

    Returns:
        The validated value (possibly coerced to the correct type).

    Raises:
        VariableValidationError: If validation fails.
    """
    # Check required
    if value is None:
        if variable.required:
            if variable.default is not None:
                return variable.default
            raise VariableValidationError(variable.name, "Required variable is missing")
        return variable.default

    # Type validation
    value = _validate_type(variable, value)

    # Additional validation rules
    if variable.validation:
        _validate_rules(variable, value)

    return value


def _validate_type(variable: Variable, value: Any) -> Any:
    """Validate and coerce the value to the expected type.

    Args:
        variable: The variable definition.
        value: The value to validate.

    Returns:
        The value coerced to the correct type.

    Raises:
        VariableValidationError: If the type is invalid.
    """
    expected_type = variable.type

    if expected_type == "string":
        if not isinstance(value, str):
            try:
                return str(value)
            except (ValueError, TypeError) as e:
                raise VariableValidationError(
                    variable.name, f"Expected string, got {type(value).__name__}"
                ) from e
        return value

    if expected_type == "number":
        if isinstance(value, bool):  # bool is subclass of int
            raise VariableValidationError(
                variable.name, f"Expected number, got {type(value).__name__}"
            )
        if not isinstance(value, (int, float)):
            try:
                return float(value)
            except (ValueError, TypeError) as e:
                raise VariableValidationError(
                    variable.name, f"Expected number, got {type(value).__name__}"
                ) from e
        return value

    if expected_type == "boolean":
        if not isinstance(value, bool):
            if isinstance(value, str):
                if value.lower() in ("true", "1", "yes"):
                    return True
                if value.lower() in ("false", "0", "no"):
                    return False
            raise VariableValidationError(
                variable.name, f"Expected boolean, got {type(value).__name__}"
            )
        return value

    if expected_type == "object":
        if not isinstance(value, dict):
            raise VariableValidationError(
                variable.name, f"Expected object, got {type(value).__name__}"
            )
        return value

    if expected_type == "array":
        if not isinstance(value, list):
            raise VariableValidationError(
                variable.name, f"Expected array, got {type(value).__name__}"
            )
        return value

    return value


def _validate_rules(variable: Variable, value: Any) -> None:
    """Validate the value against additional validation rules.

    Args:
        variable: The variable definition.
        value: The value to validate.

    Raises:
        VariableValidationError: If validation fails.
    """
    rules = variable.validation
    if rules is None:
        return

    # String validation
    if isinstance(value, str):
        if rules.pattern is not None:
            if not re.match(rules.pattern, value):
                raise VariableValidationError(
                    variable.name, f"Value does not match pattern: {rules.pattern}"
                )

        if rules.min_length is not None and len(value) < rules.min_length:
            raise VariableValidationError(
                variable.name, f"String too short (min: {rules.min_length})"
            )

        if rules.max_length is not None and len(value) > rules.max_length:
            raise VariableValidationError(
                variable.name, f"String too long (max: {rules.max_length})"
            )

    # Numeric validation
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if rules.minimum is not None and value < rules.minimum:
            raise VariableValidationError(variable.name, f"Value below minimum: {rules.minimum}")

        if rules.maximum is not None and value > rules.maximum:
            raise VariableValidationError(variable.name, f"Value above maximum: {rules.maximum}")

    # Enum validation
    if rules.enum is not None and value not in rules.enum:
        raise VariableValidationError(variable.name, f"Value not in allowed values: {rules.enum}")


def validate_variables(
    variables: list[Variable],
    values: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Validate all variables against their definitions.

    Args:
        variables: List of variable definitions.
        values: Dictionary of variable names to values.
        strict: If True, raise an error for unknown variables.

    Returns:
        Dictionary of validated variable values with defaults applied.

    Raises:
        VariableValidationError: If validation fails.
    """
    result = {}
    var_names = {v.name for v in variables}

    # Check for unknown variables
    if strict:
        for name in values:
            if name not in var_names:
                raise VariableValidationError(name, "Unknown variable")

    # Validate each defined variable
    for var in variables:
        value = values.get(var.name)
        result[var.name] = validate_variable(var, value)

    return result
