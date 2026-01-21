---
title: Validation
description: Validating LLM outputs with PromptPack validators
sidebar:
  order: 4
---

PromptPack includes a powerful validation system for checking LLM outputs against rules like banned words, length limits, and regex patterns.

## Validator Types

### Banned Words

Check for prohibited words in content:

```python
from promptpack import Validator
from promptpack_langchain import run_validators

validators = [
    Validator(
        type="banned_words",
        enabled=True,
        fail_on_violation=True,  # Blocking violation
        params={"words": ["inappropriate", "offensive", "banned"]}
    )
]

result = run_validators("This is appropriate content", validators)
print(result.is_valid)  # True

result = run_validators("This is inappropriate", validators)
print(result.is_valid)  # False
print(result.violations[0].message)
# "Content contains banned words: ['inappropriate']"
```

### Length Validators

Enforce minimum and maximum content length:

```python
validators = [
    Validator(
        type="max_length",
        enabled=True,
        fail_on_violation=False,  # Non-blocking warning
        params={"max_characters": 500}
    ),
    Validator(
        type="min_length",
        enabled=True,
        fail_on_violation=False,
        params={"min_characters": 10}
    )
]

result = run_validators("Hi", validators)
print(result.is_valid)  # True (non-blocking)
print(result.violations[0].message)
# "Content below min length: 2 < 10"
```

### Regex Patterns

Validate content against regex patterns:

```python
validators = [
    # Content MUST match this pattern
    Validator(
        type="regex_match",
        enabled=True,
        fail_on_violation=True,
        params={
            "pattern": r"^[A-Z]",  # Must start with capital
            "must_match": True
        }
    ),
    # Content must NOT match this pattern
    Validator(
        type="regex_match",
        enabled=True,
        fail_on_violation=False,
        params={
            "pattern": r"password|secret",  # Forbidden words
            "must_match": False
        }
    )
]

# Passes - starts with capital, no forbidden words
result = run_validators("Hello, how can I help?", validators)
print(result.is_valid)  # True

# Fails - doesn't start with capital
result = run_validators("hello there", validators)
print(result.is_valid)  # False
```

## Blocking vs Non-Blocking Violations

Validators can be configured as blocking or non-blocking:

```python
validators = [
    Validator(
        type="banned_words",
        enabled=True,
        fail_on_violation=True,  # BLOCKING - is_valid will be False
        params={"words": ["bad"]}
    ),
    Validator(
        type="max_length",
        enabled=True,
        fail_on_violation=False,  # NON-BLOCKING - is_valid stays True
        params={"max_characters": 10}
    )
]

result = run_validators("This is way too long", validators)

# Non-blocking violation only
print(result.is_valid)  # True
print(result.has_blocking_violations)  # False
print(len(result.violations))  # 1

result = run_validators("This is bad", validators)

# Blocking violation
print(result.is_valid)  # False
print(result.has_blocking_violations)  # True
```

## ValidationRunnable

Use `ValidationRunnable` in LangChain chains:

```python
from promptpack_langchain import ValidationRunnable

validators = [
    Validator(
        type="banned_words",
        enabled=True,
        fail_on_violation=True,
        params={"words": ["inappropriate"]}
    )
]

runnable = ValidationRunnable(validators)

# Sync
result = runnable.invoke("Check this content")

# Async
result = await runnable.ainvoke("Check this content")

if not result.is_valid:
    print("Validation failed!")
    for v in result.violations:
        print(f"  - {v.validator_type}: {v.message}")
```

## Defining Validators in PromptPack

Validators can be defined directly in your PromptPack JSON:

```json
{
  "prompts": {
    "support": {
      "system_template": "You are a support agent...",
      "validators": [
        {
          "type": "banned_words",
          "enabled": true,
          "fail_on_violation": true,
          "params": {
            "words": ["inappropriate", "offensive"]
          }
        },
        {
          "type": "max_length",
          "enabled": true,
          "fail_on_violation": false,
          "params": {
            "max_characters": 2000
          }
        }
      ]
    }
  }
}
```

Then access them from the prompt:

```python
from promptpack import parse_promptpack
from promptpack_langchain import run_validators

pack = parse_promptpack("pack.json")
prompt = pack.get_prompt("support")

# Get validators from the prompt
validators = prompt.validators

# Validate LLM output
llm_response = "Here is the response..."
result = run_validators(llm_response, validators)
```

## Complete Example

```python
#!/usr/bin/env python3
from promptpack import Validator
from promptpack_langchain import ValidationRunnable, run_validators


def main():
    # Create validators
    validators = [
        Validator(
            type="banned_words",
            enabled=True,
            fail_on_violation=True,
            params={"words": ["inappropriate", "offensive"]}
        ),
        Validator(
            type="max_length",
            enabled=True,
            fail_on_violation=False,
            params={"max_characters": 500}
        ),
        Validator(
            type="min_length",
            enabled=True,
            fail_on_violation=False,
            params={"min_characters": 10}
        ),
    ]

    # Test cases
    test_contents = [
        "This is a helpful response.",  # Valid
        "This is inappropriate.",        # Banned word
        "Hi",                            # Too short
        "x" * 600,                       # Too long
    ]

    for content in test_contents:
        result = run_validators(content, validators)
        status = "PASS" if result.is_valid else "FAIL"
        print(f"[{status}] '{content[:30]}...'")

        for v in result.violations:
            print(f"  - {v.validator_type}: {v.message}")


if __name__ == "__main__":
    main()
```

Output:
```
[PASS] 'This is a helpful response....'
[FAIL] 'This is inappropriate....'
  - banned_words: Content contains banned words: ['inappropriate']
[PASS] 'Hi...'
  - min_length: Content below min length: 2 < 10
[PASS] 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...'
  - max_length: Content exceeds max length: 600 > 500
```
