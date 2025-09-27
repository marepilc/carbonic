# Quick Start

This guide will get you up and running with Carbonic in just a few minutes.

## Your First DateTime

Let's start with the basics - creating and working with datetime objects:

```python
from carbonic import DateTime, now, today

# Get current time (UTC by default)
current = now()
print(current)  # 2024-01-15T14:30:00+00:00

# Get current time in a specific timezone
ny_time = now("America/New_York")
print(ny_time)  # 2024-01-15T09:30:00-05:00

# Create a specific datetime
birthday = DateTime(1990, 5, 15, 14, 30, tz="UTC")
print(birthday)  # 1990-05-15T14:30:00+00:00
```

## Basic Operations

Carbonic uses a fluent API - operations can be chained together naturally:

```python
from carbonic import DateTime, Duration

# Start with a datetime
dt = DateTime(2024, 1, 15, 9, 0, tz="UTC")

# Chain operations together
result = (dt
    .add(days=7)           # Add a week
    .add(hours=2)          # Add 2 hours
    .end_of("day")         # Move to end of day
)

print(result)  # 2024-01-22T23:59:59.999999+00:00
```

## Formatting Dates

Carbonic provides multiple ways to format dates and times:

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# ISO format
print(dt.to_iso_string())        # "2024-01-15T14:30:45+00:00"

# Custom format (PHP Carbon style)
print(dt.format("Y-m-d H:i:s"))   # "2024-01-15 14:30:45"
print(dt.format("l, F j, Y"))     # "Monday, January 15, 2024"

# Date only
print(dt.to_date_string())       # "2024-01-15"

# Time only
print(dt.to_time_string())       # "14:30:45"
```

## Working with Durations

Durations represent spans of time and can be added to or subtracted from datetimes:

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0, tz="UTC")

# Create durations
hour_and_half = Duration(hours=1, minutes=30)
three_days = Duration(days=3)
mixed = Duration(days=1, hours=2, minutes=30, seconds=45)

# Add durations
future = dt + hour_and_half
print(future)  # 2024-01-15T11:30:00+00:00

# Subtract durations
past = dt - three_days
print(past)    # 2024-01-12T10:00:00+00:00

# Chain with fluent methods
result = dt.add_duration(mixed).subtract(hours=1)
print(result)  # 2024-01-16T11:30:45+00:00
```

## Date-Only Operations

For when you only need dates without times:

```python
from carbonic import Date, today

# Get today's date
today_date = today()
print(today_date)  # 2024-01-15

# Create specific dates
birthday = Date(1990, 5, 15)
holiday = Date(2024, 12, 25)

# Date arithmetic
next_week = today_date.add(days=7)
last_month = today_date.subtract(months=1)

# Date boundaries
start_of_month = today_date.start_of("month")
end_of_year = today_date.end_of("year")

print(f"Start of month: {start_of_month}")  # 2024-01-01
print(f"End of year: {end_of_year}")        # 2024-12-31
```

## Timezone Conversions

Carbonic makes timezone handling straightforward:

```python
from carbonic import DateTime

# Create datetime in different timezones
utc_time = DateTime(2024, 1, 15, 14, 30, tz="UTC")
tokyo_time = DateTime(2024, 1, 15, 23, 30, tz="Asia/Tokyo")  # Same moment
london_time = DateTime(2024, 1, 15, 14, 30, tz="Europe/London")
ny_time = DateTime(2024, 1, 15, 9, 30, tz="America/New_York")

print(f"UTC:    {utc_time}")     # 2024-01-15T14:30:00+00:00
print(f"Tokyo:  {tokyo_time}")   # 2024-01-15T23:30:00+09:00
print(f"London: {london_time}")  # 2024-01-15T14:30:00+00:00
print(f"NY:     {ny_time}")      # 2024-01-15T09:30:00-05:00
```

## Comparisons

Compare dates and times naturally:

```python
from carbonic import DateTime

dt1 = DateTime(2024, 1, 15, 10, 0, tz="UTC")
dt2 = DateTime(2024, 1, 15, 14, 0, tz="UTC")
dt3 = DateTime(2024, 1, 16, 10, 0, tz="UTC")

# Basic comparisons
print(dt1 < dt2)   # True
print(dt2 > dt3)   # False
print(dt1 == dt1)  # True

# More comparisons
print(dt1 <= dt2)  # True
print(dt2 >= dt1)  # True
print(dt1 != dt2)  # True

# Check if dates are the same
same_day = (dt1.year == dt2.year and dt1.month == dt2.month and dt1.day == dt2.day)
print(f"Same day: {same_day}")  # True
```

## Common Use Cases

### Working with APIs

```python
from carbonic import DateTime

# Parse ISO datetime from API response
api_response = {"created_at": "2024-01-15T14:30:00Z"}
created = DateTime.parse(api_response["created_at"])

# Format for API request
request_data = {
    "start_date": created.to_iso_string(),
    "end_date": created.add(days=7).to_iso_string()
}
```

### Business Hours Calculations

```python
from carbonic import DateTime, Period

# Check if datetime falls on a business day
dt = DateTime(2024, 1, 15)  # Monday
date_part = dt.to_date()
print(date_part.is_weekday())  # True

# Find next business day
date_part = dt.to_date()
next_business_date = date_part.add_business_days(1)
print(f"Next business day: {next_business_date}")

# Add business days
week_later = date_part.add_business_days(5)
print(f"5 business days later: {week_later}")
```

### Scheduling and Intervals

```python
from carbonic import DateTime, Duration

# Schedule a meeting
meeting_start = DateTime(2024, 1, 22, 9, 0, tz="UTC")  # Next Monday at 9 AM
meeting_duration = Duration(hours=1)
meeting_end = meeting_start + meeting_duration

print(f"Meeting: {meeting_start} to {meeting_end}")
print(f"Duration: {meeting_duration.in_hours()} hours")
```

## Next Steps

Now that you've seen the basics, explore more advanced features:

- [Core Concepts](concepts.md) - Understand immutability, timezones, and design principles
- [DateTime Guide](../guide/datetime.md) - Complete DateTime class reference
- [Duration Guide](../guide/duration.md) - Working with time spans
- [Examples](../examples/common-tasks.md) - Real-world usage patterns