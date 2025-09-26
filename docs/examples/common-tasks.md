# Common Tasks

This page demonstrates how to accomplish common datetime-related tasks using Carbonic.

## Working with Current Time

### Getting Current Time in Different Timezones

```python
from carbonic import now

# Current time in UTC (default)
utc_now = now()
print(f"UTC: {utc_now}")

# Current time in specific timezones
ny_now = now("America/New_York")
london_now = now("Europe/London")
tokyo_now = now("Asia/Tokyo")

print(f"New York: {ny_now}")
print(f"London: {london_now}")
print(f"Tokyo: {tokyo_now}")
```

### Converting Between Timezones

```python
from carbonic import DateTime

# Create datetime in one timezone
meeting_utc = DateTime(2024, 3, 15, 14, 30, tz="UTC")

# Convert to participant timezones
meeting_ny = meeting_utc.to_timezone("America/New_York")
meeting_london = meeting_utc.to_timezone("Europe/London")
meeting_tokyo = meeting_utc.to_timezone("Asia/Tokyo")

print("Global Meeting Times:")
print(f"UTC: {meeting_utc.format('H:i')}")
print(f"New York: {meeting_ny.format('H:i')}")
print(f"London: {meeting_london.format('H:i')}")
print(f"Tokyo: {meeting_tokyo.format('H:i')}")
```

## Date Calculations

### Age Calculation

```python
from carbonic import Date, today

def calculate_age(birth_date):
    """Calculate age in years."""
    today_date = today()
    return birth_date.diff_in_years(today_date)

def calculate_detailed_age(birth_date):
    """Calculate detailed age with years, months, and days."""
    today_date = today()

    years = today_date.year - birth_date.year
    months = today_date.month - birth_date.month
    days = today_date.day - birth_date.day

    # Adjust for negative days
    if days < 0:
        months -= 1
        # Get days in previous month
        prev_month = today_date.subtract_months(1)
        days += prev_month.days_in_month

    # Adjust for negative months
    if months < 0:
        years -= 1
        months += 12

    return years, months, days

# Example usage
birthday = Date(1990, 5, 15)
age = calculate_age(birthday)
detailed_age = calculate_detailed_age(birthday)

print(f"Age: {age} years")
print(f"Detailed age: {detailed_age[0]} years, {detailed_age[1]} months, {detailed_age[2]} days")
```

### Time Until/Since Event

```python
from carbonic import DateTime, Duration, now

def time_until_event(event_datetime):
    """Calculate time remaining until an event."""
    current = now()

    if event_datetime.is_past():
        duration = current - event_datetime
        return f"Event was {humanize_duration(duration)} ago"
    else:
        duration = event_datetime - current
        return f"Event in {humanize_duration(duration)}"

def humanize_duration(duration):
    """Convert duration to human-readable string."""
    total_seconds = duration.total_seconds()

    if total_seconds < 60:
        return f"{int(total_seconds)} seconds"
    elif total_seconds < 3600:
        minutes = int(total_seconds // 60)
        return f"{minutes} minutes"
    elif total_seconds < 86400:
        hours = int(total_seconds // 3600)
        return f"{hours} hours"
    else:
        days = int(total_seconds // 86400)
        return f"{days} days"

# Example usage
new_year = DateTime(2025, 1, 1, 0, 0, tz="UTC")
birthday = DateTime(2024, 5, 15, 0, 0, tz="UTC")

print(time_until_event(new_year))
print(time_until_event(birthday))
```

## Business Logic

### Business Days and Working Hours

