"""Date implementation for Carbonic.

This module provides the core Date class with fluent API, immutability,
and comprehensive date manipulation capabilities.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import Literal, overload

from carbonic.core.duration import Duration
from carbonic.core.exceptions import ParseError


@dataclass(frozen=True, slots=True)
class Date:
    """Immutable date object with fluent API and comprehensive date operations.

    The Date class provides a modern, type-safe wrapper around Python's date
    with additional functionality for date manipulation and formatting.
    All operations return new instances, maintaining immutability.

    Attributes:
        _date: Internal datetime.date object storing the actual date value

    Examples:
        >>> date = Date(2024, 1, 15)
        >>> date.add(days=10).format("Y-m-d")
        '2024-01-25'

        >>> today = Date.today()  # doctest: +SKIP
        >>> today.start_of("month").format("F j, Y")  # doctest: +SKIP
        'January 1, 2024'
    """

    _date: datetime.date

    def __init__(self, year: int, month: int, day: int) -> None:
        """Initialize a new Date instance.

        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)
            day: Day of month (1-31)

        Raises:
            ValueError: If any date component is invalid
        """
        object.__setattr__(self, "_date", datetime.date(year, month, day))

    # Constructors
    @classmethod
    def today(cls, tz: str | None = None) -> Date:
        """Create a Date instance for today."""
        today_date = datetime.date.today()
        return cls(today_date.year, today_date.month, today_date.day)

    @classmethod
    def tomorrow(cls) -> Date:
        """Get tomorrow's date.

        Returns:
            Date object representing tomorrow
        """
        return cls.today().add(days=1)

    @classmethod
    def yesterday(cls) -> Date:
        """Get yesterday's date.

        Returns:
            Date object representing yesterday
        """
        return cls.today().add(days=-1)

    @classmethod
    def next(cls, unit: str, count: int = 1) -> Date:
        """Get a date in the future relative to today.

        Args:
            unit: Time unit ("day", "week", "month", "quarter", "year")
            count: Number of units to add (default: 1)

        Returns:
            Date object in the future

        Examples:
            >>> Date.next("day")      # Tomorrow  # doctest: +SKIP
            >>> Date.next("week", 2)  # 2 weeks from today  # doctest: +SKIP
            >>> Date.next("month")    # Next month  # doctest: +SKIP
        """
        today = cls.today()
        return cls._add_relative_unit(today, unit, count)

    @classmethod
    def previous(cls, unit: str, count: int = 1) -> Date:
        """Get a date in the past relative to today.

        Args:
            unit: Time unit ("day", "week", "month", "quarter", "year")
            count: Number of units to subtract (default: 1)

        Returns:
            Date object in the past

        Examples:
            >>> Date.previous("day")      # Yesterday  # doctest: +SKIP
            >>> Date.previous("week", 2)  # 2 weeks ago  # doctest: +SKIP
            >>> Date.previous("month")    # Last month  # doctest: +SKIP
        """
        today = cls.today()
        return cls._add_relative_unit(today, unit, -count)

    @classmethod
    def _add_relative_unit(cls, date: Date, unit: str, count: int) -> Date:
        """Add relative time units to a date."""
        if unit == "day":
            return date.add(days=count)
        elif unit == "week":
            return date.add(days=count * 7)
        elif unit == "month":
            return date.add(months=count)
        elif unit == "quarter":
            return date.add(months=count * 3)
        elif unit == "year":
            return date.add(years=count)
        else:
            raise ValueError(
                f"Unsupported time unit for Date: {unit}. Use 'day', 'week', 'month', 'quarter', or 'year'."
            )

    @classmethod
    def parse(cls, s: str, fmt: str | None = None) -> Date:
        """Parse a date string into a Date object.

        Args:
            s: The date string to parse. Supports:
                - ISO date formats (2024-01-15)
                - Custom formats when fmt is provided
            fmt: Optional format string. If None, auto-detect format.
                Supports both strftime (%Y-%m-%d) and Carbon (Y-m-d) formats.

        Returns:
            Date object

        Raises:
            ParseError: If the string cannot be parsed

        Examples:
            >>> Date.parse("2024-01-15")  # doctest: +SKIP
        """
        if not s or not s.strip():
            raise ParseError("Empty date string")

        s = s.strip()

        if fmt is None:
            return cls._auto_parse(s)
        else:
            return cls._parse_with_format(s, fmt)

    @classmethod
    def _auto_parse(cls, s: str) -> Date:
        """Auto-detect format and parse date string."""

        # First try exact ISO format
        iso_pattern = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
        match = iso_pattern.match(s)
        if match:
            try:
                year, month, day = map(int, match.groups())
                return cls(year, month, day)
            except ValueError as e:
                raise ParseError(f"Invalid date: {s}") from e

        # Try slash formats with heuristics
        slash_pattern = re.compile(r"^(\d{1,4})/(\d{1,2})/(\d{2,4})$")
        match = slash_pattern.match(s)
        if match:
            part1, part2, part3 = map(int, match.groups())

            # Heuristic: if first part > 31, it's likely year
            if part1 > 31:
                # YYYY/MM/DD format
                year, month, day = part1, part2, part3
            elif part3 > 31:
                # Ambiguous MM/DD/YYYY vs DD/MM/YYYY
                # Default to US format (MM/DD/YYYY) unless day > 12
                if part1 > 12:
                    # Must be DD/MM/YYYY
                    day, month, year = part1, part2, part3
                else:
                    # Could be either, default to US MM/DD/YYYY
                    month, day, year = part1, part2, part3
            else:
                raise ParseError(f"Ambiguous date format: {s}")

            try:
                return cls(year, month, day)
            except ValueError as e:
                raise ParseError(f"Invalid date: {s}") from e

        # Try dot format (European style)
        dot_pattern = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$")
        match = dot_pattern.match(s)
        if match:
            try:
                day, month, year = map(int, match.groups())
                return cls(year, month, day)
            except ValueError as e:
                raise ParseError(f"Invalid date: {s}") from e

        raise ParseError(f"Unable to parse date: {s}")

    @classmethod
    def _parse_with_format(cls, s: str, fmt: str) -> Date:
        """Parse date string with explicit format."""
        try:
            # Convert Carbon-style tokens to strftime if needed
            strftime_fmt = cls._carbon_to_strftime(fmt)

            # Validate that format contains required date components
            has_year = any(token in strftime_fmt for token in ["%Y", "%y"])
            has_month = any(token in strftime_fmt for token in ["%m", "%b", "%B"])
            has_day = any(token in strftime_fmt for token in ["%d", "%j"])

            if not (has_year and has_month and has_day):
                raise ParseError(f"Format must include year, month, and day: {fmt}")

            # Parse using strftime
            parsed = datetime.datetime.strptime(s, strftime_fmt)
            parsed_date = parsed.date()
            return cls(parsed_date.year, parsed_date.month, parsed_date.day)

        except ValueError as e:
            raise ParseError(f"Failed to parse '{s}' with format '{fmt}': {e}") from e

    @staticmethod
    def _carbon_to_strftime(fmt: str) -> str:
        """Convert Carbon-style format tokens to strftime format."""
        # Common Carbon to strftime mappings
        mappings = {
            "Y": "%Y",  # 4-digit year
            "y": "%y",  # 2-digit year
            "m": "%m",  # Month with leading zero
            "n": "%m",  # Month without leading zero (strftime %m handles both)
            "d": "%d",  # Day with leading zero
            "j": "%d",  # Day without leading zero (strftime %d handles both)
            "M": "%b",  # Short month name (Jan)
            "F": "%B",  # Full month name (January)
        }

        # If format contains strftime tokens (%), return as-is
        if "%" in fmt:
            return fmt

        # Convert Carbon tokens
        result = fmt
        for carbon_token, strftime_token in mappings.items():
            result = result.replace(carbon_token, strftime_token)

        return result

    @classmethod
    def from_date(cls, d: datetime.date) -> Date:
        """Create a Date instance from datetime.date."""
        return cls(d.year, d.month, d.day)

    # Properties
    @property
    def year(self) -> int:
        return self._date.year

    @property
    def month(self) -> int:
        return self._date.month

    @property
    def day(self) -> int:
        return self._date.day

    def weekday(self) -> int:
        """Return day of week where Monday=0, Sunday=6 (datetime.date compatibility)."""
        return self._date.weekday()

    def isoweekday(self) -> int:
        """ISO weekday where Monday=1, Sunday=7 (datetime.date compatibility)."""
        return self._date.isoweekday()

    def isoformat(self) -> str:
        """Return ISO 8601 format string (YYYY-MM-DD) for datetime.date compatibility."""
        return self._date.isoformat()

    def isocalendar(self) -> tuple[int, int, int]:
        """Return (year, week, weekday) tuple for datetime.date compatibility."""
        return self._date.isocalendar()

    def timetuple(self):
        """Return time.struct_time for datetime.date compatibility."""
        return self._date.timetuple()

    def toordinal(self) -> int:
        """Return proleptic Gregorian ordinal for datetime.date compatibility."""
        return self._date.toordinal()

    def replace(self, year: int | None = None, month: int | None = None, day: int | None = None) -> Date:
        """Return a Date with one or more components replaced (datetime.date compatibility)."""
        return Date(
            year if year is not None else self.year,
            month if month is not None else self.month,
            day if day is not None else self.day,
        )

    @property
    def iso_week(self) -> tuple[int, int]:
        """Return (year, week) tuple."""
        return self._date.isocalendar()[:2]

    # Comparison methods
    def __eq__(self, other: object) -> bool:
        """Check equality with another Date or datetime.date."""
        if isinstance(other, Date):
            return self._date == other._date
        if isinstance(other, datetime.date):
            return self._date == other
        return False

    def __lt__(self, other: object) -> bool:
        """Check if this date is less than another."""
        if isinstance(other, Date):
            return self._date < other._date
        if isinstance(other, datetime.date):
            return self._date < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """Check if this date is less than or equal to another."""
        if isinstance(other, Date):
            return self._date <= other._date
        if isinstance(other, datetime.date):
            return self._date <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        """Check if this date is greater than another."""
        if isinstance(other, Date):
            return self._date > other._date
        if isinstance(other, datetime.date):
            return self._date > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        """Check if this date is greater than or equal to another."""
        if isinstance(other, Date):
            return self._date >= other._date
        if isinstance(other, datetime.date):
            return self._date >= other
        return NotImplemented

    def __hash__(self) -> int:
        """Return hash of the date for use in sets and dicts."""
        return hash(self._date)

    def __str__(self) -> str:
        """Return ISO format string representation."""
        return self._date.isoformat()

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"Date({self.year}, {self.month}, {self.day})"

    def __format__(self, format_spec: str) -> str:
        """Support for Python's format() function and f-strings."""
        if not format_spec:
            return str(self)
        return self.strftime(format_spec)

    # Operations
    def add(self, *, years: int = 0, months: int = 0, days: int = 0) -> Date:
        """Add years, months, and/or days to this date."""
        # Start with the current date
        new_date = self._date

        # Add days first (simplest)
        if days:
            new_date = new_date + datetime.timedelta(days=days)

        # Add months and years (more complex due to variable month lengths)
        if months or years:
            # Calculate new year and month
            total_months = new_date.month + months + (years * 12)
            new_year = new_date.year + (total_months - 1) // 12
            new_month = ((total_months - 1) % 12) + 1

            # Handle day overflow (e.g., Jan 31 + 1 month -> Feb 28/29)
            new_day = min(new_date.day, self._last_day_of_month(new_year, new_month))

            new_date = datetime.date(new_year, new_month, new_day)

        return Date(new_date.year, new_date.month, new_date.day)

    def subtract(self, *, years: int = 0, months: int = 0, days: int = 0) -> Date:
        """Subtract years, months, and/or days from this date."""
        return self.add(years=-years, months=-months, days=-days)

    @staticmethod
    def _last_day_of_month(year: int, month: int) -> int:
        """Get the last day of the given month/year."""
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        last_day = next_month - datetime.timedelta(days=1)
        return last_day.day

    def diff(self, other: Date, *, absolute: bool = False) -> Duration:
        """Calculate difference between this date and another date.

        Args:
            other: The other date to compare with
            absolute: If True, return absolute difference (always positive)

        Returns:
            Duration representing the difference
        """

        # Calculate difference in days
        delta = self._date - other._date
        days_diff = delta.days

        if absolute:
            days_diff = abs(days_diff)

        return Duration(days=days_diff)

    def add_duration(self, duration: Duration) -> Date:
        """Add a Duration to this Date.

        Args:
            duration: The Duration to add

        Returns:
            New Date with the duration added
        """

        # Calculate total days from time components (seconds become fractional days)
        time_days = (
            duration.storage_seconds + duration.microseconds / 1_000_000
        ) / 86400

        # Add all components
        total_days = duration.days + int(time_days)
        return self.add(
            years=duration.years,
            months=duration.months,
            days=total_days,
        )

    def subtract_duration(self, duration: Duration) -> Date:
        """Subtract a Duration from this Date.

        Args:
            duration: The Duration to subtract

        Returns:
            New Date with the duration subtracted
        """

        # Use negation and add
        return self.add_duration(-duration)

    def __add__(self, other: Duration) -> Date:
        """Add a Duration to this Date using + operator."""
        if hasattr(other, "days"):  # Duck typing for Duration-like objects
            return self.add_duration(other)
        return NotImplemented

    @overload
    def __sub__(self, other: Duration) -> Date: ...

    @overload
    def __sub__(self, other: Date) -> Duration: ...

    def __sub__(self, other: Duration | Date) -> Date | Duration:
        """Subtract a Duration or Date from this Date using - operator.

        Args:
            other: Duration to subtract (returns Date) or Date to diff with (returns Duration)

        Returns:
            Date if subtracting Duration, Duration if subtracting Date
        """
        if isinstance(other, Date):
            return self.diff(other)
        elif hasattr(other, "days"):  # Duck typing for Duration-like objects
            return self.subtract_duration(other)
        return NotImplemented

    # Anchors
    def start_of(
        self, unit: Literal["day", "month", "year", "quarter", "week"]
    ) -> Date:
        """Return the start of the specified time period."""
        if unit == "day":
            return self
        elif unit == "week":
            # Monday = 0, so subtract weekday to get to Monday
            days_to_subtract = self.weekday()
            return self.subtract(days=days_to_subtract)
        elif unit == "month":
            return Date(self.year, self.month, 1)
        elif unit == "quarter":
            # Calculate quarter start month
            quarter_start_month = ((self.month - 1) // 3) * 3 + 1
            return Date(self.year, quarter_start_month, 1)
        elif unit == "year":
            return Date(self.year, 1, 1)
        else:
            raise ValueError(f"Unknown unit: {unit}")

    def end_of(self, unit: Literal["day", "month", "year", "quarter", "week"]) -> Date:
        """Return the end of the specified time period."""
        if unit == "day":
            return self
        elif unit == "week":
            # Sunday = 6, so add days to get to Sunday
            days_to_add = 6 - self.weekday()
            return self.add(days=days_to_add)
        elif unit == "month":
            # Get last day of current month
            last_day = self._last_day_of_month(self.year, self.month)
            return Date(self.year, self.month, last_day)
        elif unit == "quarter":
            # Calculate quarter end month
            quarter_start_month = ((self.month - 1) // 3) * 3 + 1
            quarter_end_month = quarter_start_month + 2
            last_day = self._last_day_of_month(self.year, quarter_end_month)
            return Date(self.year, quarter_end_month, last_day)
        elif unit == "year":
            return Date(self.year, 12, 31)
        else:
            raise ValueError(f"Unknown unit: {unit}")

    # Business day operations
    def is_weekday(self) -> bool:
        """Return True if this date is a weekday (Monday-Friday)."""
        return self.weekday() < 5  # Monday=0, Tuesday=1, ..., Friday=4

    def is_weekend(self) -> bool:
        """Return True if this date is a weekend (Saturday-Sunday)."""
        return self.weekday() >= 5  # Saturday=5, Sunday=6

    def add_business_days(self, days: int) -> Date:
        """Add business days to this date, skipping weekends.

        Args:
            days: Number of business days to add (can be negative)

        Returns:
            New Date with business days added

        Examples:
            Date(2023, 12, 25).add_business_days(1)  # Monday -> Tuesday
            Date(2023, 12, 29).add_business_days(1)  # Friday -> Monday (skip weekend)
        """

        if days < 0:
            return self.subtract_business_days(-days)

        if days == 0:
            # If we're on a weekend, move to next business day
            if self.is_weekend():
                # Move to Monday
                days_to_monday = 1 if self.weekday() == 6 else 2  # Sunday->1, Saturday->2
                return self.add(days=days_to_monday)
            else:
                return self

        current_date = self
        remaining_days = days

        # If starting on weekend, first move to Monday (this counts as adding business days)
        if current_date.is_weekend():
            days_to_monday = (
                1 if current_date.weekday() == 6 else 2
            )  # Sunday->1, Saturday->2
            current_date = current_date.add(days=days_to_monday)
            remaining_days -= 1  # Moving to Monday counts as 1 business day

        # Add complete weeks (5 business days = 7 calendar days)
        complete_weeks = remaining_days // 5
        if complete_weeks > 0:
            current_date = current_date.add(days=complete_weeks * 7)
            remaining_days = remaining_days % 5

        # Add remaining days one by one, skipping weekends
        for _ in range(remaining_days):
            current_date = current_date.add(days=1)
            # If we land on Saturday, skip to Monday
            if current_date.weekday() == 5:  # Saturday
                current_date = current_date.add(days=2)

        return current_date

    def subtract_business_days(self, days: int) -> Date:
        """Subtract business days from this date, skipping weekends.

        Args:
            days: Number of business days to subtract (can be negative)

        Returns:
            New Date with business days subtracted

        Examples:
            Date(2023, 12, 26).subtract_business_days(1)  # Tuesday -> Monday
            Date(2024, 1, 1).subtract_business_days(1)    # Monday -> Friday (skip weekend)
        """

        if days < 0:
            return self.add_business_days(-days)

        if days == 0:
            # If we're on a weekend, move to previous business day
            if self.is_weekend():
                # Move to Friday
                days_to_friday = 1 if self.weekday() == 5 else 2  # Saturday->1, Sunday->2
                return self.subtract(days=days_to_friday)
            else:
                return self

        current_date = self
        remaining_days = days

        # If starting on weekend, first move to Friday (this counts as subtracting business days)
        if current_date.is_weekend():
            days_to_friday = (
                1 if current_date.weekday() == 5 else 2
            )  # Saturday->1, Sunday->2
            current_date = current_date.subtract(days=days_to_friday)
            remaining_days -= 1  # Moving to Friday counts as 1 business day

        # Subtract complete weeks (5 business days = 7 calendar days)
        complete_weeks = remaining_days // 5
        if complete_weeks > 0:
            current_date = current_date.subtract(days=complete_weeks * 7)
            remaining_days = remaining_days % 5

        # Subtract remaining days one by one, skipping weekends
        for _ in range(remaining_days):
            current_date = current_date.subtract(days=1)
            # If we land on Sunday, skip to Friday
            if current_date.weekday() == 6:  # Sunday
                current_date = current_date.subtract(days=2)

        return current_date

    # Interop
    def to_datetime(self, tz: str | None = "UTC") -> datetime.datetime:
        """Convert to datetime.datetime with timezone (default UTC)."""
        if tz is None:
            # Return naive datetime
            return datetime.datetime.combine(self._date, datetime.time())
        else:
            # Return timezone-aware datetime
            from zoneinfo import ZoneInfo

            tzinfo = ZoneInfo(tz)
            return datetime.datetime.combine(self._date, datetime.time(), tzinfo)

    def to_date(self) -> datetime.date:
        """Return a copy of the underlying datetime.date object."""
        return datetime.date(self._date.year, self._date.month, self._date.day)

    # Formatting methods
    def strftime(self, fmt: str) -> str:
        """Format date using strftime format string."""
        return self._date.strftime(fmt)

    def format(self, fmt: str, *, locale: str | None = None) -> str:
        """Format date using Carbon-style format string.

        Uses Carbon-style tokens for flexible date formatting. Escape characters
        with backslash (\\) to include them literally.

        ## Format Tokens

        | Token | Description | Example |
        |-------|-------------|---------|
        | `Y` | 4-digit year | `2024` |
        | `y` | 2-digit year | `24` |
        | `m` | Month with leading zero | `01`, `12` |
        | `n` | Month without leading zero | `1`, `12` |
        | `d` | Day with leading zero | `01`, `31` |
        | `j` | Day without leading zero | `1`, `31` |
        | `S` | Ordinal suffix | `st`, `nd`, `rd`, `th` |
        | `F` | Full month name (localized) | `January`, `enero` |
        | `M` | Short month name (localized) | `Jan`, `ene` |
        | `l` | Full day name (localized) | `Monday`, `lunes` |
        | `D` | Short day name (localized) | `Mon`, `lun` |

        Args:
            fmt: Carbon-style format string with tokens above
            locale: Locale code for localized month/day names (default: English)
                  Supported: en, pl, es, fr, de, pt

        Returns:
            Formatted date string

        Examples:
            >>> date = Date(2024, 1, 15)
            >>> date.format("Y-m-d")
            '2024-01-15'
            >>> date.format("l, F j, Y")
            'Monday, January 15, 2024'
            >>> date.format("l, F j, Y", locale="es")  # doctest: +SKIP
            'lunes, enero 15, 2024'
            >>> date.format("jS \\\\o\\\\f F Y")
            '15th of January 2024'
        """
        return self._carbon_format(fmt, locale=locale)

    def _carbon_format(self, fmt: str, *, locale: str | None = None) -> str:
        """Format date using Carbon-style tokens."""
        # Get locale instance
        from carbonic.locale import get_locale

        locale_obj = get_locale(locale)

        # Lazy evaluation cache for expensive operations
        _cache: dict[str, str] = {}

        # Carbon format token mappings
        mappings = {
            "Y": lambda: f"{self.year:04d}",  # 4-digit year
            "y": lambda: f"{self.year % 100:02d}",  # 2-digit year
            "m": lambda: f"{self.month:02d}",  # Month with leading zero
            "n": lambda: f"{self.month}",  # Month without leading zero
            "d": lambda: f"{self.day:02d}",  # Day with leading zero
            "j": lambda: f"{self.day}",  # Day without leading zero
            "S": lambda: self._ordinal_suffix(self.day),  # Ordinal suffix
            "F": lambda: _cache.setdefault(
                f"F_{locale or 'en'}_{self.month}",
                locale_obj.get_month_name(self.month, short=False),
            ),  # Full month name (cached)
            "M": lambda: _cache.setdefault(
                f"M_{locale or 'en'}_{self.month}",
                locale_obj.get_month_name(self.month, short=True),
            ),  # Short month name (cached)
            "l": lambda: _cache.setdefault(
                f"l_{locale or 'en'}_{self.weekday()}",
                locale_obj.get_day_name(self.weekday(), short=False),
            ),  # Full day name (cached)
            "D": lambda: _cache.setdefault(
                f"D_{locale or 'en'}_{self.weekday()}",
                locale_obj.get_day_name(self.weekday(), short=True),
            ),  # Short day name (cached)
        }

        result = ""
        i = 0
        while i < len(fmt):
            char = fmt[i]

            # Handle escaped characters
            if char == "\\" and i + 1 < len(fmt):
                result += fmt[i + 1]
                i += 2
                continue

            # Handle jS (day with ordinal suffix)
            if char == "j" and i + 1 < len(fmt) and fmt[i + 1] == "S":
                result += f"{self.day}{self._ordinal_suffix(self.day)}"
                i += 2
                continue

            # Handle regular Carbon tokens
            if char in mappings:
                result += mappings[char]()
            else:
                result += char

            i += 1

        return result

    @staticmethod
    def _ordinal_suffix(day: int) -> str:
        """Get ordinal suffix for a day (st, nd, rd, th)."""
        if 10 <= day % 100 <= 20:  # Special case: 11th, 12th, 13th
            return "th"
        else:
            return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    # Common format methods
    def to_iso_string(self) -> str:
        """Return ISO date string (YYYY-MM-DD)."""
        return self._date.isoformat()

    def to_datetime_string(self) -> str:
        """Return date with default time (YYYY-MM-DD 00:00:00)."""
        return f"{self._date.isoformat()} 00:00:00"
