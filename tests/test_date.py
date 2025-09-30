import datetime
from zoneinfo import ZoneInfo

import pytest

from carbonic import Date, Duration
from carbonic.core.exceptions import ParseError


def test_date_create_basic():
    """Test basic Date creation."""
    date = Date(2023, 12, 25)
    assert date.year == 2023
    assert date.month == 12
    assert date.day == 25


def test_date_from_datetime_date():
    """Test Date creation from datetime.date."""
    dt_date = datetime.date(2023, 12, 25)
    date = Date.from_date(dt_date)
    assert date.year == 2023
    assert date.month == 12
    assert date.day == 25


def test_date_today():
    """Test Date.today() creates current date."""
    date = Date.today()
    today = datetime.date.today()
    assert date.year == today.year
    assert date.month == today.month
    assert date.day == today.day


def test_date_add_days():
    """Test adding days to a date."""
    date = Date(2023, 12, 25)
    new_date = date.add(days=5)
    assert new_date.year == 2023
    assert new_date.month == 12
    assert new_date.day == 30


def test_date_add_days_cross_month():
    """Test adding days that cross month boundary."""
    date = Date(2023, 12, 28)
    new_date = date.add(days=5)
    assert new_date.year == 2024
    assert new_date.month == 1
    assert new_date.day == 2


def test_date_add_months():
    """Test adding months to a date."""
    date = Date(2023, 10, 15)
    new_date = date.add(months=2)
    assert new_date.year == 2023
    assert new_date.month == 12
    assert new_date.day == 15


def test_date_add_months_cross_year():
    """Test adding months that cross year boundary."""
    date = Date(2023, 11, 15)
    new_date = date.add(months=3)
    assert new_date.year == 2024
    assert new_date.month == 2
    assert new_date.day == 15


def test_date_add_years():
    """Test adding years to a date."""
    date = Date(2020, 2, 29)  # leap year
    new_date = date.add(years=1)
    assert new_date.year == 2021
    assert new_date.month == 2
    assert new_date.day == 28  # Feb 29 -> Feb 28 in non-leap year


def test_date_add_combined():
    """Test adding years, months, and days together."""
    date = Date(2023, 1, 1)
    new_date = date.add(years=1, months=2, days=10)
    assert new_date.year == 2024
    assert new_date.month == 3
    assert new_date.day == 11


def test_date_subtract_days():
    """Test subtracting days from a date."""
    date = Date(2023, 12, 25)
    new_date = date.subtract(days=5)
    assert new_date.year == 2023
    assert new_date.month == 12
    assert new_date.day == 20


def test_date_subtract_days_cross_month():
    """Test subtracting days that cross month boundary."""
    date = Date(2024, 1, 3)
    new_date = date.subtract(days=5)
    assert new_date.year == 2023
    assert new_date.month == 12
    assert new_date.day == 29


def test_date_subtract_months():
    """Test subtracting months from a date."""
    date = Date(2023, 12, 15)
    new_date = date.subtract(months=2)
    assert new_date.year == 2023
    assert new_date.month == 10
    assert new_date.day == 15


def test_date_subtract_months_cross_year():
    """Test subtracting months that cross year boundary."""
    date = Date(2024, 2, 15)
    new_date = date.subtract(months=3)
    assert new_date.year == 2023
    assert new_date.month == 11
    assert new_date.day == 15


def test_date_subtract_years():
    """Test subtracting years from a date."""
    date = Date(2021, 2, 28)
    new_date = date.subtract(years=1)
    assert new_date.year == 2020
    assert new_date.month == 2
    assert new_date.day == 28


def test_date_subtract_combined():
    """Test subtracting years, months, and days together."""
    date = Date(2024, 3, 11)
    new_date = date.subtract(years=1, months=2, days=10)
    assert new_date.year == 2023
    assert new_date.month == 1
    assert new_date.day == 1


def test_date_parse_iso_format():
    """Test parsing ISO date format (YYYY-MM-DD)."""
    date = Date.parse("2023-12-25")
    assert date.year == 2023
    assert date.month == 12
    assert date.day == 25


def test_date_parse_iso_format_variations():
    """Test parsing various ISO date formats."""
    # Basic ISO format
    date1 = Date.parse("2023-01-01")
    assert date1.year == 2023
    assert date1.month == 1
    assert date1.day == 1

    # Single digit month/day
    date2 = Date.parse("2023-1-1")
    assert date2.year == 2023
    assert date2.month == 1
    assert date2.day == 1

    # Mixed padding
    date3 = Date.parse("2023-01-1")
    assert date3.year == 2023
    assert date3.month == 1
    assert date3.day == 1


def test_date_parse_auto_detect():
    """Test auto-detection of common date formats."""
    # Slash format (US style)
    date1 = Date.parse("12/25/2023")
    assert date1.year == 2023
    assert date1.month == 12
    assert date1.day == 25

    # Dot format (European style)
    date2 = Date.parse("25.12.2023")
    assert date2.year == 2023
    assert date2.month == 12
    assert date2.day == 25

    # Different slash format (YYYY/MM/DD)
    date3 = Date.parse("2023/12/25")
    assert date3.year == 2023
    assert date3.month == 12
    assert date3.day == 25


