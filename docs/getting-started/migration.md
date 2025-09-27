# Migration Guide

This guide helps you migrate from other datetime libraries to Carbonic.

## From Python's datetime

Carbonic builds on Python's standard library while providing a more fluent API.

### Basic Object Creation

=== "Before (datetime)"
    ```python
    import datetime
    from zoneinfo import ZoneInfo

    # Current time
    now = datetime.datetime.now(ZoneInfo("UTC"))

    # Specific datetime
    dt = datetime.datetime(2024, 1, 15, 14, 30, tzinfo=ZoneInfo("UTC"))

    # Date only
    date = datetime.date(2024, 1, 15)
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime, Date, now, today

    # Current time
    now_dt = now("UTC")  # UTC is default

    # Specific datetime
    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Date only
    date = Date(2024, 1, 15)
    ```

### Date Arithmetic

=== "Before (datetime)"
    ```python
    import datetime

    dt = datetime.datetime(2024, 1, 15, 14, 30)

    # Add time
    future = dt + datetime.timedelta(days=7, hours=2)

    # More complex operations require manual calculation
    # No built-in "add months" or "end of month"
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime, Duration

    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Add time - multiple ways
    future1 = dt + Duration(days=7, hours=2)
    future2 = dt.add_days(7).add_hours(2)

    # Rich date operations
    next_month = dt.add_months(1)
    end_of_month = dt.end_of_month()
    next_friday = dt.next(Period.FRIDAY)
    ```

### Formatting

=== "Before (datetime)"
    ```python
    import datetime

    dt = datetime.datetime(2024, 1, 15, 14, 30)

    # strftime only
    formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
    iso_format = dt.isoformat()
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime

    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Multiple format methods
    formatted = dt.format("Y-m-d H:i:s")  # Carbon-style
    iso_format = dt.to_iso_string()
    date_only = dt.to_date_string()
    time_only = dt.to_time_string()

    # Still supports strftime
    strftime_format = dt.strftime("%Y-%m-%d %H:%M:%S")
    ```

### Timezone Handling

=== "Before (datetime)"
    ```python
    import datetime
    from zoneinfo import ZoneInfo

    # Create timezone-aware
    utc_dt = datetime.datetime(2024, 1, 15, 14, 30, tzinfo=ZoneInfo("UTC"))

    # Convert timezone
    ny_dt = utc_dt.astimezone(ZoneInfo("America/New_York"))

    # Naive datetime (problematic)
    naive = datetime.datetime(2024, 1, 15, 14, 30)
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime

    # Create timezone-aware (encouraged)
    utc_dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Convert timezone (fluent)
    ny_dt = utc_dt.to_timezone("America/New_York")

    # Naive datetime (discouraged but supported)
    naive = DateTime(2024, 1, 15, 14, 30, tz=None)
    aware = naive.assume_timezone("UTC")
    ```

## From Arrow

Arrow users will find Carbonic familiar with some improvements.

### Object Creation

=== "Before (Arrow)"
    ```python
    import arrow

    # Current time
    now = arrow.now()
    utc_now = arrow.utcnow()

    # Specific datetime
    dt = arrow.get(2024, 1, 15, 14, 30)

    # From string
    parsed = arrow.get("2024-01-15T14:30:00Z")
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime, now

    # Current time
    now_dt = now()  # UTC by default
    local_now = now("America/New_York")

    # Specific datetime
    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # From string
    parsed = DateTime.from_iso("2024-01-15T14:30:00Z")
    ```

### Fluent Operations

=== "Before (Arrow)"
    ```python
    import arrow

    dt = arrow.get(2024, 1, 15, 14, 30)

    # Fluent operations
    result = (dt
        .shift(days=7)
        .replace(hour=0, minute=0, second=0)
        .to("America/New_York")
    )
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime

    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Similar fluent operations
    result = (dt
        .add_days(7)
        .start_of_day()
        .to_timezone("America/New_York")
    )
    ```

### Formatting and Humanizing

=== "Before (Arrow)"
    ```python
    import arrow

    dt = arrow.get(2024, 1, 15, 14, 30)

    # Formatting
    formatted = dt.format("YYYY-MM-DD HH:mm:ss")

    # Humanizing
    human = dt.humanize()  # "in 2 days"
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime

    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Formatting
    formatted = dt.format("Y-m-d H:i:s")

    # Humanizing (with localization support)
    human = dt.diff_for_humans()  # "2 days ago"
    ```

## From Pendulum

Pendulum users will appreciate Carbonic's similar philosophy with stdlib focus.

### Basic Usage

