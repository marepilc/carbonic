"""Carbonic exceptions."""


class CarbonicError(Exception):
    """Base exception for all Carbonic errors."""


class ParseError(CarbonicError):
    """Raised when parsing a date/time string fails."""
