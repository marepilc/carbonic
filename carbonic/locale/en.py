"""English locale implementation."""

from __future__ import annotations

import calendar

from .base import Locale


class EnglishLocale(Locale):
    """English locale implementation."""

    def __init__(self):
        super().__init__("en", "English")

    def pluralize(
        self, count: int | float, singular: str, plural: str, many: str | None = None
    ) -> str:
        """English pluralization: singular for 1, plural for everything else."""
        if abs(count) == 1:
            return singular
        return plural

    def format_number(self, number: float) -> str:
        """Format number using English conventions (decimal point)."""
        if number == int(number):
            return str(int(number))

        # Format with up to 6 decimal places, removing trailing zeros
        formatted = f"{number:.6f}".rstrip("0").rstrip(".")
        return formatted if formatted else "0"

    def get_duration_unit_name(self, unit: str, count: int | float) -> str:
        """Get English duration unit names with proper pluralization."""
        unit_names = {
            "second": ("second", "seconds"),
            "minute": ("minute", "minutes"),
            "hour": ("hour", "hours"),
            "day": ("day", "days"),
            "week": ("week", "weeks"),
            "month": ("month", "months"),
            "year": ("year", "years"),
        }

        if unit not in unit_names:
            raise ValueError(f"Unknown unit: {unit}")

        singular, plural = unit_names[unit]
        return self.pluralize(count, singular, plural)

    def get_month_name(self, month: int, short: bool = False) -> str:
        """Get English month names using Python's calendar module."""
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be 1-12, got {month}")

        return calendar.month_abbr[month] if short else calendar.month_name[month]

    def get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get English day names using Python's calendar module."""
        if not (0 <= weekday <= 6):
            raise ValueError(f"Weekday must be 0-6 (Monday-Sunday), got {weekday}")

        return calendar.day_abbr[weekday] if short else calendar.day_name[weekday]
