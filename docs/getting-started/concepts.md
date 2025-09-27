# Core Concepts

Understanding these fundamental concepts will help you work effectively with Carbonic.

## Immutability

One of Carbonic's core principles is **immutability**. All datetime objects are frozen dataclasses that cannot be modified after creation.

### Why Immutability?

```python
from carbonic import DateTime

original = DateTime(2024, 1, 15, 10, 0, tz="UTC")

# This creates a NEW datetime object
modified = original.add(hours=2)

print(original)  # 2024-01-15T10:00:00+00:00 (unchanged!)
print(modified)  # 2024-01-15T12:00:00+00:00 (new object)

# This would raise an error:
# original.hour = 12  # FrozenInstanceError!
```

**Benefits:**

- **Thread Safety**: Immutable objects can be safely shared between threads
- **Predictable Code**: No unexpected mutations breaking your logic
- **Easier Debugging**: Values can't change unexpectedly
- **Functional Programming**: Natural fit for functional programming patterns

### Working with Immutability

Since all operations return new objects, you can chain them fluently:

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 9, 0, tz="UTC")

# Chain operations - each returns a new object
result = (dt
    .add(days=1)
    .add(hours=2)
    .start_of("hour")
)

# Or store intermediate results
next_day = dt.add(days=1)
with_hours = next_day.add(hours=2)
final = with_hours.start_of("hour")
```

## Timezone Handling

Carbonic uses Python's standard library `zoneinfo` for robust timezone support.

### Timezone-Aware by Default

```python
from carbonic import DateTime

# Always specify timezone (UTC is default)
utc_time = DateTime(2024, 1, 15, 14, 30, tz="UTC")
local_time = DateTime(2024, 1, 15, 14, 30, tz="America/New_York")

# Current time methods default to UTC
current_utc = DateTime.now()  # UTC
current_local = DateTime.now("America/New_York")  # Local timezone
```

### Timezone Conversions

```python
from carbonic import DateTime

# Create in one timezone
paris_time = DateTime(2024, 1, 15, 15, 30, tz="Europe/Paris")

# Represent the same moment in different timezones
# Paris time: 15:30 CET (UTC+1)
tokyo_time = DateTime(2024, 1, 15, 23, 30, tz="Asia/Tokyo")   # Same moment, different timezone
utc_time = DateTime(2024, 1, 15, 14, 30, tz="UTC")           # Same moment in UTC

print(f"Paris: {paris_time}")  # 2024-01-15T15:30:00+01:00
print(f"Tokyo: {tokyo_time}")  # 2024-01-15T23:30:00+09:00
print(f"UTC:   {utc_time}")    # 2024-01-15T14:30:00+00:00
```

### Naive vs Aware

Carbonic strongly encourages timezone-aware datetimes:

```python
from carbonic import DateTime

# Timezone-aware (recommended)
aware = DateTime(2024, 1, 15, 14, 30, tz="UTC")
print(aware.tzinfo)  # <ZoneInfo 'UTC'>

# Naive datetime (discouraged)
naive = DateTime(2024, 1, 15, 14, 30, tz=None)
print(naive.tzinfo)  # None

# Converting naive to aware - create new DateTime with timezone
aware_from_naive = DateTime(naive.year, naive.month, naive.day, naive.hour, naive.minute, naive.second, tz="UTC")
```

!!! warning "Avoid Naive Datetimes"
    Naive datetimes (without timezone info) can lead to bugs and confusion. Always specify a timezone when possible.

## Fluent API Design

Carbonic's API is designed to read naturally and chain operations:

### Method Naming Convention

Methods are named to be readable and self-documenting:

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 10, 30, tz="UTC")

# Descriptive method names
next_monday = dt.add(days=7)  # Simplified: add 7 days for next week
end_of_month = dt.end_of("month")
business_day = dt.to_date().add_business_days(1).to_datetime()
midnight = dt.start_of("day")

# Boolean methods start with "is_"
print(dt.to_date().is_weekend())      # False
print(dt.to_date().is_weekday())      # True (business day)
print(dt < DateTime.now())  # True (if current time is later)

# Navigation methods
midnight = dt.start_of("day")
```

### Chaining Operations

The fluent API allows natural chaining:

```python
from carbonic import DateTime

# Readable chains
dt = DateTime.now("UTC")
date_obj = dt.to_date()
next_business_date = date_obj.add_business_days(1)
next_business_dt = DateTime(
    next_business_date.year,
    next_business_date.month,
    next_business_date.day,
    0,
    0,
    0,
    tz="UTC",
)
next_business_end = next_business_dt.end_of("day").subtract(hours=1)

# Equivalent to:
now = DateTime.now("UTC")
next_business_date = now.to_date().add_business_days(1)
next_business = DateTime(
    next_business_date.year,
    next_business_date.month,
    next_business_date.day,
    0,
    0,
    0,
    tz="UTC",
)
end_of_day = next_business.end_of("day")
result = end_of_day.subtract(hours=1)
```

