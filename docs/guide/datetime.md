# DateTime

The `DateTime` class is the heart of Carbonic, providing a comprehensive, immutable datetime object with timezone support and a fluent API.

## Overview

The `DateTime` class wraps Python's standard `datetime.datetime` while providing additional functionality and a more intuitive interface. Every `DateTime` object is immutable, meaning all operations return new instances.

```python
from carbonic import DateTime, now

# Create a DateTime instance
dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
print(dt)  # 2024-01-15T14:30:00+00:00

# Get current time
current = now()  # UTC by default
local = now("America/New_York")
```

## Creating DateTime Objects

### Constructor

```python
from carbonic import DateTime

# Full specification
dt = DateTime(
    year=2024,
    month=1,
    day=15,
    hour=14,
    minute=30,
    second=45,
    microsecond=123456,
    tz="UTC"
)

# Minimal specification (defaults to midnight UTC)
dt = DateTime(2024, 1, 15)  # 2024-01-15T00:00:00+00:00

# Without timezone (naive - not recommended)
naive = DateTime(2024, 1, 15, tz=None)
```

### Factory Methods

```python
from carbonic import DateTime

# Current time
now_utc = DateTime.now()  # UTC by default
now_local = DateTime.now("America/New_York")

# From standard library datetime
import datetime
stdlib_dt = datetime.datetime(2024, 1, 15, 14, 30, tzinfo=datetime.timezone.utc)
carbonic_dt = DateTime.from_datetime(stdlib_dt)

# From timestamp
timestamp_dt = DateTime.from_timestamp(1705330200, tz="UTC")

# From ISO string
iso_dt = DateTime.from_iso("2024-01-15T14:30:00Z")

# From custom format
custom_dt = DateTime.from_format("15/01/2024 14:30", "d/m/Y H:i")
```

## Date and Time Arithmetic

### Adding Time

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0, tz="UTC")

# Using fluent methods
future = dt.add_years(1).add_months(2).add_days(3).add_hours(4)

# Using Duration objects
duration = Duration(days=7, hours=12, minutes=30)
future = dt + duration

# Specific unit methods
next_hour = dt.add_hours(1)
next_day = dt.add_days(1)
next_week = dt.add_weeks(1)
next_month = dt.add_months(1)
next_year = dt.add_years(1)
```

### Subtracting Time

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0, tz="UTC")

# Using fluent methods
past = dt.subtract_days(5).subtract_hours(2)

# Using Duration objects
duration = Duration(days=3, hours=6)
past = dt - duration

# Specific unit methods
last_hour = dt.subtract_hours(1)
yesterday = dt.subtract_days(1)
last_week = dt.subtract_weeks(1)
last_month = dt.subtract_months(1)
last_year = dt.subtract_years(1)
```

### Setting Specific Values

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# Set specific components
new_dt = dt.set_year(2025)
new_dt = dt.set_month(12)
new_dt = dt.set_day(31)
new_dt = dt.set_hour(0)
new_dt = dt.set_minute(0)
new_dt = dt.set_second(0)
new_dt = dt.set_microsecond(0)

# Set multiple at once
new_dt = dt.set_date(2025, 12, 31)
new_dt = dt.set_time(23, 59, 59)
new_dt = dt.set_datetime(2025, 12, 31, 23, 59, 59)
```

## Date Boundaries and Navigation

### Start and End Points

```python
from carbonic import DateTime

dt = DateTime(2024, 3, 15, 14, 30, 45, tz="UTC")

# Day boundaries
start_of_day = dt.start_of_day()        # 2024-03-15T00:00:00+00:00
end_of_day = dt.end_of_day()            # 2024-03-15T23:59:59.999999+00:00

# Week boundaries
start_of_week = dt.start_of_week()      # Previous Monday
end_of_week = dt.end_of_week()          # Next Sunday

# Month boundaries
start_of_month = dt.start_of_month()    # 2024-03-01T00:00:00+00:00
end_of_month = dt.end_of_month()        # 2024-03-31T23:59:59.999999+00:00

