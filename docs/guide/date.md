# Date

The `Date` class provides date-only operations without time components. It's perfect for working with birthdays, holidays, deadlines, and other date-centric data.

## Overview

Date objects are immutable and represent calendar dates independent of time zones or time of day. They provide intuitive methods for date arithmetic, comparisons, and formatting.

```python
from carbonic import Date

# Create a Date instance
date = Date(2024, 1, 15)
print(date)  # 2024-01-15
```

### Calendar Information

```python
from carbonic import Date
import calendar

date = Date(2024, 2, 15)  # February in a leap year

# Year information
print(calendar.isleap(date.year))    # True (2024 is a leap year)
days_in_year = 366 if calendar.isleap(date.year) else 365
print(days_in_year)      # 366

# Month information
print(date.end_of("month").day)     # 29 (February in leap year)

# Quarter information
print((date.month - 1) // 3 + 1)           # 1 (Q1: Jan-Mar)
print(date.start_of("quarter")) # 2024-01-01
```

## Creating Date Objects

```python
from carbonic import Date, today

# Create a specific date
birthday = Date(1990, 5, 15)
print(birthday)  # 1990-05-15

# Get today's date
today_date = today()
print(today_date)  # 2024-01-15 (example)
```

## Creating Date Objects

### Constructor

```python
from carbonic import Date

# Create specific dates
date = Date(2024, 1, 15)      # January 15, 2024
new_year = Date(2024, 1, 1)   # January 1, 2024
christmas = Date(2024, 12, 25) # December 25, 2024

# Year, month, day are required
print(date)  # 2024-01-15
```

### Factory Methods

```python
from carbonic import Date

# Today's date
today_date = Date.today()  # Local timezone
today_utc = Date.today("UTC")  # Specific timezone

# From Python date object
import datetime
stdlib_date = datetime.date(2024, 1, 15)
carbonic_date = Date.from_date(stdlib_date)

# From DateTime object
from carbonic import DateTime
dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
date_from_dt = dt.to_date()

# From string (ISO format)
parsed_date = Date.parse("2024-01-15")

# From custom format
custom_date = Date.parse("15/01/2024", "%d/%m/%Y")
us_date = Date.parse("01-15-2024", "%m-%d-%Y")
```

## Date Arithmetic

### Adding Time

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Add various units
tomorrow = date.add(days=1)
next_week = date.add(days=7)  # Use days=7 instead of weeks=1
next_month = date.add(months=1)
next_year = date.add(years=1)

print(f"Tomorrow: {tomorrow}")     # 2024-01-16
print(f"Next week: {next_week}")   # 2024-01-22
print(f"Next month: {next_month}") # 2024-02-15
print(f"Next year: {next_year}")   # 2025-01-15

# Chain operations
future = date.add(years=1, months=6, days=10)
print(f"Future: {future}")  # 2025-07-25
```

### Subtracting Time

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Subtract various units
yesterday = date.subtract(days=1)
last_week = date.subtract(days=7)  # Use days=7 instead of weeks=1
last_month = date.subtract(months=1)
last_year = date.subtract(years=1)

print(f"Yesterday: {yesterday}")   # 2024-01-14
print(f"Last week: {last_week}")   # 2024-01-08
print(f"Last month: {last_month}") # 2023-12-15
print(f"Last year: {last_year}")   # 2023-01-15
```

### Date Differences

```python
from carbonic import Date

start_date = Date(2024, 1, 15)
end_date = Date(2024, 1, 22)

# Calculate differences
duration_diff = end_date.diff(start_date)
days_diff = int(duration_diff.in_days())
weeks_diff = int(duration_diff.in_weeks())

print(f"Days difference: {days_diff}")    # 7
print(f"Weeks difference: {weeks_diff}")  # 1

# Absolute difference
past_date = Date(2024, 1, 10)
abs_diff = abs(int(start_date.diff(past_date).in_days()))
print(f"Absolute difference: {abs_diff}")  # 5
```

## Date Boundaries and Navigation

### Start and End Points

