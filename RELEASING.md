# Releasing

Packages are published to PyPI by `.github/workflows/publish.yml` using
**trusted publishing** (PyPI's OIDC flow) — no API tokens are stored.

This repo publishes two packages:

| Package | PyPI project |
|---------|--------------|
| `packages/promptpack` | [`promptpack`](https://pypi.org/project/promptpack/) |
| `packages/promptpack-langchain` | [`promptpack-langchain`](https://pypi.org/project/promptpack-langchain/) |

## One-time setup (per PyPI project)

Until this is done, the publish workflow will fail at the upload step.

For **each** project (`promptpack` and `promptpack-langchain`):

1. Create the project on PyPI (or pre-register it via a "pending" trusted
   publisher if it doesn't exist yet).
2. Go to the project's **Settings → Publishing → Add a trusted publisher**
   (GitHub Actions) and enter:
   - **Owner:** `AltairaLabs`
   - **Repository:** `promptpack-python`
   - **Workflow name:** `publish.yml`
   - **Environment:** `pypi`
3. In this repo, create a GitHub Actions **Environment** named `pypi`
   (Settings → Environments). Add reviewers/branch protection if you want a
   manual approval gate before each publish.

Both jobs use the same workflow file and `pypi` environment, so both projects
point their trusted publisher at the same coordinates.

## Cutting a release

1. Bump the version in the relevant `pyproject.toml`
   (`packages/promptpack/pyproject.toml` and/or
   `packages/promptpack-langchain/pyproject.toml`). They version independently.
2. Refresh the vendored schema if the spec changed:
   `python scripts/sync_schema.py`.
3. Merge to `main`.
4. Publish, either:
   - **GitHub Release** — create a release; the workflow publishes **both**
     packages, or
   - **Manual** — Actions → *Publish* → *Run workflow*, and pick which
     package(s) to publish.

The workflow builds an sdist + wheel with `python -m build` and uploads via
`pypa/gh-action-pypi-publish`. The wheel bundles the vendored
`promptpack/schema/promptpack.schema.json`, so installed packages validate
offline.
