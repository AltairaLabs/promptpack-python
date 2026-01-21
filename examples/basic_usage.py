#!/usr/bin/env python3
# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""
Basic usage example for promptpack-langchain.

This example shows the core PromptPack workflow:
1. Load a pack from JSON
2. Create a template
3. Use it in a LangChain chain

To run this example:
    export OPENAI_API_KEY=your-key-here
    python examples/basic_usage.py
"""

from pathlib import Path

from promptpack import parse_promptpack
from promptpack_langchain import PromptPackTemplate


def main() -> None:
    """Run basic usage example."""
    print("=== Basic PromptPack Usage ===\n")

    # 1. Load PromptPack from JSON file
    pack_path = Path(__file__).parent / "packs" / "customer-support.json"
    pack = parse_promptpack(pack_path)

    print(f"Loaded pack: {pack.name} (v{pack.version})")
    print(f"Available prompts: {list(pack.prompts.keys())}")

    # 2. Create a template from the pack
    template = PromptPackTemplate.from_promptpack(pack, "support")

    print("\n--- Template Metadata ---")
    print(f"Input variables: {template.input_variables}")
    print(f"Parameters: {template.get_parameters()}")

    # 3. Format the template (without calling the LLM)
    formatted = template.format(role="customer support agent", issue_type="billing")
    print("\n--- Formatted System Prompt ---")
    print(formatted)

    # 4. (Optional) Use with LangChain to make actual API calls
    # Uncomment the following to use with OpenAI:
    #
    # model = ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=template.get_parameters().get("temperature", 0.7),
    # )
    #
    # # Create a chat template and invoke
    # chat_template = template.to_chat_prompt_template(
    #     role="customer support agent",
    #     issue_type="billing",
    # )
    # chain = chat_template | model
    #
    # response = chain.invoke({
    #     "messages": [("human", "I was charged twice for my subscription")]
    # })
    # print("\n--- LLM Response ---")
    # print(response.content)

    # 5. Use the escalation template
    print("\n\n--- Escalation Template ---")
    escalation_template = PromptPackTemplate.from_promptpack(pack, "escalation")
    formatted_escalation = escalation_template.format(
        issue_type="billing",
        customer_tier="enterprise",
    )
    print(formatted_escalation)


if __name__ == "__main__":
    main()
