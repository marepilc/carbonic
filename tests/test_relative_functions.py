"""Tests for relative date/time functions."""

from datetime import datetime as stdlib_datetime
from zoneinfo import ZoneInfo

import pytest

from carbonic import Date, DateTime, today, tomorrow, yesterday


class TestDateRelativeFunctions:
    """Test relative functions for Date class."""

    def test_today(self):
        """Test Date.today() function."""
        today_date = Date.today()
        assert isinstance(today_date, Date)

        # Should match system today
        expected = Date.from_date(stdlib_datetime.now().date())
        assert today_date == expected

    def test_tomorrow(self):
        """Test Date.tomorrow() function."""
        tomorrow_date = Date.tomorrow()
        assert isinstance(tomorrow_date, Date)

        # Should be one day after today
        today_date = Date.today()
        assert tomorrow_date == today_date.add(days=1)

    def test_yesterday(self):
        """Test Date.yesterday() function."""
        yesterday_date = Date.yesterday()
        assert isinstance(yesterday_date, Date)

        # Should be one day before today
        today_date = Date.today()
        assert yesterday_date == today_date.add(days=-1)

    def test_next_day(self):
        """Test Date.next() with days."""
        next_day = Date.next("day")
        tomorrow_date = Date.tomorrow()
        assert next_day == tomorrow_date

        # Multiple days
        next_days = Date.next("day", 3)
        expected = Date.today().add(days=3)
        assert next_days == expected

    def test_next_week(self):
        """Test Date.next() with weeks."""
        next_week = Date.next("week")
        expected = Date.today().add(days=7)
        assert next_week == expected

        # Multiple weeks
        next_weeks = Date.next("week", 2)
        expected = Date.today().add(days=14)
        assert next_weeks == expected

    def test_next_month(self):
        """Test Date.next() with months."""
        next_month = Date.next("month")
        expected = Date.today().add(months=1)
        assert next_month == expected

        # Multiple months
        next_months = Date.next("month", 3)
        expected = Date.today().add(months=3)
        assert next_months == expected

    def test_next_quarter(self):
        """Test Date.next() with quarters."""
        next_quarter = Date.next("quarter")
        expected = Date.today().add(months=3)
        assert next_quarter == expected

        # Multiple quarters
        next_quarters = Date.next("quarter", 2)
        expected = Date.today().add(months=6)
        assert next_quarters == expected

    def test_next_year(self):
        """Test Date.next() with years."""
        next_year = Date.next("year")
        expected = Date.today().add(years=1)
        assert next_year == expected

    def test_previous_day(self):
        """Test Date.previous() with days."""
        prev_day = Date.previous("day")
        yesterday_date = Date.yesterday()
        assert prev_day == yesterday_date

        # Multiple days
        prev_days = Date.previous("day", 3)
        expected = Date.today().add(days=-3)
        assert prev_days == expected

    def test_previous_week(self):
        """Test Date.previous() with weeks."""
        prev_week = Date.previous("week")
        expected = Date.today().add(days=-7)
        assert prev_week == expected

    def test_previous_month(self):
        """Test Date.previous() with months."""
        prev_month = Date.previous("month")
        expected = Date.today().add(months=-1)
        assert prev_month == expected

    def test_previous_year(self):
        """Test Date.previous() with years."""
        prev_year = Date.previous("year")
        expected = Date.today().add(years=-1)
        assert prev_year == expected

    def test_invalid_unit_raises_error(self):
        """Test that invalid units raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported time unit for Date"):
            Date.next("second")

        with pytest.raises(ValueError, match="Unsupported time unit for Date"):
            Date.previous("minute")


class TestDateTimeRelativeFunctions:
    """Test relative functions for DateTime class."""

    def test_today(self):
        """Test DateTime.today() function."""
        today_dt = DateTime.today()
        assert isinstance(today_dt, DateTime)

        # Should be today at midnight UTC
        assert today_dt.hour == 0
        assert today_dt.minute == 0
        assert today_dt.second == 0
        assert isinstance(today_dt.tzinfo, ZoneInfo) and today_dt.tzinfo.key == "UTC"

        # Test with timezone
        today_ny = DateTime.today("America/New_York")
        assert isinstance(today_ny.tzinfo, ZoneInfo) and today_ny.tzinfo.key == "America/New_York"

    def test_tomorrow(self):
        """Test DateTime.tomorrow() function."""
        tomorrow_dt = DateTime.tomorrow()
        assert isinstance(tomorrow_dt, DateTime)

        # Should be tomorrow at midnight UTC
        today_dt = DateTime.today()
        assert tomorrow_dt == today_dt.add(days=1)

    def test_yesterday(self):
        """Test DateTime.yesterday() function."""
        yesterday_dt = DateTime.yesterday()
        assert isinstance(yesterday_dt, DateTime)

        # Should be yesterday at midnight UTC
        today_dt = DateTime.today()
        assert yesterday_dt == today_dt.add(days=-1)

    def test_next_second(self):
        """Test DateTime.next() with seconds."""
        before = DateTime.now()
        next_second = DateTime.next("second")

        # Should be approximately 1 second from now
        time_diff = next_second.diff(before)
        assert 0.9 <= time_diff.total_seconds() <= 1.1

    def test_next_minute(self):
        """Test DateTime.next() with minutes."""
        before = DateTime.now()
        next_minute = DateTime.next("minute")

        # Should be approximately 1 minute from now
        time_diff = next_minute.diff(before)
        assert 59 <= time_diff.total_seconds() <= 61

    def test_next_hour(self):
        """Test DateTime.next() with hours."""
        before = DateTime.now()
        next_hour = DateTime.next("hour")

        # Should be approximately 1 hour from now
        time_diff = next_hour.diff(before)
        assert 3590 <= time_diff.total_seconds() <= 3610

    def test_next_day(self):
        """Test DateTime.next() with days."""
        next_day = DateTime.next("day")
        expected = DateTime.now().add(days=1)

        # Should be very close (within a few seconds)
        time_diff = abs((next_day - expected).total_seconds())
        assert time_diff < 5

    def test_next_with_count(self):
        """Test DateTime.next() with count parameter."""
        next_3_days = DateTime.next("day", 3)
        expected = DateTime.now().add(days=3)

        # Should be very close (within a few seconds)
        time_diff = abs((next_3_days - expected).total_seconds())
        assert time_diff < 5

    def test_previous_with_timezone(self):
        """Test DateTime.previous() with timezone."""
        prev_hour = DateTime.previous("hour", tz="America/New_York")
        assert isinstance(prev_hour.tzinfo, ZoneInfo) and prev_hour.tzinfo.key == "America/New_York"

    def test_next_quarter(self):
        """Test DateTime.next() with quarters."""
        next_quarter = DateTime.next("quarter")
        expected = DateTime.now().add(months=3)

        # Should be very close (within a few seconds)
        time_diff = abs((next_quarter - expected).total_seconds())
        assert time_diff < 5

    def test_invalid_unit_raises_error(self):
        """Test that invalid units raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported time unit"):
            DateTime.next("invalid")

        with pytest.raises(ValueError, match="Unsupported time unit"):
            DateTime.previous("badunit")


