# Timezone Handling Guide

Comprehensive guide to working with timezones in Carbonic, including conversion, DST handling, and best practices.

## Overview

Carbonic provides robust timezone support using Python's `zoneinfo` module with:
- **Automatic UTC defaults** for timezone-aware operations
- **Seamless conversions** between timezones
- **DST handling** with proper transitions
- **Naive datetime support** when needed

## Creating Timezone-Aware DateTimes

### Default Behavior

```python
from carbonic import DateTime

# Defaults to UTC
dt = DateTime(2024, 1, 15, 14, 30)
print(dt)  # 2024-01-15T14:30:00+00:00

# Explicit UTC
dt_utc = DateTime(2024, 1, 15, 14, 30, tz="UTC")
print(dt_utc)  # 2024-01-15T14:30:00+00:00
```

### Specific Timezones

```python
from carbonic import DateTime

# Major timezones
dt_ny = DateTime(2024, 1, 15, 14, 30, tz="America/New_York")
dt_london = DateTime(2024, 1, 15, 14, 30, tz="Europe/London")
dt_tokyo = DateTime(2024, 1, 15, 14, 30, tz="Asia/Tokyo")

print(dt_ny)     # 2024-01-15T14:30:00-05:00 (EST)
print(dt_london) # 2024-01-15T14:30:00+00:00 (GMT)
print(dt_tokyo)  # 2024-01-15T14:30:00+09:00 (JST)
```

### Current Time in Different Timezones

```python
from carbonic import DateTime

# Current time in various timezones
utc_now = DateTime.now()                              # UTC
ny_now = DateTime.now("America/New_York")            # New York time
paris_now = DateTime.now("Europe/Paris")             # Paris time
sydney_now = DateTime.now("Australia/Sydney")        # Sydney time

print(f"UTC:    {utc_now}")
print(f"NY:     {ny_now}")
print(f"Paris:  {paris_now}")
print(f"Sydney: {sydney_now}")
```

## Timezone Conversion

### Basic Conversion

```python
from carbonic import DateTime

# Start with UTC
utc_time = DateTime(2024, 1, 15, 14, 30, tz="UTC")
print(f"UTC: {utc_time}")

# Convert to different timezones
ny_time = utc_time.as_timezone("America/New_York")
london_time = utc_time.as_timezone("Europe/London")
tokyo_time = utc_time.as_timezone("Asia/Tokyo")

print(f"New York: {ny_time}")    # 09:30 EST (UTC-5)
print(f"London:   {london_time}") # 14:30 GMT (UTC+0)
print(f"Tokyo:    {tokyo_time}")  # 23:30 JST (UTC+9)

# All represent the same moment in time
assert utc_time == ny_time == london_time == tokyo_time
```

### Round-Trip Conversion

```python
from carbonic import DateTime

# Original time
original = DateTime(2024, 6, 15, 14, 30, tz="Europe/Warsaw")
print(f"Original: {original}")

# Convert to different timezone and back
converted = original.as_timezone("America/Los_Angeles")
back_to_original = converted.as_timezone("Europe/Warsaw")

print(f"Converted: {converted}")
print(f"Back: {back_to_original}")

# Should be identical
assert original == back_to_original
```

### Converting to Naive

```python
from carbonic import DateTime

# Timezone-aware datetime
aware_dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

# Convert to naive (removes timezone info, keeps local time)
naive_dt = aware_dt.as_timezone(None)
print(f"Aware: {aware_dt}")  # 2024-01-15T14:30:00+00:00
print(f"Naive: {naive_dt}")  # 2024-01-15T14:30:00
```

## Daylight Saving Time (DST)

### DST Transitions

```python
from carbonic import DateTime

# Before DST starts (Winter time)
winter_time = DateTime(2024, 3, 9, 15, 0, tz="America/New_York")  # EST
print(f"Winter: {winter_time}")  # UTC-5

# After DST starts (Summer time)
summer_time = DateTime(2024, 3, 11, 15, 0, tz="America/New_York")  # EDT
print(f"Summer: {summer_time}")  # UTC-4

# Convert both to UTC to see the difference
winter_utc = winter_time.as_timezone("UTC")
summer_utc = summer_time.as_timezone("UTC")
print(f"Winter UTC: {winter_utc}")  # 20:00 UTC
print(f"Summer UTC: {summer_utc}")  # 19:00 UTC
```

### DST-Safe Arithmetic

```python
from carbonic import DateTime

# Day before DST starts
before_dst = DateTime(2024, 3, 9, 10, 0, tz="America/New_York")

# Add 24 hours - this handles DST transition correctly
after_24h = before_dst.add(hours=24)
print(f"24 hours later: {after_24h}")

# Add 1 day - this maintains the same local time
next_day = before_dst.add(days=1)
print(f"1 day later: {next_day}")

# They might be different due to DST!
print(f"Same time? {after_24h == next_day}")
```

## Working with Naive DateTimes

### Creating Naive DateTimes

```python
from carbonic import DateTime

# Explicit naive datetime
naive_dt = DateTime(2024, 1, 15, 14, 30, tz=None)
print(f"Naive: {naive_dt}")  # 2024-01-15T14:30:00 (no timezone)

# Check if datetime is naive
print(f"Is naive? {naive_dt.tzinfo is None}")  # True
```

### Converting Naive to Aware

