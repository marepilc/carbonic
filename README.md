# Carbonic

A modern Python datetime library with fluent API, built with stdlib `zoneinfo`, dataclasses for immutability, and comprehensive localization support.

Carbonic provides an intuitive and fluent API for working with dates and times in Python, leveraging modern Python features for better type safety and performance.

## Features

- 🚀 **Fluent and immutable API** - Built with dataclasses for type safety
- 🌍 **Stdlib zoneinfo** - Uses Python's built-in timezone support (no external dependencies)
- 🔒 **Immutable by design** - All operations return new instances
- 🌐 **Full i18n support** - English, Polish, and extensible locale system
- ⚡ **High performance** - Minimal overhead with stdlib components
- 🔧 **Comprehensive formatting** - Extensive date/time formatting options
- 📝 **Human-readable differences** - Localized relative time descriptions
- 🎯 **Type-safe** - Full type hints throughout

## Installation

```bash
# Basic installation
pip install carbonic

# With performance optimizations (recommended)
pip install carbonic[performance]
```

## Performance

Carbonic is designed for high performance with several optimizations:

- **Fast ISO parsing**: Optional `ciso8601` integration for ~10x faster ISO 8601 datetime parsing
- **Memory efficiency**: All classes use `__slots__` for minimal memory overhead
- **Lazy evaluation**: Expensive formatting operations (locale lookups, timezone formatting) are cached
- **Stdlib only**: Core functionality requires no external dependencies

Performance benchmark results:
- **ISO parsing**: 0.001ms per operation (with ciso8601)
- **Formatting**: 0.004ms per operation (with caching)
- **Memory**: 100% slot usage, no `__dict__` overhead

## Quick Start

```python
from carbonic import DateTime, Duration

# Create and manipulate dates
now = DateTime.now()
tomorrow = now.add(days=1)
next_week = now.add(days=7)

# Parse ISO strings (fast with ciso8601)
dt = DateTime.parse("2024-12-25T15:30:00Z")

# Format with Carbon-style tokens
formatted = dt.format("F j, Y g:i A")  # "December 25, 2024 3:30 PM"

# Localized formatting
polish = dt.format("F j, Y", locale="pl")  # "grudzień 25, 2024"

# Duration calculations
duration = DateTime.now() - DateTime(2024, 1, 1)
print(duration.humanize())  # "11 months 3 weeks 2 days"