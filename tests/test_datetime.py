import datetime
from zoneinfo import ZoneInfo

import pytest

from carbonic import DateTime, Duration


class TestDateTimeConstructor:
    def test_constructor_basic(self):
        """Test basic DateTime constructor with year, month, day."""
        dt = DateTime(2025, 9, 23)
        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 0
        assert dt.minute == 0
        assert dt.second == 0
        assert dt.microsecond == 0

    def test_constructor_with_time(self):
        """Test DateTime constructor with time components."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)
        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        assert dt.microsecond == 123456

    def test_constructor_with_timezone(self):
        """Test DateTime constructor with timezone."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, tz="Europe/Warsaw")
        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        assert dt.tzinfo == ZoneInfo("Europe/Warsaw")

    def test_constructor_defaults_to_utc(self):
        """Test DateTime constructor defaults to UTC timezone."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        assert dt.tzinfo == ZoneInfo("UTC")


class TestDateTimeNow:
    def test_now_utc_default(self):
        """Test DateTime.now() defaults to UTC."""
        dt = DateTime.now()
        assert dt.tzinfo == ZoneInfo("UTC")
        # Should be close to current time (within a few seconds)
        now = datetime.datetime.now(ZoneInfo("UTC"))
        diff = abs((dt.to_datetime() - now).total_seconds())
        assert diff < 5  # Within 5 seconds

    def test_now_with_timezone(self):
        """Test DateTime.now() with specific timezone."""
        dt = DateTime.now("Europe/Warsaw")
        assert dt.tzinfo == ZoneInfo("Europe/Warsaw")


class TestDateTimeStringRepresentation:
    def test_str_representation(self):
        """Test string representation of DateTime."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        assert str(dt) == "2025-09-23T14:30:45+00:00"

    def test_repr_representation(self):
        """Test repr representation of DateTime."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        result = repr(dt)
        assert "DateTime" in result
        assert "2025" in result
        assert "9" in result
        assert "23" in result
        assert "14" in result
        assert "30" in result
        assert "45" in result


class TestDateTimeComparison:
    def test_equality(self):
        """Test DateTime equality comparison."""
        dt1 = DateTime(2025, 9, 23, 14, 30, 45)
        dt2 = DateTime(2025, 9, 23, 14, 30, 45)
        dt3 = DateTime(2025, 9, 23, 14, 30, 46)

        assert dt1 == dt2
        assert dt1 != dt3
        assert not (dt1 == "not a datetime")

    def test_ordering(self):
        """Test DateTime ordering comparisons."""
        dt1 = DateTime(2025, 9, 23, 14, 30, 45)
        dt2 = DateTime(2025, 9, 23, 14, 30, 46)
        dt3 = DateTime(2025, 9, 23, 14, 30, 44)

        assert dt1 < dt2
        assert dt1 <= dt2
        assert dt1 > dt3
        assert dt1 >= dt3
        assert dt1 <= dt1
        assert dt1 >= dt1

    def test_hash(self):
        """Test DateTime hashing for use in sets and dicts."""
        dt1 = DateTime(2025, 9, 23, 14, 30, 45)
        dt2 = DateTime(2025, 9, 23, 14, 30, 45)
        dt3 = DateTime(2025, 9, 23, 14, 30, 46)

        assert hash(dt1) == hash(dt2)
        assert hash(dt1) != hash(dt3)

        # Should work in sets
        dt_set = {dt1, dt2, dt3}
        assert len(dt_set) == 2  # dt1 and dt2 should be the same


class TestDateTimeConversions:
    def test_to_datetime(self):
        """Test conversion to stdlib datetime.datetime."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        stdlib_dt = dt.to_datetime()

        assert isinstance(stdlib_dt, datetime.datetime)
        assert stdlib_dt.year == 2025
        assert stdlib_dt.month == 9
        assert stdlib_dt.day == 23
        assert stdlib_dt.hour == 14
        assert stdlib_dt.minute == 30
        assert stdlib_dt.second == 45
        assert stdlib_dt.tzinfo == ZoneInfo("UTC")

    def test_to_date(self):
        """Test conversion to carbonic Date."""
        from carbonic.core.date import Date

        dt = DateTime(2025, 9, 23, 14, 30, 45)
        date = dt.to_date()

        assert isinstance(date, Date)
        assert date.year == 2025
        assert date.month == 9
        assert date.day == 23


