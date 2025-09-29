# DateTime

The `DateTime` class is the heart of Carbonic, providing a comprehensive, immutable datetime object with timezone support and a fluent API.

## Overview

The `DateTime` class wraps Python's standard `datetime.datetime` while providing additional functionality and a more intuitive interface. Every `DateTime` object is immutable, meaning all operations return new instances.

```python
from carbonic import DateTime

# Create a DateTime instance
dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
print(dt)  # 2024-01-15T14:30:00+00:00
```

# Get current time
```puthon
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
import datetime
from carbonic import DateTime

# Current time
now_utc = DateTime.now()  # UTC by default
now_local = DateTime.now("America/New_York")

# From standard library datetime
stdlib_dt = datetime.datetime(2024, 1, 15, 14, 30, tzinfo=datetime.timezone.utc)
carbonic_dt = DateTime.from_datetime(stdlib_dt)

# From ISO string
iso_dt = DateTime.parse("2024-01-15T14:30:00Z")

# From custom format
custom_dt = DateTime.parse("15/01/2024 14:30", "d/m/Y H:i")

# Relative date/time functions
today_dt = DateTime.today()       # Today at midnight UTC
tomorrow_dt = DateTime.tomorrow() # Tomorrow at midnight UTC
yesterday_dt = DateTime.yesterday() # Yesterday at midnight UTC

# Future dates/times
next_hour = DateTime.next("hour")        # 1 hour from now
next_day = DateTime.next("day")          # 1 day from now (tomorrow)
next_week = DateTime.next("week", 2)     # 2 weeks from now
next_month = DateTime.next("month")      # 1 month from now
next_quarter = DateTime.next("quarter")  # 3 months from now

# Past dates/times
prev_minute = DateTime.previous("minute", 30)  # 30 minutes ago
prev_day = DateTime.previous("day")             # 1 day ago (yesterday)
prev_week = DateTime.previous("week")           # 1 week ago
prev_month = DateTime.previous("month", 3)      # 3 months ago
```

## Date and Time Arithmetic

### Adding Time

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0)

# Using fluent methods
future = dt.add(years=1).add(months=2).add(days=3).add(hours=4)

# Using Duration objects
duration = Duration(days=7, hours=12, minutes=30)
future = dt + duration

# Specific unit methods
next_hour = dt.add(hours=1)
next_day = dt.add(days=1)
next_month = dt.add(months=1)
next_year = dt.add(years=1)
```

### Subtracting Time

```python
from carbonic import DateTime, Duration

dt = DateTime(2024, 1, 15, 10, 0)

# Using fluent methods
past = dt.subtract(days=5).subtract(hours=2)

# Using Duration objects
duration = Duration(days=3, hours=6)
past = dt - duration

# Specific unit methods
last_hour = dt.subtract(hours=1)
yesterday = dt.subtract(days=1)
last_month = dt.subtract(months=1)
last_year = dt.subtract(years=1)
```

## Date Boundaries and Navigation

### Start and End Points

```python
from carbonic import DateTime

dt = DateTime(2024, 3, 15, 14, 30, 45)

# Day boundaries
start_of_day = dt.start_of("day")        # 2024-03-15T00:00:00+00:00
end_of_day = dt.end_of("day")            # 2024-03-15T23:59:59.999999+00:00

# Week boundaries
start_of_week = dt.start_of("week")      # Previous Monday
end_of_week = dt.end_of("week")          # Next Sunday

# Month boundaries
start_of_month = dt.start_of("month")    # 2024-03-01T00:00:00+00:00
end_of_month = dt.end_of("month")        # 2024-03-31T23:59:59.999999+00:00

# Quarter boundaries
start_of_quarter = dt.start_of("quarter") # 2024-01-01T00:00:00+00:00
end_of_quarter = dt.end_of("quarter")     # 2024-03-31T23:59:59.999999+00:00

# Year boundaries
start_of_year = dt.start_of("year")      # 2024-01-01T00:00:00+00:00
end_of_year = dt.end_of("year")          # 2024-12-31T23:59:59.999999+00:00
```

### Navigation by Weekday

```python
from carbonic import DateTime
import datetime

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")  # Monday

# Check current weekday (Monday=0, Sunday=6)
weekday = dt.to_datetime().weekday()
print(f"Weekday: {weekday}")  # 0 (Monday)

# Calculate next Friday (4 is Friday)
days_until_friday = (4 - weekday) % 7
if days_until_friday == 0:  # If today is Friday, get next Friday
    days_until_friday = 7
next_friday = dt.add(days=days_until_friday)

# Calculate next Monday
days_until_monday = (0 - weekday) % 7  # 0 is Monday
if days_until_monday == 0:  # If today is Monday, get next Monday
    days_until_monday = 7
next_monday = dt.add(days=days_until_monday)

