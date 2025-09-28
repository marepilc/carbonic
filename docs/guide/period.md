# Period Guide

The `Period` class provides semantic time period operations using named constants for more readable and maintainable datetime code.

## Overview

Instead of writing `dt.add(months=1)`, you can write `Period.MONTH.add_to(dt)` for clearer intent and better readability.

## Available Periods

```python
from carbonic import Period

# Available period constants
Period.MINUTE    # 1 minute
Period.HOUR      # 1 hour
Period.DAY       # 1 day
Period.WEEK      # 1 week
Period.MONTH     # 1 month
Period.QUARTER   # 1 quarter (3 months)
Period.YEAR      # 1 year
```

## Basic Usage

```python
from carbonic import DateTime, Date, Period

dt = DateTime(2024, 6, 15, 14, 30)
date = Date(2024, 6, 15)

# Add periods
next_month = Period.MONTH.add_to(dt)        # 2024-07-15T14:30:00
next_week = Period.WEEK.add_to(date)        # 2024-06-22
next_quarter = Period.QUARTER.add_to(date)  # 2024-09-15

# Subtract periods
last_year = Period.YEAR.subtract_from(dt)   # 2023-06-15T14:30:00
yesterday = Period.DAY.subtract_from(date)  # 2024-06-14
```

## Multiple Units

```python
from carbonic import Date, Period

date = Date(2024, 6, 15)

# Add multiple periods
five_days_later = Period.DAY.add_to(date, count=5)     # 2024-06-20
three_months_ago = Period.MONTH.subtract_from(date, count=3)  # 2024-03-15
two_years_future = Period.YEAR.add_to(date, count=2)   # 2026-06-15
```

## Period Anchoring

Find the start or end of a period:

```python
from carbonic import DateTime, Period

dt = DateTime(2024, 6, 15, 14, 30, 45)

# Start of periods
start_of_week = Period.WEEK.start_of(dt)      # Monday 00:00:00
start_of_month = Period.MONTH.start_of(dt)    # June 1st 00:00:00
start_of_quarter = Period.QUARTER.start_of(dt) # April 1st 00:00:00
start_of_year = Period.YEAR.start_of(dt)      # January 1st 00:00:00

# End of periods
end_of_week = Period.WEEK.end_of(dt)          # Sunday 23:59:59.999999
end_of_month = Period.MONTH.end_of(dt)        # June 30th 23:59:59.999999
end_of_quarter = Period.QUARTER.end_of(dt)   # June 30th 23:59:59.999999
end_of_year = Period.YEAR.end_of(dt)          # December 31st 23:59:59.999999
```

## Time Periods (DateTime Only)

Minute and hour periods work only with `DateTime` objects:

```python
from carbonic import DateTime, Period

dt = DateTime(2024, 6, 15, 14, 30, 45)

# Time-based periods
next_minute = Period.MINUTE.add_to(dt)        # 2024-06-15T14:31:45
start_of_hour = Period.HOUR.start_of(dt)      # 2024-06-15T14:00:00
end_of_minute = Period.MINUTE.end_of(dt)      # 2024-06-15T14:30:59.999999
```

## Comparison with Direct Methods

Both approaches work - choose based on your preference:

```python
from carbonic import DateTime, Period

dt = DateTime(2024, 6, 15, 14, 30)

# Using Period (semantic)
result1 = Period.MONTH.add_to(dt)
result2 = Period.WEEK.start_of(dt)

# Using direct methods (concise)
result3 = dt.add(months=1)
result4 = dt.start_of("week")

# Both produce identical results
assert result1 == result3
assert result2 == result4
```

## Use Cases

### When to Use Periods

**Good for:**
- **Configuration**: `BILLING_PERIOD = Period.MONTH`
- **Business logic**: `if payment_due.add_to(Period.QUARTER):`
- **Templates**: More readable in configuration files
- **Domain modeling**: Express business concepts clearly

**Example:**
```python
from carbonic import Date, Period

class SubscriptionPlan:
    def __init__(self, billing_period: Period):
        self.billing_period = billing_period

    def next_billing_date(self, start_date: Date) -> Date:
        return self.billing_period.add_to(start_date)

# Usage
monthly_plan = SubscriptionPlan(Period.MONTH)
quarterly_plan = SubscriptionPlan(Period.QUARTER)

start = Date(2024, 1, 15)
next_monthly = monthly_plan.next_billing_date(start)    # 2024-02-15
next_quarterly = quarterly_plan.next_billing_date(start) # 2024-04-15
```

### When to Use Direct Methods

**Good for:**
- **Simple operations**: `dt.add(days=7)`
- **Dynamic counts**: `dt.add(months=user_input)`
- **Method chaining**: `dt.add(days=1).start_of("month")`

## Working with Dates vs DateTimes

```python
from carbonic import DateTime, Date, Period

# Works with both Date and DateTime
date = Date(2024, 6, 15)
dt = DateTime(2024, 6, 15, 14, 30)

# Calendar periods work with both
Period.DAY.add_to(date)     # Returns Date
Period.DAY.add_to(dt)       # Returns DateTime

Period.MONTH.add_to(date)   # Returns Date
Period.MONTH.add_to(dt)     # Returns DateTime

# Time periods only work with DateTime
Period.HOUR.add_to(dt)      # ✅ Works - Returns DateTime
# Period.HOUR.add_to(date)  # ❌ Would raise error
```

## Error Handling

```python
from carbonic import Date, Period

date = Date(2024, 6, 15)

# This will raise an error - time periods require DateTime
try:
    Period.MINUTE.add_to(date)  # ❌ Error
except ValueError as e:
    print(f"Error: {e}")  # Time periods require DateTime objects
```

## Performance Notes

Period operations have the same performance characteristics as direct method calls - they're just a different API for the same underlying functionality.

```python
from carbonic import DateTime, Period

dt = DateTime(2024, 6, 15, 14, 30)

# These are equivalent in performance:
result1 = Period.MONTH.add_to(dt)  # Period API
result2 = dt.add(months=1)         # Direct API
```

## See Also

- [DateTime Guide](datetime.md) - Complete DateTime reference
- [Date Guide](date.md) - Date-only operations
- [Duration Guide](duration.md) - Time spans and intervals
- [API Reference](../api/period.md) - Complete Period API