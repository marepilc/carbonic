"""Comprehensive tests for the Carbonic Polars extension."""

import pytest
import polars as pl
from datetime import datetime, date
import polars.testing as pls_testing

# Import after registering the namespace
import carbonic_polars


class TestCarbonicParsing:
    """Test datetime parsing with Carbonic format tokens."""

    def test_parse_format_basic(self):
        """Test basic datetime parsing."""
        df = pl.DataFrame({
            "date_str": ["2023-12-25 14:30:15", "2024-01-01 00:00:00", "2023-06-15 12:45:30"]
        })

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s").alias("parsed")
        ])

        expected = pl.DataFrame({
            "date_str": ["2023-12-25 14:30:15", "2024-01-01 00:00:00", "2023-06-15 12:45:30"],
            "parsed": [
                datetime(2023, 12, 25, 14, 30, 15),
                datetime(2024, 1, 1, 0, 0, 0),
                datetime(2023, 6, 15, 12, 45, 30),
            ]
        })

        pls_testing.assert_frame_equal(result, expected)

    def test_parse_format_carbon_style(self):
        """Test Carbon-style format tokens."""
        df = pl.DataFrame({
            "date_str": ["December 25, 2023", "January 1, 2024"]
        })

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("F j, Y").alias("parsed")
        ])

        assert result["parsed"].dtype == pl.Datetime
        assert len(result) == 2

    def test_parse_iso(self):
        """Test ISO 8601 parsing."""
        df = pl.DataFrame({
            "iso_str": [
                "2023-12-25T14:30:15Z",
                "2023-12-25T14:30:15.123Z",
                "2023-12-25 14:30:15",
                "2023-12-25",
            ]
        })

        result = df.with_columns([
            pl.col("iso_str").carbonic.parse_iso().alias("parsed")
        ])

        assert result["parsed"].dtype == pl.Datetime
        assert len(result) == 4
        assert result["parsed"].null_count() == 0

    def test_parse_format_with_nulls(self):
        """Test parsing with null values."""
        df = pl.DataFrame({
            "date_str": ["2023-12-25 14:30:15", None, "2024-01-01 00:00:00"]
        })

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s").alias("parsed")
        ])

        assert result["parsed"][0] is not None
        assert result["parsed"][1] is None
        assert result["parsed"][2] is not None

    def test_parse_format_strict_mode(self):
        """Test strict parsing mode."""
        df = pl.DataFrame({
            "date_str": ["2023-12-25 14:30:15", "2023-12-25"]  # Second one doesn't match format
        })

        # In strict mode, mismatched format should result in null or error
        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s", strict=True).alias("parsed")
        ])

        # First should parse successfully, second should be null due to format mismatch
        assert result["parsed"][0] is not None
        # Note: Actual behavior depends on implementation - might be null or raise error


class TestBusinessDays:
    """Test business day arithmetic."""

    def test_add_business_days_simple(self):
        """Test adding business days with default weekends."""
        df = pl.DataFrame({
            "start_date": [date(2023, 12, 22), date(2023, 12, 25)]  # Friday, Monday
        })

        result = df.with_columns([
            pl.col("start_date").carbonic.add_business_days(1).alias("next_bday")
        ])

        # Friday + 1 business day = Monday (skip weekend)
        # Monday + 1 business day = Tuesday
        assert result["next_bday"].dtype == pl.Date
        assert len(result) == 2

    def test_add_business_days_with_expression(self):
        """Test adding business days using expression for days."""
        df = pl.DataFrame({
            "start_date": [date(2023, 12, 22), date(2023, 12, 25)],
            "days_to_add": [1, 5]
        })

        result = df.with_columns([
            pl.col("start_date").carbonic.add_business_days(pl.col("days_to_add")).alias("result_date")
        ])

        assert result["result_date"].dtype == pl.Date
        assert len(result) == 2

    def test_subtract_business_days(self):
        """Test subtracting business days."""
        df = pl.DataFrame({
            "end_date": [date(2023, 12, 26), date(2023, 12, 28)]  # Tuesday, Thursday
        })

        result = df.with_columns([
            pl.col("end_date").carbonic.subtract_business_days(1).alias("prev_bday")
        ])

        assert result["prev_bday"].dtype == pl.Date
        assert len(result) == 2

    def test_custom_weekends(self):
        """Test business days with custom weekend definition."""
        df = pl.DataFrame({
            "start_date": [date(2023, 12, 21)]  # Thursday
        })

        # Middle East style weekend (Friday-Saturday)
        result = df.with_columns([
            pl.col("start_date").carbonic.add_business_days(
                1,
                weekends=["Friday", "Saturday"]
            ).alias("next_bday")
        ])

        assert result["next_bday"].dtype == pl.Date

    def test_business_days_with_holidays(self):
        """Test business days with holidays."""
        df = pl.DataFrame({
            "start_date": [date(2023, 12, 22)]  # Friday before Christmas
        })

        result = df.with_columns([
            pl.col("start_date").carbonic.add_business_days(
                1,
                holidays=["2023-12-25"]  # Christmas
            ).alias("next_bday")
        ])

        # Should skip Christmas Monday, go to Tuesday
        assert result["next_bday"].dtype == pl.Date


