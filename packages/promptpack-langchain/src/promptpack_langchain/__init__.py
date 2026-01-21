# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""PromptPack LangChain integration."""

from promptpack_langchain.multimodal import convert_content_parts, create_multimodal_message
from promptpack_langchain.template import PromptPackTemplate
from promptpack_langchain.tools import convert_tool, convert_tools
from promptpack_langchain.validators import ValidationResult, ValidationRunnable, run_validators

__version__ = "0.1.0"

__all__ = [
    # Template
    "PromptPackTemplate",
    # Tools
    "convert_tool",
    "convert_tools",
    # Validators
    "ValidationRunnable",
    "ValidationResult",
    "run_validators",
    # Multimodal
    "convert_content_parts",
    "create_multimodal_message",
]
