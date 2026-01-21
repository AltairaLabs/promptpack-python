# Contributing to PromptPack Python

Thank you for your interest in contributing to PromptPack Python! This document provides comprehensive guidelines and instructions for contributing to our open source project.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@altairalabs.ai](mailto:conduct@altairalabs.ai).

## Developer Certificate of Origin (DCO)

This project uses the Developer Certificate of Origin (DCO) to ensure that contributors have the right to submit their contributions. By making a contribution to this project, you certify that:

1. The contribution was created in whole or in part by you and you have the right to submit it under the open source license indicated in the file; or
2. The contribution is based upon previous work that, to the best of your knowledge, is covered under an appropriate open source license and you have the right under that license to submit that work with modifications, whether created in whole or in part by you, under the same open source license (unless you are permitted to submit under a different license), as indicated in the file; or
3. The contribution was provided directly to you by some other person who certified (1), (2) or (3) and you have not modified it.

### Signing Your Commits

To sign off on your commits, add the `-s` flag to your git commit command:

```bash
git commit -s -m "Your commit message"
```

This adds a "Signed-off-by" line to your commit message:

```
Signed-off-by: Your Name <your.email@example.com>
```

## How to Contribute

### Reporting Bugs

- Check existing issues first
- Provide clear reproduction steps
- Include version information
- Share relevant configuration/code samples

### Suggesting Features

- Open an issue describing the feature
- Explain the use case and benefits
- Discuss implementation approach

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Write/update tests**
5. **Run tests**: `pytest packages/ -v`
6. **Run linter**: `ruff check packages/`
7. **Run formatter**: `ruff format packages/`
8. **Run type checker**: `mypy packages/`
9. **Commit your changes**: Use clear, descriptive commit messages
10. **Push to your fork**: `git push origin feature/your-feature-name`
11. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python 3.10 or later

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/promptpack-python.git
cd promptpack-python

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all packages in development mode
pip install -e "packages/promptpack[dev]"
pip install -e "packages/promptpack-langchain[dev]"

# Run tests
pytest packages/ -v

# Run linter
ruff check packages/
```

### Project Structure

```
promptpack-python/
├── packages/
│   ├── promptpack/              # Core PromptPack library
│   │   ├── src/promptpack/      # Source code
│   │   └── tests/               # Tests
│   └── promptpack-langchain/    # LangChain integration
│       ├── src/promptpack_langchain/
│       └── tests/
├── docs/                        # Documentation
└── pyproject.toml              # Root project config
```

## Package-Specific Guidelines

### promptpack (`packages/promptpack/`)

**Focus**: Core PromptPack parsing and data structures

**Key Areas:**
- Pack file parsing (YAML/JSON)
- Data models for prompts, tools, and configurations
- Validation and error handling
- Schema support

### promptpack-langchain (`packages/promptpack-langchain/`)

**Focus**: LangChain integration for PromptPacks

**Key Areas:**
- LangChain prompt template conversion
- Tool integration with LangChain
- Chain and agent builders
- Provider-specific adapters

## Coding Guidelines

### Python Code Style

- Follow PEP 8 conventions (enforced by ruff)
- Use type hints for all function signatures
- Write clear, descriptive variable/function names
- Add docstrings for public functions and classes
- Keep functions focused and testable

### Testing

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use pytest fixtures for common setup
- Test each package independently

### Documentation

- Update README.md if adding features
- Add inline comments for complex logic
- Update relevant example configurations
- Add docstrings for new public APIs

## Pull Request Process

1. **Ensure CI passes** - All tests and linter checks must pass
2. **Update documentation** - README, examples, inline docs
3. **Request review** - Tag maintainers
4. **Address feedback** - Respond to review comments
5. **Resolve all conversations** - All review comments must be marked as resolved
6. **Sign commits** - Use `git commit -s` for DCO compliance
7. **Keep branch updated** - Rebase or merge with latest `main`

## Questions?

- Open a GitHub issue for questions
- Check existing documentation
- Review closed issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