class TestDateTimeArithmetic:
    def test_add_timedelta_components(self):
        """Test adding time components to DateTime."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Add days
        result = dt.add(days=1)
        assert result.day == 24
        assert result.hour == 14  # Time should remain the same

        # Add hours
        result = dt.add(hours=2)
        assert result.hour == 16
        assert result.day == 23  # Date should remain the same

        # Add minutes
        result = dt.add(minutes=30)
        assert result.minute == 0  # 30 + 30 = 60 -> 0 with hour increment
        assert result.hour == 15

        # Add seconds
        result = dt.add(seconds=30)
        assert result.second == 15  # 45 + 30 = 75 -> 15 with minute increment
        assert result.minute == 31

    def test_subtract_timedelta_components(self):
        """Test subtracting time components from DateTime."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Subtract days
        result = dt.subtract(days=1)
        assert result.day == 22

        # Subtract hours
        result = dt.subtract(hours=2)
        assert result.hour == 12


class TestDateTimeAnchors:
    def test_start_of_minute(self):
        """Test start_of('minute') - zeros seconds and microseconds."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)
        result = dt.start_of("minute")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 23
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 0
        assert result.microsecond == 0

    def test_start_of_hour(self):
        """Test start_of('hour') - zeros minutes, seconds and microseconds."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)
        result = dt.start_of("hour")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 23
        assert result.hour == 14
        assert result.minute == 0
        assert result.second == 0
        assert result.microsecond == 0

    def test_start_of_day(self):
        """Test start_of('day') - sets time to 00:00:00."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)
        result = dt.start_of("day")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 23
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0
        assert result.microsecond == 0

    def test_start_of_week(self):
        """Test start_of('week') - goes to Monday 00:00:00."""
        # Tuesday, Sept 23, 2025
        dt = DateTime(2025, 9, 23, 14, 30, 45)  # Tuesday
        result = dt.start_of("week")

        # Should go to Monday, Sept 22, 2025 00:00:00
        assert result.year == 2025
        assert result.month == 9
        assert result.day == 22  # Monday
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_start_of_month(self):
        """Test start_of('month') - goes to first day of month 00:00:00."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        result = dt.start_of("month")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 1
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_start_of_year(self):
        """Test start_of('year') - goes to Jan 1 00:00:00."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        result = dt.start_of("year")

        assert result.year == 2025
        assert result.month == 1
        assert result.day == 1
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

    def test_end_of_minute(self):
        """Test end_of('minute') - sets seconds to 59, microseconds to 999999."""
        dt = DateTime(2025, 9, 23, 14, 30, 15, 123456)
        result = dt.end_of("minute")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 23
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 59
        assert result.microsecond == 999999

    def test_end_of_hour(self):
        """Test end_of('hour') - sets to 59:59.999999."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)
        result = dt.end_of("hour")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 23
        assert result.hour == 14
        assert result.minute == 59
        assert result.second == 59
        assert result.microsecond == 999999

    def test_end_of_day(self):
        """Test end_of('day') - sets time to 23:59:59.999999."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)
        result = dt.end_of("day")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 23
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59
        assert result.microsecond == 999999

    def test_end_of_week(self):
        """Test end_of('week') - goes to Sunday 23:59:59.999999."""
        # Tuesday, Sept 23, 2025
        dt = DateTime(2025, 9, 23, 14, 30, 45)  # Tuesday
        result = dt.end_of("week")

        # Should go to Sunday, Sept 28, 2025 23:59:59.999999
        assert result.year == 2025
        assert result.month == 9
        assert result.day == 28  # Sunday
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59
        assert result.microsecond == 999999

    def test_end_of_month(self):
        """Test end_of('month') - goes to last day of month 23:59:59.999999."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        result = dt.end_of("month")

        assert result.year == 2025
        assert result.month == 9
        assert result.day == 30  # September has 30 days
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59
        assert result.microsecond == 999999

    def test_end_of_year(self):
        """Test end_of('year') - goes to Dec 31 23:59:59.999999."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)
        result = dt.end_of("year")

        assert result.year == 2025
        assert result.month == 12
        assert result.day == 31
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59
        assert result.microsecond == 999999


class TestDateTimeParsing:
    def test_parse_iso_datetime_utc(self):
        """Test parsing ISO datetime with UTC timezone."""
        dt = DateTime.parse("2025-09-23T14:30:45+00:00")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        assert dt.tzinfo == ZoneInfo("UTC")

    def test_parse_iso_datetime_with_timezone(self):
        """Test parsing ISO datetime with specific timezone."""
        dt = DateTime.parse("2025-09-23T14:30:45+02:00")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        # Should preserve timezone offset

    def test_parse_iso_datetime_naive(self):
        """Test parsing ISO datetime without timezone (should default to UTC)."""
        dt = DateTime.parse("2025-09-23T14:30:45")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        assert dt.tzinfo == ZoneInfo("UTC")  # Should default to UTC

    def test_parse_iso_date_only(self):
        """Test parsing ISO date (should set time to 00:00:00)."""
        dt = DateTime.parse("2025-09-23")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 0
        assert dt.minute == 0
        assert dt.second == 0
        assert dt.tzinfo == ZoneInfo("UTC")

    def test_parse_with_explicit_format_strftime(self):
        """Test parsing with explicit strftime format."""
        dt = DateTime.parse("23/09/2025 14:30:45", "%d/%m/%Y %H:%M:%S")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45

    def test_parse_with_explicit_format_carbon(self):
        """Test parsing with explicit Carbon-style format."""
        dt = DateTime.parse("23/09/2025 14:30:45", "d/m/Y H:i:s")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45

    def test_parse_with_timezone_parameter(self):
        """Test parsing with explicit timezone parameter."""
        dt = DateTime.parse("2025-09-23T14:30:45", tz="Europe/Warsaw")

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        assert dt.tzinfo == ZoneInfo("Europe/Warsaw")


class TestDateTimeParsingErrors:
    def test_parse_empty_string(self):
        """Test parsing empty string raises ParseError."""

        from carbonic.core.exceptions import ParseError

        with pytest.raises(ParseError, match="Empty datetime string"):
            DateTime.parse("")

        with pytest.raises(ParseError, match="Empty datetime string"):
            DateTime.parse("   ")  # whitespace only

    def test_parse_invalid_datetime(self):
        """Test parsing invalid datetime raises ParseError."""

        from carbonic.core.exceptions import ParseError

        with pytest.raises(ParseError, match="Unable to parse datetime"):
            DateTime.parse("not-a-datetime")

        with pytest.raises(ParseError, match="Invalid date"):
            DateTime.parse("2025-13-45")  # invalid month/day

    def test_parse_with_invalid_format(self):
        """Test parsing with invalid format raises ParseError."""

        from carbonic.core.exceptions import ParseError

        with pytest.raises(ParseError, match="Failed to parse"):
            DateTime.parse("2025-09-23", "%Y/%m/%d")  # wrong format


class TestDateTimeFormatting:
    def test_format_carbon_basic(self):
        """Test basic Carbon-style formatting."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Basic date components
        assert dt.format("Y-m-d") == "2025-09-23"
        assert dt.format("d/m/Y") == "23/09/2025"
        assert dt.format("j-n-y") == "23-9-25"

        # Basic time components
        assert dt.format("H:i:s") == "14:30:45"
        assert dt.format("h:i A") == "02:30 PM"  # 12-hour format

        # Combined datetime
        assert dt.format("Y-m-d H:i:s") == "2025-09-23 14:30:45"
        assert dt.format("d/m/Y H:i") == "23/09/2025 14:30"

    def test_format_carbon_advanced(self):
        """Test advanced Carbon-style formatting tokens."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Day names and ordinals
        assert dt.format("l, jS F Y") == "Tuesday, 23rd September 2025"
        assert dt.format("D M j") == "Tue Sep 23"

        # Various time formats
        assert dt.format("g:i A") == "2:30 PM"  # 12-hour without leading zero
        assert dt.format("G:i") == "14:30"  # 24-hour without leading zero

    def test_format_carbon_microseconds(self):
        """Test formatting with microseconds."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, 123456)

        assert dt.format("H:i:s.u") == "14:30:45.123456"
        assert dt.format("Y-m-d H:i:s.v") == "2025-09-23 14:30:45.123"  # milliseconds

    def test_format_carbon_timezone(self):
        """Test formatting with timezone information."""
        dt_utc = DateTime(2025, 9, 23, 14, 30, 45)
        dt_poland = DateTime(2025, 9, 23, 14, 30, 45, tz="Europe/Warsaw")

        assert dt_utc.format("Y-m-d H:i:s T") == "2025-09-23 14:30:45 UTC"
        assert dt_poland.format("c") == "2025-09-23T14:30:45+02:00"  # ISO 8601

    def test_strftime_enhanced(self):
        """Test enhanced strftime functionality."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Standard strftime
        assert dt.strftime("%Y-%m-%d %H:%M:%S") == "2025-09-23 14:30:45"
        assert dt.strftime("%A, %B %d, %Y") == "Tuesday, September 23, 2025"

        # With timezone
        dt_tz = DateTime(2025, 9, 23, 14, 30, 45)
        assert dt_tz.strftime("%Y-%m-%d %H:%M:%S %Z") == "2025-09-23 14:30:45 UTC"

    def test_format_shortcut_methods(self):
        """Test common format shortcut methods."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # ISO formats
        assert dt.to_iso_string() == "2025-09-23T14:30:45+00:00"
        assert dt.to_date_string() == "2025-09-23"
        assert dt.to_time_string() == "14:30:45"
        assert dt.to_datetime_string() == "2025-09-23 14:30:45"

        # Atom/RSS format
        assert dt.to_atom_string() == "2025-09-23T14:30:45+00:00"

        # Cookie format
        assert dt.to_cookie_string() == "Tue, 23-Sep-2025 14:30:45 UTC"

    def test_python_format_protocol(self):
        """Test Python's __format__ protocol support."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Should work with f-strings using Carbon format
        assert f"{dt:Y-m-d}" == "2025-09-23"
        assert f"{dt:H:i:s}" == "14:30:45"

        # Should work with format() function
        assert format(dt, "d/m/Y H:i") == "23/09/2025 14:30"


class TestDateTimeDurationIntegration:
    def test_datetime_diff_basic(self):
        """Test basic datetime difference calculation."""

        dt1 = DateTime(2023, 12, 25, 10, 30, 45)
        dt2 = DateTime(2023, 12, 25, 12, 45, 30)

        diff = dt2.diff(dt1)
        assert isinstance(diff, Duration)
        assert diff.days == 0
        assert diff.storage_seconds == 2 * 3600 + 14 * 60 + 45  # 2h 14m 45s

    def test_datetime_diff_with_days(self):
        """Test datetime difference spanning days."""

        dt1 = DateTime(2023, 12, 25, 14, 30, 0)
        dt2 = DateTime(2023, 12, 27, 10, 15, 30)

        diff = dt2.diff(dt1)
        assert isinstance(diff, Duration)
        assert diff.days == 1  # 1 full day
        # Remaining time: 27th 10:15:30 - 25th 14:30:00 = 1d 19h 45m 30s
        # So seconds part should be: 19h 45m 30s = 19*3600 + 45*60 + 30
        expected_seconds = 19 * 3600 + 45 * 60 + 30
        assert diff.storage_seconds == expected_seconds

    def test_datetime_diff_negative(self):
        """Test datetime difference with negative result."""

        dt1 = DateTime(2023, 12, 25, 14, 30, 0)
        dt2 = DateTime(2023, 12, 25, 10, 15, 0)

        diff = dt2.diff(dt1)
        assert isinstance(diff, Duration)
        assert diff.days == -1  # Goes to previous day due to negative seconds
        # -4h 15m = -15300 seconds, which gets normalized to -1 day + 70500 seconds
        expected_seconds = 24 * 3600 - (4 * 3600 + 15 * 60)
        assert diff.storage_seconds == expected_seconds

    def test_datetime_diff_absolute(self):
        """Test datetime difference with absolute flag."""

        dt1 = DateTime(2023, 12, 25, 14, 30, 0)
        dt2 = DateTime(2023, 12, 25, 10, 15, 0)

        diff = dt2.diff(dt1, absolute=True)
        assert isinstance(diff, Duration)
        assert diff.days >= 0  # Should be positive
        # Absolute difference of 4h 15m
        total_seconds = abs(dt2.to_datetime() - dt1.to_datetime()).total_seconds()
        assert diff.total_seconds() == total_seconds

    def test_datetime_diff_with_microseconds(self):
        """Test datetime difference including microseconds."""

        dt1 = DateTime(2023, 12, 25, 10, 30, 45, 123456)
        dt2 = DateTime(2023, 12, 25, 10, 30, 46, 654321)

        diff = dt2.diff(dt1)
        assert isinstance(diff, Duration)
        assert diff.days == 0
        assert diff.storage_seconds == 1  # 1 second difference
        assert diff.microseconds == 654321 - 123456  # microsecond difference

    def test_datetime_diff_timezone_aware(self):
        """Test datetime difference with timezone-aware datetimes."""

        # Same instant in different timezones
        dt_utc = DateTime(2023, 12, 25, 15, 0, 0, tz="UTC")
        dt_ny = DateTime(2023, 12, 25, 10, 0, 0, tz="America/New_York")

        diff = dt_utc.diff(dt_ny)
        assert isinstance(diff, Duration)
        # Should be zero since they represent the same instant
        assert diff.days == 0
        assert diff.storage_seconds == 0
        assert diff.microseconds == 0

    def test_datetime_diff_same_datetime(self):
        """Test difference between same datetimes."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        diff = dt.diff(dt)

        assert isinstance(diff, Duration)
        assert diff.days == 0
        assert diff.storage_seconds == 0
        assert diff.microseconds == 0

    def test_datetime_add_duration_basic(self):
        """Test adding Duration to DateTime."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        duration = Duration(hours=2, minutes=15, seconds=30)

        result = dt + duration
        assert isinstance(result, DateTime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 16  # 14 + 2
        assert result.minute == 46  # 30 + 15 + 1 (carry from seconds)
        assert result.second == 15  # 45 + 30 = 75 -> 15 with 1 minute carry

    def test_datetime_add_duration_with_days(self):
        """Test adding Duration with days to DateTime."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        duration = Duration(days=2, hours=10)

        result = dt + duration
        assert isinstance(result, DateTime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 28  # 25 + 2 + 1 (from hour overflow) = 28
        assert result.hour == 0  # 14 + 10 = 24 -> 0 with 1 day carry
        assert result.minute == 30
        assert result.second == 45

    def test_datetime_add_duration_overflow_month(self):
        """Test adding Duration that causes month overflow."""

        dt = DateTime(2023, 12, 30, 20, 0, 0)
        duration = Duration(days=3, hours=8)

        result = dt + duration
        assert isinstance(result, DateTime)
        assert result.year == 2024  # Overflow to next year
        assert result.month == 1
        assert result.day == 3  # Dec 30 + 3 days + 1 (from hour overflow) = Jan 3
        assert result.hour == 4  # 20 + 8 = 28 -> 4 next day

    def test_datetime_add_duration_with_calendar_components(self):
        """Test adding Duration with calendar components."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        duration = Duration(years=1, months=2, days=5, hours=3)

        result = dt + duration
        assert isinstance(result, DateTime)
        assert result.year == 2025
        assert result.month == 2
        assert result.day == 28  # Same logic as Date: Feb 30 -> Feb 28
        assert result.hour == 17  # 14 + 3
        assert result.minute == 30
        assert result.second == 45

    def test_datetime_subtract_duration(self):
        """Test subtracting Duration from DateTime."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        duration = Duration(hours=2, minutes=15, seconds=30)

        result = dt - duration
        assert isinstance(result, DateTime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 12  # 14 - 2
        assert result.minute == 15  # 30 - 15
        assert result.second == 15  # 45 - 30

    def test_datetime_subtract_duration_underflow(self):
        """Test subtracting Duration causing time underflow."""

        dt = DateTime(2024, 1, 2, 2, 15, 30)
        duration = Duration(days=1, hours=5, minutes=20)

        result = dt - duration
        assert isinstance(result, DateTime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 31
        assert result.hour == 20  # 2 - 5 = -3 -> 21 previous day -> 20 (with day carry)
        assert result.minute == 55  # 15 - 20 = -5 -> 55 previous hour
        assert result.second == 30

    def test_datetime_add_duration_with_microseconds(self):
        """Test adding Duration with microseconds."""

        dt = DateTime(2023, 12, 25, 14, 30, 45, 123456)
        duration = Duration(seconds=2, microseconds=500000)

        result = dt + duration
        assert isinstance(result, DateTime)
        assert result.second == 47  # 45 + 2
        assert result.microsecond == 623456  # 123456 + 500000

    def test_datetime_add_duration_microsecond_overflow(self):
        """Test adding Duration causing microsecond overflow."""

        dt = DateTime(2023, 12, 25, 14, 30, 45, 800000)
        duration = Duration(microseconds=400000)

        result = dt + duration
        assert isinstance(result, DateTime)
        assert result.second == 46  # 45 + 1 (carry from microseconds)
        assert result.microsecond == 200000  # 800000 + 400000 - 1000000

    def test_datetime_add_duration_method(self):
        """Test explicit add_duration method."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        duration = Duration(hours=1, minutes=30)

        result = dt.add_duration(duration)
        assert isinstance(result, DateTime)
        assert result.hour == 16  # 14 + 1 + 1 (carry from minutes)
        assert result.minute == 0  # 30 + 30 = 60 -> 0 with hour carry

    def test_datetime_subtract_duration_method(self):
        """Test explicit subtract_duration method."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        duration = Duration(hours=1, minutes=15)

        result = dt.subtract_duration(duration)
        assert isinstance(result, DateTime)
        assert result.hour == 13
        assert result.minute == 15  # 30 - 15

    def test_datetime_subtract_datetime(self):
        """Test DateTime - DateTime subtraction using - operator."""

        dt1 = DateTime(2023, 12, 25, 14, 30, 45)
        dt2 = DateTime(2023, 12, 25, 12, 15, 30)

        # dt1 - dt2 should give positive difference
        diff = dt1 - dt2
        assert isinstance(diff, Duration)
        assert diff.days == 0
        expected_seconds = 2 * 3600 + 15 * 60 + 15  # 2h 15m 15s
        assert diff.storage_seconds == expected_seconds

        # dt2 - dt1 should give negative difference
        diff_reverse = dt2 - dt1
        assert isinstance(diff_reverse, Duration)
        # Negative seconds get normalized to previous day
        assert diff_reverse.days == -1
        assert diff_reverse.storage_seconds == 86400 - expected_seconds

    def test_datetime_subtract_datetime_same(self):
        """Test subtracting same datetime should return zero duration."""

        dt = DateTime(2023, 12, 25, 14, 30, 45)
        diff = dt - dt

        assert isinstance(diff, Duration)
        assert diff.days == 0
        assert diff.storage_seconds == 0
        assert diff.microseconds == 0

    def test_datetime_subtract_datetime_with_days(self):
        """Test DateTime - DateTime subtraction spanning multiple days."""

        dt1 = DateTime(2023, 12, 27, 10, 15, 30)
        dt2 = DateTime(2023, 12, 25, 14, 30, 0)

        diff = dt1 - dt2
        assert isinstance(diff, Duration)
        assert diff.days == 1  # 1 full day
        # Remaining time: 27th 10:15:30 - 25th 14:30:00 = 1d 19h 45m 30s
        # So seconds part should be: 19h 45m 30s = 19*3600 + 45*60 + 30
        expected_seconds = 19 * 3600 + 45 * 60 + 30
        assert diff.storage_seconds == expected_seconds

    def test_datetime_subtract_datetime_with_microseconds(self):
        """Test DateTime - DateTime subtraction including microseconds."""

        dt1 = DateTime(2023, 12, 25, 10, 30, 46, 654321)
        dt2 = DateTime(2023, 12, 25, 10, 30, 45, 123456)

        diff = dt1 - dt2
        assert isinstance(diff, Duration)
        assert diff.days == 0
        assert diff.storage_seconds == 1  # 1 second difference
        expected_microseconds = 654321 - 123456
        assert diff.microseconds == expected_microseconds

    def test_datetime_subtract_datetime_timezone_aware(self):
        """Test DateTime - DateTime subtraction with timezone-aware datetimes."""

        # Same instant in different timezones
        dt_utc = DateTime(2023, 12, 25, 15, 0, 0, tz="UTC")
        dt_ny = DateTime(2023, 12, 25, 10, 0, 0, tz="America/New_York")

        diff = dt_utc - dt_ny
        assert isinstance(diff, Duration)
        # Should be zero since they represent the same instant
        assert diff.days == 0
        assert diff.storage_seconds == 0

    def test_datetime_duration_arithmetic_type_error(self):
        """Test Duration arithmetic with invalid types."""
        dt = DateTime(2023, 12, 25, 14, 30, 45)

        with pytest.raises(TypeError):
            dt + "not a duration"  # type: ignore

        with pytest.raises(TypeError):
            dt - 123  # type: ignore


class TestDateTimeTimezoneConversion:
    """Test timezone conversion functionality."""

    def test_as_timezone_basic_conversion(self):
        """Test basic timezone conversion between UTC and other timezones."""
        # UTC to New York (winter time, UTC-5)
        utc_dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        ny_dt = utc_dt.as_timezone("America/New_York")

        assert ny_dt.year == 2024
        assert ny_dt.month == 1
        assert ny_dt.day == 15
        assert ny_dt.hour == 9  # 14:30 UTC = 09:30 EST (UTC-5)
        assert ny_dt.minute == 30
        assert ny_dt.second == 0
        assert str(ny_dt.tzinfo) == "America/New_York"

    def test_as_timezone_summer_time(self):
        """Test timezone conversion during daylight saving time."""
        # UTC to New York (summer time, UTC-4)
        utc_dt = DateTime(2024, 7, 15, 14, 30, 0, tz="UTC")
        ny_dt = utc_dt.as_timezone("America/New_York")

        assert ny_dt.hour == 10  # 14:30 UTC = 10:30 EDT (UTC-4)
        assert ny_dt.minute == 30

    def test_as_timezone_same_moment(self):
        """Test that converted datetime represents the same moment."""
        utc_dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        ny_dt = utc_dt.as_timezone("America/New_York")
        warsaw_dt = utc_dt.as_timezone("Europe/Warsaw")

        # All should represent the same moment in time
        assert utc_dt == ny_dt
        assert utc_dt == warsaw_dt
        assert ny_dt == warsaw_dt

    def test_as_timezone_round_trip(self):
        """Test converting timezone and back preserves the original."""
        original = DateTime(2024, 1, 15, 14, 30, 45, 123456, tz="UTC")
        converted = original.as_timezone("America/New_York")
        back_to_utc = converted.as_timezone("UTC")

        assert original == back_to_utc
        assert (
            original.to_datetime() == back_to_utc.to_datetime()
        )  # Should be identical

    def test_as_timezone_multiple_conversions(self):
        """Test converting through multiple timezones."""
        utc_dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        ny_dt = utc_dt.as_timezone("America/New_York")
        warsaw_dt = ny_dt.as_timezone("Europe/Warsaw")
        tokyo_dt = warsaw_dt.as_timezone("Asia/Tokyo")

        # All should represent the same moment
        assert utc_dt == ny_dt == warsaw_dt == tokyo_dt

    def test_as_timezone_to_naive(self):
        """Test converting timezone-aware datetime to naive."""
        aware_dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        naive_dt = aware_dt.as_timezone(None)

        assert naive_dt.tzinfo is None
        assert naive_dt.year == 2024
        assert naive_dt.month == 1
        assert naive_dt.day == 15
        assert naive_dt.hour == 14  # Keeps the local time representation
        assert naive_dt.minute == 30
        assert naive_dt.second == 0

    def test_as_timezone_naive_to_naive(self):
        """Test converting naive datetime to naive (should return copy)."""
        naive_dt = DateTime(2024, 1, 15, 14, 30, 0, tz=None)
        copy_dt = naive_dt.as_timezone(None)

        assert copy_dt.tzinfo is None
        assert copy_dt == naive_dt
        assert copy_dt is not naive_dt  # Should be a new instance

    def test_as_timezone_naive_to_aware_raises_error(self):
        """Test that converting naive to timezone-aware raises ValueError."""
        naive_dt = DateTime(2024, 1, 15, 14, 30, 0, tz=None)

        with pytest.raises(
            ValueError, match="Cannot convert naive DateTime to timezone-aware"
        ):
            naive_dt.as_timezone("UTC")

    def test_as_timezone_invalid_timezone(self):
        """Test that invalid timezone raises ValueError."""
        dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")

        with pytest.raises(ValueError, match="Invalid timezone"):
            dt.as_timezone("Invalid/Timezone")

    def test_as_timezone_preserves_microseconds(self):
        """Test that timezone conversion preserves microseconds."""
        utc_dt = DateTime(2024, 1, 15, 14, 30, 45, 123456, tz="UTC")
        ny_dt = utc_dt.as_timezone("America/New_York")

        assert ny_dt.microsecond == 123456

    def test_as_timezone_dst_boundary(self):
        """Test timezone conversion around DST boundary."""
        # Test time just before DST starts in 2024 (March 10, 2:00 AM -> 3:00 AM)
        utc_dt = DateTime(2024, 3, 10, 6, 30, 0, tz="UTC")  # 1:30 AM EST
        ny_dt = utc_dt.as_timezone("America/New_York")

        assert ny_dt.hour == 1  # Should be 1:30 AM EST

        # Test time after DST starts
        utc_dt_after = DateTime(2024, 3, 10, 7, 30, 0, tz="UTC")  # After DST
        ny_dt_after = utc_dt_after.as_timezone("America/New_York")

        assert ny_dt_after.hour == 3  # Should be 3:30 AM EDT (skipped 2:30 AM)

    def test_as_timezone_various_timezones(self):
        """Test conversion to various worldwide timezones."""
        utc_dt = DateTime(2024, 1, 15, 12, 0, 0, tz="UTC")

        test_cases = [
            ("Europe/London", 12),  # UTC+0 in winter
            ("Europe/Warsaw", 13),  # UTC+1 in winter
            ("Asia/Tokyo", 21),  # UTC+9
            ("America/New_York", 7),  # UTC-5 in winter
            ("America/Los_Angeles", 4),  # UTC-8 in winter
            ("Australia/Sydney", 23),  # UTC+11 in summer
        ]

        for tz_name, expected_hour in test_cases:
            converted = utc_dt.as_timezone(tz_name)
            assert converted.hour == expected_hour, f"Failed for {tz_name}"
            assert converted == utc_dt  # Should represent same moment


class TestDateTimeFormatEscaping:
    """Test escape sequences in format strings."""

    def test_escape_carbon_tokens(self):
        """Test escaping Carbon format tokens."""
        dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

        # Escape Y token
        result = dt.format("{Y} = Y")
        assert result == "Y = 2024"

        # Escape multiple tokens
        result = dt.format("{Y}-{m}-{d} = Y-m-d")
        assert result == "Y-m-d = 2024-01-15"

        # n and j tokens
        result = dt.format("{n}/{j} = n/j")
        assert result == "n/j = 1/15"

    def test_python_string_literals(self):
        """Test using Python string literals for special characters."""
        dt = DateTime(2024, 1, 15, 14, 30, 45)

        # Test newline using Python string literal
        result = dt.format("Y-m-d\nH:i:s")
        assert result == "2024-01-15\n14:30:45"

        # Test tab using Python string literal
        result = dt.format("Y-m-d\tH:i:s")
        assert result == "2024-01-15\t14:30:45"

        # Test carriage return using Python string literal
        result = dt.format("Y-m-d\rH:i:s")
        assert result == "2024-01-15\r14:30:45"

    def test_escape_backslash(self):
        """Test escaping backslash itself."""
        dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

        # Escape backslash
        result = dt.format("Y\\m\\d")
        assert result == "2024\\01\\15"

    def test_mixed_escaping(self):
        """Test mixed Carbon token escaping with Python string literals."""
        dt = DateTime(2024, 1, 15, 14, 30, 45, tz="UTC")

        # Mix of escaped tokens and Python string literals
        result = dt.format("{Y}-{m}-{d}\nH:i:s\n{Y} BEK")
        expected = "Y-m-d\n14:30:45\nY BEK"
        assert result == expected
