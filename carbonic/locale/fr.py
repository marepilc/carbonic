"""French locale implementation."""

from __future__ import annotations

from .base import Locale


class FrenchLocale(Locale):
    """French locale implementation."""

    def __init__(self):
        super().__init__("fr", "Français")

    def pluralize(
        self, count: int | float, singular: str, plural: str, many: str | None = None
    ) -> str:
        """French pluralization: singular for 1, plural for everything else."""
        if abs(count) == 1:
            return singular
        return plural

    def format_number(self, number: float) -> str:
        """Format number using French conventions (decimal comma)."""
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
        """Get French duration unit names with proper pluralization."""
        unit_names = {
            "second": ("seconde", "secondes"),
            "minute": ("minute", "minutes"),
            "hour": ("heure", "heures"),
            "day": ("jour", "jours"),
            "week": ("semaine", "semaines"),
            "month": ("mois", "mois"),  # "mois" is invariant in French
            "year": ("an", "ans"),
        }

        if unit not in unit_names:
            raise ValueError(f"Unknown unit: {unit}")

        singular, plural = unit_names[unit]
        return self.pluralize(count, singular, plural)

    def get_month_name(self, month: int, short: bool = False) -> str:
        """Get French month names."""
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be 1-12, got {month}")

        full_names = [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ]

        short_names = [
            "jan",
            "fév",
            "mar",
            "avr",
            "mai",
            "jun",
            "jul",
            "aoû",
            "sep",
            "oct",
            "nov",
            "déc",
        ]

        return short_names[month - 1] if short else full_names[month - 1]

    def get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get French day names."""
        if not (0 <= weekday <= 6):
            raise ValueError(f"Weekday must be 0-6 (Monday-Sunday), got {weekday}")

        full_names = [
            "lundi",
            "mardi",
            "mercredi",
            "jeudi",
            "vendredi",
            "samedi",
            "dimanche",
        ]

        short_names = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"]

        return short_names[weekday] if short else full_names[weekday]
