"""Carbonic localization system."""

from .base import Locale, get_locale, register_locale, is_locale_available
from .en import EnglishLocale
from .pl import PolishLocale

# Register default locales
register_locale(EnglishLocale())
register_locale(PolishLocale())

__all__ = ["Locale", "get_locale", "register_locale", "is_locale_available", "EnglishLocale", "PolishLocale"]