# Pydantic Integration

Carbonic provides seamless integration with [Pydantic](https://pydantic.dev/) for data validation and serialization. This allows you to use Carbonic's datetime classes in Pydantic models with automatic validation and JSON serialization.

## Installation

To use Pydantic integration, install Carbonic with the pydantic extra:

```bash
pip install carbonic[pydantic]
```

## Available Field Types

Carbonic provides custom Pydantic field types for all core classes:

- `DateField` - for `carbonic.Date` objects
- `DateTimeField` - for `carbonic.DateTime` objects
- `DurationField` - for `carbonic.Duration` objects
- `IntervalField` - for `carbonic.Interval` objects
- `PeriodField` - for `carbonic.Period` objects

## Basic Usage

### Simple Model Example

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import DateField, DateTimeField, DurationField

class Event(BaseModel):
    name: str
    date: DateField
    start_time: DateTimeField
    duration: DurationField

# Create an event
event = Event(
    name="Team Meeting",
    date="2024-01-15",
    start_time="2024-01-15T14:00:00Z",
    duration="PT2H"
)

print(event.date)        # Date(2024, 1, 15)
print(event.start_time)  # DateTime(2024, 1, 15, 14, 0, 0, tz='UTC')
print(event.duration)    # Duration(days=0, storage_seconds=7200, ...)
```

### JSON Serialization

Carbonic field types automatically serialize to appropriate JSON formats:

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import DateField, DateTimeField, DurationField

class Event(BaseModel):
    name: str
    date: DateField
    start_time: DateTimeField
    duration: DurationField

# Create an event
event = Event(
    name="Team Meeting",
    date="2024-01-15",
    start_time="2024-01-15T14:00:00Z",
    duration="PT2H"
)

# Serialize to JSON
json_data = event.model_dump_json()
print(json_data)
# {"name":"Team Meeting","date":"2024-01-15","start_time":"2024-01-15T14:00:00+00:00","duration":"PT2H"}

# Deserialize from JSON
import json
event_data = json.loads(json_data)
new_event = Event(**event_data)
assert new_event.name == event.name
assert new_event.date == event.date
```

## Field Type Details

### DateField

Accepts and validates:
- `Date` instances
- ISO 8601 date strings (`"2024-01-15"`)
- Dictionaries with date components

```python
from pydantic import BaseModel
from carbonic import Date
from carbonic.integrations.pydantic import DateField

class Task(BaseModel):
    due_date: DateField

# All these work:
Task(due_date=Date(2024, 1, 15))
Task(due_date="2024-01-15")
Task(due_date={"year": 2024, "month": 1, "day": 15})
```

### DateTimeField

Accepts and validates:
- `DateTime` instances
- ISO 8601 datetime strings with timezone
- Dictionaries with datetime components

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import DateTimeField

class Meeting(BaseModel):
    start_time: DateTimeField
    end_time: DateTimeField

# All these work:
meeting = Meeting(
    start_time="2024-01-15T14:00:00Z",
    end_time="2024-01-15T16:00:00+02:00"
)
```

### DurationField

Accepts and validates:
- `Duration` instances
- ISO 8601 duration strings (`"PT2H30M"`)
- Numbers (interpreted as seconds)
- Dictionaries with duration components

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import DurationField

class Task(BaseModel):
    estimated_duration: DurationField

# All these work:
Task(estimated_duration="PT2H30M")      # ISO 8601
Task(estimated_duration=9000)           # 2.5 hours in seconds
Task(estimated_duration={"hours": 2, "minutes": 30})
```

### IntervalField

Accepts and validates:
- `Interval` instances
- Dictionaries with `start` and `end` keys
- Tuples/lists with `[start, end]` elements

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import IntervalField

class Booking(BaseModel):
    time_slot: IntervalField

# All these work:
Booking(time_slot={
    "start": "2024-01-15T14:00:00Z",
    "end": "2024-01-15T16:00:00Z"
})

Booking(time_slot=[
    "2024-01-15T14:00:00Z",
    "2024-01-15T16:00:00Z"
])
```

### PeriodField

Accepts and validates:
- `Period` instances
- Period name strings (`"DAY"`, `"WEEK"`, `"MONTH"`, etc.)

```python
from pydantic import BaseModel
from carbonic import Period
from carbonic.integrations.pydantic import PeriodField

class Schedule(BaseModel):
    frequency: PeriodField

# All these work:
Schedule(frequency=Period.WEEK)
Schedule(frequency="WEEK")
Schedule(frequency="week")  # Case insensitive
```

## Advanced Examples

### Complex Event Management System

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from carbonic.integrations.pydantic import (
    DateField, DateTimeField, DurationField,
    IntervalField, PeriodField
)

class Attendee(BaseModel):
    name: str
    email: str
    confirmed_at: Optional[DateTimeField] = None

class RecurringEvent(BaseModel):
    id: int
    title: str
    description: str
    start_date: DateField
    time_slot: IntervalField
    duration: DurationField
    recurrence: PeriodField
    attendees: List[Attendee] = Field(default_factory=list)
    created_at: DateTimeField
    updated_at: Optional[DateTimeField] = None

# Create a recurring meeting
meeting = RecurringEvent(
    id=1,
    title="Weekly Standup",
    description="Team synchronization meeting",
    start_date="2024-01-15",
    time_slot={
        "start": "2024-01-15T09:00:00Z",
        "end": "2024-01-15T10:00:00Z"
    },
    duration="PT1H",
    recurrence="WEEK",
    attendees=[
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"}
    ],
    created_at="2024-01-10T12:00:00Z"
)

# JSON serialization maintains all datetime information
json_output = meeting.model_dump_json(indent=2)
print(json_output)
```

### Validation and Error Handling

```python
from pydantic import BaseModel, ValidationError
from carbonic.integrations.pydantic import DateField, DurationField

class Event(BaseModel):
    name: str
    date: DateField
    duration: DurationField

try:
    # This will raise a validation error
    event = Event(
        name="Invalid Event",
        date="not-a-date",
        duration="invalid-duration"
    )
except ValidationError as e:
    print("Validation errors:")
    for error in e.errors():
        print(f"- {error['loc'][0]}: {error['msg']}")
```

### Custom Validators

You can combine Carbonic field types with Pydantic's custom validators:

```python
from pydantic import BaseModel, field_validator, ValidationError
from carbonic import Date
from carbonic.integrations.pydantic import DateField

class FutureEvent(BaseModel):
    name: str
    date: DateField

    @field_validator('date')
    @classmethod
    def date_must_be_future(cls, v: Date) -> Date:
        if v <= Date.today():
            raise ValueError('Event date must be in the future')
        return v

# This works
event = FutureEvent(name="Future Event", date="2026-01-15")

# This raises validation error
try:
    past_event = FutureEvent(name="Past Event", date="2020-01-15")
except ValidationError:
    print("Cannot create event in the past!")
```

## Type Aliases

For convenience, Carbonic also provides type aliases:

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import (
    CarbonicDate,      # alias for DateField
    CarbonicDateTime,  # alias for DateTimeField
    CarbonicDuration,  # alias for DurationField
    CarbonicInterval,  # alias for IntervalField
    CarbonicPeriod,    # alias for PeriodField
)

class Event(BaseModel):
    date: CarbonicDate
    start_time: CarbonicDateTime
    duration: CarbonicDuration
```

## JSON Schema Generation

Carbonic field types automatically generate appropriate JSON schemas for OpenAPI documentation:

```python
from pydantic import BaseModel
from carbonic.integrations.pydantic import DateField, DateTimeField

class Event(BaseModel):
    date: DateField
    start_time: DateTimeField

# Generate JSON schema
schema = Event.model_json_schema()
print(schema['properties']['date'])
```

This integration makes Carbonic datetime classes work seamlessly with FastAPI, SQLModel, and other Pydantic-based frameworks, providing robust datetime validation and serialization out of the box.