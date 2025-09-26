"""Polish locale implementation."""

from __future__ import annotations

from .base import Locale


class PolishLocale(Locale):
    """Polish locale implementation with complex pluralization rules."""

    def __init__(self):
        super().__init__("pl", "Polski")

    def pluralize(
        self, count: int | float, singular: str, plural: str, many: str | None = None
    ) -> str:
        """Polish pluralization rules:
        - 1: singular form (1 dzień)
        - 2-4 (but not 12-14): plural form (2 dni, 3 dni, 4 dni)
        - 0.5, 1.5, 2.5, etc.: plural form (0,5 sekundy, 1,5 sekundy)
        - 5+, 0, 12-14: many form (5 dni, 10 dni, 12 dni, 13 dni, 14 dni)
        - 22, 23, 24, 32, 33, 34, etc.: plural form (22 dni, 23 dni)
        """
        if many is None:
            many = plural

        abs_count = abs(count)

        # Handle fractional numbers - use plural form for decimals
        if abs_count != int(abs_count):
            return plural

        abs_count = int(abs_count)

        # 1 - singular
        if abs_count == 1:
            return singular

        # Complex Polish rules for integers
        last_digit = abs_count % 10
        last_two_digits = abs_count % 100

        # 12-14 - many form (teens are special)
        if 12 <= last_two_digits <= 14:
            return many
        # 2-4 - plural form
        elif 2 <= last_digit <= 4:
            return plural
        # Everything else - many form
        else:
            return many

    def format_number(self, number: float) -> str:
        """Format number using Polish conventions (decimal comma)."""
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
        """Get Polish duration unit names with proper pluralization."""
        unit_names = {
            "second": ("sekunda", "sekundy", "sekund"),
            "minute": ("minuta", "minuty", "minut"),
            "hour": ("godzina", "godziny", "godzin"),
            "day": ("dzień", "dni", "dni"),
            "week": ("tydzień", "tygodnie", "tygodni"),
            "month": ("miesiąc", "miesiące", "miesięcy"),
            "year": ("rok", "lata", "lat"),
        }

        if unit not in unit_names:
            raise ValueError(f"Unknown unit: {unit}")

        singular, plural, many = unit_names[unit]
        return self.pluralize(count, singular, plural, many)

    def get_month_name(self, month: int, short: bool = False) -> str:
        """Get Polish month names."""
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be 1-12, got {month}")

        full_names = [
            "styczeń",
            "luty",
            "marzec",
            "kwiecień",
            "maj",
            "czerwiec",
            "lipiec",
            "sierpień",
            "wrzesień",
            "październik",
            "listopad",
            "grudzień",
        ]

        short_names = [
            "sty",
            "lut",
            "mar",
            "kwi",
            "maj",
            "cze",
            "lip",
            "sie",
            "wrz",
            "paź",
            "lis",
            "gru",
        ]

        return short_names[month - 1] if short else full_names[month - 1]

    def get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get Polish day names."""
        if not (0 <= weekday <= 6):
            raise ValueError(f"Weekday must be 0-6 (Monday-Sunday), got {weekday}")

        full_names = [
            "poniedziałek",
            "wtorek",
            "środa",
            "czwartek",
            "piątek",
            "sobota",
            "niedziela",
        ]

        short_names = ["pon", "wto", "śro", "czw", "pią", "sob", "nie"]

        return short_names[weekday] if short else full_names[weekday]
