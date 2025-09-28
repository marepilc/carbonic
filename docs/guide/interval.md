# Interval Guide

The `Interval` class represents time intervals with start and end points, supporting comprehensive operations like intersection, union, and overlap detection.

## Overview

Intervals are **half-open**: `[start, end)` - inclusive start, exclusive end. This means the start time is included, but the end time is not.

```python
from carbonic import DateTime, Date, Interval

# Meeting from 9:00 AM to 10:30 AM
meeting = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 10, 30)
)

# 9:00 AM is included, 10:30 AM is not
meeting.contains(DateTime(2024, 1, 15, 9, 0))     # True - start included
meeting.contains(DateTime(2024, 1, 15, 10, 30))   # False - end excluded
meeting.contains(DateTime(2024, 1, 15, 10, 29))   # True - before end
```

## Creating Intervals

### DateTime Intervals

```python
from carbonic import DateTime, Interval

# Meeting interval
meeting = Interval(
    start=DateTime(2024, 1, 15, 9, 0, tz="UTC"),
    end=DateTime(2024, 1, 15, 10, 30, tz="UTC")
)

# Conference session
session = Interval(
    start=DateTime(2024, 3, 10, 14, 0, tz="America/New_York"),
    end=DateTime(2024, 3, 10, 16, 30, tz="America/New_York")
)
```

### Date Intervals

```python
from carbonic import Date, Interval

# Vacation period
vacation = Interval(
    start=Date(2024, 7, 1),
    end=Date(2024, 7, 15)
)

# Project sprint
sprint = Interval(
    start=Date(2024, 2, 5),
    end=Date(2024, 2, 19)  # 2-week sprint
)
```

### Mixed Date/DateTime Intervals

```python
from carbonic import Date, DateTime, Interval

# Event spanning from a date to a specific time
event = Interval(
    start=Date(2024, 6, 15),           # Start of June 15th
    end=DateTime(2024, 6, 16, 18, 0)   # 6:00 PM on June 16th
)
```

## Basic Properties

```python
from carbonic import DateTime, Interval

meeting = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 10, 30)
)

# Duration of the interval
duration = meeting.duration()
print(duration.in_minutes())  # 90.0 minutes

# Check if interval is empty (start == end)
empty = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 9, 0)
)
print(empty.is_empty())  # True
```

## Containment Operations

### Contains Point in Time

```python
from carbonic import DateTime, Date, Interval

# DateTime interval
meeting = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 10, 30)
)

# Check specific times
print(meeting.contains(DateTime(2024, 1, 15, 9, 15)))   # True
print(meeting.contains(DateTime(2024, 1, 15, 10, 30)))  # False (end excluded)
print(meeting.contains(DateTime(2024, 1, 15, 11, 0)))   # False

# Date interval
vacation = Interval(start=Date(2024, 7, 1), end=Date(2024, 7, 15))

print(vacation.contains(Date(2024, 7, 5)))   # True
print(vacation.contains(Date(2024, 7, 15)))  # False (end excluded)
```

### Check if One Interval Contains Another

```python
from carbonic import DateTime, Interval

# Main conference day
conference = Interval(
    start=DateTime(2024, 3, 10, 8, 0),
    end=DateTime(2024, 3, 10, 18, 0)
)

# Morning keynote
keynote = Interval(
    start=DateTime(2024, 3, 10, 9, 0),
    end=DateTime(2024, 3, 10, 10, 30)
)

# Check if keynote is within conference
def contains_interval(outer, inner):
    """Check if outer interval contains inner interval."""
    return (inner.start >= outer.start and inner.end <= outer.end)

keynote_within_conference = contains_interval(conference, keynote)
print(keynote_within_conference)  # True
```

## Overlap Operations

### Check for Overlap

```python
from carbonic import DateTime, Interval

morning_meeting = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 10, 30)
)

afternoon_meeting = Interval(
    start=DateTime(2024, 1, 15, 14, 0),
    end=DateTime(2024, 1, 15, 15, 30)
)

overlapping_meeting = Interval(
    start=DateTime(2024, 1, 15, 10, 0),  # Overlaps last 30 minutes
    end=DateTime(2024, 1, 15, 11, 0)
)

print(morning_meeting.overlaps(afternoon_meeting))   # False
print(morning_meeting.overlaps(overlapping_meeting)) # True
```

### Find Intersection

```python
from carbonic import DateTime, Interval

meeting1 = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 11, 0)
)

meeting2 = Interval(
    start=DateTime(2024, 1, 15, 10, 0),
    end=DateTime(2024, 1, 15, 12, 0)
)

# Find overlapping time
overlap = meeting1.intersection(meeting2)
if overlap:
    print(f"Overlap: {overlap.start} to {overlap.end}")  # 10:00 to 11:00
else:
    print("No overlap")
```

