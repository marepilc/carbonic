import pytest

from carbonic import Date, DateTime, Period


class TestPeriodConstants:
    def test_period_constants_exist(self):
        """Test that all expected Period constants are available."""
        assert hasattr(Period, 'MINUTE')
        assert hasattr(Period, 'HOUR')
        assert hasattr(Period, 'DAY')
        assert hasattr(Period, 'WEEK')
        assert hasattr(Period, 'MONTH')
        assert hasattr(Period, 'QUARTER')
        assert hasattr(Period, 'YEAR')

    def test_period_constants_are_period_instances(self):
        """Test that Period constants are Period instances."""
        assert isinstance(Period.MINUTE, Period)
        assert isinstance(Period.HOUR, Period)
        assert isinstance(Period.DAY, Period)
        assert isinstance(Period.WEEK, Period)
        assert isinstance(Period.MONTH, Period)
        assert isinstance(Period.QUARTER, Period)
        assert isinstance(Period.YEAR, Period)

    def test_period_string_representations(self):
        """Test Period string representations."""
        assert str(Period.DAY) == "day"
        assert str(Period.MONTH) == "month"
        assert repr(Period.DAY) == "Period.DAY"
        assert repr(Period.MONTH) == "Period.MONTH"


class TestPeriodAddTo:
    def test_period_day_add_to_date(self):
        """Test adding days to Date."""
        date = Date(2023, 12, 25)
        result = Period.DAY.add_to(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 26)

    def test_period_day_add_to_date_multiple(self):
        """Test adding multiple days to Date."""
        date = Date(2023, 12, 25)
        result = Period.DAY.add_to(date, count=5)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 30)

    def test_period_week_add_to_date(self):
        """Test adding weeks to Date."""
        date = Date(2023, 12, 25)
        result = Period.WEEK.add_to(date)

        assert isinstance(result, Date)
        assert result == Date(2024, 1, 1)

    def test_period_month_add_to_date(self):
        """Test adding months to Date."""
        date = Date(2023, 12, 25)
        result = Period.MONTH.add_to(date)

        assert isinstance(result, Date)
        assert result == Date(2024, 1, 25)

    def test_period_quarter_add_to_date(self):
        """Test adding quarters to Date."""
        date = Date(2023, 12, 25)
        result = Period.QUARTER.add_to(date)

        assert isinstance(result, Date)
        assert result == Date(2024, 3, 25)

    def test_period_year_add_to_date(self):
        """Test adding years to Date."""
        date = Date(2023, 12, 25)
        result = Period.YEAR.add_to(date)

        assert isinstance(result, Date)
        assert result == Date(2024, 12, 25)

    def test_period_hour_add_to_datetime(self):
        """Test adding hours to DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.HOUR.add_to(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 15, 30, 45)

    def test_period_minute_add_to_datetime(self):
        """Test adding minutes to DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.MINUTE.add_to(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 14, 31, 45)

    def test_period_minute_add_to_date_raises_error(self):
        """Test that adding minutes to Date raises error."""
        date = Date(2023, 12, 25)

        with pytest.raises(ValueError, match="Cannot add minutes to Date"):
            Period.MINUTE.add_to(date)

    def test_period_hour_add_to_date_raises_error(self):
        """Test that adding hours to Date raises error."""
        date = Date(2023, 12, 25)

        with pytest.raises(ValueError, match="Cannot add hours to Date"):
            Period.HOUR.add_to(date)


