"""Carbonic localization system.

This module provides comprehensive internationalization support for the Carbonic
datetime library, including pluralization rules, number formatting, and
localized names for time units, months, and days.

Supported locales:
- English (en): Default locale with standard English pluralization
- Polish (pl): Complex pluralization rules and Polish translations

Example:
    >>> from carbonic.locale import get_locale
    >>> locale = get_locale("pl")
    >>> locale.get_duration_unit_name("day", 5)
    'dni'
"""

from .base import Locale, get_locale, is_locale_available, register_locale
from .en import EnglishLocale
from .pl import PolishLocale

# Register default locales
register_locale(EnglishLocale())
register_locale(PolishLocale())

__all__ = [
    "Locale",
    "get_locale",
    "register_locale",
    "is_locale_available",
    "EnglishLocale",
    "PolishLocale",
]