def test_date_parse_with_format():
    """Test parsing with explicit format specification."""
    # Custom format with strftime-style tokens
    date1 = Date.parse("25-12-2023", fmt="%d-%m-%Y")
    assert date1.year == 2023
    assert date1.month == 12
    assert date1.day == 25

    # Different separator
    date2 = Date.parse("2023|12|25", fmt="%Y|%m|%d")
    assert date2.year == 2023
    assert date2.month == 12
    assert date2.day == 25

    # Month names
    date3 = Date.parse("25 Dec 2023", fmt="%d %b %Y")
    assert date3.year == 2023
    assert date3.month == 12
    assert date3.day == 25

    # Full month name
    date4 = Date.parse("December 25, 2023", fmt="%B %d, %Y")
    assert date4.year == 2023
    assert date4.month == 12
    assert date4.day == 25


def test_date_parse_carbon_style_tokens():
    """Test parsing with Carbon-style format tokens."""
    # Y-m-d format
    date1 = Date.parse("2023-12-25", fmt="Y-m-d")
    assert date1.year == 2023
    assert date1.month == 12
    assert date1.day == 25

    # d/m/Y format
    date2 = Date.parse("25/12/2023", fmt="d/m/Y")
    assert date2.year == 2023
    assert date2.month == 12
    assert date2.day == 25

    # j M Y format (day without leading zero, short month)
    date3 = Date.parse("25 Dec 2023", fmt="j M Y")
    assert date3.year == 2023
    assert date3.month == 12
    assert date3.day == 25


def test_date_parse_invalid_date():
    """Test parsing invalid dates raises ParseError."""
    # Invalid date
    with pytest.raises(ParseError):
        Date.parse("2023-02-30")  # February 30th doesn't exist

    # Invalid month
    with pytest.raises(ParseError):
        Date.parse("2023-13-01")  # Month 13 doesn't exist

    # Invalid format
    with pytest.raises(ParseError):
        Date.parse("not-a-date")

    # Empty string
    with pytest.raises(ParseError):
        Date.parse("")

    # Wrong format specified
    with pytest.raises(ParseError):
        Date.parse("2023-12-25", fmt="%d/%m/%Y")  # Format doesn't match


def test_date_parse_invalid_format_string():
    """Test parsing with invalid format strings."""
    # Unknown format token
    with pytest.raises(ParseError):
        Date.parse("2023-12-25", fmt="%Z-%Q-%X")  # Invalid tokens

    # Incomplete date
    with pytest.raises(ParseError):
        Date.parse("2023-12", fmt="%Y-%m")  # Missing day


def test_date_equality():
    """Test Date equality comparison."""
    date1 = Date(2023, 12, 25)
    date2 = Date(2023, 12, 25)
    date3 = Date(2023, 12, 26)

    # Same dates should be equal
    assert date1 == date2
    assert date2 == date1

    # Different dates should not be equal
    assert date1 != date3
    assert date3 != date1

    # Compare with same date from different constructors
    date4 = Date.from_date(datetime.date(2023, 12, 25))
    assert date1 == date4


def test_date_equality_with_other_types():
    """Test Date equality with other types."""
    date = Date(2023, 12, 25)

    # Should not be equal to incompatible types
    assert date != "2023-12-25"
    assert date != 20231225
    assert date is not None

    # Should be equal to datetime.date with same date (for compatibility)
    assert date == datetime.date(2023, 12, 25)
    assert date != datetime.date(2023, 12, 26)

    # Should return NotImplemented for unknown types
    assert (date == "string") is False
    assert (date != "string") is True


def test_date_ordering():
    """Test Date ordering comparisons."""
    date1 = Date(2023, 12, 24)  # Christmas Eve
    date2 = Date(2023, 12, 25)  # Christmas
    date3 = Date(2023, 12, 26)  # Boxing Day
    date4 = Date(2023, 12, 25)  # Same as date2

    # Less than
    assert date1 < date2
    assert date2 < date3
    assert not (date2 < date1)
    assert not (date2 < date4)  # Equal dates

    # Less than or equal
    assert date1 <= date2
    assert date2 <= date3
    assert date2 <= date4  # Equal dates
    assert not (date3 <= date2)

    # Greater than
    assert date2 > date1
    assert date3 > date2
    assert not (date1 > date2)
    assert not (date2 > date4)  # Equal dates

    # Greater than or equal
    assert date2 >= date1
    assert date3 >= date2
    assert date2 >= date4  # Equal dates
    assert not (date1 >= date2)


def test_date_ordering_cross_years():
    """Test Date ordering across different years."""
    date_2022 = Date(2022, 12, 31)
    date_2023 = Date(2023, 1, 1)

    assert date_2022 < date_2023
    assert date_2023 > date_2022
    assert date_2022 <= date_2023
    assert date_2023 >= date_2022


def test_date_ordering_with_other_types():
    """Test Date ordering with other types should raise TypeError."""
    date = Date(2023, 12, 25)

    # Should raise TypeError for comparisons with incompatible types
    with pytest.raises(TypeError):
        date < "2023-12-25"  # type: ignore

    with pytest.raises(TypeError):
        date <= 20231225  # type: ignore

    with pytest.raises(TypeError):
        date >= None  # type: ignore

    # Should work with datetime.date (for compatibility)
    assert date > datetime.date(2023, 12, 24)
    assert date < datetime.date(2023, 12, 26)
    assert date >= datetime.date(2023, 12, 25)
    assert date <= datetime.date(2023, 12, 25)


