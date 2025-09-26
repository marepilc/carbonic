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
    """Carbonic operations namespace for Polars expressions (minimal version)."""

    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr

    def placeholder(self) -> pl.Expr:
        """Placeholder method to verify namespace registration."""
        # Just return the original expression for now
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