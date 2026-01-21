#!/usr/bin/env python3
# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""
Tools integration example for promptpack-langchain.

This example shows how to use PromptPack tools with LangChain:
1. Load a pack with tool definitions
2. Convert tools to LangChain format
3. Use tools with an LLM

To run this example:
    export OPENAI_API_KEY=your-key-here
    python examples/tools_example.py
"""

import json
from pathlib import Path
from typing import Any

from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate, convert_tools

# Mock database for the example
MOCK_DB = {
    "customers": {
        "CUST-001": {
            "id": "CUST-001",
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "tier": "premium",
        },
        "CUST-002": {
            "id": "CUST-002",
            "name": "Bob Smith",
            "email": "bob@example.com",
            "tier": "standard",
        },
    },
    "products": [
        {"id": "PROD-001", "name": "Laptop Pro", "category": "computers", "price": 1299},
        {"id": "PROD-002", "name": "Wireless Mouse", "category": "accessories", "price": 29},
        {"id": "PROD-003", "name": "USB-C Cable", "category": "accessories", "price": 15},
    ],
    "orders": [],
}


def lookup_customer(customer_id: str, email: str | None = None) -> str:
    """Look up customer by ID or email."""
    customer = MOCK_DB["customers"].get(customer_id)
    if not customer:
        return json.dumps({"error": "Customer not found"})
    return json.dumps(customer)


def check_inventory(product_id: str, warehouse: str | None = None) -> str:
    """Check inventory for a product."""
    for product in MOCK_DB["products"]:
        if product["id"] == product_id:
            return json.dumps({**product, "in_stock": True, "quantity": 50})
    return json.dumps({"error": "Product not found"})


def create_order(customer_id: str, items: list[dict[str, Any]], **kwargs: Any) -> str:
    """Create a new order."""
    import time

    order = {
        "order_id": f"ORD-{int(time.time())}",
        "customer_id": customer_id,
        "items": items,
        "status": "created",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    MOCK_DB["orders"].append(order)
    return json.dumps(order)


def calculate_discount(customer_id: str, order_total: float, promo_code: str | None = None) -> str:
    """Calculate discount for a customer."""
    customer = MOCK_DB["customers"].get(customer_id)
    discount = 0.15 if customer and customer.get("tier") == "premium" else 0.05
    return json.dumps(
        {
            "discount_percentage": discount * 100,
            "discount_amount": order_total * discount,
        }
    )


def check_order_status(order_id: str) -> str:
    """Check status of an order."""
    for order in MOCK_DB["orders"]:
        if order["order_id"] == order_id:
            return json.dumps({**order, "tracking": "TRK-123456", "status": "shipped"})
    return json.dumps({"error": "Order not found"})


# Map tool names to handler functions
TOOL_HANDLERS = {
    "lookup_customer": lookup_customer,
    "check_inventory": check_inventory,
    "create_order": create_order,
    "calculate_discount": calculate_discount,
    "check_order_status": check_order_status,
}


def main() -> None:
    """Run tools integration example."""
    print("=== PromptPack Tools Integration ===\n")

    # 1. Load the sales assistant pack
    pack_path = Path(__file__).parent / "packs" / "sales-assistant.json"
    pack = parse_promptpack(pack_path)

    print(f"Loaded pack: {pack.name}")
    print(f"Available tools: {list(pack.tools.keys()) if pack.tools else []}")

    # 2. Create a template
    template = PromptPackTemplate.from_promptpack(pack, "sales")

    print("\n--- System Prompt ---")
    formatted = template.format(company="Acme Corp")
    print(formatted)

    # 3. Convert tools to LangChain format (with handlers)
    tools = convert_tools(pack, prompt_name="sales", handlers=TOOL_HANDLERS)

    print(f"\n--- Converted Tools ({len(tools)}) ---")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:50]}...")

    # 4. Demonstrate tool execution
    print("\n--- Tool Execution Demo ---")

    # Look up a customer
    lookup_tool = next(t for t in tools if t.name == "lookup_customer")
    result = lookup_tool.invoke({"customer_id": "CUST-001"})
    print(f"\nLookup customer CUST-001: {result}")

    # Check inventory
    inventory_tool = next(t for t in tools if t.name == "check_inventory")
    result = inventory_tool.invoke({"product_id": "PROD-001"})
    print(f"\nCheck inventory PROD-001: {result}")

    # Create an order
    order_tool = next(t for t in tools if t.name == "create_order")
    result = order_tool.invoke(
        {
            "customer_id": "CUST-001",
            "items": [{"product_id": "PROD-001", "quantity": 1}],
        }
    )
    print(f"\nCreate order: {result}")

    # 5. Show tool filtering for different prompts
    print("\n--- Tool Filtering by Prompt ---")

    # Sales prompt has all tools
    sales_tools = convert_tools(pack, prompt_name="sales", handlers=TOOL_HANDLERS)
    print(f"Sales prompt tools: {[t.name for t in sales_tools]}")

    # Inquiry prompt has limited tools (read-only)
    inquiry_tools = convert_tools(pack, prompt_name="inquiry", handlers=TOOL_HANDLERS)
    print(f"Inquiry prompt tools: {[t.name for t in inquiry_tools]}")

    # 6. (Optional) Use with LangChain to make actual API calls
    # Uncomment to use with OpenAI:
    #
    # from langchain_openai import ChatOpenAI
    #
    # model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
    # chat_template = template.to_chat_prompt_template(company="Acme Corp")
    # chain = chat_template | model
    #
    # response = chain.invoke({
    #     "messages": [("human", "Can you look up customer CUST-001?")]
    # })
    #
    # if response.tool_calls:
    #     for tool_call in response.tool_calls:
    #         print(f"Tool call: {tool_call['name']}({tool_call['args']})")
    #         # Execute the tool
    #         tool = next(t for t in tools if t.name == tool_call['name'])
    #         result = tool.invoke(tool_call['args'])
    #         print(f"Result: {result}")


if __name__ == "__main__":
    main()