```python
from carbonic import Date

date = Date(2024, 3, 15)  # March 15, 2024

# Week boundaries
start_of_week = date.start_of("week")      # Previous Monday
end_of_week = date.end_of("week")          # Next Sunday

# Month boundaries
start_of_month = date.start_of("month")    # 2024-01-01
end_of_month = date.end_of("month")        # 2024-01-31

# Quarter boundaries
start_of_quarter = date.start_of("quarter") # 2024-01-01 (Q1)
end_of_quarter = date.end_of("quarter")     # 2024-03-31 (Q1)

# Year boundaries
start_of_year = date.start_of("year")      # 2024-01-01
end_of_year = date.end_of("year")          # 2024-12-31

print(f"Start of month: {start_of_month}")
print(f"End of month: {end_of_month}")
```

### Weekday Navigation

```python
from carbonic import Date

date = Date(2024, 1, 15)  # Monday

# Calculate next Friday (weekday 4)
current_weekday = date.weekday  # Monday = 0
days_until_friday = (4 - current_weekday) % 7
if days_until_friday == 0:  # If today is Friday
    days_until_friday = 7
next_friday = date.add(days=days_until_friday)

# Calculate next Monday
days_until_monday = (0 - current_weekday) % 7
if days_until_monday == 0:  # If today is Monday
    days_until_monday = 7
next_monday = date.add(days=days_until_monday)

print(f"Next Friday: {next_friday}")      # 2024-01-19
print(f"Next Monday: {next_monday}")      # 2024-01-22

# Weekday checks
print(f"Is Monday: {date.weekday == 0}")     # True
print(f"Is weekend: {date.is_weekend()}")   # False
print(f"Is weekday: {date.is_weekday()}")   # True
```

## Business Day Operations

```python
from carbonic import Date

date = Date(2024, 1, 15)  # Monday

# Business day checks
print(f"Is business day: {date.is_weekday()}")  # True

# Navigate business days
next_business = date.add_business_days(1)
previous_business = date.subtract_business_days(1)

print(f"Next business day: {next_business}")
print(f"Previous business day: {previous_business}")

# Add business days (skipping weekends)
in_5_business_days = date.add_business_days(5)
print(f"5 business days later: {in_5_business_days}")

# Count business days between dates would require manual calculation
# (No direct business_days_until method available)
```

## Comparisons

### Basic Comparisons

```python
from carbonic import Date

date1 = Date(2024, 1, 15)
date2 = Date(2024, 1, 20)
date3 = Date(2024, 1, 15)

# Standard operators
print(date1 < date2)   # True
print(date1 > date2)   # False
print(date1 == date3)  # True
print(date1 != date2)  # True

# Use standard comparison operators
print(date1 < date2)      # True (date1 is before date2)
print(date1 > date2)       # False (date1 is not after date2)
print(date1 == date3)   # True  # Use equality comparison instead
```

### Temporal Relationships

```python
from carbonic import Date, today

date = Date(2024, 1, 15)
current_date = today()

# Relative to today using comparison operators
print(date < current_date)       # True (if today is after Jan 15, 2024)
print(date > current_date)       # False (if today is after Jan 15, 2024) 
print(date == current_date)      # True (if today is Jan 15, 2024)

# Between dates using comparison operators
start = Date(2024, 1, 10)
end = Date(2024, 1, 20)
print(start <= date <= end)  # True
```

### Date-Specific Comparisons

```python
from carbonic import Date

date = Date(2024, 3, 15)

# Same period checks
march_1 = Date(2024, 3, 1)
april_15 = Date(2024, 4, 15)
next_year = Date(2025, 3, 15)

print(date.month == march_1.month)    # True
print(date.month == april_15.month)   # False
print(date.year == next_year.year)   # False

# Quarter checks
print((date.month - 1) // 3 == (march_1.month - 1) // 3)  # True (both in Q1)
```

## Formatting and Output

### Built-in Formats

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Standard formats
print(date.to_iso_string())      # "2024-01-15"
print(str(date))                 # "2024-01-15"

# Alternative formats using format method
print(date.format("Y-m-d"))   # "2024-01-15"
print(date.format("d/m/Y"))   # "15/01/2024"
print(date.format("F j, Y")) # "January 15, 2024"
```

### Custom Formatting

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Carbon-style formatting
print(date.format("Y-m-d"))       # "2024-01-15"
print(date.format("d/m/Y"))       # "15/01/2024"
print(date.format("l, F j, Y"))   # "Monday, January 15, 2024"
print(date.format("D M j, Y"))    # "Mon Jan 15, 2024"

# Python strftime (also supported)
print(date.strftime("%Y-%m-%d"))       # "2024-01-15"
print(date.strftime("%B %d, %Y"))      # "January 15, 2024"
print(date.strftime("%A, %b %d"))      # "Monday, Jan 15"
```

