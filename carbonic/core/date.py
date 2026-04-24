"""Native date subtype for Carbonic."""

from __future__ import annotations

import datetime as _dt
from typing import Callable, Literal, Protocol, cast, overload
from zoneinfo import ZoneInfo

from carbonic.core.duration import Duration
from carbonic.core.exceptions import ParseError
from carbonic.enums.weekday import Weekday


DateUnit = Literal["day", "week", "month", "quarter", "year"]
DateNavigationTarget = DateUnit | Weekday
_YEAR_DIRECTIVES = ("%Y", "%y", "%G")
_MONTH_DIRECTIVES = ("%m", "%b", "%B")
_DAY_DIRECTIVES = ("%d", "%e")
_DAY_OF_YEAR_DIRECTIVES = ("%j",)


class _DateInstanceNavigation(Protocol):
    def __call__(self, target: DateNavigationTarget, count: int = 1) -> Date: ...


class _DateClassNavigation(Protocol):
    def __call__(
        self,
        unit: DateUnit,
        count: int = 1,
        tz: str | _dt.tzinfo | None = None,
    ) -> Date: ...


_DateInstanceMethod = Callable[["Date", DateNavigationTarget, int], "Date"]
_DateClassMethod = Callable[
    [type["Date"], DateUnit, int, str | _dt.tzinfo | None],
    "Date",
]


class _DualMethod:
    """Descriptor that dispatches to class or instance implementation."""

    def __init__(
        self,
        instance_func: _DateInstanceMethod,
        class_func: _DateClassMethod,
    ):
        self.instance_func: _DateInstanceMethod = instance_func
        self.class_func: _DateClassMethod = class_func

    @overload
    def __get__(self, obj: None, owner: type[Date]) -> _DateClassNavigation: ...

    @overload
    def __get__(self, obj: Date, owner: type[Date]) -> _DateInstanceNavigation: ...

    def __get__(self, obj, owner):
        if obj is None:
            def class_bound(
                unit: DateUnit,
                count: int = 1,
                tz: str | _dt.tzinfo | None = None,
            ) -> Date:
                return self.class_func(owner, unit, count, tz)

            return class_bound

        def bound(target: DateNavigationTarget, count: int = 1) -> Date:
            return self.instance_func(obj, target, count)

        return bound


def _coerce_tzinfo(tz: str | _dt.tzinfo | None) -> _dt.tzinfo | None:
    """Convert a timezone string or tzinfo object to tzinfo."""
    if tz is None:
        return None
    if isinstance(tz, str):
        return ZoneInfo(tz)
    return tz


def _last_day_of_month(year: int, month: int) -> int:
    """Return the last day number for the given month."""
    if month == 12:
        next_month = _dt.date(year + 1, 1, 1)
    else:
        next_month = _dt.date(year, month + 1, 1)
    return (next_month - _dt.timedelta(days=1)).day


def _validate_explicit_date_format(format_string: str) -> None:
    """Reject explicit formats that do not describe a full calendar date."""
    normalized = format_string.replace("%%", "")

    has_year = any(token in normalized for token in _YEAR_DIRECTIVES)
    if not has_year:
        raise ParseError("Explicit date formats must include a year component")

    has_day_of_year = any(token in normalized for token in _DAY_OF_YEAR_DIRECTIVES)
    if has_day_of_year:
        return

    has_month = any(token in normalized for token in _MONTH_DIRECTIVES)
    has_day = any(token in normalized for token in _DAY_DIRECTIVES)
    if not has_month or not has_day:
        raise ParseError(
            "Explicit date formats must include year, month, and day components"
        )


