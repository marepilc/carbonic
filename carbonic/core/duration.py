from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Duration:
    _days: int
    _seconds: int
    _microseconds: int
    _months: int = 0
    _years: int = 0

    def __init__(
        self,
        *,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        microseconds=0,
        weeks=0,
        months=0,
        years=0,
    ):
        """Create a Duration from individual time components."""
        # Convert all components to basic units
        total_days = days + (weeks * 7)
        total_seconds = seconds + (minutes * 60) + (hours * 3600)

        object.__setattr__(self, "_days", total_days)
        object.__setattr__(self, "_seconds", total_seconds)
        object.__setattr__(self, "_microseconds", microseconds)
        object.__setattr__(self, "_months", months)
        object.__setattr__(self, "_years", years)

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
    def months(self) -> int:
        return self._months

    @property
    def years(self) -> int:
        return self._years

    # Constructors
    @classmethod
    def parse(cls, s: str) -> Duration: ...  # ISO 8601 / token forms

    # Properties and operations
    def total_seconds(self) -> float:
        """Get total seconds for this duration (excluding calendar components)."""
        total = self.days * 86400 + self.seconds + (self.microseconds / 1_000_000)
        return total

    def __str__(self) -> str:
        """Return human-readable string representation."""
        parts = []

        if self.years:
            parts.append(f"{self.years} year{'s' if self.years != 1 else ''}")
        if self.months:
            parts.append(f"{self.months} month{'s' if self.months != 1 else ''}")
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
        total_months = self.months + (self.years * 12)
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

        # Add all components
        total_days = self.days + other.days
        total_seconds = self.seconds + other.seconds
        total_microseconds = self.microseconds + other.microseconds
        total_months = self.months + other.months
        total_years = self.years + other.years

        # Handle month overflow
        if total_months >= 12:
            extra_years = total_months // 12
            total_years += extra_years
            total_months = total_months % 12

        # Handle second/day overflow
        if total_seconds >= 86400:
            extra_days = total_seconds // 86400
            total_days += extra_days
            total_seconds = total_seconds % 86400

        # Handle microsecond overflow
        if total_microseconds >= 1_000_000:
            extra_seconds = total_microseconds // 1_000_000
            total_seconds += extra_seconds
            total_microseconds = total_microseconds % 1_000_000

            # Check again for second overflow after microsecond adjustment
            if total_seconds >= 86400:
                extra_days = total_seconds // 86400
                total_days += extra_days
                total_seconds = total_seconds % 86400

        return Duration(
            days=total_days,
            seconds=total_seconds,
            microseconds=total_microseconds,
            months=total_months,
            years=total_years,
        )

    def __sub__(self, other: Duration) -> Duration:
        """Subtract another Duration from this one."""
        if not isinstance(other, Duration):
            return NotImplemented

        # Add the negation
        return self + (-other)

    def __neg__(self) -> Duration:
        """Return the negation of this Duration."""
        return Duration(
            days=-self.days,
            seconds=-self.seconds,
            microseconds=-self.microseconds,
            months=-self.months,
            years=-self.years,
        )

    def __mul__(self, k: int | float) -> Duration:
        """Multiply Duration by a number."""
        if not isinstance(k, (int, float)):
            return NotImplemented

        # Multiply all components
        total_days: int | float = self.days * k
        total_seconds: int | float = self.seconds * k
        total_microseconds: int | float = self.microseconds * k
        total_months: int | float = self.months * k
        total_years: int | float = self.years * k

        # Convert fractional parts to appropriate units
        if isinstance(k, float):
            # Handle fractional months -> days (approximate: 1 month ≈ 30 days)
            if total_months != int(total_months):
                fractional_months = total_months - int(total_months)
                total_days += fractional_months * 30  # Approximate
                total_months = int(total_months)

            # Handle fractional years -> months
            if total_years != int(total_years):
                fractional_years = total_years - int(total_years)
                total_months += fractional_years * 12
                total_years = int(total_years)

            # Handle month overflow after fractional conversions
            if total_months >= 12:
                extra_years = int(total_months // 12)
                total_years += extra_years
                total_months = int(total_months % 12)
            elif total_months != int(total_months):
                total_months = int(total_months)

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

            # Handle microsecond overflow
            if total_microseconds >= 1_000_000:
                extra_seconds = int(total_microseconds // 1_000_000)
                total_seconds += extra_seconds
                total_microseconds = int(total_microseconds % 1_000_000)
            else:
                total_microseconds = int(total_microseconds)

            # Handle second/day overflow after all conversions
            if total_seconds >= 86400:
                extra_days = int(total_seconds // 86400)
                total_days += extra_days
                total_seconds = int(total_seconds % 86400)

            # Ensure final conversion to int
            total_days = int(total_days)
            total_seconds = int(total_seconds)
            total_years = int(total_years)

        else:
            # For integers, everything stays as integers
            total_days = int(total_days)
            total_seconds = int(total_seconds)
            total_microseconds = int(total_microseconds)
            total_months = int(total_months)
            total_years = int(total_years)

        # Ensure all values are integers for the constructor
        final_days: int = int(total_days)
        final_seconds: int = int(total_seconds)
        final_microseconds: int = int(total_microseconds)
        final_months: int = int(total_months)
        final_years: int = int(total_years)

        return Duration(
            days=final_days,
            seconds=final_seconds,
            microseconds=final_microseconds,
            months=final_months,
            years=final_years,
        )

    def __rmul__(self, k: int | float) -> Duration:
        """Right multiplication: k * duration."""
        return self * k

    def __abs__(self) -> Duration:
        """Return the absolute value of this Duration."""
        return Duration(
            days=abs(self.days),
            seconds=abs(self.seconds),
            microseconds=abs(self.microseconds),
            months=abs(self.months),
            years=abs(self.years),
        )

    def humanize(self, *, max_units=2, locale: str | None = None) -> str: ...
