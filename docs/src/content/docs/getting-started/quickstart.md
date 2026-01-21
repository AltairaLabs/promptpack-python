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

# Access prompts
prompt = pack.prompts["support"]
print(prompt.system_template)
```

### Rendering Templates

```python
from promptpack import parse_promptpack

pack = parse_promptpack("path/to/pack.json")
prompt = pack.prompts["support"]

# Render template with variables
rendered = prompt.render({
    "role": "support agent",
    "company": "Acme Inc."
})

print(rendered)
```

## LangChain Integration

### Creating Prompt Templates

```python
from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate

pack = parse_promptpack("path/to/pack.json")

# Create LangChain prompt template
template = PromptPackTemplate.from_promptpack(pack, "support")

# Use with LangChain
messages = template.format_messages(
    role="support agent",
    company="Acme Inc."
)
```

### Converting Tools

```python
from promptpack import parse_promptpack
from promptpack_langchain import convert_tools

pack = parse_promptpack("path/to/pack.json")

# Convert tools to LangChain format
tools = convert_tools(pack)

# Use with LangChain agent
from langchain.agents import create_tool_calling_agent
agent = create_tool_calling_agent(llm, tools, prompt)
```

## Example PromptPack

Here's an example PromptPack JSON file:

```json
{
  "version": "1.0",
  "name": "support-agent",
  "prompts": {
    "support": {
      "system": "You are a {{role}} at {{company}}. Help customers with their questions.",
      "variables": {
        "role": {
          "type": "string",
          "description": "The role of the agent"
        },
        "company": {
          "type": "string",
          "description": "The company name"
        }
      }
    }
  },
  "tools": [
    {
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
  ]
}
```