```python
from carbonic import DateTime

# Start with naive
naive_dt = DateTime(2024, 1, 15, 14, 30, tz=None)

# Cannot directly convert naive to aware - would be ambiguous
try:
    aware_dt = naive_dt.as_timezone("UTC")  # This will raise an error
except ValueError as e:
    print(f"Error: {e}")

# Instead, create a new aware datetime
aware_dt = DateTime(
    naive_dt.year, naive_dt.month, naive_dt.day,
    naive_dt.hour, naive_dt.minute, naive_dt.second,
    naive_dt.microsecond, tz="UTC"
)
print(f"Now aware: {aware_dt}")
```

## Common Timezone Operations

### Comparing Times Across Timezones

```python
from carbonic import DateTime

# Same moment in different timezones
utc_meeting = DateTime(2024, 1, 15, 15, 0, tz="UTC")
ny_meeting = utc_meeting.as_timezone("America/New_York")  # 10:00 EST
london_meeting = utc_meeting.as_timezone("Europe/London")  # 15:00 GMT

# All comparisons work correctly
print(f"UTC == NY: {utc_meeting == ny_meeting}")        # True
print(f"NY < London: {ny_meeting < london_meeting}")    # False (same time)
print(f"Meeting times equal: {utc_meeting == ny_meeting == london_meeting}")  # True
```

### Finding Business Hours

```python
from carbonic import DateTime

def is_business_hours(dt, timezone="America/New_York"):
    """Check if datetime falls within business hours (9 AM - 5 PM)."""
    local_time = dt.as_timezone(timezone)
    return 9 <= local_time.hour < 17 and local_time.to_date().is_weekday()

# Test with different times
utc_time = DateTime(2024, 1, 15, 14, 0, tz="UTC")  # Monday 2 PM UTC

print(f"Business hours in NY: {is_business_hours(utc_time, 'America/New_York')}")  # True (9 AM EST)
print(f"Business hours in Tokyo: {is_business_hours(utc_time, 'Asia/Tokyo')}")     # False (11 PM JST)
```

## Best Practices

### Always Use Timezone-Aware DateTimes

```python
from carbonic import DateTime

# ✅ Good: Explicit timezone
meeting_time = DateTime(2024, 1, 15, 14, 0, tz="UTC")
user_time = meeting_time.as_timezone("America/New_York")

# ❌ Avoid: Naive datetime for anything that will be shared
# naive_time = DateTime(2024, 1, 15, 14, 0, tz=None)  # Ambiguous!
```

### Store in UTC, Display in Local

```python
from carbonic import DateTime

# Store everything in UTC
def store_event(event_data):
    """Store event with UTC timestamp."""
    return {
        **event_data,
        'created_at': DateTime.now().to_iso_string(),  # Always UTC
        'scheduled_for': event_data['local_time'].as_timezone("UTC").to_iso_string()
    }

# Display in user's timezone
def display_event(event_data, user_timezone="America/New_York"):
    """Display event in user's local timezone."""
    utc_time = DateTime.parse(event_data['scheduled_for'])
    local_time = utc_time.as_timezone(user_timezone)
    return f"Event at {local_time.format('g:i A')} ({user_timezone})"
```

### Handle Timezone Conversion Errors

```python
from carbonic import DateTime

def safe_timezone_convert(dt, target_timezone):
    """Safely convert timezone with error handling."""
    try:
        return dt.as_timezone(target_timezone)
    except ValueError as e:
        print(f"Timezone conversion failed: {e}")
        return dt  # Return original if conversion fails

# Usage
dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
result = safe_timezone_convert(dt, "Invalid/Timezone")  # Handles error gracefully
```

## Common Timezones Reference

### Major World Timezones

```python
from carbonic import DateTime

utc_time = DateTime(2024, 1, 15, 12, 0, tz="UTC")  # Noon UTC

major_timezones = {
    "UTC": "UTC",
    "New York": "America/New_York",      # EST/EDT
    "Los Angeles": "America/Los_Angeles", # PST/PDT
    "London": "Europe/London",           # GMT/BST
    "Paris": "Europe/Paris",             # CET/CEST
    "Warsaw": "Europe/Warsaw",           # CET/CEST
    "Tokyo": "Asia/Tokyo",               # JST
    "Sydney": "Australia/Sydney",        # AEST/AEDT
    "Mumbai": "Asia/Kolkata",            # IST
    "Dubai": "Asia/Dubai",               # GST
}

print("Noon UTC in major cities:")
for city, tz in major_timezones.items():
    local_time = utc_time.as_timezone(tz)
    print(f"{city:12}: {local_time.format('H:i (T)')}")
```

### US Timezones

```python
from carbonic import DateTime

us_timezones = {
    "Eastern": "America/New_York",
    "Central": "America/Chicago",
    "Mountain": "America/Denver",
    "Pacific": "America/Los_Angeles",
    "Alaska": "America/Anchorage",
    "Hawaii": "Pacific/Honolulu",
}

utc_time = DateTime(2024, 7, 15, 20, 0, tz="UTC")  # 8 PM UTC in summer

print("8 PM UTC across US timezones:")
for zone_name, tz in us_timezones.items():
    local_time = utc_time.as_timezone(tz)
    print(f"{zone_name:8}: {local_time.format('g:i A')}")
```

## See Also

- [DateTime Guide](datetime.md) - Complete DateTime operations
- [Parsing & Formatting](parsing-formatting.md) - Working with timezone strings
- [API Reference](../api/datetime.md#timezone-methods) - Complete timezone API
- [Examples](../examples/common-tasks.md#timezone-operations) - Practical timezone examples