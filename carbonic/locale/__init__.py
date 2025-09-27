"""Carbonic localization system.

This module provides comprehensive internationalization support for the Carbonic
datetime library, including pluralization rules, number formatting, and
localized names for time units, months, and days.

Supported locales:
- English (en): Default locale with standard English pluralization
- Polish (pl): Complex pluralization rules and Polish translations
- Spanish (es): Spanish localization with decimal comma formatting
- French (fr): French localization with decimal comma formatting
- German (de): German localization with decimal comma formatting
- Portuguese (pt): Portuguese localization with decimal comma formatting

Example:
    >>> from carbonic.locale import get_locale
    >>> locale = get_locale("pl")
    >>> locale.get_duration_unit_name("day", 5)
    'dni'
"""

from .base import Locale, get_locale, is_locale_available, register_locale
from .de import GermanLocale
from .en import EnglishLocale
from .es import SpanishLocale
from .fr import FrenchLocale
from .pl import PolishLocale
from .pt import PortugueseLocale

# Register default locales
register_locale(EnglishLocale())
register_locale(PolishLocale())
register_locale(SpanishLocale())
register_locale(FrenchLocale())
register_locale(GermanLocale())
register_locale(PortugueseLocale())

__all__ = [
    "Locale",
    "get_locale",
    "register_locale",
    "is_locale_available",
    "EnglishLocale",
    "PolishLocale",
    "SpanishLocale",
    "FrenchLocale",
    "GermanLocale",
    "PortugueseLocale",
]
