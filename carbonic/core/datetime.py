"""DateTime implementation for Carbonic.

This module provides the core DateTime class with fluent API, immutability,
timezone support, and comprehensive formatting capabilities.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Callable, Literal, cast, overload
from zoneinfo import ZoneInfo

from carbonic.core.date import Date
from carbonic.core.duration import Duration


@dataclass(frozen=True, slots=True)
class DateTime:
    """Immutable datetime object with fluent API and timezone support.

    The DateTime class provides a modern, type-safe wrapper around Python's datetime
    with comprehensive datetime manipulation. All operations return new
    instances, maintaining immutability.

    Attributes:
        _dt: Internal datetime.datetime object storing the actual datetime value

    Examples:
        >>> dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        >>> dt.add(hours=2).format("Y-m-d H:i:s")
        '2024-01-15 16:30:00'

        >>> now = DateTime.now("America/New_York")  # doctest: +SKIP
        >>> now.to_date_string()  # doctest: +SKIP
        '2024-01-15'
    """

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
    ) -> None:
        """Initialize a new DateTime instance.

        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)
            day: Day of month (1-31)
            hour: Hour (0-23, default: 0)
            minute: Minute (0-59, default: 0)
            second: Second (0-59, default: 0)
            microsecond: Microsecond (0-999999, default: 0)
            tz: Timezone string (default: "UTC", None for naive datetime)

        Raises:
            ValueError: If any datetime component is invalid
            ZoneInfoNotFoundError: If timezone string is invalid
        """
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
        """Create a DateTime instance for the current moment.

        Args:
            tz: Timezone string (default: "UTC", None for system local time)

        Returns:
            DateTime instance representing the current moment

        Examples:
            >>> DateTime.now()  # Current time in UTC  # doctest: +SKIP
            >>> DateTime.now("America/New_York")  # Current time in NY timezone  # doctest: +SKIP
            >>> DateTime.now(None)  # Current local time (naive)  # doctest: +SKIP
        """
        if tz is None:
            now_dt = datetime.datetime.now()
        else:
            now_dt = datetime.datetime.now(ZoneInfo(tz))
        return cls.from_datetime(now_dt)

    @classmethod
    def today(cls, tz: str | None = "UTC") -> DateTime:
        """Get the current date at 00:00:00 in the specified timezone.

        Args:
            tz: Timezone string (default: "UTC")

        Returns:
            DateTime object representing today at midnight
        """
        now = cls.now(tz)
        return cls(now.year, now.month, now.day, 0, 0, 0, tz=tz)

    @classmethod
    def tomorrow(cls, tz: str | None = "UTC") -> DateTime:
        """Get tomorrow's date at 00:00:00 in the specified timezone.

        Args:
            tz: Timezone string (default: "UTC")

        Returns:
            DateTime object representing tomorrow at midnight
        """
        return cls.today(tz).add(days=1)

    @classmethod
    def yesterday(cls, tz: str | None = "UTC") -> DateTime:
        """Get yesterday's date at 00:00:00 in the specified timezone.

        Args:
            tz: Timezone string (default: "UTC")

        Returns:
            DateTime object representing yesterday at midnight
        """
        return cls.today(tz).add(days=-1)

    @classmethod
    def next(cls, unit: str, count: int = 1, tz: str | None = "UTC") -> DateTime:
        """Get a datetime in the future relative to now.

        Args:
            unit: Time unit ("second", "minute", "hour", "day", "week", "month", "quarter", "year")
            count: Number of units to add (default: 1)
            tz: Timezone string (default: "UTC")

        Returns:
            DateTime object in the future

        Examples:
            >>> DateTime.next("day")      # Tomorrow  # doctest: +SKIP
            >>> DateTime.next("week", 2)  # 2 weeks from now  # doctest: +SKIP
            >>> DateTime.next("month")    # Next month  # doctest: +SKIP
        """
        now = cls.now(tz)
        return cls._add_relative_unit(now, unit, count)

    @classmethod
    def previous(cls, unit: str, count: int = 1, tz: str | None = "UTC") -> DateTime:
        """Get a datetime in the past relative to now.

        Args:
            unit: Time unit ("second", "minute", "hour", "day", "week", "month", "quarter", "year")
            count: Number of units to subtract (default: 1)
            tz: Timezone string (default: "UTC")

        Returns:
            DateTime object in the past

        Examples:
            >>> DateTime.previous("day")      # Yesterday  # doctest: +SKIP
            >>> DateTime.previous("week", 2)  # 2 weeks ago  # doctest: +SKIP
            >>> DateTime.previous("month")    # Last month  # doctest: +SKIP
        """
        now = cls.now(tz)
        return cls._add_relative_unit(now, unit, -count)

    @classmethod
    def _add_relative_unit(cls, dt: DateTime, unit: str, count: int) -> DateTime:
        """Add relative time units to a datetime."""
        if unit == "second":
            return dt.add(seconds=count)
        elif unit == "minute":
            return dt.add(minutes=count)
        elif unit == "hour":
            return dt.add(hours=count)
        elif unit == "day":
            return dt.add(days=count)
        elif unit == "week":
            return dt.add(days=count * 7)
        elif unit == "month":
            return dt.add(months=count)
        elif unit == "quarter":
            return dt.add(months=count * 3)
        elif unit == "year":
            return dt.add(years=count)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")

    @classmethod
    def parse(cls, s: str, fmt: str | None = None, tz: str | None = None) -> DateTime:
        """Parse a datetime string into a DateTime object.

        Args:
            s: The datetime string to parse. Supports:
                - ISO 8601 formats (2024-01-15T14:30:00Z)
                - Custom formats when fmt is provided
            fmt: Optional format string. If None, auto-detect format.
                Supports both strftime (%Y-%m-%d %H:%M:%S) and Carbon (Y-m-d H:i:s) formats.
            tz: Optional timezone. If provided, applies to naive parsed datetimes.

        Returns:
            DateTime object

        Raises:
            ParseError: If the string cannot be parsed

        Examples:
            >>> DateTime.parse("2024-01-15T14:30:00Z")  # doctest: +SKIP
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
        import re

        from carbonic.core.exceptions import ParseError

        # Try fast ciso8601 parsing for ISO formats first
        parsed_dt: datetime.datetime | None = None
        try:
            import ciso8601  # type: ignore[import-not-found]

            # Try parsing with ciso8601 (handles ISO 8601 formats efficiently)
            try:
                parsed_dt = cast(datetime.datetime, ciso8601.parse_datetime(s))  # type: ignore[attr-defined]
            except ValueError:
                # ciso8601 failed to parse, fall back to manual parsing
                parsed_dt = None

            if parsed_dt is not None:
                # ciso8601 successfully parsed the datetime
                if parsed_dt.tzinfo is None:
                    # Naive datetime - apply provided timezone or default to UTC
                    final_tz = tz if tz is not None else "UTC"
                    return cls(
                        parsed_dt.year,
                        parsed_dt.month,
                        parsed_dt.day,
                        parsed_dt.hour,
                        parsed_dt.minute,
                        parsed_dt.second,
                        parsed_dt.microsecond,
                        tz=final_tz,
                    )
                else:
                    # Timezone-aware datetime - convert timezone if needed
                    if tz is not None:
                        # User wants a specific timezone, apply it
                        final_tz = tz
                    else:
                        # Keep original timezone, convert to string
                        if isinstance(parsed_dt.tzinfo, ZoneInfo):
                            final_tz = parsed_dt.tzinfo.key
                        elif str(parsed_dt.tzinfo) in ("UTC", "+00:00", "Z"):
                            final_tz = "UTC"
                        else:
                            final_tz = "UTC"  # Fallback for complex timezone offsets

                    return cls(
                        parsed_dt.year,
                        parsed_dt.month,
                        parsed_dt.day,
                        parsed_dt.hour,
                        parsed_dt.minute,
                        parsed_dt.second,
                        parsed_dt.microsecond,
                        tz=final_tz,
                    )
        except ImportError:
            # ciso8601 not available, fall back to manual parsing
            pass

        # Fallback to manual regex parsing for non-ISO formats or when ciso8601 fails
        # Try ISO datetime with timezone first (2025-09-23T14:30:45.123456+00:00 or Z)
        iso_tz_pattern = re.compile(
            r"^(\d{4})-(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{1,2}):(\d{1,2})(?:\.(\d+))?([+-]\d{2}:\d{2}|Z)$"
        )
        match = iso_tz_pattern.match(s)
        if match:
            try:
                year, month, day, hour, minute, second = map(int, match.groups()[:6])
                microsecond_str = match.groups()[6]
                tz_str = match.groups()[7]

                # Parse microseconds if present
                microsecond = 0
                if microsecond_str:
                    # Pad or truncate to 6 digits
                    microsecond_str = microsecond_str.ljust(6, "0")[:6]
                    microsecond = int(microsecond_str)

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
                return cls(
                    year, month, day, hour, minute, second, microsecond, tz=final_tz
                )
            except ValueError as e:
                raise ParseError(f"Invalid datetime: {s}") from e

        # Try ISO datetime without timezone (2025-09-23T14:30:45.123456)
        iso_naive_pattern = re.compile(
            r"^(\d{4})-(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{1,2}):(\d{1,2})(?:\.(\d+))?$"
        )
        match = iso_naive_pattern.match(s)
        if match:
            try:
                year, month, day, hour, minute, second = map(int, match.groups()[:6])
                microsecond_str = match.groups()[6]

                # Parse microseconds if present
                microsecond = 0
                if microsecond_str:
                    # Pad or truncate to 6 digits
                    microsecond_str = microsecond_str.ljust(6, "0")[:6]
                    microsecond = int(microsecond_str)

                final_tz = tz if tz is not None else "UTC"
                return cls(
                    year, month, day, hour, minute, second, microsecond, tz=final_tz
                )
            except ValueError as e:
                raise ParseError(f"Invalid datetime: {s}") from e

        # Try space-separated datetime (2024-01-15 14:30:45.123456)
        space_pattern = re.compile(
            r"^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2}):(\d{1,2})(?:\.(\d+))?$"
        )
        match = space_pattern.match(s)
        if match:
            try:
                year, month, day, hour, minute, second = map(int, match.groups()[:6])
                microsecond_str = match.groups()[6]

                # Parse microseconds if present
                microsecond = 0
                if microsecond_str:
                    # Pad or truncate to 6 digits
                    microsecond_str = microsecond_str.ljust(6, "0")[:6]
                    microsecond = int(microsecond_str)

                final_tz = tz if tz is not None else "UTC"
                return cls(
                    year, month, day, hour, minute, second, microsecond, tz=final_tz
                )
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

        result: str = fmt
        placeholders: dict[str, str] = {}

        for i, (carbon_token, strftime_token) in enumerate(mappings):
            if carbon_token in result:
                placeholder = f"\x00{i}\x00"  # Use null chars as safe delimiters
                result = result.replace(carbon_token, placeholder)
                placeholders[placeholder] = strftime_token

        for placeholder, strftime_token in placeholders.items():
            result = result.replace(placeholder, strftime_token)

        return result

    # Formatting methods
    def strftime(self, fmt: str) -> str:
        """Format datetime using strftime format string."""
        return self._dt.strftime(fmt)

    def format(self, fmt: str, *, locale: str | None = None) -> str:
        """Format datetime using Carbon-style format string.

        Uses Carbon-style tokens for flexible datetime formatting. Escape Carbon tokens
        with curly braces like {Y} to include them literally. Use Python string literals
        for special characters like \\n, \\t, \\r.

        ## Format Tokens

        | Token | Description | Example |
        |-------|-------------|---------|
        | **Date** | | |
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
        | **Time** | | |
        | `H` | Hour 24-format with leading zero | `00`, `23` |
        | `G` | Hour 24-format without leading zero | `0`, `23` |
        | `h` | Hour 12-format with leading zero | `01`, `12` |
        | `g` | Hour 12-format without leading zero | `1`, `12` |
        | `i` | Minutes with leading zero | `00`, `59` |
        | `s` | Seconds with leading zero | `00`, `59` |
        | `A` | AM/PM uppercase | `AM`, `PM` |
        | `a` | am/pm lowercase | `am`, `pm` |
        | `u` | Microseconds (6 digits) | `000000`, `123456` |
        | `v` | Milliseconds (3 digits) | `000`, `123` |
        | **Timezone** | | |
        | `T` | Timezone abbreviation | `UTC`, `EST` |
        | `O` | Timezone offset | `+0000`, `+0200` |
        | `P` | Timezone offset with colon | `+00:00`, `+02:00` |
        | `Z` | Timezone offset in seconds | `0`, `7200` |
        | **Combined** | | |
        | `c` | ISO 8601 datetime | `2024-01-15T14:30:45+00:00` |
        | `r` | RFC 2822 datetime | `Mon, 15 Jan 2024 14:30:45 +0000` |

        Args:
            fmt: Carbon-style format string with tokens above
            locale: Locale code for localized month/day names (default: English)
                  Supported: en, pl, es, fr, de, pt

        Returns:
            Formatted datetime string

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")
            >>> dt.format("Y-m-d H:i:s")
            '2024-01-15 14:30:45'
            >>> dt.format("l, F j, Y")
            'Monday, January 15, 2024'
            >>> dt.format("l, F j, Y", locale="es")  # doctest: +SKIP
            'lunes, enero 15, 2024'
            >>> dt.format("H:i A (T)")
            '14:30 PM (UTC)'

            # Escaping Carbon tokens with curly braces
            >>> dt.format("{Y} = Y")
            'Y = 2024'

            # Mix of escaped tokens and literal text
            >>> dt.format("{Y}-{m}-{d} = Y-m-d")
            'Y-m-d = 2024-01-15'

            # Use Python string literals for special characters
            >>> dt.format("Y-m-d\\nH:i:s")  # \\n in Python string
            '2024-01-15\\n14:30:45'
        """
        return self._carbon_format(fmt, locale=locale)

    def _carbon_format(self, fmt: str, *, locale: str | None = None) -> str:
        """Format datetime using Carbon-style tokens."""
        # Get locale instance
        from carbonic.locale import get_locale

        locale_obj = get_locale(locale or "en")

        # Lazy evaluation cache for expensive operations
        _cache: dict[str, str] = {}

        # Extended Carbon format token mappings for datetime
        mappings: dict[str, Callable[[], str]] = {
            # Date tokens
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
                f"l_{locale or 'en'}_{self._dt.weekday()}",
                locale_obj.get_day_name(self._dt.weekday(), short=False),
            ),  # Full day name (cached)
            "D": lambda: _cache.setdefault(
                f"D_{locale or 'en'}_{self._dt.weekday()}",
                locale_obj.get_day_name(self._dt.weekday(), short=True),
            ),  # Short day name (cached)
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
            # Timezone tokens (cached for performance)
            "T": lambda: _cache.setdefault(
                f"T_{self.tzinfo}", self._timezone_abbr()
            ),  # Timezone abbreviation (cached)
            "O": lambda: _cache.setdefault(
                f"O_{self.tzinfo}", self._timezone_offset()
            ),  # Timezone offset (+0200) (cached)
            "P": lambda: _cache.setdefault(
                f"P_{self.tzinfo}", self._timezone_offset_colon()
            ),  # Timezone offset (+02:00) (cached)
            "Z": lambda: _cache.setdefault(
                f"Z_{self.tzinfo}", self._timezone_offset_seconds()
            ),  # Timezone offset in seconds (cached)
            # Combined formats
            "c": lambda: self._dt.isoformat(),  # ISO 8601 date (2025-09-23T14:30:45+00:00)
            "r": lambda: self._dt.strftime("%a, %d %b %Y %H:%M:%S %z"),  # RFC 2822
        }

        result = ""
        i = 0
        while i < len(fmt):
            char = fmt[i]

            # Handle bracket escapes for Carbon tokens {Y}, {m}, etc.
            if char == "{" and i + 1 < len(fmt):
                # Find the closing bracket
                close_bracket = fmt.find("}", i + 1)
                if close_bracket != -1:
                    escape_content = fmt[i + 1 : close_bracket]
                    # Include the content literally (escape Carbon tokens)
                    result += escape_content
                    i = close_bracket + 1
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
        """Return ISO 8601 string (2025-09-23T14:30:45+00:00).

        Returns:
            ISO 8601 formatted datetime string with timezone

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
            >>> dt.to_iso_string()
            '2024-01-15T14:30:00+00:00'
        """
        return self._dt.isoformat()

    def to_date_string(self) -> str:
        """Return date string (2025-09-23).

        Returns:
            Date portion formatted as YYYY-MM-DD

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30)
            >>> dt.to_date_string()
            '2024-01-15'
        """
        return self._dt.date().isoformat()

    def to_time_string(self) -> str:
        """Return time string (14:30:45).

        Returns:
            Time portion formatted as HH:MM:SS

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30, 45)
            >>> dt.to_time_string()
            '14:30:45'
        """
        return self._dt.time().strftime("%H:%M:%S")

    def to_datetime_string(self) -> str:
        """Return datetime string (2025-09-23 14:30:45).

        Returns:
            Datetime formatted as YYYY-MM-DD HH:MM:SS (no timezone)

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30, 45)
            >>> dt.to_datetime_string()
            '2024-01-15 14:30:45'
        """
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")

    def to_atom_string(self) -> str:
        """Return Atom/RSS datetime string (ISO 8601).

        Returns:
            ISO 8601 formatted string suitable for Atom/RSS feeds

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
            >>> dt.to_atom_string()
            '2024-01-15T14:30:00+00:00'
        """
        return self._dt.isoformat()

    def to_cookie_string(self) -> str:
        """Return cookie datetime string (Tue, 23-Sep-2025 14:30:45 UTC).

        Returns:
            Cookie-compatible datetime string format

        Examples:
            >>> dt = DateTime(2024, 1, 15, 14, 30, tz="UTC")
            >>> dt.to_cookie_string()
            'Mon, 15-Jan-2024 14:30:00 UTC'
        """
        # Format: Wdy, DD-Mon-YYYY HH:MM:SS GMT
        tz_name = (
            "UTC"
            if self.tzinfo and str(self.tzinfo) == "UTC"
            else str(self.tzinfo or "")
        )
        return self._dt.strftime(f"%a, %d-%b-%Y %H:%M:%S {tz_name}").strip()

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> DateTime:
        """Create a DateTime from a standard Python datetime object.

        Args:
            dt: Python datetime.datetime object to convert

        Returns:
            New DateTime instance preserving timezone information

        Examples:
            >>> import datetime
            >>> dt = datetime.datetime(2024, 1, 15, 14, 30)
            >>> carbonic_dt = DateTime.from_datetime(dt)
        """
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
        """The year component (e.g., 2024)."""
        return self._dt.year

    @property
    def month(self) -> int:
        """The month component (1-12)."""
        return self._dt.month

    @property
    def day(self) -> int:
        """The day of month component (1-31)."""
        return self._dt.day

    @property
    def hour(self) -> int:
        """The hour component (0-23)."""
        return self._dt.hour

    @property
    def minute(self) -> int:
        """The minute component (0-59)."""
        return self._dt.minute

    @property
    def second(self) -> int:
        """The second component (0-59)."""
        return self._dt.second

    @property
    def microsecond(self) -> int:
        """The microsecond component (0-999999)."""
        return self._dt.microsecond

    @property
    def tzinfo(self) -> datetime.tzinfo | None:
        """The timezone info, or None for naive datetime."""
        return self._dt.tzinfo

    @property
    def fold(self) -> int:
        """Fold attribute for disambiguation during DST transitions (datetime.datetime compatibility)."""
        return self._dt.fold

    def __str__(self) -> str:
        return self._dt.isoformat()

    def __repr__(self) -> str:
        if self.tzinfo is None:
            return f"DateTime({self.year}, {self.month}, {self.day}, {self.hour}, {self.minute}, {self.second})"
        else:
            return f"DateTime({self.year}, {self.month}, {self.day}, {self.hour}, {self.minute}, {self.second}, tz='{self.tzinfo}')"

    # Comparison methods
    def __eq__(self, other: object) -> bool:
        """Check equality with another DateTime or datetime.datetime."""
        if isinstance(other, DateTime):
            return self._dt == other._dt
        if isinstance(other, datetime.datetime):
            return self._dt == other
        return False

    def __lt__(self, other: object) -> bool:
        """Check if this datetime is less than another."""
        if isinstance(other, DateTime):
            return self._dt < other._dt
        if isinstance(other, datetime.datetime):
            return self._dt < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """Check if this datetime is less than or equal to another."""
        if isinstance(other, DateTime):
            return self._dt <= other._dt
        if isinstance(other, datetime.datetime):
            return self._dt <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        """Check if this datetime is greater than another."""
        if isinstance(other, DateTime):
            return self._dt > other._dt
        if isinstance(other, datetime.datetime):
            return self._dt > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        """Check if this datetime is greater than or equal to another."""
        if isinstance(other, DateTime):
            return self._dt >= other._dt
        if isinstance(other, datetime.datetime):
            return self._dt >= other
        return NotImplemented

    def __hash__(self) -> int:
        """Return hash of the datetime for use in sets and dicts."""
        return hash(self._dt)

    # Ops
    def add(
        self,
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        months: int = 0,
        years: int = 0,
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

    def subtract(self, **kwargs: int) -> DateTime:
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

    def diff(self, other: DateTime, *, absolute: bool = False) -> Duration:
        """Calculate difference between this datetime and another datetime.

        Args:
            other: The other datetime to compare with
            absolute: If True, return absolute difference (always positive)

        Returns:
            Duration representing the difference
        """

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

        # Convert this datetime to stdlib datetime for calculation
        dt = self.to_datetime()

        # Create a timedelta from the Duration's time components
        delta = datetime.timedelta(
            days=duration.days,
            seconds=duration.storage_seconds,
            microseconds=duration.microseconds,
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

        # Use negation and add
        return self.add_duration(-duration)

    def __add__(self, other: Duration) -> DateTime:
        """Add a Duration to this DateTime using + operator."""
        if hasattr(other, "days"):  # Duck typing for Duration-like objects
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
        elif hasattr(other, "days"):  # Duck typing for Duration-like objects
            return self.subtract_duration(other)
        return NotImplemented

    # Anchors
    def start_of(
        self, unit: Literal["minute", "hour", "day", "week", "month", "quarter", "year"]
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
        elif unit == "quarter":
            # First month of quarter
            first_month_of_quarter = ((self.month - 1) // 3) * 3 + 1
            return DateTime(
                self.year,
                first_month_of_quarter,
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
        self, unit: Literal["minute", "hour", "day", "week", "month", "quarter", "year"]
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
        elif unit == "quarter":
            # Last month of quarter
            last_month_of_quarter = ((self.month - 1) // 3) * 3 + 3
            last_day = self._last_day_of_month(self.year, last_month_of_quarter)
            return DateTime(
                self.year,
                last_month_of_quarter,
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

    def as_timezone(self, tz: str | None) -> DateTime:
        """Convert this DateTime to a different timezone.

        This method converts a timezone-aware DateTime to a different timezone,
        representing the same moment in time. It can also convert to a naive
        datetime by passing None as the timezone.

        Args:
            tz: Target timezone string (e.g., "America/New_York", "Europe/Warsaw")
                or None for naive datetime (removes timezone info)

        Returns:
            New DateTime instance in the target timezone representing the same moment

        Raises:
            ValueError: If this DateTime is naive and target timezone is not None
            ZoneInfoNotFoundError: If timezone string is invalid

        Examples:
            >>> utc_time = DateTime(2024, 1, 15, 14, 30, tz="UTC")
            >>> ny_time = utc_time.as_timezone("America/New_York")
            >>> # Same moment, different timezone representation
            >>> utc_time == ny_time
            True

            >>> # Convert to naive datetime
            >>> naive_time = utc_time.as_timezone(None)  # doctest: +SKIP
        """
        # Check if source datetime is naive
        if self.tzinfo is None:
            if tz is not None:
                raise ValueError(
                    "Cannot convert naive DateTime to timezone-aware. "
                    "Create a new DateTime with timezone information first."
                )
            # Naive to naive - return copy
            return DateTime(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
                tz=None,
            )

        # Source is timezone-aware
        if tz is None:
            # Convert to naive - remove timezone info but keep the local time
            return DateTime(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
                tz=None,
            )

        # Convert between timezones using stdlib astimezone
        try:
            target_tzinfo = ZoneInfo(tz)
        except Exception as e:
            raise ValueError(f"Invalid timezone: {tz}") from e

        converted_dt = self._dt.astimezone(target_tzinfo)
        return DateTime.from_datetime(converted_dt)

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

    # datetime.datetime API compatibility methods
    def weekday(self) -> int:
        """Return day of week where Monday=0, Sunday=6 (datetime.datetime compatibility)."""
        return self._dt.weekday()

    def isoweekday(self) -> int:
        """Return ISO day of week where Monday=1, Sunday=7 (datetime.datetime compatibility)."""
        return self._dt.isoweekday()

    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str:
        """Return ISO 8601 format string (datetime.datetime compatibility)."""
        return self._dt.isoformat(sep=sep, timespec=timespec)

    def isocalendar(self) -> tuple[int, int, int]:
        """Return (year, week, weekday) tuple (datetime.datetime compatibility)."""
        return self._dt.isocalendar()

    def date(self) -> datetime.date:
        """Return date object with same date (datetime.datetime compatibility)."""
        return self._dt.date()

    def time(self) -> datetime.time:
        """Return time object with same time (datetime.datetime compatibility)."""
        return self._dt.time()

    def timetz(self) -> datetime.time:
        """Return time object with same time and tzinfo (datetime.datetime compatibility)."""
        return self._dt.timetz()

    def replace(
        self,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int | None = None,
        minute: int | None = None,
        second: int | None = None,
        microsecond: int | None = None,
        tzinfo: datetime.tzinfo | None | object = ...,
    ) -> DateTime:
        """Return a DateTime with one or more components replaced (datetime.datetime compatibility)."""
        # Use ellipsis to distinguish between None (set to None) and not provided (keep current)
        tzinfo_to_use: datetime.tzinfo | None
        if tzinfo is ...:
            tzinfo_to_use = self.tzinfo
        else:
            tzinfo_to_use = cast(datetime.tzinfo | None, tzinfo)

        # Convert tzinfo to tz string if needed
        tz_str: str | None
        if tzinfo_to_use is None:
            tz_str = None
        elif isinstance(tzinfo_to_use, ZoneInfo):
            tz_str = tzinfo_to_use.key
        elif hasattr(tzinfo_to_use, "zone"):
            tz_str = cast(str, getattr(tzinfo_to_use, "zone"))
        else:
            tz_str = "UTC"  # Fallback

        return DateTime(
            year if year is not None else self.year,
            month if month is not None else self.month,
            day if day is not None else self.day,
            hour if hour is not None else self.hour,
            minute if minute is not None else self.minute,
            second if second is not None else self.second,
            microsecond if microsecond is not None else self.microsecond,
            tz=tz_str,
        )

    def timetuple(self):
        """Return time.struct_time (datetime.datetime compatibility)."""
        return self._dt.timetuple()

    def utctimetuple(self):
        """Return UTC time.struct_time (datetime.datetime compatibility)."""
        return self._dt.utctimetuple()

    def toordinal(self) -> int:
        """Return proleptic Gregorian ordinal (datetime.datetime compatibility)."""
        return self._dt.toordinal()

    def timestamp(self) -> float:
        """Return POSIX timestamp (datetime.datetime compatibility)."""
        return self._dt.timestamp()

    def utcoffset(self) -> datetime.timedelta | None:
        """Return UTC offset (datetime.datetime compatibility)."""
        return self._dt.utcoffset()

    def dst(self) -> datetime.timedelta | None:
        """Return DST offset (datetime.datetime compatibility)."""
        return self._dt.dst()

    def tzname(self) -> str | None:
        """Return timezone name (datetime.datetime compatibility)."""
        return self._dt.tzname()

    def astimezone(self, tz: datetime.tzinfo | None = None) -> DateTime:
        """Convert to another timezone (datetime.datetime compatibility)."""
        if tz is None:
            # Convert to local timezone
            new_dt = self._dt.astimezone()
        else:
            new_dt = self._dt.astimezone(tz)

        return DateTime.from_datetime(new_dt)

    def ctime(self) -> str:
        """Return ctime() style string (datetime.datetime compatibility)."""
        return self._dt.ctime()