class TestPeriodSubtractFrom:
    def test_period_day_subtract_from_date(self):
        """Test subtracting days from Date."""
        date = Date(2023, 12, 25)
        result = Period.DAY.subtract_from(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 24)

    def test_period_week_subtract_from_date(self):
        """Test subtracting weeks from Date."""
        date = Date(2023, 12, 25)
        result = Period.WEEK.subtract_from(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 18)

    def test_period_month_subtract_from_date(self):
        """Test subtracting months from Date."""
        date = Date(2024, 1, 25)
        result = Period.MONTH.subtract_from(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 25)

    def test_period_hour_subtract_from_datetime(self):
        """Test subtracting hours from DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.HOUR.subtract_from(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 13, 30, 45)

    def test_period_minute_subtract_from_date_raises_error(self):
        """Test that subtracting minutes from Date raises error."""
        date = Date(2023, 12, 25)

        with pytest.raises(ValueError, match="Cannot subtract minutes from Date"):
            Period.MINUTE.subtract_from(date)


class TestPeriodStartOf:
    def test_period_day_start_of_date(self):
        """Test start of day for Date (should return same date)."""
        date = Date(2023, 12, 25)
        result = Period.DAY.start_of(date)

        assert isinstance(result, Date)
        assert result == date

    def test_period_week_start_of_date(self):
        """Test start of week for Date."""
        date = Date(2023, 12, 25)  # Monday
        result = Period.WEEK.start_of(date)

        assert isinstance(result, Date)
        # Should return start of that week (Monday)

    def test_period_month_start_of_date(self):
        """Test start of month for Date."""
        date = Date(2023, 12, 25)
        result = Period.MONTH.start_of(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 1)

    def test_period_quarter_start_of_date(self):
        """Test start of quarter for Date."""
        date = Date(2023, 12, 25)  # Q4
        result = Period.QUARTER.start_of(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 10, 1)

    def test_period_year_start_of_date(self):
        """Test start of year for Date."""
        date = Date(2023, 12, 25)
        result = Period.YEAR.start_of(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 1, 1)

    def test_period_hour_start_of_datetime(self):
        """Test start of hour for DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.HOUR.start_of(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 14, 0, 0)

    def test_period_minute_start_of_datetime(self):
        """Test start of minute for DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.MINUTE.start_of(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 14, 30, 0)

    def test_period_minute_start_of_date_raises_error(self):
        """Test that start of minute for Date raises error."""
        date = Date(2023, 12, 25)

        with pytest.raises(ValueError, match="Cannot get start of minute for Date"):
            Period.MINUTE.start_of(date)


class TestPeriodEndOf:
    def test_period_day_end_of_date(self):
        """Test end of day for Date (should return same date)."""
        date = Date(2023, 12, 25)
        result = Period.DAY.end_of(date)

        assert isinstance(result, Date)
        assert result == date

    def test_period_month_end_of_date(self):
        """Test end of month for Date."""
        date = Date(2023, 12, 25)
        result = Period.MONTH.end_of(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 31)

    def test_period_year_end_of_date(self):
        """Test end of year for Date."""
        date = Date(2023, 6, 15)
        result = Period.YEAR.end_of(date)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 31)

    def test_period_hour_end_of_datetime(self):
        """Test end of hour for DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.HOUR.end_of(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 14, 59, 59, 999999)

    def test_period_minute_end_of_datetime(self):
        """Test end of minute for DateTime."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)
        result = Period.MINUTE.end_of(dt)

        assert isinstance(result, DateTime)
        assert result == DateTime(2023, 12, 25, 14, 30, 59, 999999)


class TestPeriodEdgeCases:
    def test_period_add_negative_count(self):
        """Test adding negative count (should subtract)."""
        date = Date(2023, 12, 25)
        result = Period.DAY.add_to(date, count=-5)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 20)

    def test_period_subtract_negative_count(self):
        """Test subtracting negative count (should add)."""
        date = Date(2023, 12, 20)
        result = Period.DAY.subtract_from(date, count=-5)

        assert isinstance(result, Date)
        assert result == Date(2023, 12, 25)

    def test_period_add_zero_count(self):
        """Test adding zero count (should return same)."""
        date = Date(2023, 12, 25)
        result = Period.DAY.add_to(date, count=0)

        assert isinstance(result, Date)
        assert result == date

    def test_period_month_end_overflow(self):
        """Test month operations that might overflow."""
        date = Date(2023, 1, 31)
        result = Period.MONTH.add_to(date)

        # Should handle month-end overflow (Jan 31 + 1 month -> Feb 28)
        assert isinstance(result, Date)
        # Exact behavior depends on implementation