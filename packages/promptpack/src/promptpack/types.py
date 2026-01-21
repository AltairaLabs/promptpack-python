# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Pydantic models for PromptPack JSON schema."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class VariableValidation(BaseModel):
    """Validation rules for a variable."""

    model_config = ConfigDict(extra="forbid")

    pattern: str | None = Field(default=None, description="Regex pattern for string types")
    min_length: int | None = Field(default=None, ge=0, description="Minimum string length")
    max_length: int | None = Field(default=None, ge=1, description="Maximum string length")
    minimum: float | None = Field(default=None, description="Minimum numeric value")
    maximum: float | None = Field(default=None, description="Maximum numeric value")
    enum: list[Any] | None = Field(default=None, description="List of allowed values")


class Variable(BaseModel):
    """A template variable definition with type information and validation rules."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")
    type: Literal["string", "number", "boolean", "object", "array"]
    required: bool
    default: Any | None = None
    description: str | None = None
    example: Any | None = None
    validation: VariableValidation | None = None


class ToolParameters(BaseModel):
    """JSON Schema for tool parameters."""

    model_config = ConfigDict(extra="allow")

    type: Literal["object"] = "object"
    properties: dict[str, Any] = Field(default_factory=dict)
    required: list[str] | None = None


class Tool(BaseModel):
    """A tool definition following OpenAI's function calling format."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$")
    description: str = Field(..., min_length=1)
    parameters: ToolParameters | None = None


class ToolPolicy(BaseModel):
    """Governance policy for tool usage."""

    model_config = ConfigDict(extra="forbid")

    tool_choice: Literal["auto", "required", "none"] = "auto"
    max_rounds: int = Field(default=5, ge=1)
    max_tool_calls_per_turn: int = Field(default=10, ge=1)
    blocklist: list[str] | None = None


class MiddlewareConfig(BaseModel):
    """Configuration for a single middleware component."""

    model_config = ConfigDict(extra="forbid")

    type: str
    config: dict[str, Any] | None = None


class PipelineConfig(BaseModel):
    """Pipeline configuration for processing stages."""

    model_config = ConfigDict(extra="forbid")

    stages: list[str]
    middleware: list[MiddlewareConfig] | None = None


class Parameters(BaseModel):
    """LLM generation parameters."""

    model_config = ConfigDict(extra="forbid")

    temperature: float | None = Field(default=None, ge=0, le=2)
    max_tokens: int | None = Field(default=None, ge=1)
    top_p: float | None = Field(default=None, ge=0, le=1)
    top_k: int | None = Field(default=None, ge=1)
    frequency_penalty: float | None = Field(default=None, ge=-2, le=2)
    presence_penalty: float | None = Field(default=None, ge=-2, le=2)


class Validator(BaseModel):
    """A validation rule (guardrail) applied to LLM responses."""

    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "banned_words",
        "max_length",
        "min_length",
        "regex_match",
        "json_schema",
        "sentiment",
        "toxicity",
        "pii_detection",
        "custom",
    ]
    enabled: bool
    fail_on_violation: bool = False
    params: dict[str, Any] | None = None


class TestedModel(BaseModel):
    """Testing results for a specific model."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    date: str
    success_rate: float | None = Field(default=None, ge=0, le=1)
    avg_tokens: float | None = Field(default=None, ge=0)
    avg_cost: float | None = Field(default=None, ge=0)
    avg_latency_ms: float | None = Field(default=None, ge=0)
    notes: str | None = None


class ModelOverride(BaseModel):
    """Model-specific template modifications."""

    model_config = ConfigDict(extra="forbid")

    system_template_prefix: str | None = None
    system_template_suffix: str | None = None
    system_template: str | None = None
    parameters: Parameters | None = None


class ImageConfig(BaseModel):
    """Configuration for image content."""

    model_config = ConfigDict(extra="forbid")

    max_size_mb: int | None = Field(default=None, ge=1)
    allowed_formats: list[Literal["jpeg", "jpg", "png", "webp", "gif", "bmp"]] | None = None
    default_detail: Literal["low", "high", "auto"] | None = "auto"
    require_caption: bool = False
    max_images_per_msg: int | None = Field(default=None, ge=1)


class AudioConfig(BaseModel):
    """Configuration for audio content."""

    model_config = ConfigDict(extra="forbid")

    max_size_mb: int | None = Field(default=None, ge=1)
    allowed_formats: list[Literal["mp3", "wav", "opus", "flac", "m4a", "aac"]] | None = None
    max_duration_sec: int | None = Field(default=None, ge=1)
    require_metadata: bool = False


class VideoConfig(BaseModel):
    """Configuration for video content."""

    model_config = ConfigDict(extra="forbid")

    max_size_mb: int | None = Field(default=None, ge=1)
    allowed_formats: list[Literal["mp4", "webm", "mov", "avi", "mkv"]] | None = None
    max_duration_sec: int | None = Field(default=None, ge=1)
    require_metadata: bool = False


class DocumentConfig(BaseModel):
    """Configuration for document content."""

    model_config = ConfigDict(extra="forbid")

    max_size_mb: int | None = Field(default=None, ge=1)
    allowed_formats: list[str] | None = None
    max_pages: int | None = Field(default=None, ge=1)
    require_metadata: bool = False
    extraction_mode: Literal["text", "structured", "raw"] | None = "text"


class GenericMediaTypeConfig(BaseModel):
    """Generic configuration for custom media types."""

    model_config = ConfigDict(extra="allow")

    max_size_mb: int | None = Field(default=None, ge=1)
    allowed_formats: list[str] | None = None
    require_metadata: bool = False
    validation_params: dict[str, Any] | None = None


class MediaReference(BaseModel):
    """Reference to a media file."""

    model_config = ConfigDict(extra="forbid")

    file_path: str | None = None
    url: str | None = None
    base64: str | None = None
    mime_type: str
    detail: Literal["low", "high", "auto"] | None = None
    caption: str | None = None


class ContentPart(BaseModel):
    """A single content part within a multimodal message."""

    model_config = ConfigDict(extra="forbid")

    type: str = Field(..., pattern=r"^[a-z0-9_]+$")
    text: str | None = None
    media: MediaReference | None = None


class MultimodalExample(BaseModel):
    """Example multimodal message."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None
    role: Literal["user", "assistant", "system"]
    parts: list[ContentPart] = Field(..., min_length=1)


