# PromptPack Python Examples

This directory contains example scripts demonstrating how to use the PromptPack Python library with LangChain.

## Prerequisites

Install the packages:

```bash
pip install promptpack promptpack-langchain
```

For examples that use OpenAI:

```bash
pip install langchain-openai
export OPENAI_API_KEY=your-key-here
```

## Examples

### Basic Usage (`basic_usage.py`)

Demonstrates the core PromptPack workflow:
- Loading a pack from JSON
- Creating templates
- Formatting prompts with variables
- Using fragments

```bash
python examples/basic_usage.py
```

### Tools Integration (`tools_example.py`)

Shows how to use PromptPack tools with LangChain:
- Converting PromptPack tools to LangChain format
- Binding handlers to tools
- Tool filtering by prompt
- Executing tools

```bash
python examples/tools_example.py
```

### Validation (`validation_example.py`)

Demonstrates the validation system:
- Creating validators (banned words, length limits, regex)
- Running validators on content
- Using ValidationRunnable in chains

```bash
python examples/validation_example.py
```

## Example Packs

The `packs/` directory contains example PromptPack JSON files:

- **customer-support.json**: Customer support prompts with multiple roles, fragments, and validators
- **sales-assistant.json**: Sales assistant with CRM tools (customer lookup, inventory, orders)

## Using with LangChain

Each example shows both standalone usage and integration with LangChain. To use with an actual LLM, uncomment the LangChain sections and set your API key.

Example with OpenAI:

```python
from langchain_openai import ChatOpenAI
from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate

# Load pack and create template
pack = parse_promptpack("examples/packs/customer-support.json")
template = PromptPackTemplate.from_promptpack(pack, "support")

# Create chain
model = ChatOpenAI(model="gpt-4o-mini")
chat_template = template.to_chat_prompt_template(
    role="customer support agent",
    issue_type="billing",
)
chain = chat_template | model

# Invoke
response = chain.invoke({
    "messages": [("human", "I was charged twice")]
})
print(response.content)
```