# Weekday checks using datetime methods
print(dt.to_datetime().weekday() == 0)     # True (Monday)
print(dt.to_datetime().weekday() == 4)     # False (Friday)
print(dt.to_datetime().weekday() >= 5)     # False (not weekend)
print(dt.to_datetime().weekday() < 5)      # True (is weekday)
```

## Business Day Operations

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")  # Monday

# Business day checks using weekday
def is_business_day(dt):
    return dt.to_datetime().weekday() < 5  # Monday=0 to Friday=4

def add_business_days(dt, days):
    current = dt
    added = 0
    while added < days:
        current = current.add(days=1)
        if is_business_day(current):
            added += 1
    return current

# Business day navigation
print(f"Is business day: {is_business_day(dt)}")  # True (Monday)

# Add 5 business days
five_business_days_later = add_business_days(dt, 5)
print(f"5 business days later: {five_business_days_later}")

# Count business days between dates
start_date = DateTime(2024, 1, 10, tz="UTC")  # Wednesday
end_date = DateTime(2024, 1, 20, tz="UTC")    # Saturday
current = start_date
business_days = 0
while current <= end_date:
    if is_business_day(current):
        business_days += 1
    current = current.add(days=1)
print(f"Business days: {business_days}")
```

## Timezone Operations

### Creating with Timezones

```python
from carbonic import DateTime

# Different timezone formats
utc_dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
ny_dt = DateTime(2024, 1, 15, 14, 30, tz="America/New_York")
london_dt = DateTime(2024, 1, 15, 14, 30, tz="Europe/London")

print(f"UTC: {utc_dt}")
print(f"New York: {ny_dt}")
print(f"London: {london_dt}")
```

### Using Timezone Objects

```python
# Using timezone objects
from carbonic import DateTime
from zoneinfo import ZoneInfo

# Create with timezone string (DateTime internally creates ZoneInfo)
tokyo_dt = DateTime(2024, 1, 15, 14, 30, tz="Asia/Tokyo")
print(f"Tokyo: {tokyo_dt}")

# Or use ZoneInfo for other operations
tokyo_tz = ZoneInfo("Asia/Tokyo")
print(f"Timezone object: {tokyo_tz}")
```

### Converting Timezones

```python
from carbonic import DateTime

# Create in one timezone
paris_time = DateTime(2024, 1, 15, 15, 30, tz="Europe/Paris")
print(paris_time)  # 2024-01-15T15:30:00+01:00

# Convert to different timezones using as_timezone()
utc_time = paris_time.as_timezone("UTC")
tokyo_time = paris_time.as_timezone("Asia/Tokyo")
ny_time = paris_time.as_timezone("America/New_York")

print(f"UTC:   {utc_time}")    # 2024-01-15T14:30:00+00:00
print(f"Tokyo: {tokyo_time}")  # 2024-01-15T23:30:00+09:00
print(f"NY:    {ny_time}")     # 2024-01-15T09:30:00-05:00

# All represent the same moment in time
assert paris_time == utc_time == tokyo_time == ny_time

# Convert to naive datetime (removes timezone info)
naive_time = paris_time.as_timezone(None)
print(f"Naive: {naive_time}")  # 2024-01-15T15:30:00 (no timezone)
```

### Working with Naive Datetimes

```python
from carbonic import DateTime

# Naive datetime (no timezone)
naive = DateTime(2024, 1, 15, 14, 30, tz=None)
print(naive.tzinfo)  # None

# Convert naive to timezone-aware by creating new instance
aware = DateTime(naive.year, naive.month, naive.day, naive.hour, 
                naive.minute, naive.second, naive.microsecond, tz="UTC")
print(aware.tzinfo)  # <ZoneInfo 'UTC'>

# Check if naive using tzinfo
print(naive.tzinfo is None)   # True (is naive)
print(aware.tzinfo is not None)   # True (is aware)
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

# Using comparison operators instead of fluent methods
print(dt1 < dt2)               # is_before equivalent: True
print(dt2 > dt1)               # is_after equivalent: True
print(dt1 == dt1)              # is_same_instant equivalent: True
```

### Date-Level Comparisons

```python
from carbonic import DateTime

dt1 = DateTime(2024, 1, 15, 10, 0, tz="UTC")
dt2 = DateTime(2024, 1, 15, 20, 0, tz="UTC")  # Same day, different time
dt3 = DateTime(2024, 1, 16, 5, 0, tz="UTC")   # Different day

# Same date checks using date properties
print(dt1.to_date() == dt2.to_date())  # is_same_day equivalent: True
print(dt1.to_date() == dt3.to_date())  # is_same_day equivalent: False

print(dt1.year == dt2.year and dt1.month == dt2.month)  # is_same_month equivalent: True
print(dt1.year == dt2.year)  # is_same_year equivalent: True

# Timezone-aware comparisons
ny_time = DateTime(2024, 1, 15, 5, 0, tz="America/New_York")  # Same as 10:00 UTC
print(dt1 == ny_time)  # is_same_instant equivalent: True
# For same day comparison, convert to same timezone first
ny_utc = DateTime.from_datetime(ny_time.to_datetime().astimezone())
print(dt1.to_date() == ny_utc.to_date())  # Different local dates check
```

