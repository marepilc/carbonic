# Contributing to Carbonic

Thank you for your interest in contributing to Carbonic! This guide will help you get started with development.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- UV package manager
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/marepilc/carbonic.git
   cd carbonic
   ```

2. **Install development dependencies:**
   ```bash
   uv sync --dev
   ```

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

4. **Install pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=carbonic --cov-report=html

# Run specific test file
uv run pytest tests/test_datetime.py

# Run with verbose output
uv run pytest -v
```

### Code Quality

Carbonic uses several tools to maintain code quality:

```bash
# Type checking
uv run mypy carbonic

# Linting
uv run ruff check carbonic

# Formatting
uv run ruff format carbonic

# Run all checks
uv run pre-commit run --all-files
```

### Documentation

Build and serve documentation locally:

```bash
# Install docs dependencies (if not already installed)
uv sync --group docs

# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

## Project Structure

```
carbonic/
├── carbonic/              # Main package
│   ├── core/             # Core classes (DateTime, Date, etc.)
│   │   ├── datetime.py   # DateTime implementation
│   │   ├── date.py       # Date implementation
│   │   ├── duration.py   # Duration implementation
│   │   ├── period.py     # Period constants and logic
│   │   ├── interval.py   # Interval implementation
│   │   └── exceptions.py # Custom exceptions
│   ├── locale/           # Localization support
│   │   ├── base.py       # Base locale class
│   │   ├── en.py         # English locale
│   │   └── pl.py         # Polish locale
│   └── __init__.py       # Public API
├── tests/                # Test suite
├── docs/                 # Documentation
├── pyproject.toml        # Project configuration
├── mkdocs.yml           # Documentation configuration
└── README.md            # Project overview
```

## Coding Standards

### Code Style

- Follow PEP 8 and use Ruff for formatting
- Use type hints for all public APIs
- Prefer descriptive names over comments
- Keep functions focused and small

### Docstrings

Use Google-style docstrings:

```python
def add_days(self, days: int) -> "DateTime":
    """Add the specified number of days.

    Args:
        days: Number of days to add (can be negative).

    Returns:
        New DateTime instance with added days.

    Example:
        >>> dt = DateTime(2024, 1, 15, tz="UTC")
        >>> future = dt.add_days(7)
        >>> print(future)
        2024-01-22T00:00:00+00:00
    """
    return self._replace_dt(self._dt + timedelta(days=days))
```

### Type Annotations

- Use modern type hints (Python 3.12+ syntax)
- Import types from `typing` when needed
- Use `Self` for methods returning the same type
- Be explicit about optional parameters

```python
from typing import Self, Optional
from datetime import datetime

def from_datetime(cls, dt: datetime) -> Self:
    """Create from standard library datetime."""
    ...
```

## Testing Guidelines

### Test Structure

- Place tests in the `tests/` directory
- Mirror the package structure in test files
- Use descriptive test method names
- Group related tests in classes

```python
class TestDateTimeArithmetic:
    def test_add_days_positive(self):
        """Test adding positive number of days."""
        dt = DateTime(2024, 1, 15, tz="UTC")
        result = dt.add_days(7)
        expected = DateTime(2024, 1, 22, tz="UTC")
        assert result == expected

    def test_add_days_negative(self):
        """Test adding negative number of days."""
        dt = DateTime(2024, 1, 15, tz="UTC")
        result = dt.add_days(-7)
        expected = DateTime(2024, 1, 8, tz="UTC")
        assert result == expected
```

### Test Categories

1. **Unit Tests**: Test individual methods in isolation
2. **Integration Tests**: Test interactions between classes
3. **Property Tests**: Test invariants and edge cases
4. **Performance Tests**: Ensure operations meet performance requirements

### Writing Good Tests

- Test both happy path and edge cases
- Use meaningful assertions with clear error messages
- Avoid testing implementation details
- Prefer multiple focused tests over complex tests

## Making Changes

### Before You Start

1. Check existing issues to avoid duplication
2. For large changes, open an issue to discuss the approach
3. Fork the repository and create a feature branch

### Development Process

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following the established patterns
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes:**
   ```bash
   uv run pytest
   uv run mypy carbonic
   uv run ruff check carbonic
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines

Follow conventional commit format:

```
type: brief description

Longer description if needed

- List any breaking changes
- Reference relevant issues
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code changes that don't add features or fix bugs
- `perf`: Performance improvements
- `chore`: Maintenance tasks

## Design Principles

### Immutability

All datetime objects must be immutable:

```python
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass(frozen=True, slots=True)
class DateTime:
    _dt: datetime

    def add_days(self, days: int) -> "DateTime":
        # Return new instance, never modify self
        return DateTime(self._dt + timedelta(days=days))
```

### Fluent API

Methods should be chainable and read naturally:

```python
from carbonic import DateTime

# Create a sample datetime for the example
dt = DateTime.now()

# Good - fluent and readable
result = (dt
    .add(days=1)
    .start_of("day")
)

# Avoid - requires intermediate variables
dt1 = dt.add(days=1)
dt2 = dt1.start_of("day")
result = dt2  # Note: timezone conversion would be done during creation
```

### Type Safety

Maintain strict typing throughout:

```python
from typing import Any
from datetime import datetime

# Good - explicit types
def diff_in_days(self, other: "DateTime") -> float:
    delta = other._dt - self._dt
    return delta.total_seconds() / 86400

# Avoid - untyped or Any
def diff_in_days(self, other) -> Any:
    pass  # Using pass instead of ... for valid syntax
```

### Error Handling

Use specific exceptions:

```python
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from carbonic.core.exceptions import CarbonicError

# Define a custom exception for this example
class InvalidTimezone(CarbonicError):
    pass

def _validate_timezone(tz_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        raise InvalidTimezone(f"Unknown timezone: {tz_name}")
```

## Contributing Guidelines

### What We're Looking For

- **Bug fixes**: Always welcome with tests
- **Performance improvements**: With benchmarks showing improvement
- **New features**: Discuss in an issue first
- **Documentation**: Improvements and examples
- **Tests**: Additional test coverage

### What We're Not Looking For

- Breaking changes without strong justification
- Features that significantly increase complexity
- Code that doesn't follow established patterns
- Changes without tests

### Pull Request Process

1. **Fork and branch**: Create a feature branch from `main`
2. **Implement**: Make your changes with tests
3. **Document**: Update docs if needed
4. **Test**: Ensure all tests pass
5. **Submit**: Create a pull request with clear description

### PR Requirements

- [ ] All tests pass
- [ ] Type checking passes (mypy)
- [ ] Linting passes (ruff)
- [ ] New code has tests
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated for user-facing changes

## Release Process

Carbonic follows semantic versioning:

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Creating a Release

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. GitHub Actions handles PyPI publication

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact maintainers for private concerns

## Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for significant contributions

Thank you for contributing to Carbonic!