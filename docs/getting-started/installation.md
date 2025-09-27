# Installation

## Requirements

Carbonic requires Python 3.12 or higher. It's designed to work with modern Python features and type annotations.

```bash
python --version  # Should be 3.12+
```

## Installation Methods

### PyPI Installation (Recommended)

Install the latest stable version from PyPI:

```bash
pip install carbonic
```

### Development Installation

For the latest development version:

```bash
pip install git+https://github.com/marepilc/carbonic.git
```

### Poetry

If you're using Poetry for dependency management:

```bash
poetry add carbonic
```

### UV

If you're using UV for package management:

```bash
uv add carbonic
```

## Optional Dependencies

Carbonic offers optional dependencies for enhanced functionality:

### Performance Optimizations (Recommended)

For significantly faster ISO datetime parsing and other performance improvements:

```bash
pip install carbonic[performance]
```

This installs `ciso8601`, which provides C-accelerated ISO datetime parsing that's ~10x faster than the standard library, plus enables other performance optimizations like lazy evaluation caching.

### Pydantic Integration

For data validation and serialization with Pydantic:

```bash
pip install carbonic[pydantic]
```

This enables custom Pydantic field types for all Carbonic datetime classes, allowing seamless integration with FastAPI, SQLModel, and other Pydantic-based frameworks.

### Development

For development and contributing:

```bash
pip install carbonic[dev]
```

This includes testing, linting, documentation, and type checking tools.

### All Optional Dependencies

To install everything:

```bash
pip install carbonic[all]
```

## Verify Installation

Verify that Carbonic is installed correctly:

```python
import carbonic
print(carbonic.__version__)

# Test basic functionality
from carbonic import now, DateTime

current_time = now()
print(f"Current time: {current_time}")

dt = DateTime(2025, 1, 15, 14, 30)
print(f"Example datetime: {dt.format('Y-m-d H:i:s')}")
```

Expected output:
```
0.2.0
Current time: 2025-01-15T10:30:00+00:00
Example datetime: 2025-01-15 14:30:00
```

## Troubleshooting

### ImportError: No module named 'carbonic'

This usually means the installation failed or you're using the wrong Python environment:

1. Check your Python version: `python --version`
2. Verify pip is working: `pip --version`
3. Try reinstalling: `pip uninstall carbonic && pip install carbonic`
4. Check virtual environment: `which python` and `which pip`

### ModuleNotFoundError: No module named 'zoneinfo'

This should not happen with Python 3.12+, but if you see this error:

1. Verify your Python version: `python --version`
2. Update Python to 3.12 or higher
3. If using an older Python version, install the backport: `pip install backports.zoneinfo`

### Performance Issues

If datetime parsing is slow:

1. Install the performance extra: `pip install carbonic[performance]`
2. Verify ciso8601 is installed: `pip list | grep ciso8601`

### Type Checking Issues

If you're using mypy and seeing type errors:

1. Ensure you have the latest version: `pip install --upgrade carbonic`
2. Check mypy configuration for PEP 561 support
3. Verify you're using a supported Python version (3.12+)

## Next Steps

Now that you have Carbonic installed, continue with:

- [Quick Start Guide](quickstart.md) - Get up and running quickly
- [Core Concepts](concepts.md) - Understand the fundamental principles
- [User Guide](../guide/datetime.md) - Dive into specific features