class TestConvenienceFunctions:
    """Test convenience functions imported from main module."""

    def test_today_function(self):
        """Test today() convenience function."""
        today_date = today()
        date_today = Date.today()
        assert today_date == date_today

    def test_tomorrow_function(self):
        """Test tomorrow() convenience function."""
        tomorrow_date = tomorrow()
        date_tomorrow = Date.tomorrow()
        assert tomorrow_date == date_tomorrow

    def test_yesterday_function(self):
        """Test yesterday() convenience function."""
        yesterday_date = yesterday()
        date_yesterday = Date.yesterday()
        assert yesterday_date == date_yesterday


class TestRelativeFunctionEdgeCases:
    """Test edge cases and specific scenarios."""

    def test_month_end_handling(self):
        """Test that month arithmetic handles month-end correctly."""
        # This test ensures the underlying add() method works correctly
        jan_31 = Date(2024, 1, 31)

        # Mock today to be Jan 31 for testing
        # We'll test the underlying logic directly
        result = jan_31.add(months=1)
        # Should handle Feb 29 (2024 is leap year) correctly
        expected = Date(2024, 2, 29)  # Feb doesn't have 31 days
        assert result == expected

    def test_leap_year_handling(self):
        """Test leap year handling in relative calculations."""
        feb_28_2023 = Date(2023, 2, 28)  # Non-leap year
        feb_28_2024 = Date(2024, 2, 28)  # Leap year

        # Add one year to each
        result_2023 = feb_28_2023.add(years=1)
        result_2024 = feb_28_2024.add(years=1)

        assert result_2023 == Date(2024, 2, 28)
        assert result_2024 == Date(2025, 2, 28)

    def test_zero_count(self):
        """Test that zero count returns equivalent time."""
        now = DateTime.now()

        zero_days = now.add(days=0)
        assert zero_days == now

        today_date = Date.today()
        zero_months = today_date.add(months=0)
        assert zero_months == today_date

    def test_negative_count_equivalent_to_previous(self):
        """Test that negative count in next() equals previous()."""
        # For DateTime
        next_neg = DateTime.next("day", -2)
        prev_pos = DateTime.previous("day", 2)

        # Should be very close (within a few seconds due to execution time)
        time_diff = abs((next_neg - prev_pos).total_seconds())
        assert time_diff < 5

        # For Date (exact comparison possible)
        date_next_neg = Date.next("month", -3)
        date_prev_pos = Date.previous("month", 3)
        assert date_next_neg == date_prev_pos
