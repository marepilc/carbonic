"""Carbonic Polars Extension - High-performance datetime operations for Polars."""

import polars as pl
from pathlib import Path
from typing import Union

# Import the compiled Rust extension
try:
    from ._internal import (
        parse_format,
        parse_iso,
        add_business_days,
        subtract_business_days,
        format_localized,
        humanize_duration,
    )
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
        """Parse datetime strings using Carbonic format tokens.

        Args:
            format: Carbonic format string (e.g., "Y-m-d H:i:s", "F j, Y")
            locale: Locale for month/day names (default: "en")
            strict: If True, input must match format exactly (default: False)

        Returns:
            Expression returning datetime column

        Examples:
            >>> df.with_columns([
            ...     pl.col("date_str").carbonic.parse_format("Y-m-d"),
            ...     pl.col("custom_date").carbonic.parse_format("F j, Y", locale="en"),
            ... ])
        """
        return pl.Expr.register_plugin(
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
        """Parse ISO 8601 datetime strings.

        Returns:
            Expression returning datetime column

        Examples:
            >>> df.with_columns([
            ...     pl.col("iso_date").carbonic.parse_iso(),
            ... ])
        """
        return pl.Expr.register_plugin(
            lib=LIB,
            symbol="parse_iso",
            args=[self._expr],
            is_elementwise=True,
        )

    def add_business_days(
        self,
        days: Union[pl.Expr, int],
        weekends: list[str] = None,
        holidays: list[str] = None
    ) -> pl.Expr:
        """Add business days to dates.

        Args:
            days: Number of business days to add (can be expression or integer)
            weekends: List of weekend day names (default: ["Saturday", "Sunday"])
            holidays: List of holiday dates in YYYY-MM-DD format

        Returns:
            Expression returning date column

        Examples:
            >>> df.with_columns([
            ...     pl.col("start_date").carbonic.add_business_days(5),
            ...     pl.col("due_date").carbonic.add_business_days(
            ...         pl.col("offset_days"),
            ...         holidays=["2023-12-25", "2024-01-01"]
            ...     ),
            ... ])
        """
        if weekends is None:
            weekends = ["Saturday", "Sunday"]

        if holidays is None:
            holidays = []

        days_expr = pl.lit(days) if isinstance(days, int) else days

        return pl.Expr.register_plugin(
            lib=LIB,
            symbol="add_business_days",
            args=[self._expr, days_expr],
            kwargs={
                "weekends": weekends,
                "holidays": holidays,
            },
            is_elementwise=True,
        )

    def subtract_business_days(
        self,
        days: Union[pl.Expr, int],
        weekends: list[str] = None,
        holidays: list[str] = None
    ) -> pl.Expr:
        """Subtract business days from dates.

        Args:
            days: Number of business days to subtract (can be expression or integer)
            weekends: List of weekend day names (default: ["Saturday", "Sunday"])
            holidays: List of holiday dates in YYYY-MM-DD format

        Returns:
            Expression returning date column

        Examples:
            >>> df.with_columns([
            ...     pl.col("end_date").carbonic.subtract_business_days(3),
            ...     pl.col("start_date").carbonic.subtract_business_days(
            ...         pl.col("lead_time"),
            ...         weekends=["Friday", "Saturday"]  # Middle East style
            ...     ),
            ... ])
        """
        if weekends is None:
            weekends = ["Saturday", "Sunday"]

        if holidays is None:
            holidays = []

        days_expr = pl.lit(days) if isinstance(days, int) else days

        return pl.Expr.register_plugin(
            lib=LIB,
            symbol="subtract_business_days",
            args=[self._expr, days_expr],
            kwargs={
                "weekends": weekends,
                "holidays": holidays,
            },
            is_elementwise=True,
        )

    def format_localized(
        self,
        format: str = "Y-m-d H:i:s",
        locale: str = "en"
    ) -> pl.Expr:
        """Format datetime with localized month/day names.

        Args:
            format: Carbonic format string (e.g., "F j, Y", "l, M d")
            locale: Locale for output (e.g., "en", "pl")

        Returns:
            Expression returning string column

        Examples:
            >>> df.with_columns([
            ...     pl.col("date").carbonic.format_localized("F j, Y", "en"),  # "December 25, 2023"
            ...     pl.col("date").carbonic.format_localized("F j, Y", "pl"),  # "grudzień 25, 2023"
            ... ])
        """
        return pl.Expr.register_plugin(
            lib=LIB,
            symbol="format_localized",
            args=[self._expr],
            kwargs={
                "format": format,
                "locale": locale,
            },
            is_elementwise=True,
        )

    def humanize_duration(
        self,
        locale: str = "en",
        max_units: int = 2
    ) -> pl.Expr:
        """Convert duration to human-readable format.

        Args:
            locale: Locale for pluralization (e.g., "en", "pl")
            max_units: Maximum number of units to display

        Returns:
            Expression returning string column

        Examples:
            >>> df.with_columns([
            ...     pl.col("duration").carbonic.humanize_duration("en", 2),  # "2 days 3 hours"
            ...     pl.col("duration").carbonic.humanize_duration("pl", 1),  # "2 dni"
            ... ])
        """
        return pl.Expr.register_plugin(
            lib=LIB,
            symbol="humanize_duration",
            args=[self._expr],
            kwargs={
                "locale": locale,
                "max_units": max_units,
            },
            is_elementwise=True,
        )


@pl.api.register_dataframe_namespace("carbonic")
class CarbonicDataFrameNamespace:
    """Carbonic operations namespace for Polars DataFrames."""

    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    def parse_datetime_columns(
        self,
        columns: list[str],
        format: str = "Y-m-d H:i:s",
        locale: str = "en"
    ) -> pl.DataFrame:
        """Parse multiple datetime columns at once.

        Args:
            columns: List of column names to parse
            format: Carbonic format string
            locale: Locale for parsing

        Returns:
            DataFrame with parsed datetime columns

        Examples:
            >>> df.carbonic.parse_datetime_columns(
            ...     ["start_date", "end_date", "created_at"],
            ...     format="Y-m-d H:i:s"
            ... )
        """
        return self._df.with_columns([
            pl.col(col).carbonic.parse_format(format=format, locale=locale).alias(col)
            for col in columns
        ])

    def add_business_days_bulk(
        self,
        date_columns: list[str],
        days: Union[list[int], int],
        weekends: list[str] = None,
        holidays: list[str] = None
    ) -> pl.DataFrame:
        """Add business days to multiple date columns.

        Args:
            date_columns: List of date column names
            days: Days to add (single int for all columns, or list matching columns)
            weekends: Weekend day names
            holidays: Holiday dates in YYYY-MM-DD format

        Returns:
            DataFrame with updated date columns

        Examples:
            >>> df.carbonic.add_business_days_bulk(
            ...     date_columns=["start", "middle", "end"],
            ...     days=[1, 5, 10],  # Different days for each column
            ...     holidays=["2023-12-25"]
            ... )
        """
        if isinstance(days, int):
            days_list = [days] * len(date_columns)
        else:
            days_list = days

        if len(days_list) != len(date_columns):
            raise ValueError("Length of 'days' must match length of 'date_columns'")

        return self._df.with_columns([
            pl.col(col).carbonic.add_business_days(
                day_count,
                weekends=weekends,
                holidays=holidays
            ).alias(col)
            for col, day_count in zip(date_columns, days_list)
        ])

    def format_datetime_columns(
        self,
        columns: list[str],
        format: str = "Y-m-d H:i:s",
        locale: str = "en"
    ) -> pl.DataFrame:
        """Format multiple datetime columns with localization.

        Args:
            columns: List of datetime column names
            format: Carbonic format string
            locale: Locale for formatting

        Returns:
            DataFrame with formatted string columns

        Examples:
            >>> df.carbonic.format_datetime_columns(
            ...     ["created_at", "updated_at"],
            ...     format="F j, Y",
            ...     locale="pl"
            ... )
        """
        return self._df.with_columns([
            pl.col(col).carbonic.format_localized(format=format, locale=locale).alias(col)
            for col in columns
        ])


# Convenience functions for direct use
def parse_datetime_column(
    column: str,
    format: str = "Y-m-d H:i:s",
    locale: str = "en",
    strict: bool = False
) -> pl.Expr:
    """Convenience function to parse a datetime column.

    Args:
        column: Column name
        format: Carbonic format string
        locale: Locale for parsing
        strict: Strict parsing mode

    Returns:
        Expression for parsing the column

    Examples:
        >>> df.with_columns([
        ...     parse_datetime_column("date_str", "Y-m-d"),
        ... ])
    """
    return pl.col(column).carbonic.parse_format(format=format, locale=locale, strict=strict)


def add_business_days_to_column(
    column: str,
    days: Union[pl.Expr, int],
    weekends: list[str] = None,
    holidays: list[str] = None
) -> pl.Expr:
    """Convenience function to add business days to a column.

    Args:
        column: Date column name
        days: Number of business days to add
        weekends: Weekend day names
        holidays: Holiday dates

    Returns:
        Expression for adding business days

    Examples:
        >>> df.with_columns([
        ...     add_business_days_to_column("start_date", 5),
        ... ])
    """
    return pl.col(column).carbonic.add_business_days(
        days=days,
        weekends=weekends,
        holidays=holidays
    )


# Version information
__version__ = "0.1.0"
__all__ = [
    "CarbonicExprNamespace",
    "CarbonicDataFrameNamespace",
    "parse_datetime_column",
    "add_business_days_to_column",
]