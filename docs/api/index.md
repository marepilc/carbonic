# API Reference

Complete API documentation for all Carbonic classes and functions.

## Overview

Carbonic provides a comprehensive set of classes for working with dates, times, durations, and intervals. All classes are immutable and provide fluent APIs for chaining operations.

## Core Classes

### [DateTime](datetime.md)
The main datetime class with timezone support and comprehensive date/time operations.

```python
from carbonic import DateTime, now

# Current time
current = now()

# Specific datetime
dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

# Fluent operations
result = dt.add(days=7).end_of("month")
# Convert between timezones
result = dt.as_timezone("America/New_York")
```

### [Date](date.md)
Date-only operations without time components.

```python
from carbonic import Date, today

# Today's date
today_date = today()

# Specific date
birthday = Date(1990, 5, 15)

# Date arithmetic
next_month = birthday.add(months=1)
```

### [Duration](duration.md)
Represents spans of time that can be added to or subtracted from datetime objects.

```python
from carbonic import DateTime, Duration

# Create duration
duration = Duration(hours=2, minutes=30)

# Use with datetime
dt = DateTime.now()
future = dt + duration
```

### [Period](period.md)
Named time periods and weekday constants.

```python
from carbonic import DateTime, Period

dt = DateTime.now()

# Add time periods using Period constants
next_month = Period.MONTH.add_to(dt)
next_week = Period.WEEK.add_to(dt)

# Time period constants
monthly_period = Period.MONTH
```

### [Interval](interval.md)
Represents time ranges between two datetime points.

```python
from carbonic import DateTime, Interval

# Create interval
start_dt = DateTime.now()
end_dt = start_dt.add(hours=2)
meeting = Interval(start_dt, end_dt)

# Check overlaps
other_start = start_dt.add(hours=1)
other_end = other_start.add(hours=2)
other_meeting = Interval(other_start, other_end)
is_conflicting = meeting.overlaps(other_meeting)
```

## Factory Functions

### now()
```python
from carbonic import now

# Get current time in UTC (default)
current_utc = now()

# Get current time in specific timezone
current_ny = now("America/New_York")
```

Create a DateTime instance for the current moment in the specified timezone.

**Parameters:**
- `tz`: Timezone string (IANA timezone name) or None for naive datetime

**Returns:**
- DateTime object representing the current moment

### today()
```python
from carbonic import today

# Get today's date
today_date = today()

# Get today's date in specific timezone
today_tokyo = today("Asia/Tokyo")
```

Create a Date instance for today in the specified timezone.

**Parameters:**
- `tz`: Timezone string for determining "today" or None for system timezone

**Returns:**
- Date object representing today

## Exception Classes

### [Exceptions](exceptions.md)
Custom exceptions for error handling.

```python
from carbonic.core.exceptions import (
    CarbonicError,
    ParseError
)

# Example usage
try:
    from carbonic import DateTime
    dt = DateTime.parse("invalid-date-string")
except ParseError as e:
    print(f"Failed to parse: {e}")
```

## Locale Support

### [Locale](locale.md)
Localization and internationalization support for 6 languages.

```python
from carbonic import DateTime, Duration
from carbonic.locale import get_locale

# Create datetime and duration
dt = DateTime(2024, 1, 15, 14, 30)
duration = Duration(hours=2, minutes=30)

# Format with different locales
formatted_en = dt.format("l, F j, Y")           # "Monday, January 15, 2024"
formatted_pl = dt.format("l, j F Y", locale="pl")  # "poniedziałek, 15 stycznia 2024"
formatted_es = dt.format("l, j F Y", locale="es")  # "lunes, 15 enero 2024"
formatted_fr = dt.format("l j F Y", locale="fr")   # "lundi 15 janvier 2024"
formatted_de = dt.format("l, j. F Y", locale="de") # "Montag, 15. Januar 2024"
formatted_pt = dt.format("l, j F Y", locale="pt")  # "segunda-feira, 15 janeiro 2024"

# Duration humanization
duration_en = duration.humanize()              # "2 hours 30 minutes"
duration_es = duration.humanize(locale="es")   # "2 horas 30 minutos"
```

**Supported Languages:** English (en), Polish (pl), Spanish (es), French (fr), German (de), Portuguese (pt)

## Type System

Carbonic is fully typed and supports PEP 561. All classes and functions include comprehensive type annotations for excellent IDE support and static type checking.

### Import Structure

```python
# Main classes and functions
from carbonic import DateTime, Date, Duration, Period, Interval, now, today

# Exceptions
from carbonic.core.exceptions import CarbonicError, ParseError

# Locale support
from carbonic.locale import get_locale

# Example usage
dt = DateTime.now()
today_date = today()
duration = Duration(hours=2)
```

## Design Principles

### Immutability
All objects are immutable dataclasses with `frozen=True` and `slots=True` for memory efficiency and thread safety.

### Fluent API
Methods are designed to chain naturally while maintaining readability:

```python
from carbonic import DateTime

result = (DateTime.now()
    .add(days=1)
    .start_of("day")
    .format("Y-m-d H:i:s")
)
```

### Type Safety
Comprehensive type annotations throughout:

```python
from carbonic import DateTime, Duration

def schedule_meeting(
    start: DateTime,
    duration: Duration,
    attendee_count: int
) -> list[DateTime]:
    return [
        start.add(hours=i)
        for i in range(attendee_count)
    ]

# Example usage
start_time = DateTime.now()
duration = Duration(hours=2)
meetings = schedule_meeting(start_time, duration, 3)
```

### Timezone Awareness
Strong emphasis on timezone-aware operations:

```python
from carbonic import DateTime

# Encouraged: explicit timezone
dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

# Discouraged: naive datetime
naive = DateTime(2024, 1, 15, 14, 30, tz=None)
```

## Performance Characteristics

- **Memory Efficient**: `__slots__` usage reduces memory overhead
- **Fast Operations**: Leverages Python's datetime internally
- **Optional Acceleration**: Fast ISO parsing with `ciso8601`
- **Lazy Evaluation**: Expensive formatting operations are deferred

## Version Compatibility

Current version: **1.0.1**

- **Python**: 3.12+
- **Dependencies**: None (stdlib only)
- **Optional Dependencies**: `ciso8601`

## Navigation

Browse the detailed API documentation for each component:

- **[DateTime](datetime.md)** - Main datetime class
- **[Date](date.md)** - Date-only operations
- **[Duration](duration.md)** - Time spans and intervals
- **[Period](period.md)** - Named time periods
- **[Interval](interval.md)** - Time ranges
- **[Exceptions](exceptions.md)** - Error handling
- **[Locale](locale.md)** - Internationalization

Each page includes comprehensive method documentation with examples, parameters, return types, and usage notes.