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
    .add_days(7)           # Add a week
    .add_hours(2)          # Add 2 hours
    .end_of_day()          # Move to end of day
    .to_timezone("America/New_York")  # Convert timezone
)

print(result)  # 2024-01-22T18:59:59.999999-05:00
```

## Formatting Dates

Carbonic provides multiple ways to format dates and times:

```python
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
result = dt.add_duration(mixed).subtract_hours(1)
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
next_week = today_date.add_days(7)
last_month = today_date.subtract_months(1)

# Date boundaries
start_of_month = today_date.start_of_month()
end_of_year = today_date.end_of_year()

print(f"Start of month: {start_of_month}")  # 2024-01-01
print(f"End of year: {end_of_year}")        # 2024-12-31
```

## Timezone Conversions

Carbonic makes timezone handling straightforward:

```python
from carbonic import DateTime

# Create UTC datetime
utc_time = DateTime(2024, 1, 15, 14, 30, tz="UTC")

# Convert to different timezones
tokyo_time = utc_time.to_timezone("Asia/Tokyo")
london_time = utc_time.to_timezone("Europe/London")
ny_time = utc_time.to_timezone("America/New_York")

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

# Useful methods
print(dt1.is_before(dt2))      # True
print(dt2.is_after(dt1))       # True
print(dt1.is_same_day(dt2))    # True
print(dt1.is_same_day(dt3))    # False

# Check relationships
print(dt1.is_past())           # True (assuming current time is later)
print(dt3.is_future())         # True (assuming current time is earlier)
```

## Common Use Cases

### Working with APIs

```python
from carbonic import DateTime

# Parse ISO datetime from API response
api_response = {"created_at": "2024-01-15T14:30:00Z"}
created = DateTime.from_iso(api_response["created_at"])

# Format for API request
request_data = {
    "start_date": created.to_iso_string(),
    "end_date": created.add_days(7).to_iso_string()
}
```

### Business Hours Calculations

```python
from carbonic import DateTime, Period

# Check if datetime falls on a business day
dt = DateTime(2024, 1, 15)  # Monday
print(dt.is_business_day())  # True

# Find next business day
next_business = dt.next_business_day()

# Get last Friday
last_friday = dt.previous(Period.FRIDAY)
```

### Scheduling and Intervals

```python
from carbonic import DateTime, Duration

# Schedule something for next Monday at 9 AM
now_dt = DateTime.now()
next_monday = now_dt.next(Period.MONDAY).set_time(9, 0, 0)

# Create a recurring interval
meeting_start = next_monday
meeting_duration = Duration(hours=1)
meeting_end = meeting_start + meeting_duration

print(f"Meeting: {meeting_start} to {meeting_end}")
```

## Next Steps

Now that you've seen the basics, explore more advanced features:

- [Core Concepts](concepts.md) - Understand immutability, timezones, and design principles
- [DateTime Guide](../guide/datetime.md) - Complete DateTime class reference
- [Duration Guide](../guide/duration.md) - Working with time spans
- [Examples](../examples/common-tasks.md) - Real-world usage patterns