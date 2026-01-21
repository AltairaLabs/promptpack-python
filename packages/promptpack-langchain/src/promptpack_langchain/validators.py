# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Validators for LLM output based on PromptPack validator definitions."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Sequence

from langchain_core.runnables import Runnable, RunnableConfig

from promptpack import Validator


@dataclass
class ValidationViolation:
    """A single validation violation."""

    validator_type: str
    message: str
    fail_on_violation: bool


@dataclass
class ValidationResult:
    """Result of running validators on content."""

    is_valid: bool
    violations: list[ValidationViolation] = field(default_factory=list)
    content: str = ""

    @property
    def has_blocking_violations(self) -> bool:
        """Check if any violations should fail the request."""
        return any(v.fail_on_violation for v in self.violations)


def run_validators(
    content: str,
    validators: Sequence[Validator],
) -> ValidationResult:
    """Run validators on content.

    Args:
        content: The content to validate.
        validators: List of validators to apply.

    Returns:
        ValidationResult with any violations found.
    """
    violations = []

    for validator in validators:
        if not validator.enabled:
            continue

        violation = _run_single_validator(content, validator)
        if violation:
            violations.append(violation)

    is_valid = not any(v.fail_on_violation for v in violations)

    return ValidationResult(
        is_valid=is_valid,
        violations=violations,
        content=content,
    )


def _run_single_validator(
    content: str,
    validator: Validator,
) -> ValidationViolation | None:
    """Run a single validator on content.

    Args:
        content: The content to validate.
        validator: The validator to apply.

    Returns:
        A ValidationViolation if the validation fails, None otherwise.
    """
    params = validator.params or {}

    if validator.type == "banned_words":
        return _validate_banned_words(content, params, validator.fail_on_violation)

    if validator.type == "max_length":
        return _validate_max_length(content, params, validator.fail_on_violation)

    if validator.type == "min_length":
        return _validate_min_length(content, params, validator.fail_on_violation)

    if validator.type == "regex_match":
        return _validate_regex_match(content, params, validator.fail_on_violation)

    # For other validator types, we return None (not implemented)
    # These could be extended with more complex logic (sentiment, toxicity, PII)
    return None


def _validate_banned_words(
    content: str,
    params: dict[str, Any],
    fail_on_violation: bool,
) -> ValidationViolation | None:
    """Check for banned words in content."""
    words = params.get("words", [])
    if not words:
        return None

    content_lower = content.lower()
    found_words = [w for w in words if w.lower() in content_lower]

    if found_words:
        return ValidationViolation(
            validator_type="banned_words",
            message=f"Content contains banned words: {found_words}",
            fail_on_violation=fail_on_violation,
        )
    return None


def _validate_max_length(
    content: str,
    params: dict[str, Any],
    fail_on_violation: bool,
) -> ValidationViolation | None:
    """Check content length against maximum."""
    max_chars = params.get("max_characters")
    if max_chars and len(content) > max_chars:
        return ValidationViolation(
            validator_type="max_length",
            message=f"Content exceeds max length: {len(content)} > {max_chars}",
            fail_on_violation=fail_on_violation,
        )
    return None


def _validate_min_length(
    content: str,
    params: dict[str, Any],
    fail_on_violation: bool,
) -> ValidationViolation | None:
    """Check content length against minimum."""
    min_chars = params.get("min_characters")
    if min_chars and len(content) < min_chars:
        return ValidationViolation(
            validator_type="min_length",
            message=f"Content below min length: {len(content)} < {min_chars}",
            fail_on_violation=fail_on_violation,
        )
    return None


def _validate_regex_match(
    content: str,
    params: dict[str, Any],
    fail_on_violation: bool,
) -> ValidationViolation | None:
    """Check content against regex pattern."""
    pattern = params.get("pattern")
    if not pattern:
        return None

    must_match = params.get("must_match", True)

    try:
        matches = bool(re.search(pattern, content))
    except re.error as e:
        return ValidationViolation(
            validator_type="regex_match",
            message=f"Invalid regex pattern: {e}",
            fail_on_violation=fail_on_violation,
        )

    if must_match and not matches:
        return ValidationViolation(
            validator_type="regex_match",
            message=f"Content does not match required pattern: {pattern}",
            fail_on_violation=fail_on_violation,
        )

    if not must_match and matches:
        return ValidationViolation(
            validator_type="regex_match",
            message=f"Content matches forbidden pattern: {pattern}",
            fail_on_violation=fail_on_violation,
        )

    return None


class ValidationRunnable(Runnable[str, ValidationResult]):
    """A LangChain Runnable that validates content.

    This can be used in chains to validate LLM output.
    """

    def __init__(self, validators: Sequence[Validator]):
        """Initialize with validators.

        Args:
            validators: List of validators to apply.
        """
        self.validators = list(validators)

    def invoke(
        self,
        input: str,
        config: RunnableConfig | None = None,
    ) -> ValidationResult:
        """Validate the input content.

        Args:
            input: Content to validate.
            config: Optional runnable config.

        Returns:
            ValidationResult with any violations.
        """
        return run_validators(input, self.validators)

    async def ainvoke(
        self,
        input: str,
        config: RunnableConfig | None = None,
    ) -> ValidationResult:
        """Async version of invoke."""
        return self.invoke(input, config)