```python
from carbonic import DateTime, Date, Duration, today

def is_business_hours(dt, start_hour=9, end_hour=17):
    """Check if datetime falls within business hours."""
    if not dt.is_business_day():
        return False
    return start_hour <= dt.hour < end_hour

def next_business_datetime(dt, target_hour=9):
    """Get next business day at specific hour."""
    next_business = dt.next_business_day()
    return next_business.set_hour(target_hour).set_minute(0).set_second(0)

def add_business_hours(dt, hours):
    """Add business hours (8 hours per day, Mon-Fri)."""
    remaining_hours = hours
    current = dt

    while remaining_hours > 0:
        if current.is_business_day() and is_business_hours(current, 9, 17):
            # Calculate hours until end of business day
            end_of_business = current.set_hour(17).set_minute(0).set_second(0)
            hours_until_end = current.diff_in_hours(end_of_business)

            if remaining_hours <= hours_until_end:
                # Can finish today
                return current.add_hours(remaining_hours)
            else:
                # Move to next business day
                remaining_hours -= hours_until_end
                current = next_business_datetime(current, 9)
        else:
            # Move to next business day start
            current = next_business_datetime(current, 9)

    return current

# Example usage
start_work = DateTime(2024, 1, 15, 10, 0, tz="UTC")  # Monday 10 AM

print(f"Is business hours: {is_business_hours(start_work)}")
print(f"Next business day: {next_business_datetime(start_work)}")
print(f"After 20 business hours: {add_business_hours(start_work, 20)}")
```

### Deadline Management

```python
from carbonic import DateTime, Duration, now

class DeadlineTracker:
    def __init__(self, deadline, warning_hours=24):
        self.deadline = deadline
        self.warning_threshold = Duration(hours=warning_hours)

    def status(self):
        """Get current status of the deadline."""
        current = now()

        if current > self.deadline:
            overdue_duration = current - self.deadline
            return f"OVERDUE by {self._format_duration(overdue_duration)}"

        remaining = self.deadline - current

        if remaining <= self.warning_threshold:
            return f"WARNING: {self._format_duration(remaining)} remaining"

        return f"OK: {self._format_duration(remaining)} remaining"

    def _format_duration(self, duration):
        """Format duration for display."""
        hours = duration.total_hours()
        if hours < 1:
            return f"{int(duration.total_minutes())} minutes"
        elif hours < 24:
            return f"{int(hours)} hours"
        else:
            days = int(duration.total_days())
            remaining_hours = int(hours % 24)
            if remaining_hours == 0:
                return f"{days} days"
            return f"{days} days, {remaining_hours} hours"

# Example usage
project_deadline = DateTime(2024, 1, 20, 17, 0, tz="UTC")
tracker = DeadlineTracker(project_deadline, warning_hours=48)

print(f"Project status: {tracker.status()}")
```

## Scheduling and Recurrence

### Meeting Scheduler

```python
from carbonic import DateTime, Period, Duration

class MeetingScheduler:
    def __init__(self, start_date, duration_minutes=60):
        self.start_date = start_date
        self.duration = Duration(minutes=duration_minutes)

    def weekly_meetings(self, count=10):
        """Generate weekly recurring meetings."""
        meetings = []
        current = self.start_date

        for _ in range(count):
            end_time = current + self.duration
            meetings.append({
                'start': current,
                'end': end_time,
                'title': f"Weekly Meeting - {current.format('F j, Y')}"
            })
            current = current.add_weeks(1)

        return meetings

    def monthly_first_friday(self, months=6):
        """Generate monthly meetings on first Friday."""
        meetings = []
        current_month = self.start_date.start_of_month()

        for _ in range(months):
            # Find first Friday of the month
            first_friday = current_month.next(Period.FRIDAY)
            # Set time from start_date
            meeting_time = first_friday.set_time(
                self.start_date.hour,
                self.start_date.minute,
                self.start_date.second
            ).assume_timezone(self.start_date.timezone_name)

            end_time = meeting_time + self.duration
            meetings.append({
                'start': meeting_time,
                'end': end_time,
                'title': f"Monthly Review - {meeting_time.format('F Y')}"
            })
            current_month = current_month.add_months(1)

        return meetings

# Example usage
start_meeting = DateTime(2024, 1, 15, 14, 0, tz="America/New_York")
scheduler = MeetingScheduler(start_meeting, duration_minutes=90)

# Weekly meetings
weekly = scheduler.weekly_meetings(4)
print("Weekly Meetings:")
for meeting in weekly:
    print(f"  {meeting['title']}: {meeting['start'].format('l, F j - H:i')}")

print()

# Monthly meetings
monthly = scheduler.monthly_first_friday(3)
print("Monthly Meetings:")
for meeting in monthly:
    print(f"  {meeting['title']}: {meeting['start'].format('l, F j - H:i')}")
```