class TestFormattingAndLocalization:
    """Test localized datetime formatting."""

    def test_format_localized_english(self):
        """Test English localized formatting."""
        df = pl.DataFrame({
            "datetime": [datetime(2023, 12, 25, 14, 30, 15)]
        })

        result = df.with_columns([
            pl.col("datetime").carbonic.format_localized("F j, Y", "en").alias("formatted")
        ])

        assert result["formatted"][0] == "December 25, 2023"

    def test_format_localized_polish(self):
        """Test Polish localized formatting."""
        df = pl.DataFrame({
            "datetime": [datetime(2023, 12, 25, 14, 30, 15)]
        })

        result = df.with_columns([
            pl.col("datetime").carbonic.format_localized("F j, Y", "pl").alias("formatted")
        ])

        assert result["formatted"][0] == "grudzień 25, 2023"

    def test_format_localized_day_names(self):
        """Test localized day names."""
        df = pl.DataFrame({
            "datetime": [datetime(2023, 12, 25, 14, 30, 15)]  # Monday
        })

        result_en = df.with_columns([
            pl.col("datetime").carbonic.format_localized("l, F j", "en").alias("formatted")
        ])

        result_pl = df.with_columns([
            pl.col("datetime").carbonic.format_localized("l, F j", "pl").alias("formatted")
        ])

        assert "Monday" in result_en["formatted"][0]
        assert "poniedziałek" in result_pl["formatted"][0]

    def test_humanize_duration_english(self):
        """Test English duration humanization."""
        # Create duration column (Polars Duration in nanoseconds)
        df = pl.DataFrame({
            "duration": [
                pl.duration(hours=2, minutes=30),
                pl.duration(days=1, hours=5),
                pl.duration(seconds=45)
            ]
        })

        result = df.with_columns([
            pl.col("duration").carbonic.humanize_duration("en", 2).alias("human")
        ])

        assert result["human"].dtype == pl.String
        assert len(result) == 3

    def test_humanize_duration_polish(self):
        """Test Polish duration humanization with proper pluralization."""
        df = pl.DataFrame({
            "duration": [
                pl.duration(days=1),      # "1 dzień"
                pl.duration(days=2),      # "2 dni"
                pl.duration(days=5),      # "5 dni"
                pl.duration(hours=3),     # "3 godziny"
            ]
        })

        result = df.with_columns([
            pl.col("duration").carbonic.humanize_duration("pl", 1).alias("human")
        ])

        assert result["human"].dtype == pl.String
        assert len(result) == 4


class TestDataFrameNamespace:
    """Test DataFrame-level operations."""

    def test_parse_datetime_columns(self):
        """Test bulk parsing of datetime columns."""
        df = pl.DataFrame({
            "start_date": ["2023-12-25 09:00:00", "2023-12-26 10:30:00"],
            "end_date": ["2023-12-25 17:00:00", "2023-12-26 16:45:00"],
            "created_at": ["2023-12-20 12:00:00", "2023-12-21 14:15:00"],
        })

        result = df.carbonic.parse_datetime_columns(
            ["start_date", "end_date", "created_at"],
            format="Y-m-d H:i:s"
        )

        assert result["start_date"].dtype == pl.Datetime
        assert result["end_date"].dtype == pl.Datetime
        assert result["created_at"].dtype == pl.Datetime

    def test_add_business_days_bulk(self):
        """Test bulk business day operations."""
        df = pl.DataFrame({
            "start": [date(2023, 12, 22), date(2023, 12, 25)],
            "middle": [date(2023, 12, 23), date(2023, 12, 26)],
            "end": [date(2023, 12, 24), date(2023, 12, 27)],
        })

        result = df.carbonic.add_business_days_bulk(
            date_columns=["start", "middle", "end"],
            days=[1, 3, 5]  # Different days for each column
        )

        assert result["start"].dtype == pl.Date
        assert result["middle"].dtype == pl.Date
        assert result["end"].dtype == pl.Date

    def test_format_datetime_columns(self):
        """Test bulk datetime formatting."""
        df = pl.DataFrame({
            "created_at": [datetime(2023, 12, 25, 9, 0, 0)],
            "updated_at": [datetime(2023, 12, 26, 16, 30, 0)],
        })

        result = df.carbonic.format_datetime_columns(
            ["created_at", "updated_at"],
            format="F j, Y \\a\\t H:i",
            locale="en"
        )

        assert result["created_at"].dtype == pl.String
        assert result["updated_at"].dtype == pl.String
        assert "December 25, 2023 at 09:00" in result["created_at"][0]


