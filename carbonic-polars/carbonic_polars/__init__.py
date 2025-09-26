"""Carbonic Polars Extension - High-performance datetime operations for Polars."""

import polars as pl
from pathlib import Path
from typing import Union

# Import the compiled Rust extension (minimal version for now)
try:
    from . import _internal
except ImportError as e:
    raise ImportError(
        "Carbonic Polars extension not available. "
        "Please ensure the package was installed correctly with: pip install carbonic-polars"
    ) from e


# Get the library path for plugin registration
LIB = Path(__file__).parent


@pl.api.register_expr_namespace("carbonic")
class CarbonicExprNamespace:
    """Carbonic operations namespace for Polars expressions."""

    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr

    def parse_format(
        self,
        format: str = "Y-m-d H:i:s",
        locale: str = "en",
        strict: bool = False
    ) -> pl.Expr:
        """Parse datetime strings using Carbonic format tokens (placeholder implementation).

        Args:
            format: Carbonic format string (e.g., "Y-m-d H:i:s", "F j, Y")
            locale: Locale for month/day names (default: "en")
            strict: If True, input must match format exactly (default: False)

        Returns:
            Expression returning string column (placeholder - will return parsed:input)
        """
        return self._expr.register_plugin(
            lib=LIB,
            symbol="parse_format",
            args=[self._expr],
            kwargs={
                "format": format,
                "locale": locale,
                "strict": strict,
            },
            is_elementwise=True,
        )

    def parse_iso(self) -> pl.Expr:
        """Parse ISO 8601 datetime strings (placeholder implementation).

        Returns:
            Expression returning string column (placeholder - will return iso:input)
        """
        return self._expr.register_plugin(
            lib=LIB,
            symbol="parse_iso",
            args=[self._expr],
            is_elementwise=True,
        )

    def placeholder(self) -> pl.Expr:
        """Legacy placeholder method for backward compatibility."""
        return self._expr


@pl.api.register_dataframe_namespace("carbonic")
class CarbonicDataFrameNamespace:
    """Carbonic operations namespace for Polars DataFrames (minimal version)."""

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    def info(self) -> str:
        """Return basic info about the carbonic namespace."""
        return f"Carbonic DataFrame namespace on {len(self._df)} rows"


# Version information
__version__ = "0.1.0"
__all__ = [
    "CarbonicExprNamespace",
    "CarbonicDataFrameNamespace",
]