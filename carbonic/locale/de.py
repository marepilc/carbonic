"""German locale implementation."""

from __future__ import annotations

from .base import Locale


class GermanLocale(Locale):
    """German locale implementation."""

    def __init__(self):
        super().__init__("de", "Deutsch")

    def pluralize(
        self, count: int | float, singular: str, plural: str, many: str | None = None
    ) -> str:
        """German pluralization: singular for 1, plural for everything else."""
        if abs(count) == 1:
            return singular
        return plural

    def format_number(self, number: float) -> str:
        """Format number using German conventions (decimal comma)."""
        if number == int(number):
            return str(int(number))

        # Format with up to 6 decimal places, removing trailing zeros
        formatted = f"{number:.6f}".rstrip("0").rstrip(".")
        if formatted:
            # Replace decimal point with comma
            formatted = formatted.replace(".", ",")
        else:
            formatted = "0"

        return formatted

    def get_duration_unit_name(self, unit: str, count: int | float) -> str:
        """Get German duration unit names with proper pluralization."""
        unit_names = {
            "second": ("Sekunde", "Sekunden"),
            "minute": ("Minute", "Minuten"),
            "hour": ("Stunde", "Stunden"),
            "day": ("Tag", "Tage"),
            "week": ("Woche", "Wochen"),
            "month": ("Monat", "Monate"),
            "year": ("Jahr", "Jahre"),
        }

        if unit not in unit_names:
            raise ValueError(f"Unknown unit: {unit}")

        singular, plural = unit_names[unit]
        return self.pluralize(count, singular, plural)

    def get_month_name(self, month: int, short: bool = False) -> str:
        """Get German month names."""
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be 1-12, got {month}")

        full_names = [
            "Januar",
            "Februar",
            "März",
            "April",
            "Mai",
            "Juni",
            "Juli",
            "August",
            "September",
            "Oktober",
            "November",
            "Dezember",
        ]

        short_names = [
            "Jan",
            "Feb",
            "Mär",
            "Apr",
            "Mai",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Okt",
            "Nov",
            "Dez",
        ]

        return short_names[month - 1] if short else full_names[month - 1]

    def get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get German day names."""
        if not (0 <= weekday <= 6):
            raise ValueError(f"Weekday must be 0-6 (Monday-Sunday), got {weekday}")

        full_names = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag",
        ]

        short_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

        return short_names[weekday] if short else full_names[weekday]