## Type Safety

Carbonic is designed with strong typing throughout:

### Full Type Annotations

```python
from carbonic import DateTime, Duration, Date

# All methods are fully typed
dt: DateTime = DateTime.now()
duration: Duration = Duration(hours=2)
future: DateTime = dt + duration  # Type checker knows this is DateTime

# Date operations return Date objects
date: Date = dt.to_date()
tomorrow: Date = date.add(days=1)
```

### Generic Return Types

Methods return the appropriate types:

```python
from carbonic import DateTime, Date

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
date = Date(2024, 1, 15)

# DateTime methods return DateTime
new_dt: DateTime = dt.add(hours=2)

# Date methods return Date
new_date: Date = date.add(days=1)

# Conversion methods return appropriate types
converted_date: Date = dt.to_date()
converted_datetime: DateTime = date.to_datetime(tz="UTC")
```

### IDE Support

Strong typing enables excellent IDE support:

- **Autocomplete**: See all available methods
- **Type Checking**: Catch errors before runtime
- **Refactoring**: Safe renaming and restructuring
- **Documentation**: Inline help and parameter hints

## Performance Considerations

Carbonic is designed for both ease of use and performance:

### Efficient Immutability

```python
from carbonic import DateTime

# Objects use __slots__ for memory efficiency  
dt = DateTime.now()
print(f"DateTime object: {dt}")

# Internal datetime is reused when possible
dt1 = DateTime(2024, 1, 15, 10, 0, tz="UTC")
dt2 = DateTime(dt1.year, dt1.month, dt1.day, dt1.hour, 30, dt1.second, tz="UTC")  # Create new with different minute
```

### Lazy Evaluation

Expensive operations are performed only when needed:

```python
from carbonic import DateTime

dt = DateTime.now()

# Formatting is lazy - only computed when string is accessed
formatted = dt.format("l, F j, Y")  # Not computed yet
print(formatted)  # Now it's computed
```

### Optional Acceleration

Use fast parsing when available:

```python
# Install with: pip install carbonic[fast]
from carbonic import DateTime

# Uses ciso8601 if available, falls back to stdlib
dt = DateTime.parse("2024-01-15T14:30:00Z")  # Fast parsing
```

## Error Handling

Carbonic uses specific exceptions for different error conditions:

```python
from carbonic import DateTime
from carbonic.core.exceptions import ParseError

try:
    # Invalid timezone will raise ZoneInfoNotFoundError from zoneinfo
    dt = DateTime(2024, 1, 15, tz="Invalid/Timezone")
except Exception as e:
    print(f"Timezone error: {e}")

try:
    # Invalid date format
    dt = DateTime.parse("invalid", "Y-m-d")
except ParseError as e:
    print(f"Parse error: {e}")
```

## Design Philosophy

Understanding Carbonic's design philosophy helps you use it effectively:

### Principle of Least Surprise

Methods do what their names suggest:

```python
from carbonic import DateTime

dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")

# These do exactly what you'd expect
print(dt.start_of("day"))    # 2024-01-15T00:00:00+00:00
print(dt.end_of("month"))    # 2024-01-31T23:59:59.999999+00:00
print(dt.add(days=1))        # 2024-01-16T14:30:00+00:00
```

### Explicit Over Implicit

When there's ambiguity, Carbonic requires explicit choices:

```python
from carbonic import DateTime

# Explicit timezone specification
dt = DateTime(2024, 1, 15, tz="UTC")  # Clear intent

# Explicit conversion
naive_dt = DateTime(2024, 1, 15, tz=None)
aware_dt = DateTime(naive_dt.year, naive_dt.month, naive_dt.day, tz="UTC")  # Explicit conversion
```

### Modern Python Features

Carbonic leverages modern Python capabilities:

- **Dataclasses**: Clean, efficient object definitions
- **Type Hints**: Full PEP 561 compliance
- **Slots**: Memory-efficient objects
- **Union Types**: Flexible parameter types (Python 3.12+ syntax)

## Next Steps

Now that you understand the core concepts:

1. **Practice**: Try the examples in the [Quick Start](quickstart.md)
2. **Explore**: Read the detailed [User Guide](../guide/datetime.md)
3. **Apply**: Check out real-world [Examples](../examples/common-tasks.md)
4. **Reference**: Use the [API Documentation](../api/index.md) for details