# Duration

The `Duration` class represents a span of time - the difference between two moments. It provides a rich API for creating, manipulating, and working with time intervals.

## Overview

Duration objects are immutable and represent exact amounts of time that can be added to or subtracted from datetime objects. Unlike periods (which are calendar-based), durations represent fixed amounts of time.

```python
from carbonic import Duration, DateTime

# Create a duration
duration = Duration(days=2, hours=3, minutes=30)
print(duration)  # Duration(days=2, hours=3, minutes=30)

# Use with DateTime
dt = DateTime(2024, 1, 15, 10, 0, tz="UTC")
future = dt + duration
print(future)  # 2024-01-17T13:30:00+00:00
```

## Creating Duration Objects

### Constructor

```python
from carbonic import Duration

# All units are optional
duration = Duration(
    days=7,
    hours=12,
    minutes=30,
    seconds=45,
    microseconds=123456
)

# Common patterns
one_hour = Duration(hours=1)
half_day = Duration(hours=12)
three_days = Duration(days=3)
mixed = Duration(days=1, hours=2, minutes=30)
```

### From Total Units

```python
from carbonic import Duration

# Create from total values
from_seconds = Duration(seconds=3661)     # 1 hour, 1 minute, 1 second
from_minutes = Duration(minutes=90)       # 1 hour, 30 minutes
from_hours = Duration(hours=25)           # 25 hours
from_days = Duration(days=1, hours=12)    # 1 day, 12 hours

# From microseconds
from_microseconds = Duration(microseconds=1500000)  # 1.5 seconds
```

### From Timedelta

```python
from carbonic import Duration
import datetime

# Convert from Python's timedelta
td = datetime.timedelta(days=3, hours=2, minutes=15)
duration = Duration(seconds=int(td.total_seconds()))
print(duration)  # 3.0 days, 2.0 hours, and 15.0 minutes
```

### Zero Duration

```python
from carbonic import Duration

# Zero duration
zero = Duration()
print(zero)  # 0 seconds

# Alternative - explicit zero values
zero_alt = Duration(days=0, hours=0, minutes=0, seconds=0)
print(zero_alt)  # 0 seconds
```

## Duration Arithmetic

### Adding Durations

```python
from carbonic import Duration

d1 = Duration(hours=2, minutes=30)
d2 = Duration(hours=1, minutes=45)

# Add durations
total = d1 + d2
print(total)  # Duration(hours=4, minutes=15)

# Chain additions
result = (Duration(hours=1) +
    Duration(minutes=30) +
    Duration(seconds=45)
)
print(result)  # 1 hour, 30 minutes, and 45 seconds
```

### Subtracting Durations

```python
from carbonic import Duration

d1 = Duration(hours=3, minutes=30)
d2 = Duration(hours=1, minutes=15)

# Subtract durations
difference = d1 - d2
print(difference)  # Duration(hours=2, minutes=15)

# Same result using operator
result = d1 - d2
print(result)  # 2 hours and 15 minutes
```

### Multiplication and Division

```python
from carbonic import Duration

base = Duration(hours=2, minutes=30)

# Multiply by scalar
doubled = base * 2
print(doubled)  # 5 hours

# Division not directly supported, but can create new duration
half_seconds = base.total_seconds() / 2
halved = Duration(seconds=int(half_seconds))
print(halved)  # Duration for half the time
```

### Negation and Absolute Value

```python
from carbonic import Duration

duration = Duration(hours=2, minutes=30)

# Negate
negative = -duration
print(negative)  # Duration(days=0, hours=-2, minutes=-30)

# Absolute value
abs_duration = abs(negative)
print(abs_duration)  # Duration(hours=2, minutes=30)

# Check if negative
print(duration < Duration())   # False
print(negative < Duration())   # True
print(duration > Duration())   # True
```

## Using Durations with DateTime