# Quarter boundaries
start_of_quarter = dt.start_of_quarter() # 2024-01-01T00:00:00+00:00
end_of_quarter = dt.end_of_quarter()     # 2024-03-31T23:59:59.999999+00:00

# Year boundaries
start_of_year = dt.start_of_year()      # 2024-01-01T00:00:00+00:00
end_of_year = dt.end_of_year()          # 2024-12-31T23:59:59.999999+00:00
```

### Navigation by Weekday

```python
from carbonic import DateTime, Period

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")  # Monday

# Next occurrence of a weekday
next_friday = dt.next(Period.FRIDAY)
next_monday = dt.next(Period.MONDAY)  # Following Monday

# Previous occurrence of a weekday
last_friday = dt.previous(Period.FRIDAY)
previous_monday = dt.previous(Period.MONDAY)  # Previous Monday

# Weekday checks
print(dt.is_monday())     # True
print(dt.is_friday())     # False
print(dt.is_weekend())    # False
print(dt.is_weekday())    # True
```

## Business Day Operations

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")  # Monday

# Business day checks
print(dt.is_business_day())  # True (Monday is a business day)

# Navigate business days
next_business = dt.next_business_day()
previous_business = dt.previous_business_day()

# Count business days
future_dt = dt.add_days(10)
business_days = dt.business_days_until(future_dt)
print(f"Business days between: {business_days}")

# Add business days
in_5_business_days = dt.add_business_days(5)
```

## Timezone Operations

### Creating with Timezones

```python
from carbonic import DateTime

# Different timezone formats
utc_dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
ny_dt = DateTime(2024, 1, 15, 14, 30, tz="America/New_York")
london_dt = DateTime(2024, 1, 15, 14, 30, tz="Europe/London")

# Using timezone objects
from zoneinfo import ZoneInfo
tokyo_tz = ZoneInfo("Asia/Tokyo")
tokyo_dt = DateTime(2024, 1, 15, 14, 30, tz=tokyo_tz)
```

### Converting Timezones

```python
from carbonic import DateTime

# Create in one timezone
paris_time = DateTime(2024, 1, 15, 15, 30, tz="Europe/Paris")
print(paris_time)  # 2024-01-15T15:30:00+01:00

# Convert to different timezones
utc_time = paris_time.to_timezone("UTC")
tokyo_time = paris_time.to_timezone("Asia/Tokyo")
ny_time = paris_time.to_timezone("America/New_York")

print(f"UTC:   {utc_time}")    # 2024-01-15T14:30:00+00:00
print(f"Tokyo: {tokyo_time}")  # 2024-01-15T23:30:00+09:00
print(f"NY:    {ny_time}")     # 2024-01-15T09:30:00-05:00
```

### Working with Naive Datetimes

```python
from carbonic import DateTime

# Naive datetime (no timezone)
naive = DateTime(2024, 1, 15, 14, 30, tz=None)
print(naive.tzinfo)  # None

# Assume a timezone
aware = naive.assume_timezone("UTC")
print(aware.tzinfo)  # <ZoneInfo 'UTC'>

# Check if naive
print(naive.is_naive())   # True
print(aware.is_naive())   # False
```

## Comparisons

### Basic Comparisons

```python
from carbonic import DateTime

dt1 = DateTime(2024, 1, 15, 10, 0, tz="UTC")
dt2 = DateTime(2024, 1, 15, 14, 0, tz="UTC")
dt3 = DateTime(2024, 1, 16, 10, 0, tz="UTC")

# Standard operators
print(dt1 < dt2)   # True
print(dt2 > dt3)   # False
print(dt1 == dt1)  # True
print(dt1 != dt2)  # True

# Fluent methods
print(dt1.is_before(dt2))      # True
print(dt2.is_after(dt1))       # True
print(dt1.is_same_instant(dt1)) # True
```

### Date-Level Comparisons

