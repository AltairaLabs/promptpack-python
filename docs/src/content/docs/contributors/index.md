---
title: Contributing
description: Guidelines for contributing to PromptPack Python
sidebar:
  order: 1
---

We welcome contributions to PromptPack Python! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [Hatch](https://hatch.pypa.io/) for project management

### Clone and Install

```bash
git clone https://github.com/AltairaLabs/promptpack-python.git
cd promptpack-python
pip install hatch
```

## Development Commands

All development commands are run through Hatch:

```bash
# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Lint code
hatch run lint

# Format code
hatch run format

# Type checking
hatch run typecheck
```

## Project Structure

```
promptpack-python/
├── packages/
│   ├── promptpack/           # Base library
│   │   ├── src/promptpack/
│   │   └── tests/
│   └── promptpack-langchain/ # LangChain integration
│       ├── src/promptpack_langchain/
│       └── tests/
├── docs/                     # Documentation (Astro/Starlight)
└── pyproject.toml           # Root project configuration
```

## Code Style

- Use [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- Follow PEP 8 style guidelines
- Add type hints to all public functions and methods
- Write docstrings for all public APIs (Google style)

## Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use pytest for testing
- Place tests in the `tests/` directory of each package

### Running Specific Tests

```bash
# Run tests for a specific package
hatch run test packages/promptpack/tests/

# Run a specific test file
hatch run test packages/promptpack/tests/test_parser.py

# Run tests matching a pattern
hatch run test -k "test_parse"
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Ensure all tests pass
5. Ensure code passes linting and type checking
6. Submit a pull request

### Commit Messages

Use clear, descriptive commit messages:

- `feat: add support for array variables`
- `fix: handle missing optional fields`
- `docs: update installation instructions`
- `test: add tests for fragment parsing`
- `chore: update dependencies`

## Documentation

### Building Documentation

```bash
cd docs
npm install
npm run dev
```

The documentation site will be available at `http://localhost:4321`.

### Writing Documentation

- Documentation is in `docs/src/content/docs/`
- Use Markdown or MDX format
- Include frontmatter with title and description
- Add code examples where appropriate

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