def test_date_sorting():
    """Test that Date objects can be sorted."""
    dates = [
        Date(2023, 12, 25),
        Date(2023, 1, 1),
        Date(2023, 6, 15),
        Date(2022, 12, 31),
    ]

    sorted_dates = sorted(dates)

    expected = [
        Date(2022, 12, 31),
        Date(2023, 1, 1),
        Date(2023, 6, 15),
        Date(2023, 12, 25),
    ]

    assert sorted_dates == expected


def test_date_hash():
    """Test Date hashing for use in sets and dicts."""
    date1 = Date(2023, 12, 25)
    date2 = Date(2023, 12, 25)  # Same date
    date3 = Date(2023, 12, 26)  # Different date

    # Equal dates should have equal hashes
    assert hash(date1) == hash(date2)

    # Different dates should have different hashes (usually)
    assert hash(date1) != hash(date3)

    # Should be usable in sets
    date_set = {date1, date2, date3}
    assert len(date_set) == 2  # date1 and date2 are the same

    # Should be usable as dict keys
    date_dict = {date1: "Christmas", date3: "Boxing Day"}
    assert date_dict[date2] == "Christmas"  # date2 same as date1


def test_date_repr():
    """Test Date string representation."""
    date = Date(2023, 12, 25)

    # Should have a useful repr
    repr_str = repr(date)
    assert "Date" in repr_str
    assert "2023" in repr_str
    assert "12" in repr_str
    assert "25" in repr_str

    # Should be eval-able (ideally)
    assert "Date(" in repr_str


def test_date_str():
    """Test Date string conversion."""
    date = Date(2023, 12, 25)

    # Should have a clean string representation
    str_repr = str(date)
    assert "2023-12-25" in str_repr or str_repr == "2023-12-25"


def test_date_strftime():
    """Test Date strftime formatting."""
    date = Date(2023, 12, 25)

    # Basic strftime formats
    assert date.strftime("%Y-%m-%d") == "2023-12-25"
    assert date.strftime("%d/%m/%Y") == "25/12/2023"
    assert date.strftime("%B %d, %Y") == "December 25, 2023"
    assert date.strftime("%b %d, %Y") == "Dec 25, 2023"
    assert date.strftime("%A, %B %d, %Y") == "Monday, December 25, 2023"

    # Year formats
    assert date.strftime("%Y") == "2023"
    assert date.strftime("%y") == "23"

    # Month formats
    assert date.strftime("%m") == "12"
    assert date.strftime("%B") == "December"
    assert date.strftime("%b") == "Dec"

    # Day formats
    assert date.strftime("%d") == "25"
    assert date.strftime("%A") == "Monday"
    assert date.strftime("%a") == "Mon"


def test_date_strftime_edge_cases():
    """Test strftime with edge cases."""
    # Single digit month/day
    date1 = Date(2023, 1, 5)
    assert date1.strftime("%Y-%m-%d") == "2023-01-05"
    assert date1.strftime("%Y-%-m-%-d") == "2023-1-5"  # No leading zeros on Unix

    # Leap year
    date2 = Date(2024, 2, 29)
    assert date2.strftime("%Y-%m-%d") == "2024-02-29"

    # Different weekday
    date3 = Date(2023, 12, 31)  # Sunday
    assert date3.strftime("%A") == "Sunday"


def test_date_carbon_format():
    """Test Carbon-style formatting."""
    date = Date(2023, 12, 25)

    # Basic Carbon formats
    assert date.format("Y-m-d") == "2023-12-25"
    assert date.format("d/m/Y") == "25/12/2023"
    assert date.format("F j, Y") == "December 25, 2023"
    assert date.format("M j, Y") == "Dec 25, 2023"
    assert date.format("l, F j, Y") == "Monday, December 25, 2023"

    # Year formats
    assert date.format("Y") == "2023"
    assert date.format("y") == "23"

    # Month formats
    assert date.format("m") == "12"
    assert date.format("n") == "12"  # Month without leading zero
    assert date.format("F") == "December"  # Full month name
    assert date.format("M") == "Dec"  # Short month name

    # Day formats
    assert date.format("d") == "25"
    assert date.format("j") == "25"  # Day without leading zero
    assert date.format("l") == "Monday"  # Full day name
    assert date.format("D") == "Mon"  # Short day name


def test_date_carbon_format_edge_cases():
    """Test Carbon formatting with edge cases."""
    # Single digit month/day
    date1 = Date(2023, 1, 5)
    assert date1.format("Y-m-d") == "2023-01-05"
    assert date1.format("Y-n-j") == "2023-1-5"  # No leading zeros

    # Test different combinations
    date2 = Date(2023, 6, 15)
    assert date2.format("D, M j, Y") == "Thu, Jun 15, 2023"
    assert date2.format("l the jS of F") == "Thursday the 15th of June"


def test_date_carbon_format_ordinals():
    """Test Carbon formatting with ordinal suffixes."""
    # Test ordinal suffixes (1st, 2nd, 3rd, 4th, etc.)
    date1 = Date(2023, 12, 1)
    assert date1.format("jS") == "1st"

    date2 = Date(2023, 12, 2)
    assert date2.format("jS") == "2nd"

    date3 = Date(2023, 12, 3)
    assert date3.format("jS") == "3rd"

    date4 = Date(2023, 12, 4)
    assert date4.format("jS") == "4th"

    date21 = Date(2023, 12, 21)
    assert date21.format("jS") == "21st"

    date22 = Date(2023, 12, 22)
    assert date22.format("jS") == "22nd"


