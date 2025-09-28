# Business Days Guide

Comprehensive guide to working with business days, weekends, and business day calculations in Carbonic.

## Overview

Carbonic provides built-in support for business day operations:
- **Weekend detection** (Saturday and Sunday)
- **Business day arithmetic** with automatic weekend skipping
- **Weekday validation** for scheduling and planning
- **Clean integration** with Date and DateTime objects

## Basic Concepts

### Weekdays vs Weekends

```python
from carbonic import Date

# Create some test dates
monday = Date(2024, 1, 15)    # Monday
friday = Date(2024, 1, 19)    # Friday
saturday = Date(2024, 1, 20)  # Saturday
sunday = Date(2024, 1, 21)    # Sunday

# Check if dates are weekdays
print(f"Monday is weekday: {monday.is_weekday()}")      # True
print(f"Friday is weekday: {friday.is_weekday()}")      # True
print(f"Saturday is weekday: {saturday.is_weekday()}")  # False
print(f"Sunday is weekday: {sunday.is_weekday()}")      # False

# Check if dates are weekends
print(f"Saturday is weekend: {saturday.is_weekend()}")  # True
print(f"Sunday is weekend: {sunday.is_weekend()}")      # True
print(f"Monday is weekend: {monday.is_weekend()}")      # False
```

### Week Structure

Carbonic follows the ISO 8601 standard where:
- **Monday** = 1 (first day of week)
- **Sunday** = 7 (last day of week)
- **Weekdays** = Monday through Friday (1-5)
- **Weekend** = Saturday and Sunday (6-7)

```python
from carbonic import Date

date = Date(2024, 1, 15)  # Monday
print(f"Day of week: {date.weekday}")  # 1 (Monday)

# Check each day of the week
dates = [Date(2024, 1, 15 + i) for i in range(7)]  # Monday to Sunday
for date in dates:
    day_name = date.format("l")
    day_num = date.weekday
    is_business = date.is_weekday()
    print(f"{day_name} ({day_num}): Business day = {is_business}")
```

## Business Day Arithmetic

### Adding Business Days

```python
from carbonic import Date

start_date = Date(2024, 1, 15)  # Monday
print(f"Start: {start_date.format('l, F j')} (Monday)")

# Add business days
next_business_day = start_date.add_business_days(1)
print(f"1 business day later: {next_business_day.format('l, F j')}")  # Tuesday

# Add multiple business days
five_business_days = start_date.add_business_days(5)
print(f"5 business days later: {five_business_days.format('l, F j')}")  # Monday (next week)

# Starting from Friday
friday = Date(2024, 1, 19)  # Friday
next_from_friday = friday.add_business_days(1)
print(f"1 business day after Friday: {next_from_friday.format('l, F j')}")  # Monday (skips weekend)
```

### Adding Business Days from Weekends

```python
from carbonic import Date

# Starting from Saturday
saturday = Date(2024, 1, 20)  # Saturday
print(f"Start: {saturday.format('l, F j')} (Saturday)")

# Add business days from weekend
next_business = saturday.add_business_days(1)
print(f"1 business day later: {next_business.format('l, F j')}")  # Monday

# Add multiple business days from weekend
three_business = saturday.add_business_days(3)
print(f"3 business days later: {three_business.format('l, F j')}")  # Wednesday
```

### Subtracting Business Days

```python
from carbonic import Date

start_date = Date(2024, 1, 19)  # Friday
print(f"Start: {start_date.format('l, F j')} (Friday)")

# Subtract business days
prev_business_day = start_date.subtract_business_days(1)
print(f"1 business day earlier: {prev_business_day.format('l, F j')}")  # Thursday

# Subtract multiple business days
five_business_days_ago = start_date.subtract_business_days(5)
print(f"5 business days earlier: {five_business_days_ago.format('l, F j')}")  # Friday (previous week)

# Subtracting from Monday
monday = Date(2024, 1, 22)  # Monday
prev_from_monday = monday.subtract_business_days(1)
print(f"1 business day before Monday: {prev_from_monday.format('l, F j')}")  # Friday (skips weekend)
```

### Zero Business Days

```python
from carbonic import Date

# Adding zero business days
date = Date(2024, 1, 20)  # Saturday
same_date = date.add_business_days(0)
print(f"Original: {date}")
print(f"Zero business days added: {same_date}")
print(f"Same date: {date == same_date}")  # True
```

## Practical Examples

### Project Planning

