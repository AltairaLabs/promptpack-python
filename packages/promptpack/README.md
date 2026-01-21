# promptpack

Base library for parsing PromptPack JSON files in Python.

## Installation

```bash
pip install promptpack
```

## Usage

```python
from promptpack import load_promptpack, PromptPack

# Load from file
pack = load_promptpack("path/to/pack.json")

# Access prompts
prompt = pack.prompts["greeting"]
print(prompt.system_template)

# Render template with variables
from promptpack import render_template
rendered = render_template(prompt.system_template, {"name": "Alice"})
```

## Features

- Parse and validate PromptPack JSON files
- Template rendering with `{{variable}}` substitution
- Variable validation (type, required, min/max length)
- Fragment resolution for template composition

## License

Apache-2.0
