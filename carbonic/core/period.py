"""Period implementation for Carbonic.

This module provides the Period class for semantic datetime operations using
named time periods like Period.DAY, Period.MONTH, etc. This enables more
readable and maintainable date/datetime manipulation code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Literal

if TYPE_CHECKING:
    from carbonic.core.date import Date
    from carbonic.core.datetime import DateTime


@dataclass(frozen=True, slots=True)
class Period:
    """Represents a named time period for semantic datetime operations.

    Provides named constants like Period.DAY, Period.MONTH, etc. for
    more readable and semantic datetime arithmetic operations.

    Examples:
        Period.MONTH.add_to(date)           # Add 1 month to date
        Period.WEEK.subtract_from(date)     # Subtract 1 week from date
        Period.QUARTER.start_of(date)       # Start of current quarter
        Period.YEAR.end_of(date)            # End of current year
        Period.DAY.add_to(date, count=5)    # Add 5 days to date
    """

    name: str
    _type: Literal["minute", "hour", "day", "week", "month", "quarter", "year"]

    # Class variable declarations for type checking
    MINUTE: ClassVar["Period"]
    HOUR: ClassVar["Period"]
    DAY: ClassVar["Period"]
    WEEK: ClassVar["Period"]
    MONTH: ClassVar["Period"]
    QUARTER: ClassVar["Period"]
    YEAR: ClassVar["Period"]

    def add_to(self, dt: Date | DateTime, *, count: int = 1) -> Date | DateTime:
        """Add this period to a Date or DateTime.

        Args:
            dt: The Date or DateTime to add to
            count: Number of periods to add (default: 1)

        Returns:
            New Date or DateTime with the period added
        """
        if self._type == "minute":
            if hasattr(dt, "hour"):  # DateTime has hour attribute, Date doesn't
                return dt.add(minutes=count)  # type: ignore[call-arg]
            else:
                raise ValueError("Cannot add minutes to Date (use DateTime)")
        elif self._type == "hour":
            if hasattr(dt, "hour"):  # DateTime has hour attribute, Date doesn't
                return dt.add(hours=count)  # type: ignore[call-arg]
            else:
                raise ValueError("Cannot add hours to Date (use DateTime)")
        elif self._type == "day":
            return dt.add(days=count)
        elif self._type == "week":
            # Convert weeks to days since add() doesn't support weeks directly
            return dt.add(days=count * 7)
        elif self._type == "month":
            return dt.add(months=count)
        elif self._type == "quarter":
            return dt.add(months=count * 3)
        elif self._type == "year":
            return dt.add(years=count)
        else:
            raise ValueError(f"Unknown period type: {self._type}")

    def subtract_from(self, dt: Date | DateTime, *, count: int = 1) -> Date | DateTime:
        """Subtract this period from a Date or DateTime.

        Args:
            dt: The Date or DateTime to subtract from
            count: Number of periods to subtract (default: 1)

        Returns:
            New Date or DateTime with the period subtracted
        """
        if self._type == "minute":
            if hasattr(dt, "hour"):  # DateTime has hour attribute, Date doesn't
                return dt.subtract(minutes=count)  # type: ignore[call-arg]
            else:
                raise ValueError("Cannot subtract minutes from Date (use DateTime)")
        elif self._type == "hour":
            if hasattr(dt, "hour"):  # DateTime has hour attribute, Date doesn't
                return dt.subtract(hours=count)  # type: ignore[call-arg]
            else:
                raise ValueError("Cannot subtract hours from Date (use DateTime)")
        elif self._type == "day":
            return dt.subtract(days=count)
        elif self._type == "week":
            # Convert weeks to days since subtract() doesn't support weeks directly
            return dt.subtract(days=count * 7)
        elif self._type == "month":
            return dt.subtract(months=count)
        elif self._type == "quarter":
            return dt.subtract(months=count * 3)
        elif self._type == "year":
            return dt.subtract(years=count)
        else:
            raise ValueError(f"Unknown period type: {self._type}")

    def start_of(self, dt: Date | DateTime) -> Date | DateTime:
        """Get the start of this period for the given date/datetime.

        Args:
            dt: The Date or DateTime to get the period start for

        Returns:
            New Date or DateTime at the start of the period
        """
        # Check if the period type is supported for this datetime type
        if hasattr(dt, "start_of"):
            try:
                return dt.start_of(self._type)  # type: ignore[arg-type]
            except (ValueError, TypeError):
                if self._type in ("minute", "hour") and not hasattr(dt, "hour"):
                    raise ValueError(
                        f"Cannot get start of {self._type} for Date (use DateTime)"
                    )
                raise

        raise ValueError(f"start_of not supported for {type(dt)}")

    def end_of(self, dt: Date | DateTime) -> Date | DateTime:
        """Get the end of this period for the given date/datetime.

        Args:
            dt: The Date or DateTime to get the period end for

        Returns:
            New Date or DateTime at the end of the period
        """
        # Check if the period type is supported for this datetime type
        if hasattr(dt, "end_of"):
            try:
                return dt.end_of(self._type)  # type: ignore[arg-type]
            except (ValueError, TypeError):
                if self._type in ("minute", "hour") and not hasattr(dt, "hour"):
                    raise ValueError(
                        f"Cannot get end of {self._type} for Date (use DateTime)"
                    )
                raise

        raise ValueError(f"end_of not supported for {type(dt)}")

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return self.name

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"Period.{self.name.upper()}"


# Define Period class first, then add constants at module level after the class definition
# This avoids the type checker issue with Period.CONSTANT = ...

# Named period constants - similar to enum but with more flexibility
MINUTE = Period("minute", "minute")
HOUR = Period("hour", "hour")
DAY = Period("day", "day")
WEEK = Period("week", "week")
MONTH = Period("month", "month")
QUARTER = Period("quarter", "quarter")
YEAR = Period("year", "year")

# Assign the constants to the class
Period.MINUTE = MINUTE
Period.HOUR = HOUR
Period.DAY = DAY
Period.WEEK = WEEK
Period.MONTH = MONTH
Period.QUARTER = QUARTER
Period.YEAR = YEAR