```python
from carbonic import Date

def calculate_project_schedule(start_date, business_days_required):
    """Calculate project end date given business days required."""
    if not start_date.is_weekday():
        # If starting on weekend, move to next Monday
        actual_start = start_date.add_business_days(0)  # Moves to next business day
        print(f"Adjusted start date from {start_date} to {actual_start}")
        start_date = actual_start

    end_date = start_date.add_business_days(business_days_required - 1)  # -1 because start day counts
    return start_date, end_date

# Example: 10-day project starting on Friday
project_start = Date(2024, 1, 19)  # Friday
start, end = calculate_project_schedule(project_start, 10)

print(f"Project starts: {start.format('l, F j')} (business day 1)")
print(f"Project ends: {end.format('l, F j')} (business day 10)")

# Calculate actual calendar days
calendar_days = (end - start).days + 1
print(f"Total calendar days: {calendar_days}")
```

### Meeting Scheduler

```python
from carbonic import Date, DateTime

def schedule_next_meeting(last_meeting_date, frequency_business_days=5):
    """Schedule next meeting on a business day."""
    next_date = last_meeting_date.add_business_days(frequency_business_days)
    return next_date

def schedule_weekly_meetings(start_date, num_weeks=4):
    """Schedule weekly meetings, always on business days."""
    meetings = []
    current_date = start_date

    # Ensure start date is a business day
    if not current_date.is_weekday():
        current_date = current_date.add_business_days(0)

    for week in range(num_weeks):
        meetings.append(current_date)
        current_date = schedule_next_meeting(current_date, 5)  # Every 5 business days (weekly)

    return meetings

# Schedule meetings starting from a Saturday
start = Date(2024, 1, 20)  # Saturday
meetings = schedule_weekly_meetings(start, 4)

print("Scheduled meetings:")
for i, meeting in enumerate(meetings, 1):
    print(f"Meeting {i}: {meeting.format('l, F j')} ({meeting.format('Y-m-d')})")
```

### Business Day Counter

```python
from carbonic import Date

def count_business_days_between(start_date, end_date):
    """Count business days between two dates (inclusive)."""
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    business_days = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.is_weekday():
            business_days += 1
        current_date = current_date.add(days=1)

    return business_days

# Example: Count business days in January 2024
jan_start = Date(2024, 1, 1)
jan_end = Date(2024, 1, 31)

business_days_in_jan = count_business_days_between(jan_start, jan_end)
total_days_in_jan = (jan_end - jan_start).days + 1

print(f"January 2024:")
print(f"Total days: {total_days_in_jan}")
print(f"Business days: {business_days_in_jan}")
print(f"Weekend days: {total_days_in_jan - business_days_in_jan}")
```

### SLA Calculator

```python
from carbonic import Date, DateTime

class BusinessDaySLA:
    """Calculate SLA deadlines based on business days."""

    def __init__(self, business_days=5):
        self.business_days = business_days

    def calculate_deadline(self, request_date):
        """Calculate SLA deadline from request date."""
        if isinstance(request_date, DateTime):
            request_date = request_date.to_date()

        deadline = request_date.add_business_days(self.business_days)
        return deadline

    def is_overdue(self, request_date, current_date=None):
        """Check if request is overdue."""
        if current_date is None:
            current_date = Date.today()

        deadline = self.calculate_deadline(request_date)
        return current_date > deadline

    def days_remaining(self, request_date, current_date=None):
        """Calculate business days remaining until deadline."""
        if current_date is None:
            current_date = Date.today()

        deadline = self.calculate_deadline(request_date)

        if current_date > deadline:
            # Count business days overdue
            business_days = 0
            check_date = deadline.add(days=1)
            while check_date <= current_date:
                if check_date.is_weekday():
                    business_days += 1
                check_date = check_date.add(days=1)
            return -business_days
        else:
            # Count business days remaining
            business_days = 0
            check_date = current_date.add(days=1)
            while check_date <= deadline:
                if check_date.is_weekday():
                    business_days += 1
                check_date = check_date.add(days=1)
            return business_days

# Example usage
sla = BusinessDaySLA(business_days=3)  # 3 business day SLA

# Request submitted on Friday
request_date = Date(2024, 1, 19)  # Friday
deadline = sla.calculate_deadline(request_date)

print(f"Request submitted: {request_date.format('l, F j')}")
print(f"SLA deadline: {deadline.format('l, F j')}")

# Check status on different days
check_dates = [
    Date(2024, 1, 22),  # Monday
    Date(2024, 1, 23),  # Tuesday
    Date(2024, 1, 24),  # Wednesday (deadline)
    Date(2024, 1, 25),  # Thursday (overdue)
]

for check_date in check_dates:
    overdue = sla.is_overdue(request_date, check_date)
    remaining = sla.days_remaining(request_date, check_date)

    status = "OVERDUE" if overdue else "ON TIME"
    if remaining > 0:
        time_info = f"{remaining} business days remaining"
    elif remaining == 0:
        time_info = "due today"
    else:
        time_info = f"{abs(remaining)} business days overdue"

    print(f"{check_date.format('l')}: {status} - {time_info}")
```