### Event Countdown

```python
from carbonic import DateTime, Duration
import math

def create_countdown(event_datetime, event_name):
    """Create a countdown function for an event."""

    def countdown():
        current = DateTime.now()

        if current >= event_datetime:
            return f"{event_name} has started!"

        remaining = event_datetime - current

        days = int(remaining.total_days())
        hours = int(remaining.total_hours() % 24)
        minutes = int(remaining.total_minutes() % 60)
        seconds = int(remaining.total_seconds() % 60)

        parts = []
        if days > 0:
            parts.append(f"{days} days")
        if hours > 0:
            parts.append(f"{hours} hours")
        if minutes > 0:
            parts.append(f"{minutes} minutes")
        if seconds > 0 and days == 0:  # Only show seconds if less than a day
            parts.append(f"{seconds} seconds")

        if not parts:
            return f"{event_name} starts now!"

        return f"{event_name} in: {', '.join(parts)}"

    return countdown

# Example usage
launch_date = DateTime(2024, 6, 15, 12, 0, tz="UTC")
product_countdown = create_countdown(launch_date, "Product Launch")

print(product_countdown())
```

## Data Processing

### Log Analysis

```python
from carbonic import DateTime
from typing import List, Dict

def parse_log_entries(log_lines: List[str]) -> List[Dict]:
    """Parse log entries with timestamps."""
    entries = []

    for line in log_lines:
        # Assuming format: "2024-01-15 14:30:45 [INFO] Message"
        try:
            timestamp_str = line[:19]  # First 19 characters
            dt = DateTime.from_format(timestamp_str, "Y-m-d H:i:s")

            # Extract log level and message
            rest = line[20:]
            level_end = rest.find(']')
            level = rest[1:level_end] if rest.startswith('[') else 'UNKNOWN'
            message = rest[level_end + 2:] if level_end != -1 else rest

            entries.append({
                'timestamp': dt,
                'level': level,
                'message': message.strip()
            })
        except Exception as e:
            print(f"Failed to parse line: {line}")
            continue

    return entries

def analyze_logs(entries: List[Dict]) -> Dict:
    """Analyze log entries for patterns."""
    if not entries:
        return {}

    # Sort by timestamp
    entries.sort(key=lambda x: x['timestamp'])

    start_time = entries[0]['timestamp']
    end_time = entries[-1]['timestamp']
    duration = end_time - start_time

    # Count by level
    level_counts = {}
    for entry in entries:
        level = entry['level']
        level_counts[level] = level_counts.get(level, 0) + 1

    # Find peak hour
    hourly_counts = {}
    for entry in entries:
        hour = entry['timestamp'].hour
        hourly_counts[hour] = hourly_counts.get(hour, 0) + 1

    peak_hour = max(hourly_counts.items(), key=lambda x: x[1])

    return {
        'total_entries': len(entries),
        'time_span': duration,
        'start_time': start_time,
        'end_time': end_time,
        'level_counts': level_counts,
        'peak_hour': f"{peak_hour[0]:02d}:00 ({peak_hour[1]} entries)",
        'entries_per_minute': len(entries) / max(duration.total_minutes(), 1)
    }

# Example usage
sample_logs = [
    "2024-01-15 14:30:45 [INFO] Application started",
    "2024-01-15 14:30:46 [INFO] Database connected",
    "2024-01-15 14:31:15 [WARNING] High memory usage",
    "2024-01-15 14:31:45 [ERROR] Database timeout",
    "2024-01-15 14:32:00 [INFO] Retry successful",
]

parsed_entries = parse_log_entries(sample_logs)
analysis = analyze_logs(parsed_entries)

print("Log Analysis:")
for key, value in analysis.items():
    print(f"  {key}: {value}")
```

### Time Series Data

