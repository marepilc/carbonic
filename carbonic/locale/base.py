"""Base localization infrastructure for Carbonic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class Locale(ABC):
    """Abstract base class for locales."""

    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    @abstractmethod
    def pluralize(
        self, count: int | float, singular: str, plural: str, many: str | None = None
    ) -> str:
        """Return the correct plural form based on count and locale rules.

        Args:
            count: The number to use for pluralization
            singular: Singular form (e.g., "day")
            plural: Plural form for 2-4 in languages that have it (e.g., "days")
            many: Many form for 5+ in languages that have it (e.g., "days")

        Returns:
            The correct plural form
        """
        pass

    @abstractmethod
    def format_number(self, number: float) -> str:
        """Format number according to locale conventions (decimal separator, etc.)."""
        pass

    @abstractmethod
    def get_duration_unit_name(self, unit: str, count: int | float) -> str:
        """Get the localized name for a duration unit.

        Args:
            unit: The unit name ("second", "minute", "hour", "day", "week", "month", "year")
            count: The count to determine plural form

        Returns:
            Localized unit name
        """
        pass

    @abstractmethod
    def get_month_name(self, month: int, short: bool = False) -> str:
        """Get localized month name.

        Args:
            month: Month number (1-12)
            short: Whether to return short form

        Returns:
            Localized month name
        """
        pass

    @abstractmethod
    def get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get localized day name.

        Args:
            weekday: Weekday number (0=Monday, 6=Sunday)
            short: Whether to return short form

        Returns:
            Localized day name
        """
        pass


# Global registry of locales
_LOCALES: Dict[str, Locale] = {}


def register_locale(locale: Locale) -> None:
    """Register a locale in the global registry."""
    _LOCALES[locale.code] = locale


def is_locale_available(code: str) -> bool:
    """Check if a locale is available.

    Args:
        code: Locale code (e.g., "en", "pl")

    Returns:
        True if the locale is registered, False otherwise
    """
    return code in _LOCALES


def get_locale(code: str | None) -> Locale:
    """Get a locale by code, defaulting to English if None or not found.

    Args:
        code: Locale code (e.g., "en", "pl") or None for default

    Returns:
        Locale instance

    Raises:
        ValueError: If locale code is not supported
    """
    if code is None:
        code = "en"

    if code not in _LOCALES:
        raise ValueError(f"Unsupported locale: {code}")

    return _LOCALES[code]
