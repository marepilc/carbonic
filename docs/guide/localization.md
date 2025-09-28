# Localization Guide

Comprehensive guide to using Carbonic's multi-language support for datetime formatting and humanization.

## Overview

Carbonic provides comprehensive localization support for:
- **Date/time formatting** with localized month and day names
- **Duration humanization** with proper pluralization rules
- **Number formatting** with locale-specific decimal separators
- **6 languages**: English, Polish, Spanish, French, German, Portuguese

## Supported Locales

```python
from carbonic import DateTime, Duration

# Available locales
locales = ["en", "pl", "es", "fr", "de", "pt"]

dt = DateTime(2024, 1, 15, 14, 30)
duration = Duration(hours=2, minutes=30)

for locale in locales:
    formatted = dt.format("l, F j, Y", locale=locale)
    humanized = duration.humanize(locale=locale)
    print(f"{locale}: {formatted} - {humanized}")
```

## Date and Time Formatting

### Month Names

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30)

# Full month names
print("Full month names:")
print(f"English:    {dt.format('F', locale='en')}")     # January
print(f"Polish:     {dt.format('F', locale='pl')}")     # stycznia (genitive)
print(f"Spanish:    {dt.format('F', locale='es')}")     # enero
print(f"French:     {dt.format('F', locale='fr')}")     # janvier
print(f"German:     {dt.format('F', locale='de')}")     # Januar
print(f"Portuguese: {dt.format('F', locale='pt')}")     # janeiro

# Short month names
print("\nShort month names:")
print(f"English:    {dt.format('M', locale='en')}")     # Jan
print(f"Polish:     {dt.format('M', locale='pl')}")     # sty
print(f"Spanish:    {dt.format('M', locale='es')}")     # ene
```

### Day Names

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30)  # Monday

# Full day names
print("Full day names:")
print(f"English:    {dt.format('l', locale='en')}")     # Monday
print(f"Polish:     {dt.format('l', locale='pl')}")     # poniedziałek
print(f"Spanish:    {dt.format('l', locale='es')}")     # lunes
print(f"French:     {dt.format('l', locale='fr')}")     # lundi
print(f"German:     {dt.format('l', locale='de')}")     # Montag
print(f"Portuguese: {dt.format('l', locale='pt')}")     # segunda-feira

# Short day names
print("\nShort day names:")
print(f"English:    {dt.format('D', locale='en')}")     # Mon
print(f"Polish:     {dt.format('D', locale='pl')}")     # pon
print(f"Spanish:    {dt.format('D', locale='es')}")     # lun
```

### Complete Date Formats

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30)

# Natural date formats for each locale
formats = {
    "en": "l, F j, Y",           # Monday, January 15, 2024
    "pl": "l, j F Y",            # poniedziałek, 15 stycznia 2024
    "es": "l, j {d}e F {d}e Y",  # lunes, 15 de enero de 2024
    "fr": "l j F Y",             # lundi 15 janvier 2024
    "de": "l, j. F Y",           # Montag, 15. Januar 2024
    "pt": "l, j {d}e F {d}e Y",  # segunda-feira, 15 de janeiro de 2024
}

for locale, format_str in formats.items():
    result = dt.format(format_str, locale=locale)
    print(f"{locale}: {result}")
```

## Duration Humanization

### Basic Humanization

```python
from carbonic import Duration

duration = Duration(hours=2, minutes=30)

print("2 hours 30 minutes:")
print(f"English:    {duration.humanize(locale='en')}")    # 2 hours 30 minutes
print(f"Polish:     {duration.humanize(locale='pl')}")    # 2 godziny 30 minut
print(f"Spanish:    {duration.humanize(locale='es')}")    # 2 horas 30 minutos
print(f"French:     {duration.humanize(locale='fr')}")    # 2 heures 30 minutes
print(f"German:     {duration.humanize(locale='de')}")    # 2 Stunden 30 Minuten
print(f"Portuguese: {duration.humanize(locale='pt')}")    # 2 horas 30 minutos
```

### Pluralization Rules

Different languages have different pluralization rules:

```python
from carbonic import Duration

# English: simple plural (1 hour, 2 hours)
print("English pluralization:")
print(Duration(hours=1).humanize(locale="en"))    # 1 hour
print(Duration(hours=2).humanize(locale="en"))    # 2 hours
print(Duration(hours=5).humanize(locale="en"))    # 5 hours