```python
from carbonic import DateTime, Duration
from typing import List, Tuple

class TimeSeriesData:
    def __init__(self):
        self.data: List[Tuple[DateTime, float]] = []

    def add_point(self, timestamp: DateTime, value: float):
        """Add a data point."""
        self.data.append((timestamp, value))
        # Keep sorted by timestamp
        self.data.sort(key=lambda x: x[0])

    def get_range(self, start: DateTime, end: DateTime) -> List[Tuple[DateTime, float]]:
        """Get data points within a time range."""
        return [(ts, val) for ts, val in self.data if start <= ts <= end]

    def resample_hourly(self) -> List[Tuple[DateTime, float]]:
        """Resample data to hourly averages."""
        if not self.data:
            return []

        hourly_data = {}

        for timestamp, value in self.data:
            # Round down to the hour
            hour_key = timestamp.set_minute(0).set_second(0).set_microsecond(0)

            if hour_key not in hourly_data:
                hourly_data[hour_key] = []
            hourly_data[hour_key].append(value)

        # Calculate averages
        result = []
        for hour, values in sorted(hourly_data.items()):
            avg_value = sum(values) / len(values)
            result.append((hour, avg_value))

        return result

    def find_peaks(self, threshold: float) -> List[Tuple[DateTime, float]]:
        """Find values above threshold."""
        return [(ts, val) for ts, val in self.data if val > threshold]

# Example usage
ts_data = TimeSeriesData()

# Simulate adding temperature readings
base_time = DateTime(2024, 1, 15, 10, 0, tz="UTC")
for i in range(24):  # 24 hours of data
    timestamp = base_time.add_hours(i)
    # Simulate temperature variation
    temperature = 20 + 5 * (i % 12) / 12  # Varies between 20-25°C
    ts_data.add_point(timestamp, temperature)

# Analysis
hourly_avg = ts_data.resample_hourly()
peaks = ts_data.find_peaks(23.0)

print(f"Total data points: {len(ts_data.data)}")
print(f"Hourly averages: {len(hourly_avg)}")
print(f"High temperature readings (>23°C): {len(peaks)}")

if peaks:
    print("Peak temperatures:")
    for timestamp, temp in peaks[:3]:  # Show first 3
        print(f"  {timestamp.format('H:i')}: {temp:.1f}°C")
```

## File and System Operations

### Log Rotation

```python
from carbonic import DateTime, Duration
import os
from pathlib import Path

class LogRotator:
    def __init__(self, log_dir: str, max_age_days: int = 30):
        self.log_dir = Path(log_dir)
        self.max_age = Duration(days=max_age_days)

    def rotate_logs(self):
        """Remove old log files."""
        if not self.log_dir.exists():
            return

        cutoff_time = DateTime.now() - self.max_age
        removed_files = []

        for log_file in self.log_dir.glob("*.log"):
            # Get file modification time
            mtime = log_file.stat().st_mtime
            file_datetime = DateTime.from_timestamp(mtime)

            if file_datetime < cutoff_time:
                log_file.unlink()  # Delete file
                removed_files.append(str(log_file))

        return removed_files

    def archive_logs(self, archive_pattern: str = "archive_{Y}-{m}"):
        """Archive logs by month."""
        if not self.log_dir.exists():
            return

        # Group files by month
        monthly_groups = {}

        for log_file in self.log_dir.glob("*.log"):
            mtime = log_file.stat().st_mtime
            file_datetime = DateTime.from_timestamp(mtime)

            # Create month key
            month_key = file_datetime.format("Y-m")

            if month_key not in monthly_groups:
                monthly_groups[month_key] = []
            monthly_groups[month_key].append(log_file)

        # Create archives
        for month_key, files in monthly_groups.items():
            archive_name = archive_pattern.format(
                Y=month_key[:4],
                m=month_key[5:]
            )
            archive_dir = self.log_dir / archive_name
            archive_dir.mkdir(exist_ok=True)

            for file_path in files:
                # Move file to archive directory
                new_path = archive_dir / file_path.name
                file_path.rename(new_path)

# Example usage (mock - doesn't actually create files)
rotator = LogRotator("/var/log/myapp", max_age_days=7)
print("Log rotation would remove files older than 7 days")
```

### Backup Scheduling