class Date(_dt.date):
    """Carbonic date implemented as a native datetime.date subtype."""

    __slots__ = ()
    next: _DualMethod
    previous: _DualMethod

    @classmethod
    def from_date(cls, value: _dt.date) -> Date:
        """Create a Carbonic Date from a native date."""
        if isinstance(value, cls):
            return value
        return cls(value.year, value.month, value.day)

    @classmethod
    def today(cls, tz: str | _dt.tzinfo | None = None) -> Date:
        """Return today's date, optionally in the provided timezone."""
        if tz is None:
            today_value = _dt.date.today()
        else:
            today_value = _dt.datetime.now(_coerce_tzinfo(tz)).date()
        return cls.from_date(today_value)

    @classmethod
    def tomorrow(cls, tz: str | _dt.tzinfo | None = None) -> Date:
        """Return tomorrow's date."""
        return cls.today(tz).add(days=1)

    @classmethod
    def yesterday(cls, tz: str | _dt.tzinfo | None = None) -> Date:
        """Return yesterday's date."""
        return cls.today(tz).subtract(days=1)

    def _next_from_self(
        self: Date,
        target: DateNavigationTarget,
        count: int = 1,
    ) -> Date:
        """Return the next weekday or relative unit from this date."""
        if isinstance(target, Weekday):
            return self._shift_to_weekday(target, count, direction=1)
        return type(self)._add_relative_unit(self, target, count)

    @classmethod
    def _next_from_today(
        cls,
        unit: DateUnit,
        count: int = 1,
        tz: str | _dt.tzinfo | None = None,
    ) -> Date:
        """Return a future date relative to today()."""
        return cls._add_relative_unit(cls.today(tz), unit, count)

    def _previous_from_self(
        self: Date,
        target: DateNavigationTarget,
        count: int = 1,
    ) -> Date:
        """Return the previous weekday or relative unit from this date."""
        if isinstance(target, Weekday):
            return self._shift_to_weekday(target, count, direction=-1)
        return type(self)._add_relative_unit(self, target, -count)

    @classmethod
    def _previous_from_today(
        cls,
        unit: DateUnit,
        count: int = 1,
        tz: str | _dt.tzinfo | None = None,
    ) -> Date:
        """Return a past date relative to today()."""
        return cls._add_relative_unit(cls.today(tz), unit, -count)

    @classmethod
    def _add_relative_unit(cls, date: Date, unit: DateUnit, count: int) -> Date:
        if unit == "day":
            return date.add(days=count)
        if unit == "week":
            return date.add(weeks=count)
        if unit == "month":
            return date.add(months=count)
        if unit == "quarter":
            return date.add(months=count * 3)
        if unit == "year":
            return date.add(years=count)
        raise ValueError(
            "Unsupported time unit for Date. "
            "Use 'day', 'week', 'month', 'quarter', or 'year'."
        )

    def _shift_to_weekday(self, target: Weekday, count: int, *, direction: int) -> Date:
        """Shift to the next or previous weekday occurrence."""
        if count == 0:
            return self
        if count < 0:
            opposite = -direction
            return self._shift_to_weekday(target, -count, direction=opposite)

        current_weekday = self.weekday()
        target_weekday = target.value

        if direction > 0:
            delta = (target_weekday - current_weekday) % 7
            if delta == 0:
                delta = 7
            delta += (count - 1) * 7
            return self.add(days=delta)

        delta = (current_weekday - target_weekday) % 7
        if delta == 0:
            delta = 7
        delta += (count - 1) * 7
        return self.subtract(days=delta)

    @classmethod
    def parse(cls, text: str, format_string: str | None = None) -> Date:
        """Parse a date string.

        If the format string is omitted, only ISO 8601 YYYY-MM-DD parsing is supported.
        If a format string is provided, it must use Python strptime directives.
        """
        if not text or not text.strip():
            raise ParseError("Empty date string")

        text = text.strip()

        try:
            if format_string is None:
                return cls.fromisoformat(text)

            if "%" not in format_string:
                raise ParseError(
                    "Explicit date formats must use Python strptime directives"
                )

            _validate_explicit_date_format(format_string)
            parsed = _dt.datetime.strptime(text, format_string).date()
            return cls.from_date(parsed)
        except ValueError as exc:
            raise ParseError(f"Failed to parse '{text}'") from exc

    def __format__(self, format_spec: str) -> str:
        """Support format() and f-strings using strftime semantics."""
        if not format_spec:
            return str(self)
        return self.strftime(format_spec)

    def strftime(self, format_string: str) -> str:
        """Format the date using Python strftime directives.

        A small portability layer is included for common Unix directives that
        fail on Windows, such as %-m and %-d.
        """
        try:
            return super().strftime(format_string)
        except ValueError as exc:
            return self._portable_strftime(format_string, exc)

    @staticmethod
    def _portable_tokens(date: Date) -> dict[str, str]:
        return {
            "%-d": str(date.day),
            "%-m": str(date.month),
        }

    def _portable_strftime(
        self,
        format_string: str,
        original_error: ValueError,
    ) -> str:
        """Handle a limited set of non-portable directives on Windows."""
        tokens = self._portable_tokens(self)
        if not any(token in format_string for token in tokens):
            raise original_error

        placeholder_format = format_string
        replacements: dict[str, str] = {}

        for index, (token, value) in enumerate(tokens.items()):
            placeholder = f"__carbonic_portable_{index}__"
            if token in placeholder_format:
                placeholder_format = placeholder_format.replace(token, placeholder)
                replacements[placeholder] = value

        result = super().strftime(placeholder_format)
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        return result

    def add(
        self,
        *,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
    ) -> Date:
        """Return a new date with the provided relative offset applied."""
        result: Date = self + _dt.timedelta(days=days + (weeks * 7))

        if not months and not years:
            return type(self).from_date(result)

        month_index = result.year * 12 + (result.month - 1) + months + (years * 12)
        new_year, month_zero_index = divmod(month_index, 12)
        new_month = month_zero_index + 1
        new_day = min(result.day, _last_day_of_month(new_year, new_month))
        return type(self)(new_year, new_month, new_day)

    def subtract(
        self,
        *,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
    ) -> Date:
        """Return a new date with the provided offset subtracted."""
        return self.add(years=-years, months=-months, weeks=-weeks, days=-days)

    def diff(self, other: _dt.date, *, absolute: bool = False) -> Duration:
        """Return a Duration representing the day difference."""
        if isinstance(other, _dt.datetime):
            raise TypeError("Date.diff() expects a date, not a datetime")
        if not isinstance(other, _dt.date):
            raise TypeError("Date.diff() expects a datetime.date-compatible value")

        day_delta = (self.to_date() - _dt.date(other.year, other.month, other.day)).days
        if absolute:
            day_delta = abs(day_delta)
        return Duration(days=day_delta)

    def start_of(self, unit: Literal["day", "week", "month", "quarter", "year"]) -> Date:
        """Return the start of the requested period."""
        if unit == "day":
            return self
        if unit == "week":
            return self.subtract(days=self.weekday())
        if unit == "month":
            return type(self)(self.year, self.month, 1)
        if unit == "quarter":
            quarter_start_month = ((self.month - 1) // 3) * 3 + 1
            return type(self)(self.year, quarter_start_month, 1)
        if unit == "year":
            return type(self)(self.year, 1, 1)
        raise ValueError(f"Unknown unit: {unit}")

    def end_of(self, unit: Literal["day", "week", "month", "quarter", "year"]) -> Date:
        """Return the end of the requested period."""
        if unit == "day":
            return self
        if unit == "week":
            return self.add(days=6 - self.weekday())
        if unit == "month":
            return type(self)(self.year, self.month, _last_day_of_month(self.year, self.month))
        if unit == "quarter":
            quarter_end_month = ((self.month - 1) // 3) * 3 + 3
            return type(self)(
                self.year,
                quarter_end_month,
                _last_day_of_month(self.year, quarter_end_month),
            )
        if unit == "year":
            return type(self)(self.year, 12, 31)
        raise ValueError(f"Unknown unit: {unit}")

    def is_weekday(self) -> bool:
        """Return True when the date is Monday through Friday."""
        return self.weekday() < 5

    def is_weekend(self) -> bool:
        """Return True when the date is Saturday or Sunday."""
        return self.weekday() >= 5

    def add_business_days(self, days: int) -> Date:
        """Add business days while skipping weekends."""
        if not isinstance(days, int):
            raise TypeError("days must be an integer")
        if days < 0:
            return self.subtract_business_days(-days)
        if days == 0:
            return self.add(days=(1 if self.weekday() == 6 else 2)) if self.is_weekend() else self

        current: Date = self
        remaining = days

        if current.is_weekend():
            current = current.add(days=(1 if current.weekday() == 6 else 2))
            remaining -= 1

        full_weeks, remaining = divmod(remaining, 5)
        if full_weeks:
            current = current.add(days=full_weeks * 7)

        for _ in range(remaining):
            current = current.add(days=1)
            if current.weekday() == 5:
                current = current.add(days=2)

        return current

    def subtract_business_days(self, days: int) -> Date:
        """Subtract business days while skipping weekends."""
        if not isinstance(days, int):
            raise TypeError("days must be an integer")
        if days < 0:
            return self.add_business_days(-days)
        if days == 0:
            return (
                self.subtract(days=(1 if self.weekday() == 5 else 2))
                if self.is_weekend()
                else self
            )

        current: Date = self
        remaining = days

        if current.is_weekend():
            current = current.subtract(days=(1 if current.weekday() == 5 else 2))
            remaining -= 1

        full_weeks, remaining = divmod(remaining, 5)
        if full_weeks:
            current = current.subtract(days=full_weeks * 7)

        for _ in range(remaining):
            current = current.subtract(days=1)
            if current.weekday() == 6:
                current = current.subtract(days=2)

        return current

    def to_datetime(self, tz: str | _dt.tzinfo | None = "UTC") -> _dt.datetime:
        """Return this date as a native datetime.datetime at midnight."""
        tzinfo = _coerce_tzinfo(tz)
        return _dt.datetime(self.year, self.month, self.day, tzinfo=tzinfo)

    def to_date(self) -> _dt.date:
        """Return a plain native datetime.date copy."""
        return _dt.date(self.year, self.month, self.day)

    next = _DualMethod(_next_from_self, cast(classmethod, _next_from_today).__func__)
    previous = _DualMethod(
        _previous_from_self,
        cast(classmethod, _previous_from_today).__func__,
    )
