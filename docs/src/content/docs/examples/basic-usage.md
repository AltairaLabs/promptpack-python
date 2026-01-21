---
title: Basic Usage
description: Getting started with PromptPack Python
sidebar:
  order: 2
---

This example demonstrates the core PromptPack workflow: loading packs, creating templates, and formatting prompts.

## Loading a PromptPack

```python
from pathlib import Path
from promptpack import parse_promptpack

# Load from a file
pack = parse_promptpack("path/to/pack.json")

# Or parse from a string
from promptpack import parse_promptpack_string

pack_json = '{"id": "my-pack", ...}'
pack = parse_promptpack_string(pack_json)
```

## Creating Templates

Use `PromptPackTemplate` to create LangChain-compatible templates:

```python
from promptpack_langchain import PromptPackTemplate

# Create a template from a specific prompt in the pack
template = PromptPackTemplate.from_promptpack(pack, "support")

# Check input variables
print(template.input_variables)  # ['role', 'company']

# Get LLM parameters
params = template.get_parameters()
print(params)  # {'temperature': 0.7, 'max_tokens': 1500}
```

## Formatting Prompts

Format the template with your variables:

```python
# Format with variables
formatted = template.format(
    role="customer support agent",
    issue_type="billing"
)

print(formatted)
```

Output:
```
You are a customer support agent assistant for TechCorp.

# Company Context
TechCorp provides cloud infrastructure, SaaS products, and enterprise solutions.

# Your Role
Handle billing customer inquiries effectively.

# Guidelines
Maintain a professional yet friendly tone. Be concise and solution-oriented.
```

## Using Fragments

PromptPacks support reusable fragments that are automatically resolved:

```json
{
  "fragments": {
    "company_context": "TechCorp provides cloud infrastructure...",
    "tone_guidelines": "Maintain a professional yet friendly tone..."
  },
  "prompts": {
    "support": {
      "system_template": "{{fragment:company_context}}\n\n{{fragment:tone_guidelines}}"
    }
  }
}
```

Fragments are resolved automatically when you call `template.format()`.

## Model Overrides

Templates can have model-specific configurations:

```python
# Create template with model-specific overrides
template = PromptPackTemplate.from_promptpack(
    pack,
    "support",
    model_name="gpt-4"
)

# The template and parameters will use GPT-4 specific settings
params = template.get_parameters()
```

## Using with LangChain

Convert to a ChatPromptTemplate for use with LangChain:

```python
from langchain_openai import ChatOpenAI

# Create chat template
chat_template = template.to_chat_prompt_template(
    role="support agent",
    company="Acme Corp"
)

# Create chain
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=template.get_parameters().get("temperature", 0.7)
)

chain = chat_template | model

# Invoke
response = chain.invoke({
    "messages": [("human", "I was charged twice for my subscription")]
})

print(response.content)
```

## Complete Example

Here's the complete `basic_usage.py` example:

```python
#!/usr/bin/env python3
from pathlib import Path

from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate


def main():
    # Load PromptPack
    pack_path = Path(__file__).parent / "packs" / "customer-support.json"
    pack = parse_promptpack(pack_path)

    print(f"Loaded pack: {pack.name} (v{pack.version})")
    print(f"Available prompts: {list(pack.prompts.keys())}")

    # Create template
    template = PromptPackTemplate.from_promptpack(pack, "support")
    print(f"Input variables: {template.input_variables}")
    print(f"Parameters: {template.get_parameters()}")

    # Format
    formatted = template.format(
        role="customer support agent",
        issue_type="billing"
    )
    print(formatted)


if __name__ == "__main__":
    main()
```
