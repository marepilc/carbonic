import datetime
from zoneinfo import ZoneInfo

import pytest

from carbonic import Date, DateTime, Duration
from carbonic.core.exceptions import ParseError


def test_datetime_is_native_datetime_subtype():
    value = DateTime(2026, 4, 24, 12, 30, tz="UTC")

    assert isinstance(value, datetime.datetime)
    assert isinstance(value, DateTime)

    native_value: datetime.datetime = value
    assert native_value.year == 2026


def test_datetime_constructor_uses_native_naive_default():
    value = DateTime(2026, 4, 24, 12, 30)

    assert value.tzinfo is None


def test_datetime_now_none_is_local_naive():
    value = DateTime.now()

    assert value.tzinfo is None


def test_datetime_now_accepts_timezone_string():
    value = DateTime.now("Europe/Warsaw")

    assert value.tzinfo == ZoneInfo("Europe/Warsaw")


def test_datetime_parse_iso_only_by_default():
    value = DateTime.parse("2026-04-24T12:30:45")

    assert value == DateTime(2026, 4, 24, 12, 30, 45)

    with pytest.raises(ParseError):
        DateTime.parse("24/04/2026 12:30:45")


def test_datetime_parse_rejects_carbon_style_format_tokens():
    with pytest.raises(ParseError):
        DateTime.parse("24/04/2026 12:30:45", "d/m/Y H:i:s")


def test_datetime_parse_accepts_python_strptime_format():
    value = DateTime.parse("24/04/2026 12:30:45", "%d/%m/%Y %H:%M:%S")

    assert value == DateTime(2026, 4, 24, 12, 30, 45)


def test_datetime_parse_preserves_offset_aware_instant():
    value = DateTime.parse("2025-09-23T14:30:45+02:00")

    assert value.utcoffset() == datetime.timedelta(hours=2)
    assert value.astimezone(datetime.timezone.utc).hour == 12
    assert value.astimezone(datetime.timezone.utc).minute == 30


def test_datetime_parse_converts_aware_input_to_requested_timezone():
    value = DateTime.parse("2025-09-23T14:30:45+02:00", tz="UTC")

    assert value.tzinfo == ZoneInfo("UTC")
    assert value.hour == 12
    assert value.minute == 30


def test_datetime_has_no_carbon_format_alias():
    value = DateTime(2026, 4, 24, 12, 30)

    assert not hasattr(value, "format")
    assert value.strftime("%Y-%m-%d %H:%M") == "2026-04-24 12:30"


def test_datetime_conversions_return_expected_types():
    value = DateTime(2026, 4, 24, 12, 30, tz="Europe/Warsaw")

    assert value.to_date() == Date(2026, 4, 24)

    native = value.to_datetime()
    assert type(native) is datetime.datetime
    assert native.tzinfo == ZoneInfo("Europe/Warsaw")


def test_datetime_duration_arithmetic_still_returns_datetime():
    value = DateTime(2026, 1, 31, 23, 30, tz="UTC")

    assert value.add(months=1, hours=1) == DateTime(2026, 3, 1, 0, 30, tz="UTC")
    assert value.diff(DateTime(2026, 1, 31, 22, 30, tz="UTC")) == Duration(hours=1)
