# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Template engine for PromptPack variable substitution."""

from __future__ import annotations

import re
from typing import Any


class TemplateError(Exception):
    """Error raised during template rendering."""


class TemplateEngine:
    """Template engine for rendering PromptPack templates.

    Supports {{variable}} syntax for variable substitution and
    {{fragment:name}} syntax for fragment resolution.
    """

    # Pattern for {{variable}} or {{fragment:name}}
    VARIABLE_PATTERN = re.compile(r"\{\{([a-zA-Z_][a-zA-Z0-9_]*(?::[a-zA-Z_][a-zA-Z0-9_]*)?)\}\}")

    def __init__(self, syntax: str = "{{variable}}", fragments: dict[str, str] | None = None):
        """Initialize the template engine.

        Args:
            syntax: Template syntax pattern (currently only {{variable}} is supported).
            fragments: Dictionary of fragment names to their content.
        """
        self.syntax = syntax
        self.fragments = fragments or {}

    def render(
        self,
        template: str,
        variables: dict[str, Any],
        *,
        strict: bool = True,
    ) -> str:
        """Render a template with variable substitution.

        Args:
            template: The template string to render.
            variables: Dictionary of variable names to values.
            strict: If True, raise an error for undefined variables.
                   If False, leave undefined variables as-is.

        Returns:
            The rendered template string.

        Raises:
            TemplateError: If a required variable is not provided (when strict=True).
        """

        def replace_match(match: re.Match[str]) -> str:
            key = match.group(1)

            # Check if this is a fragment reference
            if ":" in key:
                prefix, name = key.split(":", 1)
                if prefix == "fragment":
                    return self._resolve_fragment(name, variables, strict=strict)

            # Regular variable substitution
            if key in variables:
                value = variables[key]
                return self._format_value(value)

            if strict:
                raise TemplateError(f"Undefined variable: {key}")

            # Leave undefined variables as-is
            return match.group(0)

        return self.VARIABLE_PATTERN.sub(replace_match, template)

    def _resolve_fragment(
        self,
        name: str,
        variables: dict[str, Any],
        *,
        strict: bool = True,
    ) -> str:
        """Resolve a fragment reference.

        Args:
            name: Fragment name.
            variables: Variables for substitution within the fragment.
            strict: If True, raise an error for undefined fragments.

        Returns:
            The resolved fragment content.

        Raises:
            TemplateError: If the fragment is not found (when strict=True).
        """
        if name not in self.fragments:
            if strict:
                raise TemplateError(f"Undefined fragment: {name}")
            return f"{{{{fragment:{name}}}}}"

        # Recursively render the fragment
        fragment_content = self.fragments[name]
        return self.render(fragment_content, variables, strict=strict)

    def _format_value(self, value: Any) -> str:
        """Format a value for template substitution.

        Args:
            value: The value to format.

        Returns:
            String representation of the value.
        """
        if value is None:
            return ""
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (list, dict)):
            import json

            return json.dumps(value)
        return str(value)

    def extract_variables(self, template: str) -> set[str]:
        """Extract all variable names from a template.

        Args:
            template: The template string.

        Returns:
            Set of variable names found in the template.
        """
        variables = set()
        for match in self.VARIABLE_PATTERN.finditer(template):
            key = match.group(1)
            # Skip fragment references
            if ":" not in key:
                variables.add(key)
        return variables

    def extract_fragments(self, template: str) -> set[str]:
        """Extract all fragment names from a template.

        Args:
            template: The template string.

        Returns:
            Set of fragment names found in the template.
        """
        fragments = set()
        for match in self.VARIABLE_PATTERN.finditer(template):
            key = match.group(1)
            if ":" in key:
                prefix, name = key.split(":", 1)
                if prefix == "fragment":
                    fragments.add(name)
        return fragments