```python
from carbonic import DateTime

dt1 = DateTime(2024, 1, 15, 10, 0, tz="UTC")
dt2 = DateTime(2024, 1, 15, 20, 0, tz="UTC")  # Same day, different time
dt3 = DateTime(2024, 1, 16, 5, 0, tz="UTC")   # Different day

# Same date checks
print(dt1.is_same_day(dt2))    # True
print(dt1.is_same_day(dt3))    # False

print(dt1.is_same_month(dt2))  # True
print(dt1.is_same_year(dt2))   # True

# Timezone-aware comparisons
ny_time = DateTime(2024, 1, 15, 5, 0, tz="America/New_York")  # Same as 10:00 UTC
print(dt1.is_same_instant(ny_time))  # True
print(dt1.is_same_day(ny_time))      # False (different local dates)
```

### Temporal Relationships

```python
from carbonic import DateTime, now

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
current = now()

# Relative to current time
print(dt.is_past())       # True (if current time is after)
print(dt.is_future())     # False (if current time is after)

# Between dates
start = DateTime(2024, 1, 10, tz="UTC")
end = DateTime(2024, 1, 20, tz="UTC")
print(dt.is_between(start, end))  # True
```

## Differences and Durations

### Calculating Differences

```python
from carbonic import DateTime

start = DateTime(2024, 1, 15, 10, 0, tz="UTC")
end = DateTime(2024, 1, 17, 14, 30, tz="UTC")

# Get Duration object
duration = end - start
print(duration)  # Duration(days=2, hours=4, minutes=30)

# Get difference in specific units
days = start.diff_in_days(end)
hours = start.diff_in_hours(end)
minutes = start.diff_in_minutes(end)
seconds = start.diff_in_seconds(end)

print(f"Days: {days}")        # 2.1875
print(f"Hours: {hours}")      # 52.5
print(f"Minutes: {minutes}")  # 3150
print(f"Seconds: {seconds}")  # 189000
```

### Humanized Differences

```python
from carbonic import DateTime, now

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
current = now()

# Human-readable differences
human = dt.diff_for_humans()  # "2 days ago" or "in 2 days"
human_abs = dt.diff_for_humans(absolute=True)  # "2 days"

# Relative to specific datetime
other = DateTime(2024, 1, 10, tz="UTC")
relative = dt.diff_for_humans(other)  # "5 days after"
```

## Formatting and Output

### Built-in Formats

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, 123456, tz="UTC")

# Standard formats
print(dt.to_iso_string())      # "2024-01-15T14:30:45.123456+00:00"
print(dt.to_date_string())     # "2024-01-15"
print(dt.to_time_string())     # "14:30:45"
print(dt.to_datetime_string()) # "2024-01-15 14:30:45"

# With timezone conversion
ny_dt = dt.to_timezone("America/New_York")
print(ny_dt.to_iso_string())   # "2024-01-15T09:30:45.123456-05:00"
```

### Custom Formatting

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# Carbon-style formatting
print(dt.format("Y-m-d H:i:s"))     # "2024-01-15 14:30:45"
print(dt.format("l, F j, Y"))       # "Monday, January 15, 2024"
print(dt.format("D M j G:i A"))     # "Mon Jan 15 14:30 PM"

# Python strftime (also supported)
print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # "2024-01-15 14:30:45"
print(dt.strftime("%A, %B %d, %Y"))      # "Monday, January 15, 2024"
```

### Format Tokens

Carbonic supports Carbon-style format tokens:

| Token | Description | Example |
|-------|-------------|---------|
| `Y` | 4-digit year | 2024 |
| `y` | 2-digit year | 24 |
| `m` | Month (01-12) | 01 |
| `n` | Month (1-12) | 1 |
| `M` | Short month name | Jan |
| `F` | Full month name | January |
| `d` | Day (01-31) | 15 |
| `j` | Day (1-31) | 15 |
| `D` | Short day name | Mon |
| `l` | Full day name | Monday |
| `H` | Hour 24-format (00-23) | 14 |
| `G` | Hour 24-format (0-23) | 14 |
| `h` | Hour 12-format (01-12) | 02 |
| `g` | Hour 12-format (1-12) | 2 |
| `i` | Minutes (00-59) | 30 |
| `s` | Seconds (00-59) | 45 |
| `A` | AM/PM | PM |
| `a` | am/pm | pm |

## Conversion Methods

