from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Duration:
    # Core storage - aligned with datetime.timedelta
    _days: int
    _seconds: int
    _microseconds: int

    # Calendar components stored separately for display/parsing only
    _calendar_months: int = 0
    _calendar_years: int = 0

    def __init__(
        self,
        *,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        weeks=0,
        months=0,
        years=0,
    ):
        """Create a Duration from individual time components."""
        # Convert time components to basic units (timedelta-compatible)
        # Keep calendar components (months/years) separate for now
        total_days = days + (weeks * 7)
        total_seconds = seconds + (minutes * 60) + (hours * 3600)
        total_microseconds = microseconds + (milliseconds * 1000)

        # Normalize microseconds and seconds overflow like timedelta does
        if total_microseconds >= 1_000_000:
            extra_seconds = total_microseconds // 1_000_000
            total_seconds += extra_seconds
            total_microseconds = total_microseconds % 1_000_000
        elif total_microseconds < 0:
            # Handle negative microseconds
            borrowed_seconds = (-total_microseconds - 1) // 1_000_000 + 1
            total_seconds -= borrowed_seconds
            total_microseconds += borrowed_seconds * 1_000_000

        # Normalize seconds overflow like timedelta does
        if total_seconds >= 86400:
            extra_days = total_seconds // 86400
            total_days += extra_days
            total_seconds = total_seconds % 86400
        elif total_seconds < 0:
            # Handle negative seconds
            borrowed_days = (-total_seconds - 1) // 86400 + 1
            total_days -= borrowed_days
            total_seconds += borrowed_days * 86400

        object.__setattr__(self, "_days", total_days)
        object.__setattr__(self, "_seconds", total_seconds)
        object.__setattr__(self, "_microseconds", total_microseconds)
        object.__setattr__(self, "_calendar_months", months)
        object.__setattr__(self, "_calendar_years", years)

    # Properties
    @property
    def days(self) -> int:
        return self._days

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def microseconds(self) -> int:
        return self._microseconds

    @property
    def milliseconds(self) -> int:
        """Get milliseconds component."""
        return self._microseconds // 1000

    @property
    def hours(self) -> int:
        """Get total hours for this duration (excluding calendar components)."""
        return int(self.total_seconds() // 3600)

    @property
    def weeks(self) -> int:
        """Get total weeks for this duration."""
        return self._days // 7

    @property
    def months(self) -> int:
        """Get calendar months component (for display purposes only)."""
        return self._calendar_months

    @property
    def years(self) -> int:
        """Get calendar years component (for display purposes only)."""
        return self._calendar_years

    # Constructors
    @classmethod
    def parse(cls, s: str) -> Duration:
        """Parse ISO 8601 duration string or custom format."""
        raise NotImplementedError("Duration parsing not yet implemented")

    # Properties and operations
    def total_seconds(self) -> float:
        """Get total seconds for this duration (excluding calendar components)."""
        total = self.days * 86400 + self.seconds + (self.microseconds / 1_000_000)
        return total

    # Intuitive alias properties for total duration conversion
    @property
    def in_seconds(self) -> float:
        """Get total duration expressed as seconds (alias for total_seconds)."""
        return self.total_seconds()

    @property
    def in_minutes(self) -> float:
        """Get total duration expressed as minutes."""
        return self.total_seconds() / 60

    @property
    def in_hours(self) -> float:
        """Get total duration expressed as hours."""
        return self.total_seconds() / 3600

    @property
    def in_days(self) -> float:
        """Get total duration expressed as days."""
        return self.total_seconds() / 86400

    @property
    def in_weeks(self) -> float:
        """Get total duration expressed as weeks."""
        return self.in_days / 7

    @property
    def in_milliseconds(self) -> float:
        """Get total duration expressed as milliseconds."""
        return self.total_seconds() * 1000

    @property
    def in_microseconds(self) -> float:
        """Get total duration expressed as microseconds."""
        return self.total_seconds() * 1_000_000

    def __str__(self) -> str:
        """Return human-readable string representation."""
        parts = []

        # Show calendar components if they were provided in constructor
        if self._calendar_years:
            parts.append(f"{self._calendar_years} year{'s' if self._calendar_years != 1 else ''}")
        if self._calendar_months:
            parts.append(f"{self._calendar_months} month{'s' if self._calendar_months != 1 else ''}")

        # Show actual time-based components
        if self.days:
            parts.append(f"{self.days} day{'s' if self.days != 1 else ''}")

        # Convert seconds to hours, minutes, seconds for display
        if self.seconds or self.microseconds:
            hours, remainder = divmod(self.seconds, 3600)
            minutes, secs = divmod(remainder, 60)

            if hours:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes:
                parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if secs or self.microseconds:
                if self.microseconds:
                    total_secs = secs + (self.microseconds / 1_000_000)
                    parts.append(f"{total_secs} seconds")
                else:
                    parts.append(f"{secs} second{'s' if secs != 1 else ''}")

        if not parts:
            return "0 seconds"

        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        else:
            return ", ".join(parts[:-1]) + f", and {parts[-1]}"

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"Duration(days={self.days}, seconds={self.seconds}, microseconds={self.microseconds}, months={self.months}, years={self.years})"

    # Comparison methods
    def _normalize_for_comparison(self) -> tuple[float, int, int]:
        """Normalize duration for comparison purposes."""
        # Return (total_seconds, total_months, total_years) for comparison
        # Note: Calendar components are already converted to approximate days in storage
        total_months = self._calendar_months + (self._calendar_years * 12)
        return (self.total_seconds(), total_months, 0)

    def __eq__(self, other: object) -> bool:
        """Check equality with another Duration."""
        if not isinstance(other, Duration):
            return False
        return self._normalize_for_comparison() == other._normalize_for_comparison()

    def __lt__(self, other: Duration) -> bool:
        """Check if this duration is less than another."""
        if not isinstance(other, Duration):
            return NotImplemented
        return self._normalize_for_comparison() < other._normalize_for_comparison()

    def __le__(self, other: Duration) -> bool:
        """Check if this duration is less than or equal to another."""
        if not isinstance(other, Duration):
            return NotImplemented
        return self._normalize_for_comparison() <= other._normalize_for_comparison()

    def __gt__(self, other: Duration) -> bool:
        """Check if this duration is greater than another."""
        if not isinstance(other, Duration):
            return NotImplemented
        return self._normalize_for_comparison() > other._normalize_for_comparison()

    def __ge__(self, other: Duration) -> bool:
        """Check if this duration is greater than or equal to another."""
        if not isinstance(other, Duration):
            return NotImplemented
        return self._normalize_for_comparison() >= other._normalize_for_comparison()

    def __hash__(self) -> int:
        """Return hash for use in sets and dicts."""
        # Hash based on normalized values for consistency with equality
        normalized = self._normalize_for_comparison()
        return hash(normalized)

    # Arithmetic operations
    def __add__(self, other: Duration) -> Duration:
        """Add two Duration objects."""
        if not isinstance(other, Duration):
            return NotImplemented

        # Add calendar components separately
        total_calendar_months = self._calendar_months + other._calendar_months
        total_calendar_years = self._calendar_years + other._calendar_years

        # Handle month overflow in calendar components
        if total_calendar_months >= 12:
            extra_years = total_calendar_months // 12
            total_calendar_years += extra_years
            total_calendar_months = total_calendar_months % 12

        # Add time-based components (already normalized like timedelta)
        total_days = self.days + other.days
        total_seconds = self.seconds + other.seconds
        total_microseconds = self.microseconds + other.microseconds

        # Handle overflow like timedelta does
        if total_microseconds >= 1_000_000:
            extra_seconds = total_microseconds // 1_000_000
            total_seconds += extra_seconds
            total_microseconds = total_microseconds % 1_000_000
        elif total_microseconds < 0:
            borrowed_seconds = (-total_microseconds - 1) // 1_000_000 + 1
            total_seconds -= borrowed_seconds
            total_microseconds += borrowed_seconds * 1_000_000

        if total_seconds >= 86400:
            extra_days = total_seconds // 86400
            total_days += extra_days
            total_seconds = total_seconds % 86400
        elif total_seconds < 0:
            borrowed_days = (-total_seconds - 1) // 86400 + 1
            total_days -= borrowed_days
            total_seconds += borrowed_days * 86400

        return Duration(
            days=total_days,
            seconds=total_seconds,
            microseconds=total_microseconds,
            months=total_calendar_months,
            years=total_calendar_years,
        )

    def __sub__(self, other: Duration) -> Duration:
        """Subtract another Duration from this one."""
        if not isinstance(other, Duration):
            return NotImplemented

        # Add the negation
        return self + (-other)

    def __neg__(self) -> Duration:
        """Return the negation of this Duration."""
        # Create Duration directly without going through constructor normalization
        # to avoid negative seconds affecting days count
        new_duration = object.__new__(Duration)
        object.__setattr__(new_duration, "_days", -self._days)
        object.__setattr__(new_duration, "_seconds", -self._seconds)
        object.__setattr__(new_duration, "_microseconds", -self._microseconds)
        object.__setattr__(new_duration, "_calendar_months", -self._calendar_months)
        object.__setattr__(new_duration, "_calendar_years", -self._calendar_years)
        return new_duration

    def __mul__(self, k: int | float) -> Duration:
        """Multiply Duration by a number."""
        if not isinstance(k, (int, float)):
            return NotImplemented

        # Multiply time-based components (timedelta-compatible)
        total_days: int | float = self.days * k
        total_seconds: int | float = self.seconds * k
        total_microseconds: int | float = self.microseconds * k

        # Multiply calendar components separately
        total_calendar_months: int | float = self._calendar_months * k
        total_calendar_years: int | float = self._calendar_years * k

        # Handle fractional parts for float multiplication
        if isinstance(k, float):
            # Handle fractional calendar years -> months
            if total_calendar_years != int(total_calendar_years):
                fractional_years = total_calendar_years - int(total_calendar_years)
                total_calendar_months += fractional_years * 12
                total_calendar_years = int(total_calendar_years)

            # Handle fractional calendar months (keep as months, don't convert to days automatically)
            total_calendar_months = int(total_calendar_months)

            # Handle month overflow in calendar components
            if total_calendar_months >= 12:
                extra_years = int(total_calendar_months // 12)
                total_calendar_years += extra_years
                total_calendar_months = int(total_calendar_months % 12)

            # Handle fractional days -> seconds
            if total_days != int(total_days):
                fractional_days = total_days - int(total_days)
                total_seconds += fractional_days * 86400
                total_days = int(total_days)

            # Handle fractional seconds -> microseconds
            if total_seconds != int(total_seconds):
                fractional_seconds = total_seconds - int(total_seconds)
                total_microseconds += fractional_seconds * 1_000_000
                total_seconds = int(total_seconds)

            # Normalize overflow like timedelta
            if total_microseconds >= 1_000_000:
                extra_seconds = int(total_microseconds // 1_000_000)
                total_seconds += extra_seconds
                total_microseconds = int(total_microseconds % 1_000_000)
            else:
                total_microseconds = int(total_microseconds)

            if total_seconds >= 86400:
                extra_days = int(total_seconds // 86400)
                total_days += extra_days
                total_seconds = int(total_seconds % 86400)

            # Ensure all are integers
            total_days = int(total_days)
            total_seconds = int(total_seconds)
            total_calendar_years = int(total_calendar_years)
            total_calendar_months = int(total_calendar_months)

        else:
            # For integers, straightforward multiplication
            total_days = int(total_days)
            total_seconds = int(total_seconds)
            total_microseconds = int(total_microseconds)
            total_calendar_months = int(total_calendar_months)
            total_calendar_years = int(total_calendar_years)

        return Duration(
            days=total_days,
            seconds=total_seconds,
            microseconds=total_microseconds,
            months=total_calendar_months,
            years=total_calendar_years,
        )

    def __rmul__(self, k: int | float) -> Duration:
        """Right multiplication: k * duration."""
        return self * k

    def __abs__(self) -> Duration:
        """Return the absolute value of this Duration."""
        # Check if already positive
        total_seconds = self.total_seconds()
        if (total_seconds >= 0 and self._calendar_months >= 0 and self._calendar_years >= 0):
            return self

        # For negative durations, create positive version
        # Convert to absolute total seconds, then reconstruct
        abs_total_seconds = abs(total_seconds)
        abs_days = int(abs_total_seconds // 86400)
        abs_seconds = int(abs_total_seconds % 86400)
        abs_microseconds = abs(self._microseconds)

        # Create new duration directly to avoid normalization issues
        new_duration = object.__new__(Duration)
        object.__setattr__(new_duration, "_days", abs_days)
        object.__setattr__(new_duration, "_seconds", abs_seconds)
        object.__setattr__(new_duration, "_microseconds", abs_microseconds)
        object.__setattr__(new_duration, "_calendar_months", abs(self._calendar_months))
        object.__setattr__(new_duration, "_calendar_years", abs(self._calendar_years))
        return new_duration

    def humanize(self, *, max_units=2, locale: str | None = None) -> str:
        """Return human-readable duration string."""
        raise NotImplementedError("Duration humanization not yet implemented")
