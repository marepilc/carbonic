# Parsing & Formatting Guide

Comprehensive guide to parsing datetime strings and formatting datetime objects in Carbonic.

## Overview

Carbonic provides flexible parsing and formatting capabilities:
- **Automatic parsing** for common formats (ISO 8601, etc.)
- **Custom format parsing** using strftime or Carbon-style tokens
- **Rich formatting options** with Carbon-style tokens
- **Locale-aware formatting** for international applications

## Parsing DateTime Strings

### Automatic Parsing

Carbonic automatically detects and parses common datetime formats:

```python
from carbonic import DateTime

# ISO 8601 formats (recommended)
dt1 = DateTime.parse("2024-01-15T14:30:45+00:00")  # With timezone
dt2 = DateTime.parse("2024-01-15T14:30:45Z")       # UTC (Z suffix)
dt3 = DateTime.parse("2024-01-15T14:30:45")        # Naive (defaults to UTC)

# Date only (time defaults to 00:00:00)
dt4 = DateTime.parse("2024-01-15")                 # 2024-01-15T00:00:00+00:00

# Common variations
dt5 = DateTime.parse("2024-01-15 14:30:45")        # Space separator
```

### Parsing with Explicit Formats

For non-standard formats, specify the format explicitly:

```python
from carbonic import DateTime

# Using strftime format codes
dt1 = DateTime.parse("15/01/2024 14:30:45", "%d/%m/%Y %H:%M:%S")
dt2 = DateTime.parse("Jan 15, 2024 2:30 PM", "%b %d, %Y %I:%M %p")

# Using Carbon-style format tokens
dt3 = DateTime.parse("15-01-2024 14:30:45", "d-m-Y H:i:s")
dt4 = DateTime.parse("15 January 2024", "j F Y")
```

### Parsing with Timezone

```python
from carbonic import DateTime

# Parse and apply specific timezone
dt1 = DateTime.parse("2024-01-15 14:30:45", tz="Europe/Warsaw")
dt2 = DateTime.parse("15/01/2024 14:30", "%d/%m/%Y %H:%M", tz="America/New_York")

# Parse with timezone in the string
dt3 = DateTime.parse("2024-01-15T14:30:45+01:00")  # Preserves timezone info
```

## Parsing Date Strings

```python
from carbonic import Date

# Automatic parsing
date1 = Date.parse("2024-01-15")        # ISO format

# With explicit format
date2 = Date.parse("2024/01/15", "%Y/%m/%d")        # Slash format with explicit format
date3 = Date.parse("15-01-2024", "d-m-Y")           # European format with explicit format
date4 = Date.parse("Jan 15, 2024", "%b %d, %Y")
date5 = Date.parse("15 January 2024", "j F Y")      # Carbon format
```

## Error Handling

```python
from carbonic import DateTime
from carbonic.core.exceptions import ParseError

try:
    dt = DateTime.parse("invalid-date-string")
except ParseError as e:
    print(f"Parsing failed: {e}")

try:
    dt = DateTime.parse("2024-01-15", "%Y/%m/%d")  # Wrong format
except ParseError as e:
    print(f"Format mismatch: {e}")
```

## Formatting DateTime Objects

### Carbon-Style Formatting

Carbonic uses Carbon-inspired format tokens for flexible formatting:

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45)

# Date components
print(dt.format("Y-m-d"))          # 2024-01-15
print(dt.format("d/m/Y"))          # 15/01/2024
print(dt.format("j F Y"))          # 15 January 2024
print(dt.format("l, jS F Y"))      # Monday, 15th January 2024

# Time components
print(dt.format("H:i:s"))          # 14:30:45
print(dt.format("h:i A"))          # 02:30 PM
print(dt.format("g:i a"))          # 2:30 pm

# Combined formats
print(dt.format("Y-m-d H:i:s"))    # 2024-01-15 14:30:45
print(dt.format("l, F j, Y \\a\\t g:i A"))  # Monday, January 15, 2024 at 2:30 PM
```

### Format Token Reference

#### Date Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `Y` | 4-digit year | 2024 |
| `y` | 2-digit year | 24 |
| `m` | Month with leading zero | 01-12 |
| `n` | Month without leading zero | 1-12 |
| `F` | Full month name | January |
| `M` | Short month name | Jan |
| `d` | Day with leading zero | 01-31 |
| `j` | Day without leading zero | 1-31 |
| `S` | Ordinal suffix | st, nd, rd, th |
| `l` | Full day name | Monday |
| `D` | Short day name | Mon |

#### Time Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `H` | 24-hour with leading zero | 00-23 |
| `G` | 24-hour without leading zero | 0-23 |
| `h` | 12-hour with leading zero | 01-12 |
| `g` | 12-hour without leading zero | 1-12 |
| `i` | Minutes with leading zero | 00-59 |
| `s` | Seconds with leading zero | 00-59 |
| `A` | Uppercase AM/PM | AM, PM |
| `a` | Lowercase am/pm | am, pm |
| `u` | Microseconds | 000000-999999 |
| `v` | Milliseconds | 000-999 |

#### Timezone Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `T` | Timezone abbreviation | UTC, EST |
| `O` | Timezone offset | +0000, -0500 |
| `P` | Timezone offset with colon | +00:00, -05:00 |
| `Z` | Timezone offset in seconds | 0, -18000 |

#### Special Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `c` | ISO 8601 format | 2024-01-15T14:30:45+00:00 |
| `r` | RFC 2822 format | Mon, 15 Jan 2024 14:30:45 +0000 |

### Escaping Tokens

To include literal characters that would otherwise be interpreted as tokens:

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45)

# Escape tokens with curly braces
print(dt.format("{Y} = Y"))          # Y = 2024
print(dt.format("Year: {Y}Y"))       # Year: Y2024
print(dt.format("{H}:{i} means H:i")) # H:i means 14:30

# Use Python string literals for special characters
print(dt.format("Y-m-d\nH:i:s"))     # 2024-01-15\n14:30:45
```