## Advanced Usage

### Business Day Validation

```python
from carbonic import Date

def validate_business_date(date, field_name="date"):
    """Validate that a date is a business day."""
    if not isinstance(date, Date):
        raise TypeError(f"{field_name} must be a Date object")

    if not date.is_weekday():
        day_name = date.format("l")
        raise ValueError(f"{field_name} ({date}) falls on {day_name}, which is not a business day")

    return date

# Example usage
try:
    business_date = validate_business_date(Date(2024, 1, 15))  # Monday - OK
    print(f"Valid business date: {business_date}")
except ValueError as e:
    print(f"Validation error: {e}")

try:
    weekend_date = validate_business_date(Date(2024, 1, 20))  # Saturday - Error
except ValueError as e:
    print(f"Validation error: {e}")
```

### Business Day Range Generation

```python
from carbonic import Date

def generate_business_days(start_date, end_date):
    """Generate all business days between two dates."""
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    current_date = start_date
    while current_date <= end_date:
        if current_date.is_weekday():
            yield current_date
        current_date = current_date.add(days=1)

def get_business_days_in_month(year, month):
    """Get all business days in a specific month."""
    start_date = Date(year, month, 1)
    # Get last day of month by going to next month and subtracting 1 day
    next_month = start_date.add(months=1)
    end_date = next_month.subtract(days=1)
    return list(generate_business_days(start_date, end_date))

# Example: Get all business days in January 2024
business_days = get_business_days_in_month(2024, 1)
print(f"Business days in January 2024: {len(business_days)}")

for i, date in enumerate(business_days[:5], 1):  # Show first 5
    print(f"{i:2d}. {date.format('l, F j')} ({date})")

print(f"... and {len(business_days) - 5} more business days")
```

### Holiday Awareness (Basic)

```python
from carbonic import Date

def is_holiday(date, holidays=None):
    """Check if date is a holiday (basic implementation)."""
    if holidays is None:
        # Basic US federal holidays (fixed dates only)
        holidays = [
            Date(date.year, 1, 1),   # New Year's Day
            Date(date.year, 7, 4),   # Independence Day
            Date(date.year, 12, 25), # Christmas Day
        ]
    return date in holidays

def add_business_days_excluding_holidays(start_date, business_days, holidays=None):
    """Add business days while excluding holidays."""
    current_date = start_date
    days_added = 0

    while days_added < business_days:
        current_date = current_date.add(days=1)

        if current_date.is_weekday() and not is_holiday(current_date, holidays):
            days_added += 1

    return current_date

# Example: Add 5 business days from December 20, 2024
start = Date(2024, 12, 20)  # Friday before Christmas
end = add_business_days_excluding_holidays(start, 5)

print(f"Start: {start.format('l, F j')}")
print(f"5 business days later (excluding Christmas): {end.format('l, F j')}")
```

## Performance Considerations

Business day calculations are optimized for common use cases:

```python
from carbonic import Date
import time

# Efficient for reasonable ranges
start_time = time.time()
start_date = Date(2024, 1, 1)
result = start_date.add_business_days(100)  # Fast
end_time = time.time()

print(f"Added 100 business days in {(end_time - start_time) * 1000:.2f}ms")

# For very large ranges, consider chunking
def add_business_days_chunked(start_date, business_days, chunk_size=50):
    """Add business days in chunks for very large ranges."""
    current_date = start_date
    remaining = business_days

    while remaining > 0:
        chunk = min(remaining, chunk_size)
        current_date = current_date.add_business_days(chunk)
        remaining -= chunk

    return current_date
```

## See Also

- [Date Guide](date.md) - Complete Date operations
- [DateTime Guide](datetime.md) - DateTime with business day support
- [Examples](../examples/common-tasks.md#business-days) - More business day examples
- [API Reference](../api/date.md#business-days) - Complete business day API