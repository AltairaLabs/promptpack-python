---
title: Installation
description: How to install the PromptPack Python libraries
sidebar:
  order: 1
---

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

### Base Library

Install the base `promptpack` library for parsing PromptPack JSON files:

```bash
pip install promptpack
```

### LangChain Integration

Install `promptpack-langchain` for LangChain integration (includes base library):

```bash
pip install promptpack-langchain
```

## Development Installation

For development, clone the repository and install in editable mode:

```bash
git clone https://github.com/AltairaLabs/promptpack-python.git
cd promptpack-python
pip install hatch
```

Install the packages in development mode:

```bash
# Install promptpack
pip install -e packages/promptpack

# Install promptpack-langchain
pip install -e packages/promptpack-langchain
```

## Verify Installation

Verify the installation:

```bash
# For base library
python -c "from promptpack import parse_promptpack; print('promptpack installed')"

# For LangChain integration
python -c "from promptpack_langchain import PromptPackTemplate; print('promptpack-langchain installed')"
```
