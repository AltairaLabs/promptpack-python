---
title: promptpack
description: Base library for parsing PromptPack JSON files
sidebar:
  order: 1
---

The `promptpack` package is the base library for parsing and working with PromptPack JSON files. It has no framework dependencies and can be used standalone.

## Installation

```bash
pip install promptpack
```

## Features

- Parse PromptPack JSON files with full validation
- Type-safe Pydantic models for all PromptPack structures
- Template rendering with variable substitution
- Fragment support for reusable prompt components
- Comprehensive error handling

## Core Classes

### PromptPack

The main class representing a parsed PromptPack:

```python
from promptpack import PromptPack, parse_promptpack

pack = parse_promptpack("pack.json")

# Access metadata
print(pack.name)
print(pack.version)

# Access prompts
for name, prompt in pack.prompts.items():
    print(f"{name}: {prompt.system_template}")

# Access tools
for tool in pack.tools:
    print(f"{tool.name}: {tool.description}")
```

### Prompt

Represents a single prompt definition:

```python
prompt = pack.prompts["support"]

# Access templates
print(prompt.system_template)
print(prompt.user_template)

# Access variables
for name, var in prompt.variables.items():
    print(f"{name}: {var.type} - {var.description}")

# Render with variables
rendered = prompt.render({"role": "agent", "company": "Acme"})
```

### Variable

Represents a template variable:

```python
var = prompt.variables["role"]

print(var.type)         # "string"
print(var.description)  # Variable description
print(var.default)      # Default value (if any)
print(var.required)     # Whether required
```

### Tool

Represents a tool definition:

```python
tool = pack.tools[0]

print(tool.name)        # Tool name
print(tool.description) # Tool description
print(tool.parameters)  # JSON Schema for parameters
```

## Parsing Functions

### parse_promptpack

Parse a PromptPack from a file path:

```python
from promptpack import parse_promptpack

# From file path
pack = parse_promptpack("path/to/pack.json")

# From Path object
from pathlib import Path
pack = parse_promptpack(Path("path/to/pack.json"))
```

### parse_promptpack_from_dict

Parse a PromptPack from a dictionary:

```python
from promptpack import parse_promptpack_from_dict

data = {
    "version": "1.0",
    "name": "my-pack",
    "prompts": {...},
    "tools": [...]
}

pack = parse_promptpack_from_dict(data)
```

## Error Handling

The library raises descriptive errors for invalid PromptPacks:

```python
from promptpack import parse_promptpack
from promptpack.errors import PromptPackError, ValidationError

try:
    pack = parse_promptpack("invalid.json")
except ValidationError as e:
    print(f"Validation failed: {e}")
except PromptPackError as e:
    print(f"Parse error: {e}")
```
