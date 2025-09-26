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
result = dt.add_days(7).end_of_month().to_timezone("America/New_York")
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
next_month = birthday.add_months(1)
```

### [Duration](duration.md)
Represents spans of time that can be added to or subtracted from datetime objects.

```python
from carbonic import Duration

# Create duration
duration = Duration(hours=2, minutes=30)

# Use with datetime
future = dt + duration
```

### [Period](period.md)
Named time periods and weekday constants.

```python
from carbonic import Period

# Weekday navigation
next_friday = dt.next(Period.FRIDAY)

# Time periods
monthly_period = Period.MONTH
```

### [Interval](interval.md)
Represents time ranges between two datetime points.

```python
from carbonic import Interval

# Create interval
meeting = Interval(start_dt, end_dt)

# Check overlaps
is_conflicting = meeting.overlaps(other_meeting)
```

## Factory Functions

### now()
```python
from carbonic import now

now(tz: str | None = "UTC") -> DateTime
```

Create a DateTime instance for the current moment in the specified timezone.

**Parameters:**
- `tz`: Timezone string (IANA timezone name) or None for naive datetime

**Returns:**
- DateTime object representing the current moment

### today()
```python
from carbonic import today

today(tz: str | None = None) -> Date
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
    InvalidDate,
    InvalidTime,
    InvalidTimezone,
    ParseError
)
```

## Locale Support

### [Locale](locale.md)
Localization and internationalization support.

```python
from carbonic.locale import set_locale, get_locale

# Set locale for formatting
set_locale("pl")  # Polish
dt.format("l, j F Y")  # "poniedziałek, 15 stycznia 2024"
```

## Type System

Carbonic is fully typed and supports PEP 561. All classes and functions include comprehensive type annotations for excellent IDE support and static type checking.

### Import Structure

```python
# Main classes and functions
from carbonic import DateTime, Date, Duration, Period, Interval, now, today

# Core classes (alternative import)
from carbonic.core import DateTime, Date, Duration, Period, Interval

# Exceptions
from carbonic.core.exceptions import CarbonicError, ParseError

# Locale support
from carbonic.locale import set_locale, get_locale
```

## Design Principles

### Immutability
All objects are immutable dataclasses with `frozen=True` and `slots=True` for memory efficiency and thread safety.

### Fluent API
Methods are designed to chain naturally while maintaining readability:

```python
result = (DateTime.now()
    .add_days(1)
    .start_of_day()
    .to_timezone("America/New_York")
    .format("Y-m-d H:i:s")
)
```

### Type Safety
Comprehensive type annotations throughout:

```python
def schedule_meeting(
    start: DateTime,
    duration: Duration,
    attendee_timezones: list[str]
) -> list[DateTime]:
    return [
        start.to_timezone(tz)
        for tz in attendee_timezones
    ]
```

### Timezone Awareness
Strong emphasis on timezone-aware operations:

```python
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

Current version: **0.2.0**

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