from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, overload
from zoneinfo import ZoneInfo

if TYPE_CHECKING:
    from carbonic.core.date import Date
    from carbonic.core.duration import Duration


@dataclass(frozen=True, slots=True)
class DateTime:
    _dt: datetime.datetime

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tz: str | None = "UTC",
    ):
        if tz is None:
            tzinfo = None
        else:
            tzinfo = ZoneInfo(tz)

        dt = datetime.datetime(
            year, month, day, hour, minute, second, microsecond, tzinfo
        )
        object.__setattr__(self, "_dt", dt)

    # Constructors
    @classmethod
    def now(cls, tz: str | None = "UTC") -> DateTime:
        if tz is None:
            now_dt = datetime.datetime.now()
        else:
            now_dt = datetime.datetime.now(ZoneInfo(tz))
        return cls.from_datetime(now_dt)

    @classmethod
    def parse(cls, s: str, fmt: str | None = None, tz: str | None = None) -> DateTime:
        """Parse a datetime string into a DateTime object.

        Args:
            s: The datetime string to parse
            fmt: Optional format string. If None, auto-detect format.
                Supports both strftime (%Y-%m-%d %H:%M:%S) and Carbon (Y-m-d H:i:s) formats.
            tz: Optional timezone. If provided, applies to naive parsed datetimes.

        Returns:
            DateTime object

        Raises:
            ParseError: If the string cannot be parsed
        """
        from carbonic.core.exceptions import ParseError

        if not s or not s.strip():
            raise ParseError("Empty datetime string")

        s = s.strip()

        if fmt is None:
            return cls._auto_parse(s, tz)
        else:
            return cls._parse_with_format(s, fmt, tz)

    @classmethod
    def _auto_parse(cls, s: str, tz: str | None) -> DateTime:
        """Auto-detect format and parse datetime string."""
        from carbonic.core.exceptions import ParseError
        import re

        # Try ISO datetime with timezone first (2025-09-23T14:30:45+00:00)
        iso_tz_pattern = re.compile(
            r"^(\d{4})-(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{1,2}):(\d{1,2})([+-]\d{2}:\d{2}|Z)$"
        )
        match = iso_tz_pattern.match(s)
        if match:
            try:
                year, month, day, hour, minute, second = map(int, match.groups()[:6])
                tz_str = match.groups()[6]

                # Handle timezone
                if tz_str == "Z" or tz_str == "+00:00":
                    parsed_tz = "UTC"
                elif tz_str.startswith(("+", "-")):
                    # For simplicity, treat common offsets as UTC for now
                    # Full timezone offset parsing would be more complex
                    parsed_tz = "UTC"
                else:
                    parsed_tz = "UTC"

                # tz parameter overrides parsed timezone for naive datetimes
                final_tz = tz if tz is not None else parsed_tz
                return cls(year, month, day, hour, minute, second, tz=final_tz)
            except ValueError as e:
                raise ParseError(f"Invalid datetime: {s}") from e

        # Try ISO datetime without timezone (2025-09-23T14:30:45)
        iso_naive_pattern = re.compile(
            r"^(\d{4})-(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{1,2}):(\d{1,2})$"
        )
        match = iso_naive_pattern.match(s)
        if match:
            try:
                year, month, day, hour, minute, second = map(int, match.groups())
                final_tz = tz if tz is not None else "UTC"
                return cls(year, month, day, hour, minute, second, tz=final_tz)
            except ValueError as e:
                raise ParseError(f"Invalid datetime: {s}") from e

        # Try ISO date only (2025-09-23) - set time to 00:00:00
        iso_date_pattern = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
        match = iso_date_pattern.match(s)
        if match:
            try:
                year, month, day = map(int, match.groups())
                final_tz = tz if tz is not None else "UTC"
                return cls(year, month, day, 0, 0, 0, tz=final_tz)
            except ValueError as e:
                raise ParseError(f"Invalid date: {s}") from e

        raise ParseError(f"Unable to parse datetime: {s}")

    @classmethod
    def _parse_with_format(cls, s: str, fmt: str, tz: str | None) -> DateTime:
        """Parse datetime string with explicit format."""
        from carbonic.core.exceptions import ParseError

        try:
            # Convert Carbon-style tokens to strftime if needed
            strftime_fmt = cls._carbon_to_strftime(fmt)

            # Parse using strftime
            parsed = datetime.datetime.strptime(s, strftime_fmt)

            # Apply timezone
            final_tz = tz if tz is not None else "UTC"
            return cls(
                parsed.year,
                parsed.month,
                parsed.day,
                parsed.hour,
                parsed.minute,
                parsed.second,
                parsed.microsecond,
                tz=final_tz,
            )

        except ValueError as e:
            raise ParseError(f"Failed to parse '{s}' with format '{fmt}': {e}") from e

    @staticmethod
    def _carbon_to_strftime(fmt: str) -> str:
        """Convert Carbon-style format tokens to strftime format."""
        # If format contains strftime tokens (%), return as-is
        if "%" in fmt:
            return fmt

        # Use a placeholder approach to avoid conflicts
        # Common Carbon to strftime mappings for datetime
        mappings = [
            ("Y", "%Y"),  # 4-digit year
            ("y", "%y"),  # 2-digit year
            ("F", "%B"),  # Full month name (January) - do before 'm'
            ("M", "%b"),  # Short month name (Jan) - do before 'm'
            ("m", "%m"),  # Month with leading zero
            ("n", "%m"),  # Month without leading zero (strftime %m handles both)
            ("d", "%d"),  # Day with leading zero
            ("j", "%d"),  # Day without leading zero (strftime %d handles both)
            ("H", "%H"),  # Hour 24-format with leading zero
            ("h", "%I"),  # Hour 12-format with leading zero
            ("i", "%M"),  # Minutes with leading zero
            ("s", "%S"),  # Seconds with leading zero
        ]

        result = fmt

        # Use unique placeholders to avoid conflicts
        placeholders = {}
        for i, (carbon_token, strftime_token) in enumerate(mappings):
            if carbon_token in result:
                # Use a placeholder that won't conflict with Carbon tokens
                placeholder = f"\x00{i}\x00"  # Use null chars as safe delimiters
                result = result.replace(carbon_token, placeholder)
                placeholders[placeholder] = strftime_token

        # Replace placeholders with actual strftime tokens
        for placeholder, strftime_token in placeholders.items():
            result = result.replace(placeholder, strftime_token)

        return result

    # Formatting methods
    def strftime(self, fmt: str) -> str:
        """Format datetime using strftime format string."""
        return self._dt.strftime(fmt)

    def format(self, fmt: str) -> str:
        """Format datetime using Carbon-style format string."""
        return self._carbon_format(fmt)

    def _carbon_format(self, fmt: str) -> str:
        """Format datetime using Carbon-style tokens."""
        # Extended Carbon format token mappings for datetime
        mappings = {
            # Date tokens
            "Y": lambda: f"{self.year:04d}",  # 4-digit year
            "y": lambda: f"{self.year % 100:02d}",  # 2-digit year
            "m": lambda: f"{self.month:02d}",  # Month with leading zero
            "n": lambda: f"{self.month}",  # Month without leading zero
            "d": lambda: f"{self.day:02d}",  # Day with leading zero
            "j": lambda: f"{self.day}",  # Day without leading zero
            "S": lambda: self._ordinal_suffix(self.day),  # Ordinal suffix
            "F": lambda: self._dt.strftime("%B"),  # Full month name
            "M": lambda: self._dt.strftime("%b"),  # Short month name
            "l": lambda: self._dt.strftime("%A"),  # Full day name
            "D": lambda: self._dt.strftime("%a"),  # Short day name
            # Time tokens
            "H": lambda: f"{self.hour:02d}",  # Hour 24-format with leading zero
            "G": lambda: f"{self.hour}",  # Hour 24-format without leading zero
            "h": lambda: f"{self._hour_12():02d}",  # Hour 12-format with leading zero
            "g": lambda: f"{self._hour_12()}",  # Hour 12-format without leading zero
            "i": lambda: f"{self.minute:02d}",  # Minutes with leading zero
            "s": lambda: f"{self.second:02d}",  # Seconds with leading zero
            "A": lambda: "AM" if self.hour < 12 else "PM",  # AM/PM uppercase
            "a": lambda: "am" if self.hour < 12 else "pm",  # am/pm lowercase
            "u": lambda: f"{self.microsecond:06d}",  # Microseconds
            "v": lambda: f"{self.microsecond // 1000:03d}",  # Milliseconds
            # Timezone tokens
            "T": lambda: self._timezone_abbr(),  # Timezone abbreviation
            "O": lambda: self._timezone_offset(),  # Timezone offset (+0200)
            "P": lambda: self._timezone_offset_colon(),  # Timezone offset (+02:00)
            "Z": lambda: self._timezone_offset_seconds(),  # Timezone offset in seconds
            # Combined formats
            "c": lambda: self._dt.isoformat(),  # ISO 8601 date (2025-09-23T14:30:45+00:00)
            "r": lambda: self._dt.strftime("%a, %d %b %Y %H:%M:%S %z"),  # RFC 2822
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

    def _hour_12(self) -> int:
        """Get hour in 12-hour format."""
        hour_12 = self.hour % 12
        return 12 if hour_12 == 0 else hour_12

    def _timezone_abbr(self) -> str:
        """Get timezone abbreviation."""
        if self.tzinfo is None:
            return ""
        if isinstance(self.tzinfo, ZoneInfo):
            return self.tzinfo.key.split("/")[-1]  # Simple fallback
        return str(self.tzinfo)

    def _timezone_offset(self) -> str:
        """Get timezone offset in +HHMM format."""
        if self.tzinfo is None:
            return "+0000"
        offset = self._dt.utcoffset()
        if offset is None:
            return "+0000"

        total_seconds = int(offset.total_seconds())
        hours, remainder = divmod(abs(total_seconds), 3600)
        minutes = remainder // 60
        sign = "+" if total_seconds >= 0 else "-"
        return f"{sign}{hours:02d}{minutes:02d}"

    def _timezone_offset_colon(self) -> str:
        """Get timezone offset in +HH:MM format."""
        offset_str = self._timezone_offset()
        if len(offset_str) == 5:  # +HHMM
            return f"{offset_str[:3]}:{offset_str[3:]}"
        return offset_str

    def _timezone_offset_seconds(self) -> str:
        """Get timezone offset in seconds."""
        if self.tzinfo is None:
            return "0"
        offset = self._dt.utcoffset()
        if offset is None:
            return "0"
        return str(int(offset.total_seconds()))

    @staticmethod
    def _ordinal_suffix(day: int) -> str:
        """Get ordinal suffix for a day (st, nd, rd, th)."""
        if 10 <= day % 100 <= 20:  # Special case: 11th, 12th, 13th
            return "th"
        else:
            return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    def __format__(self, format_spec: str) -> str:
        """Support for Python's format() function and f-strings."""
        if not format_spec:
            return str(self)
        return self.format(format_spec)

    # Common format methods
    def to_iso_string(self) -> str:
        """Return ISO datetime string (2025-09-23T14:30:45+00:00)."""
        return self._dt.isoformat()

    def to_date_string(self) -> str:
        """Return ISO date string (2025-09-23)."""
        return self._dt.date().isoformat()

    def to_time_string(self) -> str:
        """Return time string (14:30:45)."""
        return self._dt.time().strftime("%H:%M:%S")

    def to_datetime_string(self) -> str:
        """Return datetime string (2025-09-23 14:30:45)."""
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")

    def to_atom_string(self) -> str:
        """Return Atom/RSS datetime string (ISO 8601)."""
        return self._dt.isoformat()

    def to_cookie_string(self) -> str:
        """Return cookie datetime string (Tue, 23-Sep-2025 14:30:45 UTC)."""
        # Format: Wdy, DD-Mon-YYYY HH:MM:SS GMT
        tz_name = (
            "UTC"
            if self.tzinfo and str(self.tzinfo) == "UTC"
            else str(self.tzinfo or "")
        )
        return self._dt.strftime(f"%a, %d-%b-%Y %H:%M:%S {tz_name}").strip()

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> DateTime:
        if dt.tzinfo is None:
            return cls(
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute,
                dt.second,
                dt.microsecond,
                tz=None,
            )
        else:
            # Extract timezone name from tzinfo
            if isinstance(dt.tzinfo, ZoneInfo):
                tz_name = dt.tzinfo.key
            else:
                tz_name = str(dt.tzinfo)
            return cls(
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute,
                dt.second,
                dt.microsecond,
                tz=tz_name,
            )

    # Properties
    @property
    def year(self) -> int:
        return self._dt.year

    @property
    def month(self) -> int:
        return self._dt.month

    @property
    def day(self) -> int:
        return self._dt.day

    @property
    def hour(self) -> int:
        return self._dt.hour

    @property
    def minute(self) -> int:
        return self._dt.minute

    @property
    def second(self) -> int:
        return self._dt.second

    @property
    def microsecond(self) -> int:
        return self._dt.microsecond

    @property
    def tzinfo(self) -> datetime.tzinfo | None:
        return self._dt.tzinfo

    def __str__(self) -> str:
        return self._dt.isoformat()

    def __repr__(self) -> str:
        if self.tzinfo is None:
            return f"DateTime({self.year}, {self.month}, {self.day}, {self.hour}, {self.minute}, {self.second})"
        else:
            return f"DateTime({self.year}, {self.month}, {self.day}, {self.hour}, {self.minute}, {self.second}, tz='{self.tzinfo}')"

    # Comparison methods
    def __eq__(self, other: object) -> bool:
        """Check equality with another DateTime."""
        if not isinstance(other, DateTime):
            return False
        return self._dt == other._dt

    def __lt__(self, other: DateTime) -> bool:
        """Check if this datetime is less than another."""
        if not isinstance(other, DateTime):
            return NotImplemented
        return self._dt < other._dt

    def __le__(self, other: DateTime) -> bool:
        """Check if this datetime is less than or equal to another."""
        if not isinstance(other, DateTime):
            return NotImplemented
        return self._dt <= other._dt

    def __gt__(self, other: DateTime) -> bool:
        """Check if this datetime is greater than another."""
        if not isinstance(other, DateTime):
            return NotImplemented
        return self._dt > other._dt

    def __ge__(self, other: DateTime) -> bool:
        """Check if this datetime is greater than or equal to another."""
        if not isinstance(other, DateTime):
            return NotImplemented
        return self._dt >= other._dt

    def __hash__(self) -> int:
        """Return hash of the datetime for use in sets and dicts."""
        return hash(self._dt)

    # Ops
    def add(
        self, *, days=0, hours=0, minutes=0, seconds=0, months=0, years=0
    ) -> DateTime:
        """Add time components to this datetime."""
        # Start with the current datetime
        new_dt = self._dt

        # Add timedelta components (days, hours, minutes, seconds)
        if days or hours or minutes or seconds:
            delta = datetime.timedelta(
                days=days, hours=hours, minutes=minutes, seconds=seconds
            )
            new_dt = new_dt + delta

        # Add months and years (more complex due to variable month lengths)
        if months or years:
            # Calculate new year and month
            total_months = new_dt.month + months + (years * 12)
            new_year = new_dt.year + (total_months - 1) // 12
            new_month = ((total_months - 1) % 12) + 1

            # Handle day overflow (e.g., Jan 31 + 1 month -> Feb 28/29)
            new_day = min(new_dt.day, self._last_day_of_month(new_year, new_month))

            new_dt = new_dt.replace(year=new_year, month=new_month, day=new_day)

        return DateTime.from_datetime(new_dt)

    def subtract(self, **kwargs) -> DateTime:
        """Subtract time components from this datetime."""
        # Negate all kwargs and call add
        negated_kwargs = {k: -v for k, v in kwargs.items()}
        return self.add(**negated_kwargs)

    @staticmethod
    def _last_day_of_month(year: int, month: int) -> int:
        """Get the last day of the given month/year."""
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        last_day = next_month - datetime.timedelta(days=1)
        return last_day.day

    def diff(self, other: DateTime, *, absolute=False) -> Duration:
        """Calculate difference between this datetime and another datetime.

        Args:
            other: The other datetime to compare with
            absolute: If True, return absolute difference (always positive)

        Returns:
            Duration representing the difference
        """
        from carbonic.core.duration import Duration

        if not isinstance(other, DateTime):
            raise TypeError("Can only diff with another DateTime")

        # Convert both to datetime objects for calculation
        dt1 = self.to_datetime()
        dt2 = other.to_datetime()

        # Calculate difference using standard datetime
        delta = dt1 - dt2

        if absolute:
            delta = abs(delta)

        # Extract components from timedelta
        days = delta.days
        seconds = delta.seconds
        microseconds = delta.microseconds

        return Duration(days=days, seconds=seconds, microseconds=microseconds)

    def add_duration(self, duration: Duration) -> DateTime:
        """Add a Duration to this DateTime.

        Args:
            duration: The Duration to add

        Returns:
            New DateTime with the duration added
        """
        from carbonic.core.duration import Duration

        if not isinstance(duration, Duration):
            raise TypeError("Can only add Duration objects")

        # Convert this datetime to stdlib datetime for calculation
        dt = self.to_datetime()

        # Create a timedelta from the Duration's time components
        delta = datetime.timedelta(
            days=duration.days,
            seconds=duration.storage_seconds,
            microseconds=duration.microseconds
        )

        # Add the timedelta
        result_dt = dt + delta

        # Handle calendar components (months/years) if present
        if duration.months or duration.years:
            # Extract date part for calendar arithmetic
            result_date = result_dt.date()

            # Calculate new year and month
            total_months = result_date.month + duration.months + (duration.years * 12)
            new_year = result_date.year + (total_months - 1) // 12
            new_month = ((total_months - 1) % 12) + 1

            # Handle day overflow (e.g., Jan 31 + 1 month -> Feb 28/29)
            new_day = min(result_date.day, self._last_day_of_month(new_year, new_month))

            # Create new datetime with adjusted date but same time
            result_dt = result_dt.replace(year=new_year, month=new_month, day=new_day)

        return DateTime.from_datetime(result_dt)

    def subtract_duration(self, duration: Duration) -> DateTime:
        """Subtract a Duration from this DateTime.

        Args:
            duration: The Duration to subtract

        Returns:
            New DateTime with the duration subtracted
        """
        from carbonic.core.duration import Duration

        if not isinstance(duration, Duration):
            raise TypeError("Can only subtract Duration objects")

        # Use negation and add
        return self.add_duration(-duration)

    def __add__(self, other: Duration) -> DateTime:
        """Add a Duration to this DateTime using + operator."""
        if hasattr(other, 'days'):  # Duck typing for Duration-like objects
            return self.add_duration(other)
        return NotImplemented

    @overload
    def __sub__(self, other: Duration) -> DateTime: ...

    @overload
    def __sub__(self, other: DateTime) -> Duration: ...

    def __sub__(self, other: Duration | DateTime) -> DateTime | Duration:
        """Subtract a Duration or DateTime from this DateTime using - operator.

        Args:
            other: Duration to subtract (returns DateTime) or DateTime to diff with (returns Duration)

        Returns:
            DateTime if subtracting Duration, Duration if subtracting DateTime
        """
        if isinstance(other, DateTime):
            return self.diff(other)
        elif hasattr(other, 'days'):  # Duck typing for Duration-like objects
            return self.subtract_duration(other)
        return NotImplemented

    # Anchors
    def start_of(
        self, unit: Literal["minute", "hour", "day", "month", "year", "week"]
    ) -> DateTime:
        """Return the start of the specified time period."""
        if unit == "minute":
            # Zero out seconds and microseconds
            return DateTime(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                0,
                0,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "hour":
            # Zero out minutes, seconds and microseconds
            return DateTime(
                self.year,
                self.month,
                self.day,
                self.hour,
                0,
                0,
                0,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "day":
            # Set time to 00:00:00
            return DateTime(
                self.year,
                self.month,
                self.day,
                0,
                0,
                0,
                0,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "week":
            # Monday = 0, so subtract weekday to get to Monday at 00:00:00
            days_to_subtract = self._dt.weekday()
            start_date = self._dt.date() - datetime.timedelta(days=days_to_subtract)
            return DateTime(
                start_date.year,
                start_date.month,
                start_date.day,
                0,
                0,
                0,
                0,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "month":
            # First day of month at 00:00:00
            return DateTime(
                self.year,
                self.month,
                1,
                0,
                0,
                0,
                0,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "year":
            # January 1st at 00:00:00
            return DateTime(
                self.year,
                1,
                1,
                0,
                0,
                0,
                0,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        else:
            raise ValueError(f"Unknown unit: {unit}")

    def end_of(
        self, unit: Literal["minute", "hour", "day", "month", "year", "week"]
    ) -> DateTime:
        """Return the end of the specified time period."""
        if unit == "minute":
            # Set seconds to 59, microseconds to 999999
            return DateTime(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                59,
                999999,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "hour":
            # Set to 59:59.999999
            return DateTime(
                self.year,
                self.month,
                self.day,
                self.hour,
                59,
                59,
                999999,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "day":
            # Set time to 23:59:59.999999
            return DateTime(
                self.year,
                self.month,
                self.day,
                23,
                59,
                59,
                999999,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "week":
            # Sunday = 6, so add days to get to Sunday at 23:59:59.999999
            days_to_add = 6 - self._dt.weekday()
            end_date = self._dt.date() + datetime.timedelta(days=days_to_add)
            return DateTime(
                end_date.year,
                end_date.month,
                end_date.day,
                23,
                59,
                59,
                999999,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "month":
            # Last day of month at 23:59:59.999999
            last_day = self._last_day_of_month(self.year, self.month)
            return DateTime(
                self.year,
                self.month,
                last_day,
                23,
                59,
                59,
                999999,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        elif unit == "year":
            # December 31st at 23:59:59.999999
            return DateTime(
                self.year,
                12,
                31,
                23,
                59,
                59,
                999999,
                tz=self.tzinfo.key if isinstance(self.tzinfo, ZoneInfo) else None,
            )
        else:
            raise ValueError(f"Unknown unit: {unit}")

    # Conversions
    def to_date(self) -> Date:
        """Convert to carbonic Date object."""
        from carbonic.core.date import Date

        return Date(self.year, self.month, self.day)

    def to_datetime(self) -> datetime.datetime:
        """Return a copy of the underlying datetime.datetime object."""
        return datetime.datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            self.tzinfo,
        )
