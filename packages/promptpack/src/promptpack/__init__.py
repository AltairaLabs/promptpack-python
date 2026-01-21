# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""PromptPack - Base library for parsing PromptPack JSON files."""

from promptpack.parser import parse_promptpack, parse_promptpack_string
from promptpack.template import TemplateEngine
from promptpack.types import (
    AudioConfig,
    ContentPart,
    DocumentConfig,
    ImageConfig,
    MediaConfig,
    MediaReference,
    ModelOverride,
    Parameters,
    PipelineConfig,
    Prompt,
    PromptPack,
    Tool,
    ToolPolicy,
    Validator,
    Variable,
    VideoConfig,
)
from promptpack.variables import validate_variable, validate_variables

__version__ = "0.1.0"

__all__ = [
    # Parser
    "parse_promptpack",
    "parse_promptpack_string",
    # Template
    "TemplateEngine",
    # Types
    "PromptPack",
    "Prompt",
    "Variable",
    "Tool",
    "ToolPolicy",
    "Parameters",
    "Validator",
    "PipelineConfig",
    "ModelOverride",
    "MediaConfig",
    "ImageConfig",
    "AudioConfig",
    "VideoConfig",
    "DocumentConfig",
    "ContentPart",
    "MediaReference",
    # Variables
    "validate_variable",
    "validate_variables",
]
