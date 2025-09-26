"""Tests for Polars integration."""

import pytest

try:
    import polars as pl
except ImportError:
    pytest.skip("polars not available", allow_module_level=True)

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from carbonic import Date, DateTime, Duration
from carbonic.integrations.polars import (
    date_to_polars,
    datetime_to_polars,
    duration_to_polars,
    polars_to_date,
    polars_to_datetime,
    polars_to_duration,
    dates_to_polars_series,
    datetimes_to_polars_series,
    durations_to_polars_series,
    polars_series_to_dates,
    polars_series_to_datetimes,
    polars_series_to_durations,
)


class TestCarbonic_to_Polars_Conversion:
    """Test converting Carbonic objects to Polars types."""

    def test_date_to_polars(self):
        """Test Date to pl.Date conversion."""
        date = Date(2023, 12, 25)
        result = date_to_polars(date)

        assert isinstance(result, datetime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0
        assert result.tzinfo is None

    def test_datetime_to_polars_naive(self):
        """Test DateTime to pl.Datetime conversion (naive)."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = datetime_to_polars(dt)

        assert isinstance(result, datetime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 45
        assert result.tzinfo is None

    def test_datetime_to_polars_with_timezone(self):
        """Test DateTime to pl.Datetime conversion with timezone."""
        dt = DateTime(2023, 12, 25, 14, 30, 45, tz="UTC")
        result = datetime_to_polars(dt)

        assert isinstance(result, datetime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 45
        assert result.tzinfo == timezone.utc

    def test_datetime_to_polars_custom_timezone(self):
        """Test DateTime to pl.Datetime conversion with custom timezone."""
        tz = ZoneInfo("America/New_York")
        dt = DateTime(2023, 12, 25, 14, 30, 45, tz=tz)
        result = datetime_to_polars(dt)

        assert isinstance(result, datetime)
        assert result.tzinfo == tz

    def test_duration_to_polars_simple(self):
        """Test Duration to pl.Duration conversion."""
        duration = Duration(days=5, hours=3, minutes=30, seconds=15)
        result = duration_to_polars(duration)

        assert isinstance(result, timedelta)
        expected = timedelta(days=5, hours=3, minutes=30, seconds=15)
        assert result == expected

    def test_duration_to_polars_negative(self):
        """Test negative Duration to pl.Duration conversion."""
        duration = Duration(days=-2, hours=-5)
        result = duration_to_polars(duration)

        assert isinstance(result, timedelta)
        expected = timedelta(days=-2, hours=-5)
        assert result == expected

    def test_duration_to_polars_microseconds(self):
        """Test Duration with microseconds to pl.Duration conversion."""
        duration = Duration(seconds=1, microseconds=500000)
        result = duration_to_polars(duration)

        assert isinstance(result, timedelta)
        expected = timedelta(seconds=1, microseconds=500000)
        assert result == expected

    def test_duration_to_polars_calendar_components_warning(self):
        """Test Duration with calendar components raises warning."""
        duration = Duration(years=1, months=2, days=3)

        with pytest.warns(UserWarning, match="Calendar components.*will be approximated"):
            result = duration_to_polars(duration)

        # Should approximate: 1 year + 2 months + 3 days
        # ≈ 365.25 + 60.87 + 3 = 429.12 days
        assert isinstance(result, timedelta)
        assert abs(result.days - 429) <= 1  # Allow some approximation variance


class TestPolars_to_Carbonic_Conversion:
    """Test converting Polars types to Carbonic objects."""

    def test_polars_to_date(self):
        """Test pl.Date to Date conversion."""
        py_date = datetime(2023, 12, 25)
        result = polars_to_date(py_date)

        assert isinstance(result, Date)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25

    def test_polars_to_datetime_naive(self):
        """Test pl.Datetime to DateTime conversion (naive)."""
        py_datetime = datetime(2023, 12, 25, 14, 30, 45)
        result = polars_to_datetime(py_datetime)

        assert isinstance(result, DateTime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 45
        assert result.tzinfo is None

    def test_polars_to_datetime_with_timezone(self):
        """Test pl.Datetime to DateTime conversion with timezone."""
        py_datetime = datetime(2023, 12, 25, 14, 30, 45, tzinfo=timezone.utc)
        result = polars_to_datetime(py_datetime)

        assert isinstance(result, DateTime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 45
        assert result.tzinfo == timezone.utc

    def test_polars_to_duration(self):
        """Test pl.Duration to Duration conversion."""
        py_timedelta = timedelta(days=5, hours=3, minutes=30, seconds=15)
        result = polars_to_duration(py_timedelta)

        assert isinstance(result, Duration)
        assert result.in_days() == 5
        assert result.in_hours(whole=True) == 5 * 24 + 3
        assert result.in_minutes(whole=True) == (5 * 24 + 3) * 60 + 30
        assert result.in_seconds(whole=True) == ((5 * 24 + 3) * 60 + 30) * 60 + 15

    def test_polars_to_duration_negative(self):
        """Test negative pl.Duration to Duration conversion."""
        py_timedelta = timedelta(days=-2, hours=-5)
        result = polars_to_duration(py_timedelta)

        assert isinstance(result, Duration)
        assert result.in_days() < 0
        assert result.in_seconds() < 0


class TestSeries_Conversion:
    """Test converting between Carbonic collections and Polars Series."""

    def test_dates_to_polars_series(self):
        """Test converting list of Dates to Polars Series."""
        dates = [
            Date(2023, 1, 1),
            Date(2023, 6, 15),
            Date(2023, 12, 31),
        ]

        result = dates_to_polars_series(dates, name="test_dates")

        assert isinstance(result, pl.Series)
        assert result.name == "test_dates"
        assert len(result) == 3
        assert result.dtype == pl.Date

        # Check values
        values = result.to_list()
        assert values[0].year == 2023 and values[0].month == 1 and values[0].day == 1
        assert values[1].year == 2023 and values[1].month == 6 and values[1].day == 15
        assert values[2].year == 2023 and values[2].month == 12 and values[2].day == 31

    def test_datetimes_to_polars_series(self):
        """Test converting list of DateTimes to Polars Series."""
        datetimes = [
            DateTime(2023, 1, 1, 12, 0, 0),
            DateTime(2023, 6, 15, 18, 30, 45, tz="UTC"),
            DateTime(2023, 12, 31, 23, 59, 59),
        ]

        result = datetimes_to_polars_series(datetimes, name="test_datetimes")

        assert isinstance(result, pl.Series)
        assert result.name == "test_datetimes"
        assert len(result) == 3
        assert result.dtype == pl.Datetime

    def test_durations_to_polars_series(self):
        """Test converting list of Durations to Polars Series."""
        durations = [
            Duration(days=1),
            Duration(hours=12, minutes=30),
            Duration(seconds=45, microseconds=123456),
        ]

        result = durations_to_polars_series(durations, name="test_durations")

        assert isinstance(result, pl.Series)
        assert result.name == "test_durations"
        assert len(result) == 3
        assert result.dtype == pl.Duration

    def test_polars_series_to_dates(self):
        """Test converting Polars Series to list of Dates."""
        py_dates = [
            datetime(2023, 1, 1),
            datetime(2023, 6, 15),
            datetime(2023, 12, 31),
        ]
        series = pl.Series("dates", py_dates, dtype=pl.Date)

        result = polars_series_to_dates(series)

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(d, Date) for d in result)
        assert result[0] == Date(2023, 1, 1)
        assert result[1] == Date(2023, 6, 15)
        assert result[2] == Date(2023, 12, 31)

    def test_polars_series_to_datetimes(self):
        """Test converting Polars Series to list of DateTimes."""
        py_datetimes = [
            datetime(2023, 1, 1, 12, 0, 0),
            datetime(2023, 6, 15, 18, 30, 45, tzinfo=timezone.utc),
            datetime(2023, 12, 31, 23, 59, 59),
        ]
        series = pl.Series("datetimes", py_datetimes, dtype=pl.Datetime)

        result = polars_series_to_datetimes(series)

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(dt, DateTime) for dt in result)
        assert result[0] == DateTime(2023, 1, 1, 12, 0, 0)
        assert result[1] == DateTime(2023, 6, 15, 18, 30, 45, tz=timezone.utc)
        assert result[2] == DateTime(2023, 12, 31, 23, 59, 59)

    def test_polars_series_to_durations(self):
        """Test converting Polars Series to list of Durations."""
        py_timedeltas = [
            timedelta(days=1),
            timedelta(hours=12, minutes=30),
            timedelta(seconds=45, microseconds=123456),
        ]
        series = pl.Series("durations", py_timedeltas, dtype=pl.Duration)

        result = polars_series_to_durations(series)

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(d, Duration) for d in result)
        # Verify approximate equality for durations
        assert abs(result[0].in_days() - 1) < 0.001
        assert abs(result[1].in_hours() - 12.5) < 0.001


class TestNull_and_Edge_Cases:
    """Test null values and edge cases."""

    def test_empty_list_to_series(self):
        """Test converting empty list to Polars Series."""
        result = dates_to_polars_series([], name="empty")
        assert isinstance(result, pl.Series)
        assert len(result) == 0
        assert result.name == "empty"

    def test_series_with_nulls_to_dates(self):
        """Test converting Series with null values to Dates."""
        series = pl.Series("dates_with_nulls", [
            datetime(2023, 1, 1),
            None,
            datetime(2023, 12, 31),
        ], dtype=pl.Date)

        with pytest.raises(ValueError, match="Cannot convert null"):
            polars_series_to_dates(series)

    def test_mixed_timezone_datetimes_warning(self):
        """Test warning when converting mixed timezone DateTimes."""
        datetimes = [
            DateTime(2023, 1, 1, tz="UTC"),
            DateTime(2023, 6, 15),  # naive
            DateTime(2023, 12, 31, tz="America/New_York"),
        ]

        with pytest.warns(UserWarning, match="Mixed timezone"):
            datetimes_to_polars_series(datetimes)

    def test_extreme_dates(self):
        """Test conversion with extreme date values."""
        # Test minimum and maximum supported dates
        extreme_dates = [
            Date(1, 1, 1),
            Date(9999, 12, 31),
        ]

        series = dates_to_polars_series(extreme_dates)
        result = polars_series_to_dates(series)

        assert result[0] == Date(1, 1, 1)
        assert result[1] == Date(9999, 12, 31)

    def test_microsecond_precision(self):
        """Test microsecond precision is preserved."""
        dt = DateTime(2023, 1, 1, 12, 30, 45, 123456)
        polars_dt = datetime_to_polars(dt)
        result = polars_to_datetime(polars_dt)

        assert result.microsecond == 123456
        assert result == dt


class TestDataFrame_Integration:
    """Test integration with Polars DataFrames."""

    def test_date_column_in_dataframe(self):
        """Test working with Date column in DataFrame."""
        dates = [Date(2023, 1, 1), Date(2023, 6, 15), Date(2023, 12, 31)]
        series = dates_to_polars_series(dates, name="date_col")

        df = pl.DataFrame({
            "id": [1, 2, 3],
            "date_col": series,
        })

        assert len(df) == 3
        assert "date_col" in df.columns
        assert df["date_col"].dtype == pl.Date

        # Convert back
        extracted_dates = polars_series_to_dates(df["date_col"])
        assert extracted_dates == dates

    def test_datetime_column_operations(self):
        """Test DataFrame operations on DateTime columns."""
        datetimes = [
            DateTime(2023, 1, 1, 12, 0, 0),
            DateTime(2023, 6, 15, 18, 30, 0),
            DateTime(2023, 12, 31, 23, 59, 59),
        ]
        series = datetimes_to_polars_series(datetimes, name="timestamp")

        df = pl.DataFrame({
            "event": ["start", "middle", "end"],
            "timestamp": series,
        })

        # Test filtering
        filtered = df.filter(pl.col("timestamp") > datetime(2023, 6, 1))
        assert len(filtered) == 2

    def test_duration_column_aggregations(self):
        """Test aggregating Duration columns in DataFrame."""
        durations = [
            Duration(hours=1),
            Duration(hours=2, minutes=30),
            Duration(minutes=45),
        ]
        series = durations_to_polars_series(durations, name="duration")

        df = pl.DataFrame({
            "task": ["A", "B", "C"],
            "duration": series,
        })

        # Test sum aggregation
        total = df["duration"].sum()
        assert isinstance(total, timedelta)
        # 1h + 2.5h + 0.75h = 4.25h
        assert abs(total.total_seconds() - 4.25 * 3600) < 1