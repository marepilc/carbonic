
 <img src="assets/images/carbonic_logo.svg" alt="Carbonic Logo" style="width: 400px; height: auto;">

A modern Python datetime library with fluent API, immutable design, and comprehensive timezone support.

## Overview

Carbonic is a datetime library designed for modern Python applications that need powerful, type-safe datetime manipulation. Built with dataclasses and Python's standard library `zoneinfo`, it provides an intuitive, fluent API for working with dates, times, durations, and intervals.

## Key Features

### ✨ **Fluent & Immutable**
Chain operations naturally with a fluent API while maintaining immutability for safety:

```python
from carbonic import DateTime, now

# Fluent chaining
result = now().add(days=7).end_of("month").to_date_string()

# All operations return new instances
dt = DateTime(2024, 1, 15, 14, 30)
new_dt = dt.add(hours=2)  # Original dt is unchanged
```

### 🔒 **Type Safe**
Full type annotations and PEP 561 compliance for excellent IDE support:

```python
from carbonic import DateTime, Duration

dt: DateTime = DateTime.now()
duration: Duration = Duration(hours=2, minutes=30)
future: DateTime = dt + duration  # Type checked!
```

### 🌍 **Timezone Aware**
Built-in timezone support using Python's standard `zoneinfo`:

```python
from carbonic import DateTime

# Create timezone-aware datetime
utc_time = DateTime.now()  # UTC by default
ny_time = DateTime.now("America/New_York")

# Convert between timezones
tokyo_time = utc_time.as_timezone("Asia/Tokyo")
```

### 📅 **Rich Date Operations**
Comprehensive date and time manipulation:

```python
from carbonic import DateTime, Period

dt = DateTime(2024, 1, 15)

# Date arithmetic
next_month = dt.add(months=1)
# Note: Additional methods like previous(), next_business_day() may need implementation

# Date boundaries
start_of_week = dt.start_of("week")
end_of_month = dt.end_of("month")

# Duration calculations
other_dt = DateTime(2024, 2, 15)
diff = dt.diff(other_dt)
```

### 🌐 **Localization Support**
Multi-language formatting and humanization with support for 6 languages:

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 14, 30)
duration = Duration(hours=2, minutes=30)

# English (default)
formatted_en = dt.format("l, F j, Y")  # "Monday, January 15, 2024"
duration_en = duration.humanize()      # "2 hours 30 minutes"

# Polish localization
formatted_pl = dt.format("l, j F Y", locale="pl")  # "poniedziałek, 15 stycznia 2024"
duration_pl = duration.humanize(locale="pl")       # "2 godziny 30 minut"

# Spanish localization
formatted_es = dt.format("l, j {d}e F {d}e Y", locale="es")  # "lunes, 15 de enero de 2024"
duration_es = duration.humanize(locale="es")       # "2 horas 30 minutos"

# French localization
formatted_fr = dt.format("l j F Y", locale="fr")   # "lundi 15 janvier 2024"
duration_fr = duration.humanize(locale="fr")       # "2 heures 30 minutes"

# German localization
formatted_de = dt.format("l, j. F Y", locale="de") # "Montag, 15. Januar 2024"
duration_de = duration.humanize(locale="de")       # "2 Stunden 30 Minuten"

# Portuguese localization
formatted_pt = dt.format("l, j {d}e F {d}e Y", locale="pt")  # "segunda-feira, 15 de janeiro de 2024"
duration_pt = duration.humanize(locale="pt")       # "2 horas 30 minutos"
```

**Supported Locales:** English (en), Polish (pl), Spanish (es), French (fr), German (de), Portuguese (pt)

### ⚡ **Performance Optimized**
- Zero-copy operations where possible
- Lazy evaluation for expensive formatting
- Memory-efficient immutable design with `__slots__`
- Optional fast parsing with `ciso8601`

### 🔗 **Framework Integration**
- **Pydantic**: Custom field types for validation and serialization
- **JSON Schema**: Automatic schema generation for APIs
- **FastAPI**: Seamless integration with modern web frameworks

## Quick Start

### Installation

```bash
# Install from PyPI
pip install carbonic

# With optional fast parsing
pip install carbonic[performance]

# With Pydantic integration for validation
pip install carbonic[pydantic]

# Development installation
pip install carbonic[dev]
```

### Basic Usage

```python
from carbonic import DateTime, Date, Duration, now, today

# Current time
current = now()                    # UTC by default
local = now("America/New_York")    # Specific timezone

# Create specific datetime
dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")

# Date-only operations
date = Date(2024, 1, 15)
today_date = today()

# Duration arithmetic
duration = Duration(hours=2, minutes=30)
future = dt + duration

# Formatting
iso_string = dt.to_iso_string()         # "2024-01-15T14:30:00+00:00"
readable = dt.format("Y-m-d H:i:s")    # "2024-01-15 14:30:00"

# Pydantic integration (requires: pip install carbonic[pydantic])
from pydantic import BaseModel
from carbonic.integrations.pydantic import DateTimeField

class Event(BaseModel):
    name: str
    start_time: DateTimeField

event = Event(name="Meeting", start_time="2024-01-15T14:30:00Z")
print(event.start_time)  # DateTime(2024, 1, 15, 14, 30, 0, tz='UTC')
```

## Core Classes

| Class | Purpose | Example Usage |
|-------|---------|---------------|
| **DateTime** | Full datetime with timezone | `DateTime(2024, 1, 15, 14, 30, tz="UTC")` |
| **Date** | Date-only operations | `Date(2024, 1, 15)` |
| **Duration** | Time differences | `Duration(hours=2, minutes=30)` |
| **Period** | Named time periods | `Period.MONTH`, `Period.FRIDAY` |
| **Interval** | Time ranges | `Interval(start_dt, end_dt)` |

## Why Carbonic?

### Designed for Modern Python
- **Python 3.12+**: Leverages latest Python features
- **Type Safety**: Full mypy compatibility
- **Immutability**: Prevents bugs and enables safe concurrency
- **Standard Library**: No external dependencies for core functionality

### Developer Experience
- **Intuitive API**: Natural, readable method names
- **Excellent IDE Support**: Complete type annotations
- **Comprehensive Testing**: 100% test coverage
- **Clear Documentation**: Detailed guides and examples

### Production Ready
- **Timezone Correct**: Proper timezone handling with `zoneinfo`
- **Business Logic**: Built-in business day calculations
- **Localization**: Multi-language support architecture
- **Performance**: Optimized for real-world usage patterns

## Learn More

<div class="grid cards" markdown>

-   :material-rocket-launch: **Getting Started**

    ---

    New to Carbonic? Start here for installation and basic concepts.

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-book-open: **User Guide**

    ---

    Comprehensive guides for each feature and class.

    [:octicons-arrow-right-24: Browse Guides](guide/datetime.md)

-   :material-code-braces: **API Reference**

    ---

    Complete API documentation with examples.

    [:octicons-arrow-right-24: API Docs](api/index.md)

-   :material-lightbulb: **Examples**

    ---

    Real-world examples and common use cases.

    [:octicons-arrow-right-24: See Examples](examples/common-tasks.md)

</div>

## Community & Support

- **GitHub**: [marepilc/carbonic](https://github.com/marepilc/carbonic)
- **Issues**: [Bug Reports & Feature Requests](https://github.com/marepilc/carbonic/issues)
- **PyPI**: [python.org/project/carbonic](https://pypi.org/project/carbonic/)

## License

Carbonic is released under the MIT License. See the [LICENSE](https://github.com/marepilc/carbonic/blob/main/LICENSE) file for details.