def test_date_python_format():
    """Test Python's built-in format() method."""
    date = Date(2023, 12, 25)

    # Default format (should be ISO)
    assert f"{date}" == "2023-12-25"

    # Custom format specs
    assert f"{date:%Y-%m-%d}" == "2023-12-25"
    assert f"{date:%d/%m/%Y}" == "25/12/2023"
    assert f"{date:%B %d, %Y}" == "December 25, 2023"

    # Using format() function
    assert format(date) == "2023-12-25"
    assert format(date, "%Y-%m-%d") == "2023-12-25"
    assert format(date, "%A, %B %d, %Y") == "Monday, December 25, 2023"


def test_date_common_formats():
    """Test common date format methods."""
    date = Date(2023, 12, 25)

    assert date.to_iso_string() == "2023-12-25"
    assert date.to_datetime_string() == "2023-12-25 00:00:00"  # With default time


def test_date_start_of_day():
    """Test start_of('day') - should return same date."""
    date = Date(2023, 12, 25)
    result = date.start_of("day")

    assert result == date
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 25


def test_date_start_of_month():
    """Test start_of('month')."""
    # Mid-month date
    date = Date(2023, 12, 25)
    result = date.start_of("month")

    assert result.year == 2023
    assert result.month == 12
    assert result.day == 1

    # Already at start of month
    date_start = Date(2023, 12, 1)
    result_start = date_start.start_of("month")
    assert result_start == date_start


def test_date_start_of_year():
    """Test start_of('year')."""
    # Mid-year date
    date = Date(2023, 12, 25)
    result = date.start_of("year")

    assert result.year == 2023
    assert result.month == 1
    assert result.day == 1

    # Already at start of year
    date_start = Date(2023, 1, 1)
    result_start = date_start.start_of("year")
    assert result_start == date_start


def test_date_start_of_week():
    """Test start_of('week') - Monday=0."""
    # Monday (already start of week)
    monday = Date(2023, 12, 25)  # This is a Monday
    result = monday.start_of("week")
    assert result == monday

    # Wednesday (mid-week)
    wednesday = Date(2023, 12, 27)  # Wednesday
    result = wednesday.start_of("week")

    # Should go back to Monday (2023-12-25)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 25
    assert result.weekday() == 0  # Monday

    # Sunday (end of week)
    sunday = Date(2023, 12, 31)  # Sunday
    result = sunday.start_of("week")

    # Should go back to Monday (2023-12-25)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 25


def test_date_end_of_day():
    """Test end_of('day') - should return same date."""
    date = Date(2023, 12, 25)
    result = date.end_of("day")

    assert result == date
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 25


def test_date_end_of_month():
    """Test end_of('month')."""
    # Mid-month date
    date = Date(2023, 12, 15)
    result = date.end_of("month")

    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31  # December has 31 days

    # February in non-leap year
    date_feb = Date(2023, 2, 15)
    result_feb = date_feb.end_of("month")

    assert result_feb.year == 2023
    assert result_feb.month == 2
    assert result_feb.day == 28  # February 2023 has 28 days

    # February in leap year
    date_leap = Date(2024, 2, 15)
    result_leap = date_leap.end_of("month")

    assert result_leap.year == 2024
    assert result_leap.month == 2
    assert result_leap.day == 29  # February 2024 has 29 days

    # Already at end of month
    date_end = Date(2023, 12, 31)
    result_end = date_end.end_of("month")
    assert result_end == date_end


def test_date_end_of_year():
    """Test end_of('year')."""
    # Mid-year date
    date = Date(2023, 6, 15)
    result = date.end_of("year")

    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31

    # Already at end of year
    date_end = Date(2023, 12, 31)
    result_end = date_end.end_of("year")
    assert result_end == date_end


def test_date_end_of_week():
    """Test end_of('week') - Sunday=6."""
    # Monday (start of week)
    monday = Date(2023, 12, 25)  # This is a Monday
    result = monday.end_of("week")

    # Should go to Sunday (2023-12-31)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31
    assert result.weekday() == 6  # Sunday

    # Wednesday (mid-week)
    wednesday = Date(2023, 12, 27)  # Wednesday
    result = wednesday.end_of("week")

    # Should go to Sunday (2023-12-31)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31

    # Sunday (already end of week)
    sunday = Date(2023, 12, 31)  # Sunday
    result = sunday.end_of("week")
    assert result == sunday


def test_date_start_of_quarter():
    """Test start_of('quarter')."""
    # Q1 (Jan-Mar)
    date_q1 = Date(2023, 2, 15)
    result_q1 = date_q1.start_of("quarter")
    assert result_q1.year == 2023
    assert result_q1.month == 1
    assert result_q1.day == 1

    # Q2 (Apr-Jun)
    date_q2 = Date(2023, 5, 15)
    result_q2 = date_q2.start_of("quarter")
    assert result_q2.year == 2023
    assert result_q2.month == 4
    assert result_q2.day == 1

    # Q3 (Jul-Sep)
    date_q3 = Date(2023, 8, 15)
    result_q3 = date_q3.start_of("quarter")
    assert result_q3.year == 2023
    assert result_q3.month == 7
    assert result_q3.day == 1

    # Q4 (Oct-Dec)
    date_q4 = Date(2023, 11, 15)
    result_q4 = date_q4.start_of("quarter")
    assert result_q4.year == 2023
    assert result_q4.month == 10
    assert result_q4.day == 1