# Polish: complex 3-form pluralization
print("\nPolish pluralization:")
print(Duration(hours=1).humanize(locale="pl"))    # 1 godzina (singular)
print(Duration(hours=2).humanize(locale="pl"))    # 2 godziny (plural 2-4)
print(Duration(hours=5).humanize(locale="pl"))    # 5 godzin (plural 5+)
print(Duration(hours=22).humanize(locale="pl"))   # 22 godziny (ends in 2-4)
print(Duration(hours=25).humanize(locale="pl"))   # 25 godzin (ends in 5+)
```

### Different Time Units

```python
from carbonic import Duration

# Various durations
durations = [
    Duration(seconds=30),
    Duration(minutes=1),
    Duration(hours=1),
    Duration(days=1),
    Duration(weeks=1),
    Duration(months=1),
    Duration(years=1)
]

print("Duration humanization across locales:")
for duration in durations:
    en = duration.humanize(locale="en")
    pl = duration.humanize(locale="pl")
    es = duration.humanize(locale="es")
    print(f"{en:15} | {pl:15} | {es}")
```

## Number Formatting

### Decimal Separators

```python
from carbonic import Duration

# Duration with fractional seconds
duration = Duration(seconds=45, microseconds=500000)  # 45.5 seconds

print("Decimal separator formatting:")
print(f"English (dot):     {duration.humanize(locale='en')}")    # 45.5 seconds
print(f"Polish (comma):    {duration.humanize(locale='pl')}")    # 45,5 sekundy
print(f"Spanish (comma):   {duration.humanize(locale='es')}")    # 45,5 segundos
print(f"French (comma):    {duration.humanize(locale='fr')}")    # 45,5 secondes
print(f"German (comma):    {duration.humanize(locale='de')}")    # 45,5 Sekunden
print(f"Portuguese (comma): {duration.humanize(locale='pt')}")   # 45,5 segundos
```

## Advanced Localization

### Handling Special Cases

```python
from carbonic import DateTime

# Month names in different contexts
dt = DateTime(2024, 5, 15, 14, 30)

# Polish months change form in different contexts
print("Polish month handling:")
print(f"Nominative: {dt.format('F', locale='pl')}")      # maja (genitive case)
print(f"With day:   {dt.format('j F', locale='pl')}")    # 15 maja

# French months (some are invariant)
dt_march = DateTime(2024, 3, 15)
print(f"French March: {dt_march.format('F', locale='fr')}")  # mars (no change)
```

### Zero and Negative Durations

```python
from carbonic import Duration

zero_duration = Duration()
negative_duration = Duration(hours=-2, minutes=-30)

print("Special duration cases:")
for locale in ["en", "pl", "es", "fr", "de", "pt"]:
    zero = zero_duration.humanize(locale=locale)
    negative = negative_duration.humanize(locale=locale)
    print(f"{locale}: '{zero}' | '{negative}'")
```

### Controlling Precision

```python
from carbonic import Duration

long_duration = Duration(days=1, hours=2, minutes=30, seconds=45)

print("Duration precision control:")
for locale in ["en", "pl", "es"]:
    # Default (all units)
    full = long_duration.humanize(locale=locale)

    # Limited units
    limited = long_duration.humanize(locale=locale, max_units=2)

    print(f"{locale}:")
    print(f"  Full:    {full}")
    print(f"  Limited: {limited}")
```

## Practical Examples

### User Interface Localization

```python
from carbonic import DateTime, Duration

def format_user_datetime(dt, user_locale="en"):
    """Format datetime for user interface based on their locale."""
    formats = {
        "en": "l, M j, Y \\a\\t g:i A",        # Monday, Jan 15, 2024 at 2:30 PM
        "pl": "l, j M Y o G:i",               # poniedziałek, 15 sty 2024 o 14:30
        "es": "l, j {d}e M {d}e Y {a} \\l\\a\\s G:i",  # lunes, 15 de ene de 2024 a las 14:30
        "fr": "l j M Y \\à G:i",              # lundi 15 jan 2024 à 14:30
        "de": "l, j. M Y \\u\\m G:i",         # Montag, 15. Jan 2024 um 14:30
        "pt": "l, j {d}e M {d}e Y \\à\\s G:i", # segunda-feira, 15 de jan de 2024 às 14:30
    }

    format_str = formats.get(user_locale, formats["en"])
    return dt.format(format_str, locale=user_locale)

