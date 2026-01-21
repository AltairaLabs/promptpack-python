---
title: Quickstart
description: Get started with PromptPack Python in minutes
sidebar:
  order: 2
---

## Basic Usage

### Parsing a PromptPack

```python
from promptpack import parse_promptpack

# Parse from file
pack = parse_promptpack("path/to/pack.json")

# Access pack metadata
print(f"Pack: {pack.name} v{pack.version}")
print(f"Prompts: {list(pack.prompts.keys())}")

# Access a specific prompt
prompt = pack.get_prompt("support")
print(prompt.system_template)
```

### Using with LangChain

```python
from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate

pack = parse_promptpack("path/to/pack.json")

# Create LangChain prompt template
template = PromptPackTemplate.from_promptpack(pack, "support")

# Check input variables and parameters
print(template.input_variables)  # ['role', 'company']
print(template.get_parameters())  # {'temperature': 0.7, 'max_tokens': 1500}

# Format the template
formatted = template.format(
    role="support agent",
    company="Acme Inc."
)
print(formatted)
```

## Converting Tools

```python
from promptpack import parse_promptpack
from promptpack_langchain import convert_tools

pack = parse_promptpack("path/to/pack.json")

# Define tool handlers
def lookup_customer(customer_id: str) -> str:
    return f"Customer: {customer_id}"

handlers = {"lookup_customer": lookup_customer}

# Convert tools to LangChain format with handlers
tools = convert_tools(pack, prompt_name="sales", handlers=handlers)

# Execute a tool
result = tools[0].invoke({"customer_id": "CUST-001"})
print(result)
```

## Validating Output

```python
from promptpack import Validator
from promptpack_langchain import run_validators

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
    )
]

# Validate LLM output
result = run_validators("Here is my response...", validators)

if result.is_valid:
    print("Output is valid!")
else:
    for v in result.violations:
        print(f"Violation: {v.message}")
```

## Example PromptPack

Here's an example PromptPack JSON file:

```json
{
  "$schema": "https://promptpack.org/schema/v1.0/promptpack.schema.json",
  "id": "customer-support",
  "name": "Customer Support Pack",
  "version": "1.0.0",
  "template_engine": {
    "version": "v1",
    "syntax": "{{variable}}"
  },
  "fragments": {
    "guidelines": "Be helpful and professional. Always verify customer identity."
  },
  "prompts": {
    "support": {
      "id": "support",
      "name": "Support Agent",
      "version": "1.0.0",
      "system_template": "You are a {{role}} at {{company}}.\n\n{{fragment:guidelines}}",
      "variables": [
        {
          "name": "role",
          "type": "string",
          "required": true,
          "description": "The role of the agent"
        },
        {
          "name": "company",
          "type": "string",
          "required": true,
          "description": "The company name"
        }
      ],
      "parameters": {
        "temperature": 0.7,
        "max_tokens": 1500
      },
      "validators": [
        {
          "type": "banned_words",
          "enabled": true,
          "fail_on_violation": true,
          "params": {"words": ["inappropriate"]}
        }
      ]
    }
  },
  "tools": {
    "search_docs": {
      "name": "search_docs",
      "description": "Search the documentation",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query"
          }
        },
        "required": ["query"]
      }
    }
  }
}
```

## Next Steps

- Check out the [Examples](/promptpack-python/examples/) for more detailed usage patterns
- Learn about [Tools Integration](/promptpack-python/examples/tools/) for agent workflows
- Explore [Validation](/promptpack-python/examples/validation/) for output guardrails
