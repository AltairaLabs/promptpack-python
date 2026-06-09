# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Access to the vendored PromptPack JSON Schema.

The schema under ``schema/promptpack.schema.json`` is vendored from the
canonical spec (``SCHEMA_URL``) so validation works offline and stays pinned to
a known spec version. Refresh it with ``python scripts/sync_schema.py``.

This schema — not the pydantic models in ``types`` — is the source of truth for
what a valid pack is. The models are a typed view of the stable core; the spec
schema accepts every spec-defined section (including extensions like evals,
workflow, agents and skills), so the parser never rejects a spec-valid pack.
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any

from jsonschema import Draft202012Validator

# Canonical source of truth for the vendored copy under schema/.
SCHEMA_URL = "https://promptpack.org/schema/latest/promptpack.schema.json"


@lru_cache(maxsize=1)
def load_schema() -> dict[str, Any]:
    """Return the vendored PromptPack JSON Schema as a dict."""
    resource = resources.files("promptpack") / "schema" / "promptpack.schema.json"
    return json.loads(resource.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def get_validator() -> Draft202012Validator:
    """Return a cached Draft 2020-12 validator built from the vendored schema."""
    return Draft202012Validator(load_schema())
