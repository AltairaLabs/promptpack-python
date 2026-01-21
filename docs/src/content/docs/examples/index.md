---
title: Examples Overview
description: Learn how to use PromptPack Python through practical examples
sidebar:
  order: 1
---

This section contains practical examples demonstrating how to use PromptPack Python in real-world scenarios.

## Available Examples

### [Basic Usage](/promptpack-python/examples/basic-usage/)
Learn the fundamentals of loading PromptPacks, creating templates, and formatting prompts with variables and fragments.

### [Tools Integration](/promptpack-python/examples/tools/)
Discover how to convert PromptPack tools to LangChain format, bind custom handlers, and use tools with agents.

### [Validation](/promptpack-python/examples/validation/)
Explore the validation system including banned words, length limits, and regex pattern matching.

## Running the Examples

All examples are located in the `examples/` directory of the repository. To run them:

```bash
# Clone the repository
git clone https://github.com/AltairaLabs/promptpack-python.git
cd promptpack-python

# Install dependencies
pip install -e packages/promptpack
pip install -e packages/promptpack-langchain

# Run an example
python examples/basic_usage.py
python examples/tools_example.py
python examples/validation_example.py
```

## Example Packs

The examples use PromptPack JSON files located in `examples/packs/`:

- **customer-support.json** - Customer support prompts with fragments, validators, and multiple prompt types
- **sales-assistant.json** - Sales assistant with CRM tools (customer lookup, inventory, orders)
