# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for PromptPack validators."""

import pytest

from promptpack import Validator
from promptpack_langchain import ValidationRunnable, run_validators


def make_validator(
    validator_type: str,
    params: dict | None = None,
    enabled: bool = True,
    fail_on_violation: bool = False,
) -> Validator:
    """Helper to create a Validator for testing."""
    return Validator(
        type=validator_type,  # type: ignore[arg-type]
        enabled=enabled,
        fail_on_violation=fail_on_violation,
        params=params,
    )


class TestRunValidators:
    """Tests for run_validators function."""

    def test_no_validators(self) -> None:
        """Test with no validators."""
        result = run_validators("Some content", [])
        assert result.is_valid
        assert len(result.violations) == 0

    def test_disabled_validator(self) -> None:
        """Test disabled validator is skipped."""
        validators = [
            make_validator(
                "banned_words",
                params={"words": ["bad"]},
                enabled=False,
            ),
        ]
        result = run_validators("This is bad", validators)
        assert result.is_valid
        assert len(result.violations) == 0


class TestBannedWordsValidator:
    """Tests for banned_words validator."""

    def test_no_banned_words(self) -> None:
        """Test content without banned words."""
        validators = [
            make_validator("banned_words", params={"words": ["bad", "evil"]}),
        ]
        result = run_validators("This is good content", validators)
        assert result.is_valid
        assert len(result.violations) == 0

    def test_contains_banned_word(self) -> None:
        """Test content with banned word."""
        validators = [
            make_validator("banned_words", params={"words": ["bad", "evil"]}),
        ]
        result = run_validators("This is bad content", validators)
        assert len(result.violations) == 1
        assert result.violations[0].validator_type == "banned_words"
        assert "bad" in result.violations[0].message

    def test_case_insensitive(self) -> None:
        """Test case-insensitive matching."""
        validators = [
            make_validator("banned_words", params={"words": ["bad"]}),
        ]
        result = run_validators("This is BAD", validators)
        assert len(result.violations) == 1

    def test_fail_on_violation(self) -> None:
        """Test fail_on_violation flag."""
        validators = [
            make_validator(
                "banned_words",
                params={"words": ["bad"]},
                fail_on_violation=True,
            ),
        ]
        result = run_validators("This is bad", validators)
        assert not result.is_valid
        assert result.has_blocking_violations


class TestMaxLengthValidator:
    """Tests for max_length validator."""

    def test_under_limit(self) -> None:
        """Test content under limit."""
        validators = [
            make_validator("max_length", params={"max_characters": 100}),
        ]
        result = run_validators("Short content", validators)
        assert result.is_valid

    def test_over_limit(self) -> None:
        """Test content over limit."""
        validators = [
            make_validator("max_length", params={"max_characters": 10}),
        ]
        result = run_validators("This is too long", validators)
        assert len(result.violations) == 1
        assert "max length" in result.violations[0].message


class TestMinLengthValidator:
    """Tests for min_length validator."""

    def test_over_minimum(self) -> None:
        """Test content over minimum."""
        validators = [
            make_validator("min_length", params={"min_characters": 5}),
        ]
        result = run_validators("Hello there", validators)
        assert result.is_valid

    def test_under_minimum(self) -> None:
        """Test content under minimum."""
        validators = [
            make_validator("min_length", params={"min_characters": 20}),
        ]
        result = run_validators("Hi", validators)
        assert len(result.violations) == 1
        assert "min length" in result.violations[0].message


class TestRegexMatchValidator:
    """Tests for regex_match validator."""

    def test_matches_required_pattern(self) -> None:
        """Test content matches required pattern."""
        validators = [
            make_validator(
                "regex_match",
                params={"pattern": r"\d{3}-\d{4}", "must_match": True},
            ),
        ]
        result = run_validators("Call 123-4567", validators)
        assert result.is_valid

    def test_missing_required_pattern(self) -> None:
        """Test content missing required pattern."""
        validators = [
            make_validator(
                "regex_match",
                params={"pattern": r"\d{3}-\d{4}", "must_match": True},
            ),
        ]
        result = run_validators("No phone here", validators)
        assert len(result.violations) == 1
        assert "does not match" in result.violations[0].message

    def test_matches_forbidden_pattern(self) -> None:
        """Test content matches forbidden pattern."""
        validators = [
            make_validator(
                "regex_match",
                params={"pattern": r"password", "must_match": False},
            ),
        ]
        result = run_validators("My password is secret", validators)
        assert len(result.violations) == 1
        assert "forbidden pattern" in result.violations[0].message


class TestValidationRunnable:
    """Tests for ValidationRunnable."""

    def test_invoke(self) -> None:
        """Test invoke method."""
        validators = [
            make_validator("banned_words", params={"words": ["bad"]}),
        ]
        runnable = ValidationRunnable(validators)

        result = runnable.invoke("This is bad")
        assert len(result.violations) == 1

    @pytest.mark.asyncio
    async def test_ainvoke(self) -> None:
        """Test async invoke method."""
        validators = [
            make_validator("banned_words", params={"words": ["bad"]}),
        ]
        runnable = ValidationRunnable(validators)

        result = await runnable.ainvoke("This is good")
        assert result.is_valid