```python
from carbonic import DateTime, Duration, Period

class BackupScheduler:
    def __init__(self):
        self.schedules = []

    def add_daily_backup(self, hour: int = 2):
        """Schedule daily backup at specific hour."""
        next_backup = DateTime.now().add_days(1).set_hour(hour).set_minute(0).set_second(0)
        self.schedules.append({
            'type': 'daily',
            'next_run': next_backup,
            'description': f"Daily backup at {hour:02d}:00"
        })

    def add_weekly_backup(self, weekday: Period, hour: int = 1):
        """Schedule weekly backup on specific weekday."""
        now = DateTime.now()
        next_backup = now.next(weekday).set_hour(hour).set_minute(0).set_second(0)

        # If it's the same day but time has passed, move to next week
        if next_backup <= now:
            next_backup = next_backup.add_weeks(1)

        self.schedules.append({
            'type': 'weekly',
            'next_run': next_backup,
            'description': f"Weekly backup on {weekday.name.title()} at {hour:02d}:00"
        })

    def get_next_backup(self):
        """Get the next scheduled backup."""
        if not self.schedules:
            return None

        return min(self.schedules, key=lambda x: x['next_run'])

    def update_schedule(self):
        """Update completed backups to next occurrence."""
        now = DateTime.now()

        for schedule in self.schedules:
            if schedule['next_run'] <= now:
                if schedule['type'] == 'daily':
                    schedule['next_run'] = schedule['next_run'].add_days(1)
                elif schedule['type'] == 'weekly':
                    schedule['next_run'] = schedule['next_run'].add_weeks(1)

# Example usage
scheduler = BackupScheduler()
scheduler.add_daily_backup(hour=2)  # 2 AM daily
scheduler.add_weekly_backup(Period.SUNDAY, hour=1)  # 1 AM Sunday

next_backup = scheduler.get_next_backup()
if next_backup:
    time_until = next_backup['next_run'] - DateTime.now()
    print(f"Next backup: {next_backup['description']}")
    print(f"Time until backup: {time_until.total_hours():.1f} hours")
```

## Performance Monitoring

### Execution Time Measurement

```python
from carbonic import DateTime, Duration
from contextlib import contextmanager
from typing import Dict, List

class PerformanceMonitor:
    def __init__(self):
        self.measurements: Dict[str, List[Duration]] = {}

    @contextmanager
    def measure(self, operation_name: str):
        """Context manager to measure operation duration."""
        start_time = DateTime.now()
        try:
            yield
        finally:
            end_time = DateTime.now()
            duration = end_time - start_time

            if operation_name not in self.measurements:
                self.measurements[operation_name] = []
            self.measurements[operation_name].append(duration)

    def get_stats(self, operation_name: str) -> Dict:
        """Get statistics for an operation."""
        if operation_name not in self.measurements:
            return {}

        durations = self.measurements[operation_name]
        total_seconds = [d.total_seconds() for d in durations]

        return {
            'count': len(durations),
            'total_time': sum(total_seconds),
            'average_time': sum(total_seconds) / len(total_seconds),
            'min_time': min(total_seconds),
            'max_time': max(total_seconds),
        }

    def report(self):
        """Generate performance report."""
        print("Performance Report:")
        print("-" * 50)

        for operation, _ in self.measurements.items():
            stats = self.get_stats(operation)
            print(f"\n{operation}:")
            print(f"  Executions: {stats['count']}")
            print(f"  Average: {stats['average_time']:.3f}s")
            print(f"  Min: {stats['min_time']:.3f}s")
            print(f"  Max: {stats['max_time']:.3f}s")
            print(f"  Total: {stats['total_time']:.3f}s")

# Example usage
monitor = PerformanceMonitor()

# Simulate monitoring different operations
import time

with monitor.measure("database_query"):
    time.sleep(0.1)  # Simulate database query

with monitor.measure("api_call"):
    time.sleep(0.05)  # Simulate API call

with monitor.measure("database_query"):
    time.sleep(0.12)  # Another database query

monitor.report()
```

These examples demonstrate practical applications of Carbonic for real-world datetime manipulation tasks. Each example is self-contained and can be adapted to your specific needs.