### Adding to DateTime

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0, tz="UTC")
duration = Duration(days=3, hours=2, minutes=30)

# Add duration to datetime
future = dt + duration
print(future)  # 2024-01-18T12:30:00+00:00

# Alternative syntax
future_alt = dt.add_duration(duration)
print(future_alt)  # Same result
```

### Subtracting from DateTime

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0, tz="UTC")
duration = Duration(days=2, hours=1)

# Subtract duration from datetime
past = dt - duration
print(past)  # 2024-01-13T09:00:00+00:00

# Alternative syntax
past_alt = dt.subtract_duration(duration)
print(past_alt)  # Same result
```

### DateTime Differences Result in Durations

```python
from carbonic import DateTime

start = DateTime(2024, 1, 15, 10, 0, tz="UTC")
end = DateTime(2024, 1, 17, 14, 30, tz="UTC")

# Get duration between datetimes
duration = end - start
print(duration)  # Duration(days=2, hours=4, minutes=30)
print(type(duration))  # <class 'carbonic.core.duration.Duration'>
```

## Conversion and Access

### Total Values

```python
from carbonic import Duration

duration = Duration(days=2, hours=3, minutes=30, seconds=45)

# Get total values in different units
print(duration.total_seconds())      # 183045.0
print(duration.in_minutes())      # 3050.75
print(duration.in_hours())        # 50.845833333333336
print(duration.in_days())         # 2.118576388888889

# Get individual components
print(duration.days)                    # 2
total_seconds = duration.storage_seconds
remaining_hours = (total_seconds // 3600) % 24
remaining_minutes = (total_seconds // 60) % 60
remaining_seconds = total_seconds % 60
print(f"Remaining hours: {remaining_hours}")    # 3 (remaining after days)
print(f"Remaining minutes: {remaining_minutes}") # 30 (remaining after hours)
print(f"Remaining seconds: {remaining_seconds}") # 45 (remaining after minutes)
print(duration.microseconds)           # 0
```

### Component Access

```python
from carbonic import Duration

duration = Duration(days=5, hours=25, minutes=90)  # Overflow handled

print(f"Days: {duration.days}")           # 6 (25 hours = 1 day + 1 hour)
# Calculate remaining components
total_seconds = duration.storage_seconds
remaining_hours = (total_seconds // 3600) % 24
remaining_minutes = (total_seconds // 60) % 60
remaining_seconds = total_seconds % 60
print(f"Remaining hours: {remaining_hours}")    # 1 hour remaining after days
print(f"Remaining minutes: {remaining_minutes}") # 30 minutes remaining
print(f"Remaining seconds: {remaining_seconds}") # 0 seconds
```

### To Python Timedelta

```python
from carbonic import Duration

duration = Duration(days=3, hours=2, minutes=15)

# Convert to timedelta
import datetime
td = datetime.timedelta(seconds=duration.total_seconds())
print(type(td))  # <class 'datetime.timedelta'>
print(td)        # 3 days, 2:15:00
```

## Comparisons

### Basic Comparisons

```python
from carbonic import Duration

d1 = Duration(hours=2)
d2 = Duration(minutes=120)  # Same as 2 hours
d3 = Duration(hours=3)

# Equality
print(d1 == d2)  # True (same duration)
print(d1 == d3)  # False

# Ordering
print(d1 < d3)   # True
print(d3 > d1)   # True
print(d1 <= d2)  # True
print(d3 >= d2)  # True
```

### Fluent Comparison Methods

```python
from carbonic import Duration

d1 = Duration(hours=2, minutes=30)
d2 = Duration(hours=3)

# Standard comparison operators
print(d1 == d2)      # False
print(d1 < d2)       # True
print(d1 > d2)       # False
# Check if d1 is between two durations
print(Duration(hours=2) <= d1 <= Duration(hours=3))  # True
```

### Zero and Sign Checks

