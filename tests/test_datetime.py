import datetime
from zoneinfo import ZoneInfo

import pytest

from carbonic.core.datetime import DateTime


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
        diff = abs((dt._dt - now).total_seconds())
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
