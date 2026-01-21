# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Convert PromptPack tools to LangChain tools."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langchain_core.tools import StructuredTool
from promptpack import PromptPack, Tool


def convert_tool(
    tool: Tool,
    *,
    handler: Callable[..., Any] | None = None,
) -> StructuredTool:
    """Convert a PromptPack Tool to a LangChain StructuredTool.

    Args:
        tool: The PromptPack tool definition.
        handler: Optional function to handle tool calls. If not provided,
                 a placeholder function is used that raises NotImplementedError.

    Returns:
        A LangChain StructuredTool.
    """
    # Build the argument schema from tool parameters
    args_schema = _build_args_schema(tool)

    # Use the provided handler or create a placeholder
    if handler is None:

        def placeholder_handler(**kwargs: Any) -> str:
            raise NotImplementedError(
                f"Tool '{tool.name}' has no handler configured. "
                "Provide a handler when converting the tool or use the tool manager."
            )

        handler = placeholder_handler

    return StructuredTool(
        name=tool.name,
        description=tool.description,
        args_schema=args_schema,
        func=handler,
    )


def convert_tools(
    pack: PromptPack,
    prompt_name: str | None = None,
    *,
    handlers: dict[str, Callable[..., Any]] | None = None,
) -> list[StructuredTool]:
    """Convert PromptPack tools to LangChain StructuredTools.

    Args:
        pack: The PromptPack containing tool definitions.
        prompt_name: Optional prompt name to filter tools by.
                    If provided, only tools available to that prompt are returned.
        handlers: Optional dictionary mapping tool names to handler functions.

    Returns:
        List of LangChain StructuredTools.
    """
    handlers = handlers or {}

    if prompt_name:
        # Get tools for a specific prompt
        tools = pack.get_tools_for_prompt(prompt_name)
    elif pack.tools:
        # Get all tools
        tools = list(pack.tools.values())
    else:
        tools = []

    return [convert_tool(tool, handler=handlers.get(tool.name)) for tool in tools]


def _build_args_schema(tool: Tool) -> type:
    """Build a Pydantic model for tool arguments.

    Args:
        tool: The tool definition.

    Returns:
        A Pydantic model class for the tool arguments.
    """
    from pydantic import Field, create_model

    if tool.parameters is None:
        # No parameters - return empty model
        return create_model(f"{tool.name}Args")

    properties = tool.parameters.properties
    required = set(tool.parameters.required or [])

    # Build field definitions
    fields: dict[str, Any] = {}
    for prop_name, prop_schema in properties.items():
        field_type = _json_schema_to_python_type(prop_schema)
        description = prop_schema.get("description", "")

        if prop_name in required:
            fields[prop_name] = (field_type, Field(description=description))
        else:
            default = prop_schema.get("default")
            fields[prop_name] = (
                field_type | None,
                Field(default=default, description=description),
            )

    return create_model(f"{tool.name}Args", **fields)


def _json_schema_to_python_type(schema: dict[str, Any]) -> type:
    """Convert a JSON Schema type to a Python type.

    Args:
        schema: JSON Schema property definition.

    Returns:
        Python type corresponding to the schema.
    """
    json_type = schema.get("type", "string")

    type_mapping = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    return type_mapping.get(json_type, str)
