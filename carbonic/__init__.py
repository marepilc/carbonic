"""
Carbonic - A modern Python datetime library with fluent API and immutable design.

A fluent, immutable datetime library built with dataclasses and stdlib zoneinfo.
"""

from carbonic.core.date import Date
from carbonic.core.datetime import DateTime
from carbonic.core.duration import Duration
from carbonic.core.interval import Interval
from carbonic.core.period import Period

__version__ = "1.0.0"

__all__ = [
    "DateTime",
    "Date",
    "Duration",
    "Period",
    "Interval",
    "now",
    "today",
    "tomorrow",
    "yesterday",
]


# Convenience functions for common operations
def now(tz: str | None = "UTC") -> DateTime:
    """Create a DateTime instance for the current moment."""
    return DateTime.now(tz)


def today(tz: str | None = None) -> Date:
    """Create a Date instance for today."""
    return Date.today(tz)


def tomorrow() -> Date:
    """Create a Date instance for tomorrow."""
    return Date.tomorrow()


def yesterday() -> Date:
    """Create a Date instance for yesterday."""
    return Date.yesterday()
