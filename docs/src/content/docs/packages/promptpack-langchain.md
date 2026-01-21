---
title: promptpack-langchain
description: LangChain integration for PromptPacks
sidebar:
  order: 2
---

The `promptpack-langchain` package provides seamless integration between PromptPacks and LangChain. It converts PromptPack definitions into LangChain-compatible prompt templates and tools.

## Installation

```bash
pip install promptpack-langchain
```

This will also install the base `promptpack` library as a dependency.

## Features

- Convert PromptPacks to LangChain ChatPromptTemplate
- Convert PromptPack tools to LangChain tool definitions
- Support for multimodal content (images)
- Variable validation and type coercion
- Compatible with LangChain agents and chains

## PromptPackTemplate

Create LangChain prompt templates from PromptPacks:

```python
from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate

pack = parse_promptpack("pack.json")

# Create template for a specific prompt
template = PromptPackTemplate.from_promptpack(pack, "support")

# Format messages
messages = template.format_messages(
    role="support agent",
    company="Acme Inc."
)

# Use with LangChain LLM
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
response = llm.invoke(messages)
```

### Accessing the Underlying Template

```python
# Get the LangChain ChatPromptTemplate
chat_template = template.chat_template

# Get input variables
print(template.input_variables)  # ['role', 'company']
```

## Tool Conversion

Convert PromptPack tools to LangChain format:

```python
from promptpack import parse_promptpack
from promptpack_langchain import convert_tools

pack = parse_promptpack("pack.json")

# Convert all tools
tools = convert_tools(pack)

# Use with an agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

llm = ChatOpenAI()
template = PromptPackTemplate.from_promptpack(pack, "agent")

agent = create_tool_calling_agent(llm, tools, template.chat_template)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "Search for Python tutorials"})
```

### Custom Tool Implementations

The converted tools need implementations to be functional:

```python
from promptpack_langchain import convert_tools
from langchain.tools import StructuredTool

# Get tool definitions
tool_defs = convert_tools(pack)

# Create implementations
def search_docs(query: str) -> str:
    # Your implementation
    return f"Results for: {query}"

# Create functional tool
search_tool = StructuredTool.from_function(
    func=search_docs,
    name="search_docs",
    description=tool_defs[0].description,
    args_schema=tool_defs[0].args_schema
)
```

## Multimodal Support

Handle multimodal content including images:

```python
from promptpack_langchain import PromptPackTemplate
from promptpack_langchain.multimodal import process_multimodal_content

# Process content with images
content = process_multimodal_content({
    "type": "image_url",
    "image_url": {"url": "https://example.com/image.png"}
})
```

## Validators

Validate inputs against PromptPack variable definitions:

```python
from promptpack_langchain.validators import validate_variables

# Validate input variables
errors = validate_variables(
    variables=prompt.variables,
    inputs={"role": "agent", "company": "Acme"}
)

if errors:
    for error in errors:
        print(f"Validation error: {error}")
```

## Integration Example

Complete example using PromptPack with LangChain:

```python
from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate, convert_tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Load PromptPack
pack = parse_promptpack("agent.json")

# Create template and tools
template = PromptPackTemplate.from_promptpack(pack, "main")
tools = convert_tools(pack)

# Set up LLM
llm = ChatOpenAI(model="gpt-4")

# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=template.chat_template
)

# Create executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# Run
result = executor.invoke({
    "input": "Help me find information about Python",
    "role": "assistant",
    "company": "TechCorp"
})

print(result["output"])
```