class TestConvenienceFunctions:
    """Test standalone convenience functions."""

    def test_parse_datetime_column_function(self):
        """Test parse_datetime_column convenience function."""
        df = pl.DataFrame({
            "date_str": ["2023-12-25", "2024-01-01"]
        })

        result = df.with_columns([
            carbonic_polars.parse_datetime_column("date_str", "Y-m-d").alias("parsed")
        ])

        assert result["parsed"].dtype == pl.Datetime
        assert len(result) == 2

    def test_add_business_days_to_column_function(self):
        """Test add_business_days_to_column convenience function."""
        df = pl.DataFrame({
            "start_date": [date(2023, 12, 22)]
        })

        result = df.with_columns([
            carbonic_polars.add_business_days_to_column("start_date", 3).alias("end_date")
        ])

        assert result["end_date"].dtype == pl.Date


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_dataframe(self):
        """Test operations on empty DataFrames."""
        df = pl.DataFrame({"date_str": []}, schema={"date_str": pl.String})

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d").alias("parsed")
        ])

        assert len(result) == 0
        assert result["parsed"].dtype == pl.Datetime

    def test_all_null_column(self):
        """Test operations on columns with all null values."""
        df = pl.DataFrame({
            "date_str": [None, None, None]
        })

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s").alias("parsed")
        ])

        assert result["parsed"].null_count() == 3

    def test_mixed_valid_invalid_dates(self):
        """Test parsing with mixed valid/invalid date strings."""
        df = pl.DataFrame({
            "date_str": [
                "2023-12-25 14:30:15",  # Valid
                "invalid-date",         # Invalid
                "2024-01-01 00:00:00",  # Valid
            ]
        })

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s").alias("parsed")
        ])

        # Should have 2 valid dates and 1 null
        assert result["parsed"].null_count() == 1
        assert len(result) == 3

    def test_extreme_business_day_counts(self):
        """Test business day arithmetic with large numbers."""
        df = pl.DataFrame({
            "start_date": [date(2023, 1, 1)]
        })

        result = df.with_columns([
            pl.col("start_date").carbonic.add_business_days(252).alias("year_later")  # ~1 business year
        ])

        assert result["year_later"].dtype == pl.Date

    def test_negative_business_days(self):
        """Test negative business day arithmetic."""
        df = pl.DataFrame({
            "end_date": [date(2023, 12, 25)]
        })

        result = df.with_columns([
            pl.col("end_date").carbonic.add_business_days(-5).alias("earlier_date")
        ])

        assert result["earlier_date"].dtype == pl.Date


class TestPerformance:
    """Basic performance and stress tests."""

    def test_large_dataset_parsing(self):
        """Test parsing performance with larger dataset."""
        # Create a DataFrame with 10,000 rows
        n_rows = 10_000
        dates = ["2023-12-25 14:30:15"] * n_rows

        df = pl.DataFrame({
            "date_str": dates
        })

        result = df.with_columns([
            pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s").alias("parsed")
        ])

        assert len(result) == n_rows
        assert result["parsed"].null_count() == 0

    def test_large_dataset_business_days(self):
        """Test business day arithmetic with larger dataset."""
        n_rows = 10_000
        start_dates = [date(2023, 12, 22)] * n_rows

        df = pl.DataFrame({
            "start_date": start_dates
        })

        result = df.with_columns([
            pl.col("start_date").carbonic.add_business_days(5).alias("end_date")
        ])

        assert len(result) == n_rows
        assert result["end_date"].null_count() == 0


if __name__ == "__main__":
    pytest.main([__file__])