def test_date_end_of_quarter():
    """Test end_of('quarter')."""
    # Q1 (Jan-Mar)
    date_q1 = Date(2023, 2, 15)
    result_q1 = date_q1.end_of("quarter")
    assert result_q1.year == 2023
    assert result_q1.month == 3
    assert result_q1.day == 31

    # Q2 (Apr-Jun)
    date_q2 = Date(2023, 5, 15)
    result_q2 = date_q2.end_of("quarter")
    assert result_q2.year == 2023
    assert result_q2.month == 6
    assert result_q2.day == 30

    # Q3 (Jul-Sep)
    date_q3 = Date(2023, 8, 15)
    result_q3 = date_q3.end_of("quarter")
    assert result_q3.year == 2023
    assert result_q3.month == 9
    assert result_q3.day == 30

    # Q4 (Oct-Dec)
    date_q4 = Date(2023, 11, 15)
    result_q4 = date_q4.end_of("quarter")
    assert result_q4.year == 2023
    assert result_q4.month == 12
    assert result_q4.day == 31


def test_date_anchoring_edge_cases():
    """Test anchoring edge cases."""
    # Week crossing month boundary
    date = Date(2023, 1, 1)  # Sunday, Jan 1st
    start_week = date.start_of("week")

    # Should go back to previous Monday (Dec 26, 2022)
    assert start_week.year == 2022
    assert start_week.month == 12
    assert start_week.day == 26

    end_week = date.end_of("week")
    # Should stay on the same Sunday
    assert end_week == date

    # Week crossing year boundary
    date_nye = Date(2023, 12, 31)  # Sunday, New Year's Eve
    start_week_nye = date_nye.start_of("week")

    # Should go back to Monday (Dec 25, 2023)
    assert start_week_nye.year == 2023
    assert start_week_nye.month == 12
    assert start_week_nye.day == 25

    # Leap year February
    leap_date = Date(2024, 2, 15)
    end_month = leap_date.end_of("month")
    assert end_month.day == 29  # 2024 is a leap year


def test_date_anchoring_invalid_unit():
    """Test anchoring with invalid units raises ValueError."""
    date = Date(2023, 12, 25)

    with pytest.raises(ValueError):
        date.start_of("hour")  # type: ignore

    with pytest.raises(ValueError):
        date.end_of("minute")  # type: ignore


def test_date_to_date():
    """Test converting Date to datetime.date."""
    date = Date(2023, 12, 25)
    dt_date = date.to_date()

    # Should return a datetime.date object
    assert isinstance(dt_date, datetime.date)
    assert dt_date.year == 2023
    assert dt_date.month == 12
    assert dt_date.day == 25

    # Should be the same as the result of to_date()
    assert dt_date == date.to_date()

    # Should work for edge cases
    leap_date = Date(2024, 2, 29)
    leap_dt_date = leap_date.to_date()
    assert leap_dt_date.year == 2024
    assert leap_dt_date.month == 2
    assert leap_dt_date.day == 29


def test_date_to_date_immutability():
    """Test that to_date() returns a copy, not the original."""
    date = Date(2023, 12, 25)
    dt_date1 = date.to_date()
    dt_date2 = date.to_date()

    # Should be equal but not the same object
    assert dt_date1 == dt_date2
    assert dt_date1 is not dt_date2  # Different objects

    # Modifying returned date shouldn't affect original
    # (datetime.date is immutable, but this tests the principle)
    new_date = dt_date1.replace(day=26)
    assert new_date.day == 26
    assert date.day == 25  # Original unchanged


def test_date_to_datetime_default_utc():
    """Test converting Date to datetime.datetime with default UTC."""
    date = Date(2023, 12, 25)
    dt = date.to_datetime()

    # Should return a datetime.datetime object
    assert isinstance(dt, datetime.datetime)
    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 25
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0

    # Default timezone should be UTC
    assert dt.tzinfo == ZoneInfo("UTC")
    assert dt.tzinfo is not None
    assert dt.tzinfo.tzname(dt) == "UTC"


def test_date_to_datetime_explicit_utc():
    """Test converting Date to datetime.datetime with explicit UTC."""
    date = Date(2023, 12, 25)
    dt = date.to_datetime(tz="UTC")

    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 25
    assert dt.tzinfo == ZoneInfo("UTC")


def test_date_to_datetime_custom_timezone():
    """Test converting Date to datetime.datetime with custom timezones."""
    date = Date(2023, 12, 25)

    # Test various timezones
    dt_ny = date.to_datetime(tz="America/New_York")
    assert dt_ny.year == 2023
    assert dt_ny.month == 12
    assert dt_ny.day == 25
    assert dt_ny.tzinfo == ZoneInfo("America/New_York")

    dt_tokyo = date.to_datetime(tz="Asia/Tokyo")
    assert dt_tokyo.year == 2023
    assert dt_tokyo.month == 12
    assert dt_tokyo.day == 25
    assert dt_tokyo.tzinfo == ZoneInfo("Asia/Tokyo")

    dt_london = date.to_datetime(tz="Europe/London")
    assert dt_london.year == 2023
    assert dt_london.month == 12
    assert dt_london.day == 25
    assert dt_london.tzinfo == ZoneInfo("Europe/London")


