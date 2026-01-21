# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Parser for PromptPack JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import ValidationError

from promptpack.types import PromptPack

if TYPE_CHECKING:
    from os import PathLike


class PromptPackParseError(Exception):
    """Error raised when parsing a PromptPack fails."""

    def __init__(self, message: str, errors: list[dict] | None = None):
        super().__init__(message)
        self.errors = errors or []


def parse_promptpack(path: str | PathLike[str]) -> PromptPack:
    """Parse a PromptPack from a JSON file.

    Args:
        path: Path to the PromptPack JSON file.

    Returns:
        Parsed PromptPack object.

    Raises:
        PromptPackParseError: If the file cannot be read or parsed.
        FileNotFoundError: If the file does not exist.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"PromptPack file not found: {file_path}")

    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        raise PromptPackParseError(f"Failed to read PromptPack file: {e}") from e

    return parse_promptpack_string(content)


def parse_promptpack_string(content: str) -> PromptPack:
    """Parse a PromptPack from a JSON string.

    Args:
        content: JSON string containing the PromptPack.

    Returns:
        Parsed PromptPack object.

    Raises:
        PromptPackParseError: If the JSON is invalid or doesn't match the schema.
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise PromptPackParseError(f"Invalid JSON: {e}") from e

    try:
        return PromptPack.model_validate(data)
    except ValidationError as e:
        errors = [
            {
                "loc": list(err["loc"]),
                "msg": err["msg"],
                "type": err["type"],
            }
            for err in e.errors()
        ]
        raise PromptPackParseError(
            f"PromptPack validation failed: {len(errors)} error(s)", errors=errors
        ) from e