### Built-in Format Methods

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, 123456)

# Common formats
print(dt.to_iso_string())        # 2024-01-15T14:30:45.123456+00:00
print(dt.to_date_string())       # 2024-01-15
print(dt.to_time_string())       # 14:30:45
print(dt.to_datetime_string())   # 2024-01-15 14:30:45

# Web formats
print(dt.to_atom_string())       # 2024-01-15T14:30:45+00:00
print(dt.to_cookie_string())     # Mon, 15-Jan-2024 14:30:45 UTC
```

### strftime Compatibility

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45)

# Standard strftime
print(dt.strftime("%Y-%m-%d %H:%M:%S"))      # 2024-01-15 14:30:45
print(dt.strftime("%A, %B %d, %Y"))         # Monday, January 15, 2024

# Python format protocol
print(f"{dt:%Y-%m-%d}")                     # 2024-01-15
print(format(dt, "%A, %B %d"))              # Monday, January 15
```

## Formatting Date Objects

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Carbon format
print(date.format("Y-m-d"))          # 2024-01-15
print(date.format("l, F j, Y"))      # Monday, January 15, 2024
print(date.format("d/m/y"))          # 15/01/24

# Built-in formats
print(date.to_iso_string())          # 2024-01-15
print(str(date))                     # 2024-01-15

# strftime
print(date.strftime("%B %d, %Y"))    # January 15, 2024
```

## Locale-Aware Formatting

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45)

# Different locales
print(dt.format("l, F j, Y", locale="en"))  # Monday, January 15, 2024
print(dt.format("l, j F Y", locale="pl"))   # poniedziałek, 15 stycznia 2024
print(dt.format("l, j {d}e F {d}e Y", locale="es"))  # lunes, 15 de enero de 2024
print(dt.format("l j F Y", locale="fr"))    # lundi 15 janvier 2024
```

## Performance Considerations

### Parsing Performance

```python
from carbonic import DateTime

# Fastest: ISO format auto-detection
dt1 = DateTime.parse("2024-01-15T14:30:45+00:00")

# Slower: Custom format parsing
dt2 = DateTime.parse("15/01/2024 14:30:45", "%d/%m/%Y %H:%M:%S")

# Optional: Use ciso8601 for faster ISO parsing (install separately)
# pip install carbonic[performance]
```

### Formatting Performance

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45)

# Fast: Built-in methods
iso_string = dt.to_iso_string()

# Moderate: Simple format strings
date_string = dt.format("Y-m-d")

# Slower: Complex format strings with locale
complex_string = dt.format("l, jS F Y", locale="pl")
```

## Common Patterns

### API Integration

```python
from carbonic import DateTime
import json

# Parse API responses
api_response = {"created_at": "2024-01-15T14:30:45Z"}
created = DateTime.parse(api_response["created_at"])

# Format for API requests
request_data = {
    "start_date": created.to_iso_string(),
    "end_date": created.add(days=7).to_iso_string()
}
```

### User-Friendly Display

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45)

def format_for_user(dt, user_locale="en"):
    """Format datetime for user display based on locale."""
    if user_locale == "en":
        return dt.format("l, F j, Y \\a\\t g:i A")  # Monday, January 15, 2024 at 2:30 PM
    elif user_locale == "pl":
        return dt.format("l, j F Y o G:i")         # poniedziałek, 15 stycznia 2024 o 14:30
    else:
        return dt.to_iso_string()

print(format_for_user(dt, "en"))  # Monday, January 15, 2024 at 2:30 PM
print(format_for_user(dt, "pl"))  # poniedziałek, 15 stycznia 2024 o 14:30
```

### Log Formatting

```python
from carbonic import DateTime

def create_log_entry(message, level="INFO"):
    """Create a log entry with timestamp."""
    timestamp = DateTime.now().format("Y-m-d H:i:s.v")
    return f"[{timestamp}] {level}: {message}"

print(create_log_entry("Application started"))
# [2024-01-15 14:30:45.123] INFO: Application started
```

## See Also

- [DateTime Guide](datetime.md) - Complete DateTime reference
- [Date Guide](date.md) - Date formatting and parsing
- [Localization Guide](localization.md) - Multi-language formatting
- [API Reference](../api/datetime.md#formatting) - Complete formatting API