### Find Union

```python
from carbonic import DateTime, Interval

session1 = Interval(
    start=DateTime(2024, 1, 15, 9, 0),
    end=DateTime(2024, 1, 15, 10, 30)
)

session2 = Interval(
    start=DateTime(2024, 1, 15, 10, 0),  # Overlaps with session1
    end=DateTime(2024, 1, 15, 12, 0)
)

# Combine intervals
combined = session1.union(session2)
print(f"Combined: {combined.start} to {combined.end}")  # 9:00 to 12:00
```

## Practical Examples

### Meeting Scheduler

```python
from carbonic import DateTime, Interval

def find_free_time(scheduled_meetings, work_start, work_end):
    """Find free time slots between meetings."""
    work_interval = Interval(start=work_start, end=work_end)

    # Sort meetings by start time
    meetings = sorted(scheduled_meetings, key=lambda m: m.start)

    free_slots = []
    current_time = work_start

    for meeting in meetings:
        if current_time < meeting.start:
            # Found free time before this meeting
            free_slots.append(Interval(current_time, meeting.start))
        current_time = max(current_time, meeting.end)

    # Check for free time after last meeting
    if current_time < work_end:
        free_slots.append(Interval(current_time, work_end))

    return free_slots

# Usage
meetings = [
    Interval(DateTime(2024, 1, 15, 9, 0), DateTime(2024, 1, 15, 10, 30)),
    Interval(DateTime(2024, 1, 15, 14, 0), DateTime(2024, 1, 15, 15, 30)),
]

work_day = Interval(
    DateTime(2024, 1, 15, 8, 0),
    DateTime(2024, 1, 15, 17, 0)
)

free_times = find_free_time(meetings, work_day.start, work_day.end)
for slot in free_times:
    duration = slot.duration()
    print(f"Free: {slot.start.format('H:i')} - {slot.end.format('H:i')} ({duration.in_hours():.1f}h)")
```

### Project Timeline

```python
from carbonic import Date, Interval

# Project phases
planning = Interval(Date(2024, 1, 1), Date(2024, 2, 1))
development = Interval(Date(2024, 1, 15), Date(2024, 4, 1))  # Overlaps with planning
testing = Interval(Date(2024, 3, 15), Date(2024, 4, 15))

# Find overlaps
planning_dev_overlap = planning.intersection(development)
if planning_dev_overlap:
    print(f"Planning/Development overlap: {planning_dev_overlap.duration().in_days()} days")

# Check if phases contain specific dates
milestone_date = Date(2024, 2, 15)
if development.contains(milestone_date):
    print("Milestone is during development phase")
```

### Time Range Analysis

```python
from carbonic import DateTime, Interval

def analyze_time_ranges(intervals):
    """Analyze a list of time intervals."""
    if not intervals:
        return {}

    # Sort by start time
    sorted_intervals = sorted(intervals, key=lambda i: i.start)

    # Total time covered
    earliest = sorted_intervals[0].start
    latest = max(interval.end for interval in intervals)
    total_span = Interval(earliest, latest)

    # Total duration (sum of all intervals)
    total_duration = sum(
        (interval.duration() for interval in intervals),
        start=Duration()
    )

    # Find gaps between intervals
    gaps = []
    for i in range(len(sorted_intervals) - 1):
        current_end = sorted_intervals[i].end
        next_start = sorted_intervals[i + 1].start

        if current_end < next_start:
            gaps.append(Interval(current_end, next_start))

    return {
        'total_span': total_span,
        'total_duration': total_duration,
        'gaps': gaps,
        'utilization': total_duration.total_seconds() / total_span.duration().total_seconds()
    }
```

## Error Handling

```python
from carbonic import DateTime, Interval

# Invalid interval (end before start)
try:
    invalid = Interval(
        start=DateTime(2024, 1, 15, 10, 0),
        end=DateTime(2024, 1, 15, 9, 0)
    )
except ValueError as e:
    print(f"Error: {e}")  # End time must be after start time
```

## Type Compatibility

```python
from carbonic import Date, DateTime, Interval

# Same types work seamlessly
date_interval = Interval(Date(2024, 1, 1), Date(2024, 1, 31))
datetime_interval = Interval(
    DateTime(2024, 1, 15, 9, 0),
    DateTime(2024, 1, 15, 17, 0)
)

# Mixed types are automatically handled
mixed_interval = Interval(
    Date(2024, 1, 15),                    # Converted to start of day
    DateTime(2024, 1, 16, 12, 0)         # Specific time
)
```

## See Also

- [DateTime Guide](datetime.md) - Working with datetimes
- [Date Guide](date.md) - Date-only operations
- [Duration Guide](duration.md) - Time spans and arithmetic
- [API Reference](../api/interval.md) - Complete Interval API