### Format Tokens for Dates

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
| `S` | Ordinal suffix | st, nd, rd, th |
| `w` | Day of week (0=Sunday) | 1 |
| `N` | Day of week (1=Monday) | 1 |

## Conversion Methods

### To Other Types

```python
from carbonic import Date

date = Date(2024, 1, 15)

# To Python date object
stdlib_date = date.to_date()
print(type(stdlib_date))  # <class 'datetime.date'>

# To datetime.datetime object (with timezone)
dt_utc = date.to_datetime("UTC")
dt_local = date.to_datetime("America/New_York")

print(dt_utc)    # 2024-01-15 00:00:00+00:00
print(dt_local)  # 2024-01-15 00:00:00-05:00

# To timestamp (convert via datetime)
timestamp_utc = dt_utc.timestamp()
print(timestamp_utc)  # Unix timestamp for midnight UTC
```

### String Representations

```python
from carbonic import Date

date = Date(2024, 1, 15)

# String representations
print(str(date))   # "2024-01-15"
print(repr(date))  # "Date(2024, 1, 15)"

# ISO format
print(date.to_iso_string())  # "2024-01-15"
```

## Property Access

### Date Components

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Basic properties
print(date.year)         # 2024
print(date.month)        # 1
print(date.day)          # 15

# Derived properties  
print(date.to_date().weekday())      # 0 (Monday = 0, Sunday = 6)
print(date.to_date().timetuple().tm_yday)  # 15 (day of year)
print(date.to_date().isocalendar().week)  # 3 (week of year)
print((date.month - 1) // 3 + 1)      # 1 (calculate quarter)

# Month information
print(date.end_of("month").day)  # 31 (days in month via end_of method)
print(date.format("F"))     # "January" (month name)
print(date.format("M"))     # "Jan" (month abbreviation)

# Week information  
print(date.format("l"))   # "Monday" (weekday name)
print(date.format("D"))   # "Mon" (weekday abbreviation)
```

### Calendar Information

```python
from carbonic import Date

date = Date(2024, 2, 15)  # February in a leap year

# Year information
import calendar
print(calendar.isleap(date.year))    # True (2024 is a leap year)
print(366 if calendar.isleap(date.year) else 365)  # 366

# Month information
print(date.end_of("month").day)     # 29 (February in leap year)

# Quarter information
print((date.month - 1) // 3 + 1)           # 1 (Q1: Jan-Mar)
print(date.start_of("quarter")) # 2024-01-01
```

## Common Use Cases

### Age Calculations

```python
from carbonic import Date, today

birthday = Date(1990, 5, 15)
today_date = today()

# Calculate age in years using manual calculation
age_years = today_date.year - birthday.year
# Adjust if birthday hasn't occurred this year
if (today_date.month, today_date.day) < (birthday.month, birthday.day):
    age_years -= 1
print(f"Age: {age_years} years")

# More precise age calculation
def calculate_age(birth_date, reference_date=None):
    if reference_date is None:
        reference_date = today()

    years = reference_date.year - birth_date.year

    # Adjust if birthday hasn't occurred this year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        years -= 1

    return years

precise_age = calculate_age(birthday)
print(f"Precise age: {precise_age} years")
```

### Holiday and Event Management

```python
from carbonic import Date, Period

year = 2024

# Fixed holidays
new_years = Date(year, 1, 1)
independence_day = Date(year, 7, 4)
christmas = Date(year, 12, 25)

# Calculated holidays (examples - simplified)
# Martin Luther King Jr. Day (3rd Monday in January)
# This is a simplified example - real calculation would be more complex
mlk_day = Date(year, 1, 21)  # Approximate date for 3rd Monday

# Memorial Day (last Monday in May) 
# Simplified - actual calculation would find the last Monday
memorial_day = Date(year, 5, 27)  # Approximate date

holidays = [
    ("New Year's Day", new_years),
    ("MLK Jr. Day", mlk_day),
    ("Memorial Day", memorial_day),
    ("Independence Day", independence_day),
    ("Christmas", christmas),
]

print("2024 Holidays:")
for name, date in holidays:
    print(f"{name}: {date.format('l, F j')}")
```

### Project Planning

```python
from carbonic import Date, today

# Project timeline
project_start = today()
project_duration_days = 45

# Calculate milestones
milestone_1 = project_start.add_business_days(10)  # 2 weeks
milestone_2 = project_start.add_business_days(25)  # 5 weeks
project_end = project_start.add_business_days(project_duration_days)

print(f"Project Start: {project_start}")
print(f"Milestone 1: {milestone_1}")
print(f"Milestone 2: {milestone_2}")
print(f"Project End: {project_end}")

# Check if project ends on a weekend
if project_end.is_weekend():
    # Move to next Monday
    days_to_add = 7 - project_end.weekday if project_end.weekday != 6 else 1
    project_end = project_end.add(days=days_to_add)
    print(f"Adjusted End (Monday): {project_end}")
```

### Date Ranges and Iterations

```python
from carbonic import Date

start_date = Date(2024, 1, 1)
end_date = Date(2024, 1, 31)

# Generate date range
def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current = current.add(days=1)

# All dates in January 2024
january_dates = list(date_range(start_date, end_date))
print(f"January has {len(january_dates)} days")

# Only business days
business_days = [d for d in january_dates if d.is_weekday()]
print(f"January has {len(business_days)} business days")

# Only weekends
weekends = [d for d in january_dates if d.is_weekend()]
print(f"January has {len(weekends)} weekend days")
```

### Scheduling and Recurrence

```python
from carbonic import Date, Period

# Meeting every Tuesday
start_date = Date(2024, 1, 2)  # First Tuesday of 2024
meeting_dates = []

current_date = start_date
for week in range(8):  # Next 8 weeks
    meeting_dates.append(current_date)
    current_date = current_date.add(days=7)  # Use days=7 instead of weeks=1

print("Weekly Tuesday meetings:")
for date in meeting_dates:
    print(f"  {date.format('l, F j')}")

# Monthly meetings (first Friday of each month)
monthly_meetings = []

for month in range(1, 7):  # Next 6 months
    first_of_month = Date(2024, month, 1)
    # Find first Friday (weekday 4)
    days_until_friday = (4 - first_of_month.weekday) % 7
    first_friday = first_of_month.add(days=days_until_friday)
    monthly_meetings.append(first_friday)

print("\nMonthly first Friday meetings:")
for date in monthly_meetings:
    print(f"  {date.format('F j, Y')}")
```

## Best Practices

### Always Consider Time Zones for Conversions

```python
from carbonic import Date

date = Date(2024, 1, 15)

# Good - explicit timezone when converting to DateTime
utc_dt = date.to_datetime(tz="UTC")
local_dt = date.to_datetime(tz="America/New_York")

# This creates different moments in time:
print(utc_dt)    # 2024-01-15T00:00:00+00:00
print(local_dt)  # 2024-01-15T00:00:00-05:00
```

### Use Date for Date-Only Operations

```python
from carbonic import Date, DateTime

# Good - use Date for date-centric logic
birthday = Date(1990, 5, 15)
today_date = Date.today()
# Calculate age using manual calculation
age = today_date.year - birthday.year
if (today_date.month, today_date.day) < (birthday.month, birthday.day):
    age -= 1

# Avoid - using DateTime for date-only operations
birthday_dt = DateTime(1990, 5, 15, tz="UTC")  # Unnecessary complexity
```

### Handle Month Overflow Carefully

```python
from carbonic import Date

# Be aware of month overflow behavior
jan_31 = Date(2024, 1, 31)

# Adding months can overflow
feb_result = jan_31.add(months=1)
print(feb_result)  # 2024-02-29 (leap year) or 2024-02-28

# This is usually desired behavior, but be aware
mar_result = jan_31.add(months=2)
print(mar_result)  # 2024-03-31 (back to 31st)
```

### Use Business Day Methods for Work Schedules

```python
from carbonic import Date

# Good - use business day methods for work-related dates
project_start = Date.today()
deadline = project_start.add_business_days(20)  # 4 work weeks

# Avoid - manual weekend checking
manual_deadline = project_start.add(days=28)  # Includes weekends
```