def test_date_to_datetime_naive():
    """Test converting Date to naive datetime.datetime."""
    date = Date(2023, 12, 25)
    dt = date.to_datetime(tz=None)

    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 25
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0

    # Should be naive (no timezone)
    assert dt.tzinfo is None


def test_date_to_datetime_custom_time():
    """Test converting Date to datetime.datetime with custom time components."""
    date = Date(2023, 12, 25)

    # Test with specific hour/minute/second (if we add this feature)
    dt = date.to_datetime(tz="UTC")

    # For now, should always be midnight
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0


def test_date_to_datetime_invalid_timezone():
    """Test converting Date to datetime.datetime with invalid timezone."""
    date = Date(2023, 12, 25)

    # Invalid timezone should raise an exception
    with pytest.raises(Exception):  # ZoneInfoNotFoundError or similar
        date.to_datetime(tz="Invalid/Timezone")

    # Empty string should also be invalid
    with pytest.raises(Exception):
        date.to_datetime(tz="")


def test_date_interop_edge_cases():
    """Test interop methods with edge cases."""
    # Leap year
    leap_date = Date(2024, 2, 29)
    dt_leap = leap_date.to_datetime()
    assert dt_leap.month == 2
    assert dt_leap.day == 29

    # Year boundaries
    new_year = Date(2023, 1, 1)
    dt_new_year = new_year.to_datetime(tz="America/New_York")
    assert dt_new_year.year == 2023
    assert dt_new_year.month == 1
    assert dt_new_year.day == 1

    nye = Date(2023, 12, 31)
    dt_nye = nye.to_datetime(tz="Asia/Tokyo")
    assert dt_nye.year == 2023
    assert dt_nye.month == 12
    assert dt_nye.day == 31


def test_date_interop_roundtrip():
    """Test roundtrip conversions."""
    original_date = Date(2023, 12, 25)

    # Date -> datetime.date -> Date
    dt_date = original_date.to_date()
    roundtrip_date = Date.from_date(dt_date)
    assert roundtrip_date == original_date

    # Date -> datetime.datetime -> back to date part
    dt_datetime = original_date.to_datetime()
    back_to_date = Date(dt_datetime.year, dt_datetime.month, dt_datetime.day)
    assert back_to_date == original_date


def test_date_interop_timezone_awareness():
    """Test that timezone doesn't affect the date part."""
    date = Date(2023, 12, 25)

    # Same date in different timezones should have same date part
    dt_utc = date.to_datetime(tz="UTC")
    dt_ny = date.to_datetime(tz="America/New_York")
    dt_tokyo = date.to_datetime(tz="Asia/Tokyo")

    # All should have the same date part (at midnight in their respective zones)
    # Note: These are datetime.datetime objects, so we can call .date()
    assert dt_utc.date() == dt_ny.date() == dt_tokyo.date()
    assert dt_utc.date() == date.to_date()


# Duration integration tests
def test_date_diff_basic():
    """Test basic date difference calculation."""

    date1 = Date(2023, 12, 25)
    date2 = Date(2023, 12, 30)

    diff = date2.diff(date1)
    assert isinstance(diff, Duration)
    assert diff.days == 5
    assert diff.storage_seconds == 0
    assert diff.microseconds == 0


def test_date_diff_negative():
    """Test date difference with negative result."""

    date1 = Date(2023, 12, 30)
    date2 = Date(2023, 12, 25)

    diff = date2.diff(date1)
    assert isinstance(diff, Duration)
    assert diff.days == -5


def test_date_diff_absolute():
    """Test date difference with absolute flag."""

    date1 = Date(2023, 12, 30)
    date2 = Date(2023, 12, 25)

    diff = date2.diff(date1, absolute=True)
    assert isinstance(diff, Duration)
    assert diff.days == 5


def test_date_diff_same_date():
    """Test difference between same dates."""

    date = Date(2023, 12, 25)
    diff = date.diff(date)

    assert isinstance(diff, Duration)
    assert diff.days == 0
    assert diff.storage_seconds == 0


def test_date_diff_cross_year():
    """Test date difference crossing year boundary."""

    date1 = Date(2023, 12, 25)
    date2 = Date(2024, 1, 5)

    diff = date2.diff(date1)
    assert isinstance(diff, Duration)
    assert diff.days == 11  # 6 days in Dec + 5 days in Jan


def test_date_add_duration_basic():
    """Test adding Duration to Date."""

    date = Date(2023, 12, 25)
    duration = Duration(days=5)

    result = date + duration
    assert isinstance(result, Date)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 30


def test_date_add_duration_with_time_components():
    """Test that adding Duration with time components only affects days."""

    date = Date(2023, 12, 25)
    # Duration with hours should convert to days (24h = 1 day)
    duration = Duration(days=2, hours=24, minutes=30)

    result = date + duration
    assert isinstance(result, Date)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 28  # 2 days + 1 day from 24 hours = 3 days total


