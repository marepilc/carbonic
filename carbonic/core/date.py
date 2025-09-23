from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from carbonic import Duration

from carbonic.core.exceptions import ParseError


@dataclass(frozen=True, slots=True)
class Date:
    _date: datetime.date

    def __init__(self, year: int, month: int, day: int):
        object.__setattr__(self, "_date", datetime.date(year, month, day))

    # Constructors
    @classmethod
    def today(cls, tz: str | None = None) -> Date:
        """Create a Date instance for today."""
        today_date = datetime.date.today()
        return cls(today_date.year, today_date.month, today_date.day)

    @classmethod
    def parse(cls, s: str, fmt: str | None = None) -> Date:
        """Parse a date string into a Date object.

        Args:
            s: The date string to parse
            fmt: Optional format string. If None, auto-detect format.
                Supports both strftime (%Y-%m-%d) and Carbon (Y-m-d) formats.

        Returns:
            Date object

        Raises:
            ParseError: If the string cannot be parsed
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

    @property
    def weekday(self) -> int:
        """Monday=0, Sunday=6"""
        return self._date.weekday()

    @property
    def iso_week(self) -> tuple[int, int]:
        """Return (year, week) tuple."""
        return self._date.isocalendar()[:2]

    # Comparison methods
    def __eq__(self, other: object) -> bool:
        """Check equality with another Date."""
        if not isinstance(other, Date):
            return False
        return self._date == other._date

    def __lt__(self, other: Date) -> bool:
        """Check if this date is less than another."""
        if not isinstance(other, Date):
            return NotImplemented
        return self._date < other._date

    def __le__(self, other: Date) -> bool:
        """Check if this date is less than or equal to another."""
        if not isinstance(other, Date):
            return NotImplemented
        return self._date <= other._date

    def __gt__(self, other: Date) -> bool:
        """Check if this date is greater than another."""
        if not isinstance(other, Date):
            return NotImplemented
        return self._date > other._date

    def __ge__(self, other: Date) -> bool:
        """Check if this date is greater than or equal to another."""
        if not isinstance(other, Date):
            return NotImplemented
        return self._date >= other._date

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
    def add(self, *, years=0, months=0, days=0) -> Date:
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

    def subtract(self, *, years=0, months=0, days=0) -> Date:
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

    def diff(self, other: Date, *, absolute=False) -> Duration: ...

    # Anchors
    def start_of(
        self, unit: Literal["day", "month", "year", "quarter", "week"]
    ) -> Date:
        """Return the start of the specified time period."""
        if unit == "day":
            return self
        elif unit == "week":
            # Monday = 0, so subtract weekday to get to Monday
            days_to_subtract = self.weekday
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
            days_to_add = 6 - self.weekday
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

    def format(self, fmt: str) -> str:
        """Format date using Carbon-style format string."""
        return self._carbon_format(fmt)

    def _carbon_format(self, fmt: str) -> str:
        """Format date using Carbon-style tokens."""
        # Carbon format token mappings
        mappings = {
            "Y": lambda: f"{self.year:04d}",  # 4-digit year
            "y": lambda: f"{self.year % 100:02d}",  # 2-digit year
            "m": lambda: f"{self.month:02d}",  # Month with leading zero
            "n": lambda: f"{self.month}",  # Month without leading zero
            "d": lambda: f"{self.day:02d}",  # Day with leading zero
            "j": lambda: f"{self.day}",  # Day without leading zero
            "S": lambda: self._ordinal_suffix(self.day),  # Ordinal suffix
            "F": lambda: self._date.strftime("%B"),  # Full month name
            "M": lambda: self._date.strftime("%b"),  # Short month name
            "l": lambda: self._date.strftime("%A"),  # Full day name
            "D": lambda: self._date.strftime("%a"),  # Short day name
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
