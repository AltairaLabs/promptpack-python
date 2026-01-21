# promptpack-langchain

LangChain integration for PromptPack.

## Installation

```bash
pip install promptpack-langchain
```

## Usage

```python
from promptpack import load_promptpack
from promptpack_langchain import PromptPackTemplate, convert_tools

# Load PromptPack
pack = load_promptpack("path/to/pack.json")
prompt = pack.prompts["assistant"]

# Create LangChain template
template = PromptPackTemplate.from_prompt(prompt)

# Use in LangChain chain
messages = template.format_messages(user_name="Alice")

# Convert tools to LangChain format
tools = convert_tools(pack.tools or {})
```

## Features

- `PromptPackTemplate` - LangChain prompt template from PromptPack prompts
- `convert_tools()` - Convert PromptPack tools to LangChain StructuredTool
- `ValidationRunnable` - Run PromptPack validators in LangChain chains
- Multimodal content conversion utilities

## License

Apache-2.0