```python
from carbonic import Duration

zero = Duration()
positive = Duration(hours=1)
negative = Duration(hours=-1)

# Zero checks
print(zero == Duration())        # True
print(positive == Duration())    # False

# Sign checks
print(positive > Duration())  # True
print(negative < Duration())  # True
print(zero > Duration())      # False
print(zero < Duration())      # False
```

## Formatting and Display

### String Representation

```python
from carbonic import Duration

# Various durations
d1 = Duration(days=3, hours=2, minutes=30)
d2 = Duration(hours=1, seconds=45)
d3 = Duration(minutes=90)

print(str(d1))   # "Duration(days=3, hours=2, minutes=30)"
print(str(d2))   # "Duration(hours=1, seconds=45)"
print(str(d3))   # "Duration(hours=1, minutes=30)"  # Normalized

print(repr(d1))  # Shows full constructor call
```

### Human-Readable Format

```python
from carbonic import Duration

duration = Duration(days=2, hours=3, minutes=30)

# Human readable string (basic implementation)
def humanize_duration(d):
    parts = []
    total_seconds = d.storage_seconds

    days = d.days
    remaining_hours = (total_seconds // 3600) % 24
    remaining_minutes = (total_seconds // 60) % 60
    remaining_seconds = total_seconds % 60

    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if remaining_hours:
        parts.append(f"{remaining_hours} hour{'s' if remaining_hours != 1 else ''}")
    if remaining_minutes:
        parts.append(f"{remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}")
    if remaining_seconds:
        parts.append(f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}")

    return ", ".join(parts) if parts else "0 seconds"

print(humanize_duration(duration))  # "2 days, 3 hours, 30 minutes"
```

### ISO Duration Format

```python
from carbonic import Duration

duration = Duration(days=3, hours=2, minutes=30, seconds=45)

# ISO 8601 duration format (PT2H30M for 2 hours 30 minutes)
def to_iso_duration(d):
    parts = ["P"]
    total_seconds = d.storage_seconds

    days = d.days
    remaining_hours = (total_seconds // 3600) % 24
    remaining_minutes = (total_seconds // 60) % 60
    remaining_seconds = total_seconds % 60

    if days:
        parts.append(f"{days}D")

    time_parts = []
    if remaining_hours:
        time_parts.append(f"{remaining_hours}H")
    if remaining_minutes:
        time_parts.append(f"{remaining_minutes}M")
    if remaining_seconds or d.microseconds:
        if d.microseconds:
            total_secs = remaining_seconds + d.microseconds / 1_000_000
            time_parts.append(f"{total_secs}S")
        else:
            time_parts.append(f"{remaining_seconds}S")

    if time_parts:
        parts.append("T")
        parts.extend(time_parts)

    return "".join(parts) if len(parts) > 1 else "PT0S"

print(to_iso_duration(duration))  # "P3DT2H30M45S"
```

## Common Use Cases

### Timeouts and Intervals

```python
from carbonic import Duration, DateTime

# Define timeouts
short_timeout = Duration(seconds=30)
long_timeout = Duration(minutes=5)
session_timeout = Duration(hours=2)

# Check if timeout exceeded
start_time = DateTime.now()
# ... some operation ...
current_time = DateTime.now()
elapsed = current_time - start_time

if elapsed > short_timeout:
    print("Operation timed out!")
```

### Scheduling and Delays

```python
from carbonic import Duration, DateTime

# Schedule regular intervals
now = DateTime.now()
intervals = [
    Duration(minutes=15),   # Every 15 minutes
    Duration(hours=1),      # Every hour
    Duration(days=1),       # Daily
    Duration(days=7),       # Weekly
]

# Calculate next occurrences
next_times = [now + interval for interval in intervals]
for next_time in next_times:
    print(f"Next: {next_time}")
```

### Duration Calculations