# Usage
dt = DateTime(2024, 1, 15, 14, 30)
for locale in ["en", "pl", "es", "fr", "de", "pt"]:
    formatted = format_user_datetime(dt, locale)
    print(f"{locale}: {formatted}")
```

### Relative Time Display

```python
from carbonic import DateTime, Duration

def relative_time_display(past_dt, current_dt=None, locale="en"):
    """Display relative time like 'posted 2 hours ago'."""
    if current_dt is None:
        current_dt = DateTime.now()

    duration = current_dt.diff(past_dt)
    humanized = duration.humanize(locale=locale, max_units=1)

    # Locale-specific formatting
    ago_text = {
        "en": "ago",
        "pl": "temu",
        "es": "hace",
        "fr": "il y a",
        "de": "vor",
        "pt": "atrás"
    }

    ago = ago_text.get(locale, ago_text["en"])

    if locale in ["fr"]:
        return f"{ago} {humanized}"  # French: "il y a 2 heures"
    elif locale in ["es"]:
        return f"{ago} {humanized}"  # Spanish: "hace 2 horas"
    else:
        return f"{humanized} {ago}"  # Others: "2 hours ago"

# Usage
past_time = DateTime.now().subtract(hours=2, minutes=15)
current_time = DateTime.now()

for locale in ["en", "pl", "es", "fr", "de", "pt"]:
    relative = relative_time_display(past_time, current_time, locale)
    print(f"{locale}: {relative}")
```

### Multilingual Logging

```python
from carbonic import DateTime

class LocalizedLogger:
    def __init__(self, locale="en"):
        self.locale = locale

    def log_event(self, event, level="INFO"):
        """Create localized log entry."""
        timestamp = DateTime.now()

        # Locale-specific timestamp format
        if self.locale == "en":
            time_str = timestamp.format("M j, Y H:i:s")
        elif self.locale == "pl":
            time_str = timestamp.format("j M Y H:i:s", locale="pl")
        elif self.locale == "es":
            time_str = timestamp.format("j {d}e M {d}e Y H:i:s", locale="es")
        else:
            time_str = timestamp.to_iso_string()

        return f"[{time_str}] {level}: {event}"

# Usage
loggers = {
    "en": LocalizedLogger("en"),
    "pl": LocalizedLogger("pl"),
    "es": LocalizedLogger("es")
}

for locale, logger in loggers.items():
    entry = logger.log_event("User login successful")
    print(f"{locale}: {entry}")
```

## Error Handling

```python
from carbonic import DateTime, Duration

def safe_localized_format(dt, format_str, locale="en"):
    """Safely format with fallback to English."""
    try:
        return dt.format(format_str, locale=locale)
    except (ValueError, KeyError):
        # Fallback to English if locale not supported
        return dt.format(format_str, locale="en")

# Usage
dt = DateTime(2024, 1, 15, 14, 30)
result = safe_localized_format(dt, "l, F j, Y", locale="invalid_locale")
print(result)  # Falls back to English
```

## Performance Considerations

### Locale Caching

Carbonic automatically caches locale data for performance:

```python
from carbonic import DateTime, Duration

# First call loads locale data
dt = DateTime(2024, 1, 15)
result1 = dt.format("l, F j, Y", locale="pl")  # Loads Polish locale

# Subsequent calls use cached data
result2 = dt.format("j F Y", locale="pl")      # Uses cached Polish locale

# Different locale loads separately
result3 = dt.format("l, F j, Y", locale="es")  # Loads Spanish locale
```

### Bulk Operations

```python
from carbonic import DateTime

# Efficient for multiple operations with same locale
dates = [DateTime(2024, 1, i) for i in range(1, 32)]

# Good: Consistent locale
formatted_pl = [dt.format("j F", locale="pl") for dt in dates]

# Less efficient: Switching locales frequently
# formatted_mixed = [dt.format("j F", locale="pl" if i % 2 else "en") for i, dt in enumerate(dates)]
```

## See Also

- [Parsing & Formatting](parsing-formatting.md) - Format token reference
- [Duration Guide](duration.md) - Duration humanization details
- [DateTime Guide](datetime.md) - Complete DateTime formatting
- [API Reference](../api/locale.md) - Complete localization API