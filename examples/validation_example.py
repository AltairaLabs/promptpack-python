#!/usr/bin/env python3
# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""
Validation example for promptpack-langchain.

This example shows how to use PromptPack validators:
1. Run validators on content
2. Handle validation results
3. Use ValidationRunnable in a chain

To run this example:
    python examples/validation_example.py
"""

from promptpack import Validator
from promptpack_langchain import ValidationRunnable, run_validators


def main() -> None:
    """Run validation example."""
    print("=== PromptPack Validation Example ===\n")

    # 1. Create validators
    validators = [
        Validator(
            type="banned_words",
            enabled=True,
            fail_on_violation=True,
            params={"words": ["inappropriate", "offensive", "banned"]},
        ),
        Validator(
            type="max_length",
            enabled=True,
            fail_on_violation=False,
            params={"max_characters": 500},
        ),
        Validator(
            type="min_length",
            enabled=True,
            fail_on_violation=False,
            params={"min_characters": 10},
        ),
    ]

    print("Validators configured:")
    for v in validators:
        print(f"  - {v.type} (fail_on_violation={v.fail_on_violation})")

    # 2. Test with valid content
    print("\n--- Test 1: Valid Content ---")
    valid_content = "This is a helpful and professional response to the customer's inquiry."
    result = run_validators(valid_content, validators)
    print(f"Content: '{valid_content[:50]}...'")
    print(f"Is valid: {result.is_valid}")
    print(f"Violations: {len(result.violations)}")

    # 3. Test with banned word
    print("\n--- Test 2: Content with Banned Word ---")
    bad_content = "This response contains inappropriate content."
    result = run_validators(bad_content, validators)
    print(f"Content: '{bad_content}'")
    print(f"Is valid: {result.is_valid}")
    print(f"Has blocking violations: {result.has_blocking_violations}")
    for violation in result.violations:
        print(f"  - {violation.validator_type}: {violation.message}")

    # 4. Test with length violation
    print("\n--- Test 3: Content Too Short ---")
    short_content = "Hi"
    result = run_validators(short_content, validators)
    print(f"Content: '{short_content}'")
    print(f"Is valid: {result.is_valid}")
    for violation in result.violations:
        print(f"  - {violation.validator_type}: {violation.message}")

    # 5. Test with content too long
    print("\n--- Test 4: Content Too Long ---")
    long_content = "This is a very long response. " * 50
    result = run_validators(long_content, validators)
    print(f"Content: '{long_content[:50]}...' ({len(long_content)} chars)")
    print(f"Is valid: {result.is_valid}")
    for violation in result.violations:
        print(f"  - {violation.validator_type}: {violation.message}")

    # 6. Using ValidationRunnable
    print("\n--- Using ValidationRunnable ---")
    runnable = ValidationRunnable(validators)

    contents = [
        "This is a good response.",
        "This is inappropriate.",
        "OK",  # Too short
    ]

    for content in contents:
        result = runnable.invoke(content)
        status = "PASS" if result.is_valid else "FAIL"
        print(f"  [{status}] '{content[:30]}...' - {len(result.violations)} violations")

    # 7. Regex validator example
    print("\n--- Regex Validator Example ---")
    regex_validators = [
        Validator(
            type="regex_match",
            enabled=True,
            fail_on_violation=True,
            params={
                "pattern": r"^[A-Z]",  # Must start with capital letter
                "must_match": True,
            },
        ),
        Validator(
            type="regex_match",
            enabled=True,
            fail_on_violation=False,
            params={
                "pattern": r"password|secret|key",  # Forbidden patterns
                "must_match": False,
            },
        ),
    ]

    test_cases = [
        "Hello, how can I help you today?",
        "hello, how can I help?",  # Doesn't start with capital
        "Here is your password: 12345",  # Contains forbidden word
    ]

    for content in test_cases:
        result = run_validators(content, regex_validators)
        status = "PASS" if result.is_valid else "FAIL"
        violations = ", ".join(v.validator_type for v in result.violations) or "none"
        print(f"  [{status}] '{content[:40]}...' - violations: {violations}")


if __name__ == "__main__":
    main()