```python
from carbonic import Duration

# Work day duration
work_day = Duration(hours=8)
lunch_break = Duration(minutes=30)
actual_work = work_day - lunch_break

print(f"Actual work time: {actual_work}")  # 7 hours 30 minutes

# Calculate pay periods
hourly_wage = 25  # dollars
weekly_hours = work_day * 5  # 5 work days
monthly_hours = weekly_hours * 4  # 4 weeks

weekly_pay = hourly_wage * weekly_hours.in_hours()
monthly_pay = hourly_wage * monthly_hours.in_hours()

print(f"Weekly pay: ${weekly_pay}")
print(f"Monthly pay: ${monthly_pay}")
```

### Measuring Performance

```python
from carbonic import Duration, DateTime
import time

# Measure operation duration
start = DateTime.now()

# Some operation
time.sleep(0.1)  # Simulate work

end = DateTime.now()
duration = end - start

print(f"Operation took: {duration.total_seconds():.3f} seconds")

# Performance budget
max_duration = Duration(milliseconds=100)
if duration > max_duration:
    print("Performance budget exceeded!")
```

## Advanced Features

### Duration Rounding

```python
from carbonic import Duration

# Create duration with fractional seconds
duration = Duration(seconds=45, microseconds=750000)  # 45.75 seconds

# Round to nearest second
rounded_seconds = Duration(seconds=round(duration.total_seconds()))
print(rounded_seconds)  # Duration(seconds=46)

# Round to nearest minute
rounded_minutes = Duration(minutes=round(duration.in_minutes()))
print(rounded_minutes)  # Duration(minutes=1)
```

### Duration Normalization

```python
from carbonic import Duration

# Durations are automatically normalized
duration = Duration(hours=25, minutes=90, seconds=120)
print(duration)  # Duration(days=1, hours=2, minutes=32)

# Manual normalization example
def normalize_duration(days=0, hours=0, minutes=0, seconds=0, microseconds=0):
    total_microseconds = (
        microseconds +
        seconds * 1_000_000 +
        minutes * 60 * 1_000_000 +
        hours * 60 * 60 * 1_000_000 +
        days * 24 * 60 * 60 * 1_000_000
    )
    return Duration(microseconds=total_microseconds)
```

### Working with Different Precisions

```python
from carbonic import Duration

# High precision duration
precise = Duration(microseconds=123456)
print(f"Microseconds: {precise.microseconds}")

# Convert to different precisions
milliseconds = precise.total_seconds() * 1000
print(f"Milliseconds: {milliseconds}")

# Round to millisecond precision
ms_duration = Duration(seconds=round(milliseconds / 1000, 3))
print(ms_duration)
```

## Best Practices

### Choose Appropriate Units

```python
from carbonic import Duration

# Good - use natural units
meeting_duration = Duration(hours=1, minutes=30)
coffee_break = Duration(minutes=15)
project_deadline = Duration(days=30)

# Avoid - unnecessarily complex
meeting_duration_bad = Duration(seconds=5400)  # Hard to read
```

### Use Constants for Common Durations

```python
from carbonic import Duration

# Define common durations as constants
MINUTE = Duration(minutes=1)
HOUR = Duration(hours=1)
DAY = Duration(days=1)
WEEK = Duration(days=7)

# Use in calculations
meeting_time = HOUR + Duration(minutes=30)
project_duration = WEEK * 4
```

### Handle Edge Cases

```python
from carbonic import Duration

# Be careful with zero durations
zero = Duration()
print(zero == Duration())  # True

# Handle negative durations appropriately
negative = Duration(hours=-2)
print(negative < Duration())  # True

# Consider absolute values when needed
absolute = abs(negative)
```

### Performance Considerations

```python
from carbonic import Duration

# Efficient - create once, reuse
base_interval = Duration(minutes=15)
intervals = [base_interval * i for i in range(1, 10)]

# Less efficient - create many Duration objects
intervals_bad = [Duration(minutes=15 * i) for i in range(1, 10)]
```