### Temporal Relationships

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
current = DateTime.now("UTC")

# Relative to current time using comparison operators
print(dt < current)       # is_past equivalent: True (if current time is after)
print(dt > current)       # is_future equivalent: False (if current time is after)

# Between dates using comparison operators
start = DateTime(2024, 1, 10, tz="UTC")
end = DateTime(2024, 1, 20, tz="UTC")
print(start <= dt <= end)  # is_between equivalent: True
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

# Get difference using the diff method (returns Duration)
duration = start.diff(end)

# Access duration properties
print(f"Days: {duration.in_days()}")
print(f"Hours: {duration.in_hours()}")
print(f"Minutes: {duration.in_minutes()}")
print(f"Seconds: {duration.in_seconds()}")
```

### Working with Durations

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
current = DateTime.now("UTC")

# Get duration object
duration = current.diff(dt)

# Access duration properties for humanization
days = duration.in_days()
if abs(days) >= 1:
    if days > 0:
        human = f"{int(days)} days ago"
    else:
        human = f"in {int(abs(days))} days"
else:
    hours = duration.in_hours()
    if hours > 0:
        human = f"{int(hours)} hours ago"
    else:
        human = f"in {int(abs(hours))} hours"

print(human)
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
ny_dt = dt.as_timezone("America/New_York")
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
timestamp = dt.to_datetime().timestamp()
print(timestamp)  # 1705330245.0

# To naive datetime (removes timezone)
naive_dt = dt.to_datetime().replace(tzinfo=None)
print(naive_dt.tzinfo)  # None
```

### String Representations

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# Default string representation
print(str(dt))   # "2024-01-15T14:30:45+00:00"
print(repr(dt))  # "DateTime(2024, 1, 15, 14, 30, 45, tz='UTC')"

# For debugging - convert to standard datetime if needed
print(str(dt.to_datetime()))  # Shows as standard datetime format
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
print(dt.to_datetime().weekday())  # 0
print(dt.to_datetime().timetuple().tm_yday)  # 15
print(dt.to_datetime().isocalendar().week)  # 3

# Time properties
print(dt.hour)         # 14
print(dt.minute)       # 30
print(dt.second)       # 45
print(dt.microsecond)  # 123456

# Timezone properties
print(dt.tzinfo)       # <ZoneInfo 'UTC'>
print(dt.to_datetime().utcoffset())  # datetime.timedelta(0)
```

### Derived Properties

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

# Calculate quarter information
quarter = (dt.month - 1) // 3 + 1
print(f"Quarter: {quarter}")  # 1

# Week information using underlying datetime
print(f"Week of year: {dt.to_datetime().isocalendar().week}")  # 3

# Month information using calendar module
import calendar
print(f"Days in month: {calendar.monthrange(dt.year, dt.month)[1]}")  # 31

# Timezone information
print(f"Timezone: {dt.tzinfo}")  # UTC
```

## Best Practices

### Always Use Timezones

```python
from carbonic import DateTime

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
from zoneinfo import ZoneInfo

# Good - readable chains
result = (DateTime.now()
    .add(days=1)
    .start_of("day")
    .format("Y-m-d H:i:s")
)

# For timezone conversion, use as_timezone() method
result = (DateTime.now()
    .add(days=1)
    .start_of("day")
    .as_timezone("America/New_York")
    .format("Y-m-d H:i:s")
)

# Also good - intermediate variables for clarity
tomorrow = DateTime.now().add(days=1)
start_of_tomorrow = tomorrow.start_of("day")
ny_time = start_of_tomorrow.as_timezone("America/New_York")
formatted = ny_time.format("Y-m-d H:i:s")
```

### Handle Edge Cases

```python
from carbonic import DateTime
from zoneinfo import ZoneInfo

# Handle invalid dates
try:
    invalid = DateTime(2024, 2, 30, tz="UTC")  # February 30th
except ValueError as e:
    print(f"Invalid date: {e}")

# Handle timezone conversions carefully
dt = DateTime(2024, 3, 31, 2, 30, tz="America/New_York")  # During DST transition
utc_time = dt.as_timezone("UTC")  # This works correctly
```

## Performance Tips

### Reuse Base Objects

```python
from carbonic import DateTime

# Create a base and derive from it
base = DateTime(2024, 1, 1, tz="UTC")
dates = [base.add(days=i) for i in range(365)]  # Efficient
```

### Use Appropriate Methods

```python
from carbonic import DateTime

dt = DateTime.now()

# Efficient - single operation
tomorrow = dt.add(days=1)

# Less efficient - multiple object creations
tomorrow = dt.add(hours=24)  # Still one operation, but conceptually less clear
```

### Leverage ISO Parsing for Performance

```python
# Install with: pip install carbonic[fast]
from carbonic import DateTime

# Fast ISO parsing with ciso8601 (if installed)
dt = DateTime.parse("2024-01-15T14:30:00Z")  # Very fast

# Custom parsing with format string
dt = DateTime.parse("2024-01-15 14:30:00", "Y-m-d H:i:s")  # Custom format parsing
```