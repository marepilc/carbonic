"""Native datetime subtype for Carbonic."""

from __future__ import annotations

import datetime as _dt
from typing import Any, Literal, SupportsIndex, cast, overload
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from carbonic.core.date import Date
from carbonic.core.duration import Duration
from carbonic.core.exceptions import ParseError


DateTimeUnit = Literal[
    "second",
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "quarter",
    "year",
]
_MISSING: Any = ...


def _coerce_tzinfo(tz: str | _dt.tzinfo | None) -> _dt.tzinfo | None:
    if tz is None:
        return None
    if isinstance(tz, str):
        if tz.upper() == "Z":
            return _dt.timezone.utc
        return ZoneInfo(tz)
    return tz


def _last_day_of_month(year: int, month: int) -> int:
    if month == 12:
        next_month = _dt.date(year + 1, 1, 1)
    else:
        next_month = _dt.date(year, month + 1, 1)
    return (next_month - _dt.timedelta(days=1)).day


def _to_duration(delta: _dt.timedelta) -> Duration:
    return Duration(
        days=delta.days,
        seconds=delta.seconds,
        microseconds=delta.microseconds,
    )


class DateTime(_dt.datetime):
    """Carbonic datetime implemented as a native datetime.datetime subtype."""

    __slots__ = ()

    def __new__(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: _dt.tzinfo | None = None,
        *,
        fold: int = 0,
        tz: str | _dt.tzinfo | None = None,
    ) -> DateTime:
        if tz is not None and tzinfo is not None:
            raise TypeError("Use either tz or tzinfo, not both")

        resolved_tzinfo = _coerce_tzinfo(tz) if tz is not None else tzinfo
        return super().__new__(
            cls,
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond,
            resolved_tzinfo,
            fold=fold,
        )

    @classmethod
    def now(cls, tz: str | _dt.tzinfo | None = None) -> DateTime:
        """Return the current datetime using native datetime.now semantics."""
        return cls.from_datetime(_dt.datetime.now(_coerce_tzinfo(tz)))

    @classmethod
    def today(cls) -> DateTime:
        """Return the current local naive datetime using native semantics."""
        return cls.from_datetime(_dt.datetime.today())

    @classmethod
    def tomorrow(cls, tz: str | _dt.tzinfo | None = None) -> DateTime:
        """Return the current datetime plus one day."""
        return cls.now(tz).add(days=1)

    @classmethod
    def yesterday(cls, tz: str | _dt.tzinfo | None = None) -> DateTime:
        """Return the current datetime minus one day."""
        return cls.now(tz).subtract(days=1)

    @classmethod
    def next(
        cls,
        unit: DateTimeUnit,
        count: int = 1,
        tz: str | _dt.tzinfo | None = None,
    ) -> DateTime:
        """Return a datetime in the future relative to now()."""
        return cls._add_relative_unit(cls.now(tz), unit, count)

    @classmethod
    def previous(
        cls,
        unit: DateTimeUnit,
        count: int = 1,
        tz: str | _dt.tzinfo | None = None,
    ) -> DateTime:
        """Return a datetime in the past relative to now()."""
        return cls._add_relative_unit(cls.now(tz), unit, -count)

    @classmethod
    def _add_relative_unit(
        cls,
        value: DateTime,
        unit: DateTimeUnit,
        count: int,
    ) -> DateTime:
        if unit == "second":
            return value.add(seconds=count)
        if unit == "minute":
            return value.add(minutes=count)
        if unit == "hour":
            return value.add(hours=count)
        if unit == "day":
            return value.add(days=count)
        if unit == "week":
            return value.add(weeks=count)
        if unit == "month":
            return value.add(months=count)
        if unit == "quarter":
            return value.add(months=count * 3)
        if unit == "year":
            return value.add(years=count)
        raise ValueError(
            "Unsupported time unit for DateTime. "
            "Use 'second', 'minute', 'hour', 'day', 'week', 'month', "
            "'quarter', or 'year'."
        )

    @classmethod
    def from_datetime(cls, value: _dt.datetime) -> DateTime:
        """Create a Carbonic DateTime from a native datetime."""
        if isinstance(value, cls):
            return value

        return cls(
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
            tzinfo=value.tzinfo,
            fold=value.fold,
        )

    @classmethod
    def parse(
        cls,
        text: str,
        format_string: str | None = None,
        tz: str | _dt.tzinfo | None = None,
    ) -> DateTime:
        """Parse a datetime string.

        Without a format string, only ISO 8601 input is accepted. With a format
        string, Python strptime directives are required; Carbon tokens are not
        supported.
        """
        if not text or not text.strip():
            raise ParseError("Empty datetime string")

        value = text.strip()
        tzinfo = _coerce_tzinfo(tz)

        try:
            if format_string is None:
                parsed = _dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
            else:
                if "%" not in format_string:
                    raise ParseError(
                        "Explicit datetime formats must use Python strptime directives"
                    )
                parsed = _dt.datetime.strptime(value, format_string)

            if parsed.tzinfo is None:
                if tzinfo is not None:
                    parsed = parsed.replace(tzinfo=tzinfo)
            elif tzinfo is not None:
                parsed = parsed.astimezone(tzinfo)

            return cls.from_datetime(parsed)
        except ParseError:
            raise
        except ValueError as exc:
            raise ParseError(f"Failed to parse '{value}'") from exc

    def __repr__(self) -> str:
        args = [
            str(self.year),
            str(self.month),
            str(self.day),
            str(self.hour),
            str(self.minute),
            str(self.second),
        ]

        if self.microsecond:
            args.append(str(self.microsecond))

        if self.tzinfo is not None:
            args.append(f"tzinfo={self.tzinfo!r}")

        if self.fold:
            args.append(f"fold={self.fold}")

        return f"DateTime({', '.join(args)})"

    def __str__(self) -> str:
        return self.isoformat()

    def __format__(self, format_spec: str) -> str:
        if not format_spec:
            return str(self)
        return self.strftime(format_spec)

    def add(
        self,
        *,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
    ) -> DateTime:
        """Return a new datetime with the provided relative offset applied."""
        result = _dt.datetime.__add__(
            self,
            _dt.timedelta(
                weeks=weeks,
                days=days,
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                microseconds=microseconds,
            ),
        )

        if result is NotImplemented:
            raise TypeError("Unsupported timedelta operation")

        result = type(self).from_datetime(result)
        if not months and not years:
            return result

        month_index = result.year * 12 + (result.month - 1) + months + (years * 12)
        new_year, month_zero_index = divmod(month_index, 12)
        new_month = month_zero_index + 1
        new_day = min(result.day, _last_day_of_month(new_year, new_month))
        return result.replace(year=new_year, month=new_month, day=new_day)

    def subtract(
        self,
        *,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
    ) -> DateTime:
        """Return a new datetime with the provided offset subtracted."""
        return self.add(
            years=-years,
            months=-months,
            weeks=-weeks,
            days=-days,
            hours=-hours,
            minutes=-minutes,
            seconds=-seconds,
            microseconds=-microseconds,
        )

    def diff(self, other: _dt.datetime, *, absolute: bool = False) -> Duration:
        """Return a Duration representing the difference from another datetime."""
        if not isinstance(other, _dt.datetime):
            raise TypeError("DateTime.diff() expects a datetime-compatible value")

        delta = _dt.datetime.__sub__(self, other)
        if not isinstance(delta, _dt.timedelta):
            raise TypeError("DateTime.diff() expects a datetime-compatible value")
        if absolute:
            delta = abs(delta)
        return _to_duration(delta)

    def add_duration(self, duration: Duration) -> DateTime:
        """Add a Duration to this DateTime."""
        if not isinstance(duration, Duration):
            raise TypeError("add_duration() expects a Duration")

        result = self.add(
            years=duration.years,
            months=duration.months,
            days=duration.days,
            seconds=duration.storage_seconds,
            microseconds=duration.microseconds,
        )
        return result

    def subtract_duration(self, duration: Duration) -> DateTime:
        """Subtract a Duration from this DateTime."""
        if not isinstance(duration, Duration):
            raise TypeError("subtract_duration() expects a Duration")
        return self.add_duration(-duration)

    @overload  # type: ignore[override]
    def __add__(self, other: _dt.timedelta) -> DateTime: ...

    @overload
    def __add__(self, other: Duration) -> DateTime: ...

    def __add__(self, other: object) -> DateTime:
        if isinstance(other, Duration):
            return self.add_duration(other)
        if isinstance(other, _dt.timedelta):
            result = _dt.datetime.__add__(self, other)
            if result is NotImplemented:
                return NotImplemented
            return type(self).from_datetime(result)
        return NotImplemented

    @overload  # type: ignore[override]
    def __sub__(self, other: _dt.timedelta) -> DateTime: ...

    @overload
    def __sub__(self, other: Duration) -> DateTime: ...

    @overload
    def __sub__(self, other: _dt.datetime) -> Duration: ...

    def __sub__(self, other: object) -> DateTime | Duration:
        if isinstance(other, Duration):
            return self.subtract_duration(other)
        if isinstance(other, _dt.timedelta):
            result = _dt.datetime.__sub__(self, other)
            if result is NotImplemented:
                return NotImplemented
            return type(self).from_datetime(result)
        if isinstance(other, _dt.datetime):
            return self.diff(other)
        return NotImplemented

    def replace(  # type: ignore[override]
        self,
        year: SupportsIndex = _MISSING,
        month: SupportsIndex = _MISSING,
        day: SupportsIndex = _MISSING,
        hour: SupportsIndex = _MISSING,
        minute: SupportsIndex = _MISSING,
        second: SupportsIndex = _MISSING,
        microsecond: SupportsIndex = _MISSING,
        tzinfo: _dt.tzinfo | None = _MISSING,
        *,
        fold: int = _MISSING,
        tz: str | _dt.tzinfo | None = None,
    ) -> DateTime:
        if tz is not None:
            if tzinfo is not ...:
                raise TypeError("Use either tz or tzinfo, not both")
            tzinfo = _coerce_tzinfo(tz)

        kwargs: dict[str, Any] = {}
        for name, value in (
            ("year", year),
            ("month", month),
            ("day", day),
            ("hour", hour),
            ("minute", minute),
            ("second", second),
            ("microsecond", microsecond),
            ("tzinfo", tzinfo),
            ("fold", fold),
        ):
            if value is not ...:
                kwargs[name] = value

        return type(self).from_datetime(
            cast(_dt.datetime, _dt.datetime.replace(self, **kwargs))
        )

    def astimezone(self, tz: _dt.tzinfo | None = None) -> DateTime:
        return type(self).from_datetime(_dt.datetime.astimezone(self, tz))

    def as_timezone(self, tz: str | _dt.tzinfo | None) -> DateTime:
        """Convert this DateTime to a different timezone."""
        if self.tzinfo is None:
            if tz is not None:
                raise ValueError(
                    "Cannot convert naive DateTime to timezone-aware. "
                    "Create a new DateTime with timezone information first."
                )
            return self.replace()

        if tz is None:
            return self.replace(tzinfo=None)

        try:
            return self.astimezone(_coerce_tzinfo(tz))
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Invalid timezone: {tz}") from exc

    def start_of(
        self,
        unit: Literal["minute", "hour", "day", "week", "month", "quarter", "year"],
    ) -> DateTime:
        """Return the start of the requested period."""
        if unit == "minute":
            return self.replace(second=0, microsecond=0)
        if unit == "hour":
            return self.replace(minute=0, second=0, microsecond=0)
        if unit == "day":
            return self.replace(hour=0, minute=0, second=0, microsecond=0)
        if unit == "week":
            return self.subtract(days=self.weekday()).start_of("day")
        if unit == "month":
            return self.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if unit == "quarter":
            quarter_start_month = ((self.month - 1) // 3) * 3 + 1
            return self.replace(
                month=quarter_start_month,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        if unit == "year":
            return self.replace(
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        raise ValueError(f"Unknown unit: {unit}")

    def end_of(
        self,
        unit: Literal["minute", "hour", "day", "week", "month", "quarter", "year"],
    ) -> DateTime:
        """Return the end of the requested period."""
        if unit == "minute":
            return self.replace(second=59, microsecond=999999)
        if unit == "hour":
            return self.replace(minute=59, second=59, microsecond=999999)
        if unit == "day":
            return self.replace(hour=23, minute=59, second=59, microsecond=999999)
        if unit == "week":
            return self.add(days=6 - self.weekday()).end_of("day")
        if unit == "month":
            return self.replace(
                day=_last_day_of_month(self.year, self.month),
                hour=23,
                minute=59,
                second=59,
                microsecond=999999,
            )
        if unit == "quarter":
            quarter_end_month = ((self.month - 1) // 3) * 3 + 3
            return self.replace(
                month=quarter_end_month,
                day=_last_day_of_month(self.year, quarter_end_month),
                hour=23,
                minute=59,
                second=59,
                microsecond=999999,
            )
        if unit == "year":
            return self.replace(
                month=12,
                day=31,
                hour=23,
                minute=59,
                second=59,
                microsecond=999999,
            )
        raise ValueError(f"Unknown unit: {unit}")

    def to_date(self) -> Date:
        """Return this datetime's date as a Carbonic Date."""
        return Date(self.year, self.month, self.day)

    def to_datetime(self) -> _dt.datetime:
        """Return a plain native datetime.datetime copy."""
        return _dt.datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            self.tzinfo,
            fold=self.fold,
        )
