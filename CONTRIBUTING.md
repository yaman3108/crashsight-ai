# Contributing to CrashSight AI

Thank you for your interest in contributing! This project is in its early stages, and every contribution — from fixing typos to building entire pipeline phases — makes a real difference.

## How to Contribute

### 1. Find Something to Work On

- Check the [Issues](../../issues) tab for tasks labelled **`good first issue`** or **`help wanted`**.
- If you have an idea not covered by an existing issue, open a new one to discuss it before starting work.

### 2. Fork and Branch

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/crashsight-ai.git
cd crashsight-ai
git checkout -b feature/your-feature-name
```

### 3. Set Up Your Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # linting, testing tools
```

### 4. Make Your Changes

- Write clean, commented code.
- Add or update tests if applicable.
- Follow existing code style (PEP 8 for Python).
- Update documentation if your change affects usage or architecture.

### 5. Submit a Pull Request

- Push your branch to your fork.
- Open a Pull Request against `main`.
- Fill in the PR template — describe what you changed and why.
- Link to any related issues.

## Types of Contributions We Need

| Area | Examples |
|---|---|
| **Data Collection** | Finding satellite imagery of known crash sites, labelling images |
| **Model Development** | Training experiments, architecture improvements, evaluation |
| **Pipeline Code** | Scan grid generation, tile processing, NMS implementation |
| **Cross-Reference Engine** | News API integration, NLP entity extraction, match scoring |
| **Review Interface** | Streamlit or FastAPI-based review tool |
| **Documentation** | Labelling guides, model cards, README improvements |
| **Testing** | Unit tests, integration tests, edge case coverage |

## Proposing New Crash Classes

To propose a new crash class, open an issue using the **Class Proposal** template. Your proposal must include:

- A clear description of the crash type and its visual signature from satellite altitude.
- At least 50 example satellite images showing the class.
- An explanation of why existing classes don't cover this type.

## Proposing New Data Sources

To suggest a new imagery or news data source, open an issue using the **Data Source Proposal** template with:

- The source name and URL.
- What data it provides and at what resolution/coverage.
- Licensing and access requirements.
- How it improves on existing sources.

## Code Style

- Python: PEP 8, enforced by `ruff` or `flake8`.
- Type hints encouraged for all function signatures.
- Docstrings for all public functions and classes.
- Variable names should be descriptive — no single-letter names outside loop counters.

## Review Process

- All PRs require at least one maintainer review before merging.
- Automated CI checks (linting, tests) must pass.
- Be responsive to review feedback — we aim to merge or close PRs within 2 weeks.

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and inclusive.

## Questions?

Open a [Discussion](../../discussions) or comment on the relevant issue. We're happy to help.