class MediaConfig(BaseModel):
    """Configuration for multimodal content support."""

    model_config = ConfigDict(extra="allow")

    enabled: bool
    supported_types: list[str] | None = None
    image: ImageConfig | None = None
    audio: AudioConfig | None = None
    video: VideoConfig | None = None
    document: DocumentConfig | None = None
    examples: list[MultimodalExample] | None = None


class Prompt(BaseModel):
    """A single prompt configuration within a pack."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., pattern=r"^[a-z][a-z0-9_-]*$")
    name: str = Field(..., min_length=1)
    description: str | None = None
    version: str = Field(
        ...,
        pattern=r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    )
    system_template: str = Field(..., min_length=1)
    variables: list[Variable] | None = None
    tools: list[str] | None = None
    tool_policy: ToolPolicy | None = None
    pipeline: PipelineConfig | None = None
    parameters: Parameters | None = None
    validators: list[Validator] | None = None
    tested_models: list[TestedModel] | None = None
    model_overrides: dict[str, ModelOverride] | None = None
    media: MediaConfig | None = None

    def get_variable(self, name: str) -> Variable | None:
        """Get a variable by name."""
        if self.variables is None:
            return None
        for var in self.variables:
            if var.name == name:
                return var
        return None


class TemplateEngine(BaseModel):
    """Template engine configuration."""

    model_config = ConfigDict(extra="forbid")

    version: str
    syntax: str
    features: (
        list[Literal["basic_substitution", "fragments", "conditionals", "loops", "filters"]] | None
    ) = None


class Compilation(BaseModel):
    """Information about pack compilation."""

    model_config = ConfigDict(extra="forbid")

    compiled_with: str
    created_at: str
    schema_version: str = Field(..., alias="schema")
    source: str | None = None


class CostEstimate(BaseModel):
    """Cost estimation for pack usage."""

    model_config = ConfigDict(extra="forbid")

    min_cost_usd: float | None = Field(default=None, ge=0)
    max_cost_usd: float | None = Field(default=None, ge=0)
    avg_cost_usd: float | None = Field(default=None, ge=0)


class PackMetadata(BaseModel):
    """Pack-level metadata."""

    model_config = ConfigDict(extra="allow")

    domain: str | None = None
    language: str | None = Field(default=None, pattern=r"^[a-z]{2}$")
    tags: list[str] | None = None
    cost_estimate: CostEstimate | None = None


class PromptPack(BaseModel):
    """Top-level PromptPack container."""

    model_config = ConfigDict(extra="forbid")

    schema_url: str | None = Field(default=None, alias="$schema")
    id: str = Field(..., pattern=r"^[a-z][a-z0-9-]*$", min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=200)
    version: str = Field(
        ...,
        pattern=r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    )
    description: str | None = Field(default=None, max_length=5000)
    template_engine: TemplateEngine
    prompts: dict[str, Prompt] = Field(..., min_length=1)
    fragments: dict[str, str] | None = None
    tools: dict[str, Tool] | None = None
    metadata: PackMetadata | None = None
    compilation: Compilation | None = None

    def get_prompt(self, name: str) -> Prompt | None:
        """Get a prompt by name."""
        return self.prompts.get(name)

    def get_tool(self, name: str) -> Tool | None:
        """Get a tool by name."""
        if self.tools is None:
            return None
        return self.tools.get(name)

    def get_fragment(self, name: str) -> str | None:
        """Get a fragment by name."""
        if self.fragments is None:
            return None
        return self.fragments.get(name)

    def get_tools_for_prompt(self, prompt_name: str) -> list[Tool]:
        """Get the list of tools available for a specific prompt."""
        prompt = self.get_prompt(prompt_name)
        if prompt is None or prompt.tools is None or self.tools is None:
            return []

        tools = []
        blocklist = set()
        if prompt.tool_policy and prompt.tool_policy.blocklist:
            blocklist = set(prompt.tool_policy.blocklist)

        for tool_name in prompt.tools:
            if tool_name in blocklist:
                continue
            tool = self.tools.get(tool_name)
            if tool is not None:
                tools.append(tool)

        return tools