=== "Before (Pendulum)"
    ```python
    import pendulum

    # Current time
    now = pendulum.now()
    utc_now = pendulum.now("UTC")

    # Specific datetime
    dt = pendulum.datetime(2024, 1, 15, 14, 30, tz="UTC")

    # Date only
    date = pendulum.date(2024, 1, 15)
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime, Date, now, today

    # Current time
    now_dt = now()  # UTC by default
    local_now = now("America/New_York")

    # Specific datetime
    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Date only
    date = Date(2024, 1, 15)
    ```

### Periods and Durations

=== "Before (Pendulum)"
    ```python
    import pendulum

    dt = pendulum.datetime(2024, 1, 15, 14, 30, tz="UTC")

    # Add periods
    future = dt.add(months=1, days=2, hours=3)

    # Subtract periods
    past = dt.subtract(weeks=2)

    # Duration between dates
    diff = dt2 - dt1
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime, Duration

    dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

    # Add time (fluent or duration objects)
    future = dt.add_months(1).add_days(2).add_hours(3)
    future_alt = dt + Duration(days=2, hours=3)  # months need special handling

    # Subtract time
    past = dt.subtract_weeks(2)

    # Duration between dates
    diff = dt2 - dt1  # Returns Duration object
    ```

## Common Migration Patterns

### Error Handling

=== "Before (Various)"
    ```python
    # Different libraries use different exceptions
    try:
        dt = some_library.parse("invalid")
    except ValueError:  # or TypeError, or custom exception
        handle_error()
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime
    from carbonic.core.exceptions import ParseError, InvalidTimezone

    try:
        dt = DateTime.from_format("invalid", "Y-m-d")
    except ParseError:
        handle_parse_error()

    try:
        dt = DateTime(2024, 1, 15, tz="Invalid/Zone")
    except InvalidTimezone:
        handle_timezone_error()
    ```

### Working with Business Days

=== "Before (Manual)"
    ```python
    import datetime

    def next_business_day(dt):
        days_ahead = 1
        if dt.weekday() == 4:  # Friday
            days_ahead = 3
        elif dt.weekday() == 5:  # Saturday
            days_ahead = 2
        return dt + datetime.timedelta(days=days_ahead)
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime

    dt = DateTime(2024, 1, 15, tz="UTC")
    next_business = dt.next_business_day()

    # Also available:
    is_business = dt.is_business_day()
    business_days_count = dt.business_days_until(future_dt)
    ```

### Batch Operations

=== "Before (Manual)"
    ```python
    import datetime
    from typing import List

    def add_days_to_list(dates: List[datetime.datetime], days: int):
        return [dt + datetime.timedelta(days=days) for dt in dates]
    ```

=== "After (Carbonic)"
    ```python
    from carbonic import DateTime
    from typing import List

    def add_days_to_list(dates: List[DateTime], days: int):
        return [dt.add_days(days) for dt in dates]

    # Even better with method chaining:
    processed_dates = [
        dt.add_days(7).end_of_week().to_timezone("UTC")
        for dt in original_dates
    ]
    ```

## Performance Considerations

### When Coming from Arrow/Pendulum

```python
# These libraries have some overhead for convenience
# Carbonic aims to be faster while maintaining ease of use

# For bulk operations, consider:
from carbonic import DateTime

# Example data for demonstration
many_iso_strings = ["2024-01-01T00:00:00Z", "2024-01-02T00:00:00Z"]

# Instead of parsing many strings:
dates = [DateTime.parse(s) for s in many_iso_strings]

# Consider creating once and using arithmetic:
base_date = DateTime(2024, 1, 1, tz="UTC")
dates = [base_date.add(days=i) for i in range(5)]  # Generate 5 dates for example
```

### Memory Usage

```python
# Carbonic uses __slots__ for memory efficiency
from carbonic import DateTime

# Each DateTime object is lightweight
dt = DateTime.now()
print(dt.__slots__)  # ('_dt',)

# Compared to regular objects, this uses less memory
# Important for applications handling many datetime objects
```

## Migration Checklist

When migrating to Carbonic:

- [ ] **Update imports**: Change to `from carbonic import DateTime, Date, Duration`
- [ ] **Review timezone handling**: Ensure all datetimes are timezone-aware
- [ ] **Update method calls**: Use Carbonic's fluent method names
- [ ] **Check error handling**: Update exception types
- [ ] **Test thoroughly**: Verify behavior matches expectations
- [ ] **Install optional dependencies**: Consider `carbonic[fast]` for performance
- [ ] **Update type annotations**: Use Carbonic types for better type checking

## Getting Help

If you're migrating and run into issues:

1. **Check the API reference**: [API Documentation](../api/index.md)
2. **Look at examples**: [Common Tasks](../examples/common-tasks.md)
3. **File an issue**: [GitHub Issues](https://github.com/marepilc/carbonic/issues)
4. **Ask questions**: Use GitHub Discussions for help

The Carbonic community is happy to help with migration questions!