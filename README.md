# PromptPack Python

Python libraries for parsing and using PromptPacks.

## Packages

This monorepo contains the following packages:

### `promptpack`

Base library for parsing PromptPack JSON files. No framework dependencies.

```bash
pip install promptpack
```

```python
from promptpack import PromptPack, parse_promptpack

# Parse from file
pack = parse_promptpack("path/to/pack.json")

# Access prompts
prompt = pack.prompts["support"]
print(prompt.system_template)

# Render template with variables
rendered = prompt.render({"role": "support agent", "company": "Acme"})
```

### `promptpack-langchain`

LangChain integration for PromptPacks.

```bash
pip install promptpack-langchain
```

```python
from promptpack_langchain import PromptPackTemplate, convert_tools

# Create LangChain prompt template
template = PromptPackTemplate.from_promptpack(pack, "support")

# Convert tools to LangChain format
tools = convert_tools(pack)
```

## Development

### Setup

```bash
# Install development dependencies
pip install hatch

# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Lint and format
hatch run lint
hatch run format

# Type checking
hatch run typecheck
```

## License

Apache License 2.0
