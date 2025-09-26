# Carbonic - the datetime library

The Python library, strongly inspired by PHP Carbon.

## Development Setup

**Package Manager:** uv
**Testing:** pytest
**Python:** >=3.12

### Common Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest
uv run pytest --cov=carbonic --cov-report=html

# Type checking
uv run mypy carbonic

# Linting and formatting
uv run ruff check carbonic
uv run ruff format carbonic

# Install in development mode
uv pip install -e .
```

## Project Structure

```
carbonic/
├── carbonic/
│   ├── core/           # Core datetime classes (DateTime, Date, Duration)
│   ├── locale/         # Localization and i18n support
│   └── __init__.py     # Public API exports
├── tests/              # Test suite
└── pyproject.toml      # Project configuration
```

## Core Design Principles

**Immutable `dataclass`:** All datetime objects are frozen dataclasses with `slots=True`
**Fluent API:** Carbon-style chaining with Pythonic method names
**Typed:** Full PEP 561 support, strict typing throughout
**Timezone handling:** Stdlib `zoneinfo` only, strict timezone rules

### API Design Guidelines

**Method naming:** Use Pythonic snake_case (e.g., `add_days()`, `end_of_month()`)
**Immutability:** All operations return new instances
**Error handling:** Raise specific exceptions from `carbonic.core.exceptions`
**Return types:** Always annotate with proper generic types

Example fluent chaining:
```python
now().add_days(3).end_of_month().to_date_string()
```

## Features

### Core Classes
- **DateTime:** Main datetime class with timezone support
- **Date:** Date-only operations
- **Duration:** Time differences and intervals
- **Period:** Named periods (Day, Week, Month, etc.)

### Parsing & Formatting
- **Parsing:** ISO strict/relaxed, `from_format()`, optional ciso8601 acceleration
- **Formatting:** strftime + Carbon-style tokens (Y-m-d H:i:s)

### Localization
- **Strategy:** CLDR-style localization
- **Languages:** Polish and English first, expandable architecture
- **Humanization:** Localized relative time differences ("2 days ago")

### Integrations
- **Stdlib:** First-class `datetime.datetime` compatibility
- **Data libraries:** pandas, polars adapters
- **Validation:** Pydantic field types

## Dependencies Strategy

**Required:** None (stdlib only for core functionality)
**Optional:**
- `ciso8601`: Fast ISO datetime parsing
- `pandas`: DataFrame datetime operations
- `polars`: DataFrame datetime operations
- `pydantic`: Validation field types

## Performance Goals

- Zero-copy datetime operations where possible
- Lazy evaluation for expensive formatting operations
- Memory-efficient immutable design with `__slots__`
- Optional C extensions for parsing (ciso8601)
- to memorize stick to Stdlib zoneinfo only