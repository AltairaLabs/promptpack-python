#!/usr/bin/env python3
# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Sync the vendored PromptPack JSON Schema from the canonical spec URL.

The schema is the single source of truth for what a valid pack is. We vendor a
copy into the package so validation works offline and is pinned to a known
version; run this script to refresh that copy when the spec is updated:

    python scripts/sync_schema.py            # fetch latest, write if changed
    python scripts/sync_schema.py --check    # CI: fail if the vendored copy is stale

The canonical URL is also recorded as promptpack.schema.SCHEMA_URL.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

SCHEMA_URL = "https://promptpack.org/schema/latest/promptpack.schema.json"
VENDORED = (
    Path(__file__).resolve().parents[1]
    / "packages/promptpack/src/promptpack/schema/promptpack.schema.json"
)


def fetch() -> str:
    with urllib.request.urlopen(SCHEMA_URL, timeout=30) as resp:  # noqa: S310 (trusted URL)
        raw = resp.read().decode("utf-8")
    # Round-trip so the vendored file is canonically formatted and we fail fast
    # on a non-JSON response.
    return json.dumps(json.loads(raw), indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the vendored PromptPack JSON Schema.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the vendored schema differs from the published one.",
    )
    args = parser.parse_args()

    upstream = fetch()
    current = VENDORED.read_text(encoding="utf-8") if VENDORED.exists() else None

    if args.check:
        if current != upstream:
            print(f"Vendored schema is stale. Run: python {Path(__file__).name}")
            return 1
        print("Vendored schema is up to date.")
        return 0

    if current == upstream:
        print("Vendored schema already up to date.")
        return 0

    VENDORED.write_text(upstream, encoding="utf-8")
    print(f"Synced schema -> {VENDORED}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
