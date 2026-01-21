# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Fragment resolution utilities for PromptPack."""

from __future__ import annotations

from typing import Any

from promptpack.template import TemplateEngine
from promptpack.types import PromptPack


class FragmentResolver:
    """Resolver for PromptPack fragments.

    Handles fragment references in templates and resolves them
    with variable substitution.
    """

    def __init__(self, pack: PromptPack):
        """Initialize the fragment resolver.

        Args:
            pack: The PromptPack containing fragments.
        """
        self.pack = pack
        self.fragments = pack.fragments or {}
        self.engine = TemplateEngine(
            syntax=pack.template_engine.syntax,
            fragments=self.fragments,
        )

    def resolve_template(
        self,
        template: str,
        variables: dict[str, Any],
        *,
        strict: bool = True,
    ) -> str:
        """Resolve all fragments and variables in a template.

        Args:
            template: The template string.
            variables: Variables for substitution.
            strict: If True, raise errors for undefined fragments/variables.

        Returns:
            The fully resolved template string.
        """
        return self.engine.render(template, variables, strict=strict)

    def get_required_fragments(self, template: str) -> set[str]:
        """Get the set of fragment names required by a template.

        Args:
            template: The template string.

        Returns:
            Set of fragment names referenced in the template.
        """
        return self.engine.extract_fragments(template)

    def validate_fragments(self, template: str) -> list[str]:
        """Validate that all fragments referenced in a template exist.

        Args:
            template: The template string.

        Returns:
            List of missing fragment names (empty if all exist).
        """
        required = self.get_required_fragments(template)
        missing = []
        for name in required:
            if name not in self.fragments:
                missing.append(name)
        return missing
