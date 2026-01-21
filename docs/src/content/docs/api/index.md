---
title: API Reference
description: API reference for PromptPack Python libraries
sidebar:
  order: 1
---

## promptpack

### Functions

#### `parse_promptpack(path: str | Path) -> PromptPack`

Parse a PromptPack from a file path.

**Arguments:**
- `path` - Path to the PromptPack JSON file

**Returns:** `PromptPack` instance

**Raises:** `PromptPackError` on parse failure

#### `parse_promptpack_from_dict(data: dict) -> PromptPack`

Parse a PromptPack from a dictionary.

**Arguments:**
- `data` - Dictionary containing PromptPack data

**Returns:** `PromptPack` instance

### Classes

#### `PromptPack`

Main class representing a parsed PromptPack.

**Attributes:**
- `name: str` - Pack name
- `version: str` - Pack version
- `prompts: dict[str, Prompt]` - Dictionary of prompts
- `tools: list[Tool]` - List of tool definitions
- `fragments: dict[str, str]` - Reusable fragments

#### `Prompt`

Represents a prompt definition.

**Attributes:**
- `system_template: str | None` - System message template
- `user_template: str | None` - User message template
- `variables: dict[str, Variable]` - Variable definitions

**Methods:**
- `render(variables: dict) -> str` - Render template with variables

#### `Variable`

Represents a template variable.

**Attributes:**
- `type: str` - Variable type (string, number, boolean, etc.)
- `description: str | None` - Variable description
- `default: Any` - Default value
- `required: bool` - Whether variable is required

#### `Tool`

Represents a tool definition.

**Attributes:**
- `name: str` - Tool name
- `description: str` - Tool description
- `parameters: dict` - JSON Schema for parameters

---

## promptpack-langchain

### Functions

#### `convert_tools(pack: PromptPack) -> list[Tool]`

Convert PromptPack tools to LangChain tool definitions.

**Arguments:**
- `pack` - PromptPack instance

**Returns:** List of LangChain tool definitions

### Classes

#### `PromptPackTemplate`

LangChain prompt template wrapper for PromptPacks.

**Class Methods:**
- `from_promptpack(pack: PromptPack, prompt_name: str) -> PromptPackTemplate`

**Attributes:**
- `chat_template: ChatPromptTemplate` - Underlying LangChain template
- `input_variables: list[str]` - List of input variable names

**Methods:**
- `format_messages(**kwargs) -> list[BaseMessage]` - Format messages with variables

### Validators

#### `validate_variables(variables: dict[str, Variable], inputs: dict) -> list[str]`

Validate input variables against definitions.

**Arguments:**
- `variables` - Variable definitions from PromptPack
- `inputs` - Input values to validate

**Returns:** List of validation error messages (empty if valid)

### Multimodal

#### `process_multimodal_content(content: dict) -> Any`

Process multimodal content for LangChain compatibility.

**Arguments:**
- `content` - Content dictionary with type information

**Returns:** Processed content suitable for LangChain
