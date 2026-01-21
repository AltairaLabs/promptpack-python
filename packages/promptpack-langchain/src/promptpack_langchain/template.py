# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""LangChain prompt template integration for PromptPack."""

from __future__ import annotations

from typing import Any

from langchain_core.prompts import BasePromptTemplate, ChatPromptTemplate
from langchain_core.prompts.chat import MessageLikeRepresentation
from pydantic import ConfigDict

from promptpack import PromptPack, Prompt
from promptpack.template import TemplateEngine as PPTemplateEngine
from promptpack.variables import validate_variables


class PromptPackTemplate(BasePromptTemplate):
    """LangChain prompt template backed by a PromptPack prompt.

    This class adapts a PromptPack prompt to the LangChain BasePromptTemplate
    interface, allowing it to be used in LangChain chains and agents.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    pack: PromptPack
    prompt: Prompt
    template_engine: PPTemplateEngine
    model_name: str | None = None

    @classmethod
    def from_promptpack(
        cls,
        pack: PromptPack,
        prompt_name: str,
        *,
        model_name: str | None = None,
    ) -> "PromptPackTemplate":
        """Create a PromptPackTemplate from a PromptPack.

        Args:
            pack: The PromptPack containing the prompt.
            prompt_name: Name of the prompt to use.
            model_name: Optional model name for model-specific overrides.

        Returns:
            A PromptPackTemplate instance.

        Raises:
            ValueError: If the prompt doesn't exist in the pack.
        """
        prompt = pack.get_prompt(prompt_name)
        if prompt is None:
            available = list(pack.prompts.keys())
            raise ValueError(
                f"Prompt '{prompt_name}' not found in pack. Available: {available}"
            )

        template_engine = PPTemplateEngine(
            syntax=pack.template_engine.syntax,
            fragments=pack.fragments,
        )

        # Determine input variables
        input_variables = []
        if prompt.variables:
            for var in prompt.variables:
                if var.required and var.default is None:
                    input_variables.append(var.name)

        return cls(
            pack=pack,
            prompt=prompt,
            template_engine=template_engine,
            model_name=model_name,
            input_variables=input_variables,
        )

    @property
    def _prompt_type(self) -> str:
        """Return the prompt type identifier."""
        return "promptpack"

    def _get_system_template(self) -> str:
        """Get the system template, applying model overrides if applicable."""
        base_template = self.prompt.system_template

        if self.model_name and self.prompt.model_overrides:
            override = self.prompt.model_overrides.get(self.model_name)
            if override:
                if override.system_template:
                    return override.system_template
                prefix = override.system_template_prefix or ""
                suffix = override.system_template_suffix or ""
                return prefix + base_template + suffix

        return base_template

    def format(self, **kwargs: Any) -> str:
        """Format the prompt template with the given variables.

        Args:
            **kwargs: Variable values to substitute.

        Returns:
            The formatted prompt string.
        """
        # Validate and apply defaults
        if self.prompt.variables:
            validated = validate_variables(
                self.prompt.variables, kwargs, strict=False
            )
        else:
            validated = kwargs

        # Get the template (with model overrides applied)
        template = self._get_system_template()

        # Render the template
        return self.template_engine.render(template, validated, strict=False)

    def format_prompt(self, **kwargs: Any) -> Any:
        """Format the prompt and return a PromptValue.

        Args:
            **kwargs: Variable values to substitute.

        Returns:
            A PromptValue containing the formatted prompt.
        """
        from langchain_core.prompt_values import StringPromptValue

        return StringPromptValue(text=self.format(**kwargs))

    async def aformat_prompt(self, **kwargs: Any) -> Any:
        """Async version of format_prompt."""
        return self.format_prompt(**kwargs)

    def to_chat_prompt_template(self, **partial_vars: Any) -> ChatPromptTemplate:
        """Convert to a ChatPromptTemplate with the system message.

        Args:
            **partial_vars: Variables to partially fill in.

        Returns:
            A ChatPromptTemplate with the system prompt configured.
        """
        # Format the system message with any partial variables
        system_content = self.format(**partial_vars) if partial_vars else None

        messages: list[MessageLikeRepresentation] = []

        if system_content:
            messages.append(("system", system_content))
        else:
            # Include system template for later formatting
            template = self._get_system_template()
            messages.append(("system", template))

        # Add placeholder for user messages
        messages.append(("placeholder", "{messages}"))

        return ChatPromptTemplate.from_messages(messages)

    def get_parameters(self) -> dict[str, Any]:
        """Get the LLM parameters for this prompt.

        Returns:
            Dictionary of LLM parameters (temperature, max_tokens, etc.).
        """
        params: dict[str, Any] = {}

        base_params = self.prompt.parameters
        if base_params:
            if base_params.temperature is not None:
                params["temperature"] = base_params.temperature
            if base_params.max_tokens is not None:
                params["max_tokens"] = base_params.max_tokens
            if base_params.top_p is not None:
                params["top_p"] = base_params.top_p
            if base_params.top_k is not None:
                params["top_k"] = base_params.top_k
            if base_params.frequency_penalty is not None:
                params["frequency_penalty"] = base_params.frequency_penalty
            if base_params.presence_penalty is not None:
                params["presence_penalty"] = base_params.presence_penalty

        # Apply model-specific overrides
        if self.model_name and self.prompt.model_overrides:
            override = self.prompt.model_overrides.get(self.model_name)
            if override and override.parameters:
                if override.parameters.temperature is not None:
                    params["temperature"] = override.parameters.temperature
                if override.parameters.max_tokens is not None:
                    params["max_tokens"] = override.parameters.max_tokens
                if override.parameters.top_p is not None:
                    params["top_p"] = override.parameters.top_p
                if override.parameters.top_k is not None:
                    params["top_k"] = override.parameters.top_k
                if override.parameters.frequency_penalty is not None:
                    params["frequency_penalty"] = override.parameters.frequency_penalty
                if override.parameters.presence_penalty is not None:
                    params["presence_penalty"] = override.parameters.presence_penalty

        return params