def test_date_add_duration_with_calendar_components():
    """Test adding Duration with calendar components (months/years)."""

    date = Date(2023, 12, 25)
    duration = Duration(years=1, months=2, days=5)

    result = date + duration
    assert isinstance(result, Date)
    assert result.year == 2025  # 2023 + 1 year + 2 months = 2025
    assert result.month == 2
    assert (
        result.day == 28
    )  # 25 + 5 days = 30, but Feb has only 28 days in 2025 (not leap year)


def test_date_subtract_duration():
    """Test subtracting Duration from Date."""

    date = Date(2023, 12, 25)
    duration = Duration(days=5)

    result = date - duration
    assert isinstance(result, Date)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 20


def test_date_subtract_duration_cross_month():
    """Test subtracting Duration that crosses month boundary."""

    date = Date(2024, 1, 5)
    duration = Duration(days=10)

    result = date - duration
    assert isinstance(result, Date)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 26  # Jan 5 - 10 days = Dec 26


def test_date_add_duration_method():
    """Test explicit add_duration method."""

    date = Date(2023, 12, 25)
    duration = Duration(days=3, hours=12)

    result = date.add_duration(duration)
    assert isinstance(result, Date)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 28  # 3 days + 0.5 days from 12 hours


def test_date_subtract_duration_method():
    """Test explicit subtract_duration method."""

    date = Date(2023, 12, 25)
    duration = Duration(days=3)

    result = date.subtract_duration(duration)
    assert isinstance(result, Date)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 22


def test_date_subtract_date():
    """Test Date - Date subtraction using - operator."""

    date1 = Date(2023, 12, 25)
    date2 = Date(2023, 12, 20)

    # date1 - date2 should give positive difference
    diff = date1 - date2
    assert isinstance(diff, Duration)
    assert diff.days == 5
    assert diff.storage_seconds == 0
    assert diff.microseconds == 0

    # date2 - date1 should give negative difference
    diff_reverse = date2 - date1
    assert isinstance(diff_reverse, Duration)
    assert diff_reverse.days == -5
    assert diff_reverse.storage_seconds == 0


def test_date_subtract_date_same():
    """Test subtracting same date should return zero duration."""

    date = Date(2023, 12, 25)
    diff = date - date

    assert isinstance(diff, Duration)
    assert diff.days == 0
    assert diff.storage_seconds == 0
    assert diff.microseconds == 0


def test_date_subtract_date_across_months():
    """Test Date - Date subtraction across months."""

    date1 = Date(2023, 12, 5)
    date2 = Date(2023, 11, 28)

    diff = date1 - date2
    assert isinstance(diff, Duration)
    assert diff.days == 7  # Nov 28 to Dec 5
    assert diff.storage_seconds == 0


def test_date_subtract_date_across_years():
    """Test Date - Date subtraction across years."""

    date1 = Date(2024, 1, 5)
    date2 = Date(2023, 12, 28)

    diff = date1 - date2
    assert isinstance(diff, Duration)
    assert diff.days == 8  # Dec 28 to Jan 5
    assert diff.storage_seconds == 0


def test_date_duration_arithmetic_type_error():
    """Test Duration arithmetic with invalid types."""
    date = Date(2023, 12, 25)

    with pytest.raises(TypeError):
        date + "not a duration"  # type: ignore

    with pytest.raises(TypeError):
        date - 123  # type: ignore