### To Other Types

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# To Python datetime
stdlib_dt = dt.to_datetime()
print(type(stdlib_dt))  # <class 'datetime.datetime'>

# To Date object
date_obj = dt.to_date()
print(date_obj)  # 2024-01-15

# To timestamp
timestamp = dt.to_timestamp()
print(timestamp)  # 1705330245.0

# To naive datetime (removes timezone)
naive_dt = dt.to_naive()
print(naive_dt.tzinfo)  # None
```

### String Representations

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# Default string representation
print(str(dt))   # "2024-01-15T14:30:45+00:00"
print(repr(dt))  # "DateTime(2024, 1, 15, 14, 30, 45, 0, tz='UTC')"

# For debugging
print(dt.__dict__)  # Shows internal state
```

## Property Access

### Date Components

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, 123456, tz="UTC")

# Date properties
print(dt.year)         # 2024
print(dt.month)        # 1
print(dt.day)          # 15
print(dt.weekday)      # 0 (Monday = 0, Sunday = 6)
print(dt.day_of_week)  # 0 (same as weekday)
print(dt.day_of_year)  # 15
print(dt.week_of_year) # 3

# Time properties
print(dt.hour)         # 14
print(dt.minute)       # 30
print(dt.second)       # 45
print(dt.microsecond)  # 123456

# Timezone properties
print(dt.timezone)     # <ZoneInfo 'UTC'>
print(dt.tzinfo)       # <ZoneInfo 'UTC'>
print(dt.offset)       # datetime.timedelta(0)
```

### Derived Properties

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# Quarter information
print(dt.quarter)       # 1

# Week information
print(dt.week_of_month) # 3
print(dt.week_of_year)  # 3

# Month information
print(dt.days_in_month) # 31

# Timezone information
print(dt.timezone_name) # "UTC"
print(dt.is_dst())      # False (UTC doesn't have DST)
```

## Best Practices

### Always Use Timezones

```python
# Good - explicit timezone
dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

# Better - use factory methods for current time
current = DateTime.now("America/New_York")

# Avoid - naive datetime can cause bugs
naive = DateTime(2024, 1, 15, 14, 30, tz=None)
```

### Chain Operations Fluently

```python
from carbonic import DateTime

# Good - readable chains
result = (DateTime.now()
    .add_days(1)
    .start_of_day()
    .to_timezone("America/New_York")
    .format("Y-m-d H:i:s")
)

# Also good - intermediate variables for clarity
tomorrow = DateTime.now().add_days(1)
start_of_tomorrow = tomorrow.start_of_day()
ny_time = start_of_tomorrow.to_timezone("America/New_York")
formatted = ny_time.format("Y-m-d H:i:s")
```

### Handle Edge Cases

```python
from carbonic import DateTime
from carbonic.core.exceptions import InvalidDate

# Handle invalid dates
try:
    invalid = DateTime(2024, 2, 30, tz="UTC")  # February 30th
except InvalidDate as e:
    print(f"Invalid date: {e}")

# Handle timezone conversions carefully
dt = DateTime(2024, 3, 31, 2, 30, tz="America/New_York")  # During DST transition
utc_time = dt.to_timezone("UTC")  # This works correctly
```

## Performance Tips

### Reuse Base Objects

```python
from carbonic import DateTime

# Create a base and derive from it
base = DateTime(2024, 1, 1, tz="UTC")
dates = [base.add_days(i) for i in range(365)]  # Efficient
```

### Use Appropriate Methods

```python
from carbonic import DateTime

dt = DateTime.now()

# Efficient - single operation
tomorrow = dt.add_days(1)

# Less efficient - multiple object creations
tomorrow = dt.add_hours(24)  # Creates 24 intermediate objects
```

### Leverage ISO Parsing for Performance

```python
# Install with: pip install carbonic[fast]
from carbonic import DateTime

# Fast ISO parsing with ciso8601 (if installed)
dt = DateTime.from_iso("2024-01-15T14:30:00Z")  # Very fast

# Custom parsing is slower
dt = DateTime.from_format("2024-01-15 14:30:00", "Y-m-d H:i:s")  # Slower
```