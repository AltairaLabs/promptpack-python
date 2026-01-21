---
title: Tools Integration
description: Using PromptPack tools with LangChain
sidebar:
  order: 3
---

This example shows how to convert PromptPack tools to LangChain format and use them with agents.

## Defining Tools in PromptPack

Tools are defined in your PromptPack JSON:

```json
{
  "tools": {
    "lookup_customer": {
      "name": "lookup_customer",
      "description": "Look up customer information by ID",
      "parameters": {
        "type": "object",
        "properties": {
          "customer_id": {
            "type": "string",
            "description": "The unique customer ID"
          }
        },
        "required": ["customer_id"]
      }
    }
  },
  "prompts": {
    "sales": {
      "tools": ["lookup_customer", "check_inventory"],
      "tool_policy": {
        "tool_choice": "auto",
        "max_rounds": 5,
        "blocklist": ["dangerous_tool"]
      }
    }
  }
}
```

## Converting Tools

Convert PromptPack tools to LangChain format:

```python
from promptpack import parse_promptpack
from promptpack_langchain import convert_tools

pack = parse_promptpack("sales-assistant.json")

# Convert all tools
all_tools = convert_tools(pack)

# Convert tools for a specific prompt (respects blocklist)
prompt_tools = convert_tools(pack, prompt_name="sales")

print(f"Tools: {[t.name for t in prompt_tools]}")
```

## Adding Tool Handlers

Tools need handlers to execute. Provide them when converting:

```python
def lookup_customer(customer_id: str) -> str:
    """Look up customer by ID."""
    # Your implementation here
    return json.dumps({"id": customer_id, "name": "Alice"})

def check_inventory(product_id: str) -> str:
    """Check inventory for a product."""
    return json.dumps({"product_id": product_id, "in_stock": True})

# Map tool names to handlers
handlers = {
    "lookup_customer": lookup_customer,
    "check_inventory": check_inventory,
}

# Convert with handlers
tools = convert_tools(pack, prompt_name="sales", handlers=handlers)

# Now tools are executable
result = tools[0].invoke({"customer_id": "CUST-001"})
print(result)  # {"id": "CUST-001", "name": "Alice"}
```

## Tool Filtering

Prompts can specify which tools are available and blocklisted:

```python
# Sales prompt has all tools
sales_tools = convert_tools(pack, prompt_name="sales", handlers=handlers)
print([t.name for t in sales_tools])
# ['lookup_customer', 'check_inventory', 'create_order', 'calculate_discount']

# Inquiry prompt has limited tools (read-only, create_order blocklisted)
inquiry_tools = convert_tools(pack, prompt_name="inquiry", handlers=handlers)
print([t.name for t in inquiry_tools])
# ['lookup_customer', 'check_inventory', 'check_order_status']
```

## Using with LangChain Agents

Bind tools to an LLM and create an agent:

```python
from langchain_openai import ChatOpenAI
from promptpack_langchain import PromptPackTemplate

# Create template and tools
template = PromptPackTemplate.from_promptpack(pack, "sales")
tools = convert_tools(pack, prompt_name="sales", handlers=handlers)

# Create model with tools
model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# Create chat template
chat_template = template.to_chat_prompt_template(company="Acme Corp")

# Build chain
chain = chat_template | model

# Invoke
response = chain.invoke({
    "messages": [("human", "Can you look up customer CUST-001?")]
})

# Handle tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        tool = next(t for t in tools if t.name == tool_call['name'])
        result = tool.invoke(tool_call['args'])
        print(f"Tool: {tool_call['name']}, Result: {result}")
```

## Complete Example

Here's a complete tools example with a mock database:

```python
#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any

from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate, convert_tools

# Mock database
MOCK_DB = {
    "customers": {
        "CUST-001": {"id": "CUST-001", "name": "Alice", "tier": "premium"},
    },
    "products": [
        {"id": "PROD-001", "name": "Laptop", "price": 1299},
    ],
}


def lookup_customer(customer_id: str, email: str | None = None) -> str:
    customer = MOCK_DB["customers"].get(customer_id)
    if not customer:
        return json.dumps({"error": "Customer not found"})
    return json.dumps(customer)


def check_inventory(product_id: str, warehouse: str | None = None) -> str:
    for product in MOCK_DB["products"]:
        if product["id"] == product_id:
            return json.dumps({**product, "in_stock": True, "quantity": 50})
    return json.dumps({"error": "Product not found"})


HANDLERS = {
    "lookup_customer": lookup_customer,
    "check_inventory": check_inventory,
}


def main():
    pack = parse_promptpack("examples/packs/sales-assistant.json")

    # Create template
    template = PromptPackTemplate.from_promptpack(pack, "sales")
    print(template.format(company="Acme Corp"))

    # Convert tools with handlers
    tools = convert_tools(pack, prompt_name="sales", handlers=HANDLERS)

    # Execute a tool
    lookup_tool = next(t for t in tools if t.name == "lookup_customer")
    result = lookup_tool.invoke({"customer_id": "CUST-001"})
    print(f"Customer lookup: {result}")


if __name__ == "__main__":
    main()
```