class TestDateBusinessDays:
    def test_is_weekday(self):
        """Test checking if a date is a weekday (Monday-Friday)."""
        # Monday 2023-12-25 (Christmas Day)
        monday = Date(2023, 12, 25)
        assert monday.is_weekday() is True

        # Tuesday
        tuesday = Date(2023, 12, 26)
        assert tuesday.is_weekday() is True

        # Wednesday
        wednesday = Date(2023, 12, 27)
        assert wednesday.is_weekday() is True

        # Thursday
        thursday = Date(2023, 12, 28)
        assert thursday.is_weekday() is True

        # Friday
        friday = Date(2023, 12, 29)
        assert friday.is_weekday() is True

        # Saturday
        saturday = Date(2023, 12, 30)
        assert saturday.is_weekday() is False

        # Sunday
        sunday = Date(2023, 12, 31)
        assert sunday.is_weekday() is False

    def test_is_weekend(self):
        """Test checking if a date is a weekend (Saturday-Sunday)."""
        # Weekdays should not be weekend
        monday = Date(2023, 12, 25)
        assert monday.is_weekend() is False

        friday = Date(2023, 12, 29)
        assert friday.is_weekend() is False

        # Weekend days
        saturday = Date(2023, 12, 30)
        assert saturday.is_weekend() is True

        sunday = Date(2023, 12, 31)
        assert sunday.is_weekend() is True

    def test_add_business_days_basic(self):
        """Test adding business days to dates."""
        # Start on Monday, add 1 business day -> Tuesday
        monday = Date(2023, 12, 25)
        tuesday = monday.add_business_days(1)
        assert tuesday == Date(2023, 12, 26)

        # Add 4 business days from Monday -> Friday
        friday = monday.add_business_days(4)
        assert friday == Date(2023, 12, 29)

        # Add 5 business days from Monday -> skip weekend, land on next Monday
        next_monday = monday.add_business_days(5)
        assert next_monday == Date(2024, 1, 1)  # Skip Sat 30, Sun 31

    def test_add_business_days_from_weekend(self):
        """Test adding business days starting from weekend."""
        # Start on Saturday
        saturday = Date(2023, 12, 30)

        # Add 1 business day from Saturday -> Monday (skip Sunday)
        monday = saturday.add_business_days(1)
        assert monday == Date(2024, 1, 1)

        # Start on Sunday
        sunday = Date(2023, 12, 31)

        # Add 1 business day from Sunday -> Monday
        monday = sunday.add_business_days(1)
        assert monday == Date(2024, 1, 1)

    def test_add_business_days_zero(self):
        """Test adding zero business days."""
        # From weekday - should return same date
        monday = Date(2023, 12, 25)
        same_monday = monday.add_business_days(0)
        assert same_monday == monday

        # From weekend - should return next business day (Monday)
        saturday = Date(2023, 12, 30)
        monday = saturday.add_business_days(0)
        assert monday == Date(2024, 1, 1)

    def test_add_business_days_large_numbers(self):
        """Test adding large numbers of business days."""
        start_date = Date(2023, 12, 25)  # Monday

        # Add 10 business days (2 full weeks)
        result = start_date.add_business_days(10)
        expected = Date(2024, 1, 8)  # Monday 2 weeks + 1 day later
        assert result == expected

        # Add 20 business days (4 full weeks)
        result = start_date.add_business_days(20)
        expected = Date(2024, 1, 22)  # Monday 4 weeks + 1 day later
        assert result == expected

    def test_subtract_business_days_basic(self):
        """Test subtracting business days from dates."""
        # Start on Friday, subtract 1 business day -> Thursday
        friday = Date(2023, 12, 29)
        thursday = friday.subtract_business_days(1)
        assert thursday == Date(2023, 12, 28)

        # Subtract 4 business days from Friday -> Monday
        monday = friday.subtract_business_days(4)
        assert monday == Date(2023, 12, 25)

        # Subtract 5 business days from Friday -> skip weekend, land on previous Friday
        prev_friday = friday.subtract_business_days(5)
        assert prev_friday == Date(2023, 12, 22)

    def test_subtract_business_days_from_weekend(self):
        """Test subtracting business days starting from weekend."""
        # Start on Saturday
        saturday = Date(2023, 12, 30)

        # Subtract 1 business day from Saturday -> Friday (skip going back through weekend)
        friday = saturday.subtract_business_days(1)
        assert friday == Date(2023, 12, 29)

        # Start on Sunday
        sunday = Date(2023, 12, 31)

        # Subtract 1 business day from Sunday -> Friday
        friday = sunday.subtract_business_days(1)
        assert friday == Date(2023, 12, 29)

    def test_subtract_business_days_zero(self):
        """Test subtracting zero business days."""
        # From weekday - should return same date
        friday = Date(2023, 12, 29)
        same_friday = friday.subtract_business_days(0)
        assert same_friday == friday

        # From weekend - should return previous business day (Friday)
        saturday = Date(2023, 12, 30)
        friday = saturday.subtract_business_days(0)
        assert friday == Date(2023, 12, 29)

    def test_business_days_negative_numbers(self):
        """Test business day methods with negative numbers."""
        monday = Date(2023, 12, 25)

        # add_business_days with negative number should be same as subtract_business_days
        result1 = monday.add_business_days(-3)
        result2 = monday.subtract_business_days(3)
        assert result1 == result2

        # subtract_business_days with negative number should be same as add_business_days
        result3 = monday.subtract_business_days(-3)
        result4 = monday.add_business_days(3)
        assert result3 == result4

    def test_business_days_month_boundaries(self):
        """Test business day arithmetic across month boundaries."""
        # End of month
        date = Date(2023, 11, 30)  # Thursday

        # Add 1 business day -> Friday (Dec 1)
        result = date.add_business_days(1)
        assert result == Date(2023, 12, 1)

        # Add 3 business days -> skip weekend, get Tuesday (Dec 5)
        result = date.add_business_days(3)
        assert result == Date(2023, 12, 5)

    def test_business_days_year_boundaries(self):
        """Test business day arithmetic across year boundaries."""
        # End of year
        date = Date(2023, 12, 29)  # Friday

        # Add 1 business day -> Monday (Jan 1, 2024)
        result = date.add_business_days(1)
        assert result == Date(2024, 1, 1)

        # Beginning of year
        date = Date(2024, 1, 1)  # Monday

        # Subtract 1 business day -> Friday (Dec 29, 2023)
        result = date.subtract_business_days(1)
        assert result == Date(2023, 12, 29)

    def test_business_days_with_holidays(self):
        """Test business day arithmetic with holidays."""
        # This tests the holiday parameter when implemented
        christmas = Date(2023, 12, 25)  # Monday, Christmas Day

        # Without holidays - should be normal business day
        result = christmas.add_business_days(1)
        assert result == Date(2023, 12, 26)

        # With holidays - should skip Christmas
        # TODO: Uncomment when holiday support is implemented
        # holidays = [Date(2023, 12, 25)]  # Christmas
        # result = christmas.add_business_days(1, holidays=holidays)
        # assert result == Date(2023, 12, 26)

    def test_business_days_invalid_input(self):
        """Test business day methods with invalid input."""
        date = Date(2023, 12, 25)

        # Test with non-integer input
        with pytest.raises(TypeError):
            date.add_business_days(1.5)  # type: ignore

        with pytest.raises(TypeError):
            date.subtract_business_days("1")  # type: ignore
