"""Portuguese locale implementation."""

from __future__ import annotations

from .base import Locale


class PortugueseLocale(Locale):
    """Portuguese locale implementation."""

    def __init__(self):
        super().__init__("pt", "Português")

    def pluralize(
        self, count: int | float, singular: str, plural: str, many: str | None = None
    ) -> str:
        """Portuguese pluralization: singular for 1, plural for everything else."""
        if abs(count) == 1:
            return singular
        return plural

    def format_number(self, number: float) -> str:
        """Format number using Portuguese conventions (decimal comma)."""
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
        """Get Portuguese duration unit names with proper pluralization."""
        unit_names = {
            "second": ("segundo", "segundos"),
            "minute": ("minuto", "minutos"),
            "hour": ("hora", "horas"),
            "day": ("dia", "dias"),
            "week": ("semana", "semanas"),
            "month": ("mês", "meses"),
            "year": ("ano", "anos"),
        }

        if unit not in unit_names:
            raise ValueError(f"Unknown unit: {unit}")

        singular, plural = unit_names[unit]
        return self.pluralize(count, singular, plural)

    def get_month_name(self, month: int, short: bool = False) -> str:
        """Get Portuguese month names."""
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be 1-12, got {month}")

        full_names = [
            "janeiro",
            "fevereiro",
            "março",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        ]

        short_names = [
            "jan",
            "fev",
            "mar",
            "abr",
            "mai",
            "jun",
            "jul",
            "ago",
            "set",
            "out",
            "nov",
            "dez",
        ]

        return short_names[month - 1] if short else full_names[month - 1]

    def get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get Portuguese day names."""
        if not (0 <= weekday <= 6):
            raise ValueError(f"Weekday must be 0-6 (Monday-Sunday), got {weekday}")

        full_names = [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ]

        short_names = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

        return short_names[weekday] if short else full_names[weekday]
