"""Tests for pydantic integration module.

Tests all custom field types and validation scenarios.
Requires pydantic to be installed: pip install carbonic[pydantic]
"""
# mypy: disable-error-code="assignment"
# pylint: disable=invalid-name
# pyright: reportArgumentType=false, reportAttributeAccessIssue=false

from __future__ import annotations

import json

import pytest

from carbonic import Date, DateTime, Duration, Interval, Period

# Check if pydantic is available, skip all tests if not
pytest.importorskip("pydantic")

# Now we can safely import since importorskip would have skipped the module
from pydantic import BaseModel, ValidationError

from carbonic.integrations.pydantic import (
    DateField,
    DateTimeField,
    DurationField,
    IntervalField,
    PeriodField,
)


class TestDateField:
    """Test DateField pydantic integration."""

    def test_date_field_with_date_instance(self) -> None:
        """Test DateField accepts Date instances."""

        class Model(BaseModel):
            date: DateField

        date = Date(2024, 1, 15)
        model = Model(date=date)
        assert model.date == date
        assert isinstance(model.date, Date)

    def test_date_field_with_iso_string(self) -> None:
        """Test DateField accepts ISO date strings."""

        class Model(BaseModel):
            date: DateField

        model = Model(date="2024-01-15")
        assert model.date == Date(2024, 1, 15)

    def test_date_field_with_dict(self) -> None:
        """Test DateField accepts dict with date components."""

        class Model(BaseModel):
            date: DateField

        model = Model(date={"year": 2024, "month": 1, "day": 15})
        assert model.date == Date(2024, 1, 15)

    def test_date_field_invalid_string(self) -> None:
        """Test DateField rejects invalid date strings."""

        class Model(BaseModel):
            date: DateField

        with pytest.raises(ValidationError, match="Invalid date string"):
            Model(date="invalid-date")

    def test_date_field_invalid_type(self) -> None:
        """Test DateField rejects invalid types."""

        class Model(BaseModel):
            date: DateField

        with pytest.raises(ValidationError):
            Model(date=123)

    def test_date_field_json_serialization(self) -> None:
        """Test DateField JSON serialization."""

        class Model(BaseModel):
            date: DateField

        model = Model(date="2024-01-15")
        json_data = model.model_dump_json()
        assert '"date":"2024-01-15"' in json_data

    def test_date_field_json_schema(self) -> None:
        """Test DateField JSON schema generation."""

        class Model(BaseModel):
            date: DateField

        schema = Model.model_json_schema()
        date_schema = schema["properties"]["date"]
        assert date_schema["type"] == "string"
        assert date_schema["format"] == "date"


class TestDateTimeField:
    """Test DateTimeField pydantic integration."""

    def test_datetime_field_with_datetime_instance(self):
        """Test DateTimeField accepts DateTime instances."""

        class Model(BaseModel):
            dt: DateTimeField

        dt = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        model = Model(dt=dt)
        assert model.dt == dt
        assert isinstance(model.dt, DateTime)

    def test_datetime_field_with_iso_string(self):
        """Test DateTimeField accepts ISO datetime strings."""

        class Model(BaseModel):
            dt: DateTimeField

        model = Model(dt="2024-01-15T14:30:00Z")
        expected = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        assert model.dt == expected

    def test_datetime_field_with_timezone(self):
        """Test DateTimeField handles timezone strings."""

        class Model(BaseModel):
            dt: DateTimeField

        model = Model(dt="2024-01-15T14:30:00+02:00")
        assert model.dt.tzinfo is not None  # type: ignore[attr-defined]

    def test_datetime_field_with_dict(self):
        """Test DateTimeField accepts dict with datetime components."""

        class Model(BaseModel):
            dt: DateTimeField

        model = Model(
            dt={
                "year": 2024,
                "month": 1,
                "day": 15,
                "hour": 14,
                "minute": 30,
                "second": 0,
                "tz": "UTC",
            }
        )
        expected = DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")
        assert model.dt == expected

    def test_datetime_field_invalid_string(self):
        """Test DateTimeField rejects invalid datetime strings."""

        class Model(BaseModel):
            dt: DateTimeField

        with pytest.raises(ValidationError, match="Invalid datetime string"):
            Model(dt="invalid-datetime")

    def test_datetime_field_json_serialization(self):
        """Test DateTimeField JSON serialization."""

        class Model(BaseModel):
            dt: DateTimeField

        model = Model(dt="2024-01-15T14:30:00Z")
        json_data = model.model_dump_json()
        assert '"dt":"2024-01-15T14:30:00+00:00"' in json_data

    def test_datetime_field_json_schema(self):
        """Test DateTimeField JSON schema generation."""

        class Model(BaseModel):
            dt: DateTimeField

        schema = Model.model_json_schema()
        dt_schema = schema["properties"]["dt"]
        assert dt_schema["type"] == "string"
        assert dt_schema["format"] == "date-time"


class TestDurationField:
    """Test DurationField pydantic integration."""

    def test_duration_field_with_duration_instance(self):
        """Test DurationField accepts Duration instances."""

        class Model(BaseModel):
            duration: DurationField

        duration = Duration(hours=2, minutes=30)
        model = Model(duration=duration)
        assert model.duration == duration
        assert isinstance(model.duration, Duration)

    def test_duration_field_with_iso_string(self):
        """Test DurationField accepts ISO duration strings."""

        class Model(BaseModel):
            duration: DurationField

        model = Model(duration="PT2H30M")
        expected = Duration(hours=2, minutes=30)
        assert model.duration == expected

    def test_duration_field_with_seconds_number(self):
        """Test DurationField accepts numeric seconds."""

        class Model(BaseModel):
            duration: DurationField

        model = Model(duration=3600)  # 1 hour in seconds
        expected = Duration(seconds=3600)
        assert model.duration == expected

    def test_duration_field_with_float_seconds(self):
        """Test DurationField accepts float seconds."""

        class Model(BaseModel):
            duration: DurationField

        model = Model(duration=1.5)  # 1.5 seconds
        expected = Duration(seconds=1.5)
        assert model.duration == expected

    def test_duration_field_with_dict(self):
        """Test DurationField accepts dict with duration components."""

        class Model(BaseModel):
            duration: DurationField

        model = Model(duration={"hours": 2, "minutes": 30})
        expected = Duration(hours=2, minutes=30)
        assert model.duration == expected

    def test_duration_field_invalid_string(self):
        """Test DurationField rejects invalid duration strings."""

        class Model(BaseModel):
            duration: DurationField

        with pytest.raises(ValidationError, match="Invalid ISO 8601 duration format"):
            Model(duration="invalid-duration")

    def test_duration_field_json_serialization(self):
        """Test DurationField JSON serialization."""

        class Model(BaseModel):
            duration: DurationField

        model = Model(duration="PT2H30M")
        json_data = model.model_dump_json()
        # Should serialize to ISO 8601 duration string
        assert '"duration":"PT2H30M"' in json_data


class TestIntervalField:
    """Test IntervalField pydantic integration."""

    def test_interval_field_with_interval_instance(self):
        """Test IntervalField accepts Interval instances."""

        class Model(BaseModel):
            interval: IntervalField

        start = DateTime(2024, 1, 15, 14, 0, 0, tz="UTC")
        end = DateTime(2024, 1, 15, 15, 0, 0, tz="UTC")
        interval = Interval(start, end)
        model = Model(interval=interval)
        assert model.interval == interval
        assert isinstance(model.interval, Interval)

    def test_interval_field_with_dict(self):
        """Test IntervalField accepts dict with start/end."""

        class Model(BaseModel):
            interval: IntervalField

        model = Model(
            interval={"start": "2024-01-15T14:00:00Z", "end": "2024-01-15T15:00:00Z"}
        )
        assert isinstance(model.interval, Interval)

    def test_interval_field_with_tuple(self):
        """Test IntervalField accepts tuple with start/end."""

        class Model(BaseModel):
            interval: IntervalField

        model = Model(interval=("2024-01-15T14:00:00Z", "2024-01-15T15:00:00Z"))
        assert isinstance(model.interval, Interval)

    def test_interval_field_with_list(self):
        """Test IntervalField accepts list with start/end."""

        class Model(BaseModel):
            interval: IntervalField

        model = Model(interval=["2024-01-15T14:00:00Z", "2024-01-15T15:00:00Z"])
        assert isinstance(model.interval, Interval)

    def test_interval_field_mixed_date_datetime(self):
        """Test IntervalField with mixed Date/DateTime."""

        class Model(BaseModel):
            interval: IntervalField

        model = Model(
            interval={
                "start": "2024-01-15",  # Date
                "end": "2024-01-15T23:59:59Z",  # DateTime
            }
        )
        assert isinstance(model.interval, Interval)

    def test_interval_field_invalid_dict(self):
        """Test IntervalField rejects invalid dict."""

        class Model(BaseModel):
            interval: IntervalField

        with pytest.raises(ValidationError, match="must have 'start' and 'end' keys"):
            Model(interval={"start": "2024-01-15"})  # Missing end

    def test_interval_field_invalid_tuple_length(self):
        """Test IntervalField rejects wrong tuple length."""

        class Model(BaseModel):
            interval: IntervalField

        with pytest.raises(ValidationError):
            Model(interval=("2024-01-15",))  # Only one element

    def test_interval_field_json_schema(self):
        """Test IntervalField JSON schema generation."""

        class Model(BaseModel):
            interval: IntervalField

        schema = Model.model_json_schema()
        interval_schema = schema["properties"]["interval"]
        assert interval_schema["type"] == "object"
        assert "start" in interval_schema["properties"]
        assert "end" in interval_schema["properties"]
        assert interval_schema["required"] == ["start", "end"]


class TestPeriodField:
    """Test PeriodField pydantic integration."""

    def test_period_field_with_period_instance(self):
        """Test PeriodField accepts Period instances."""

        class Model(BaseModel):
            period: PeriodField

        model = Model(period=Period.DAY)
        assert model.period == Period.DAY
        assert isinstance(model.period, Period)

    def test_period_field_with_string(self):
        """Test PeriodField accepts period name strings."""

        class Model(BaseModel):
            period: PeriodField

        model = Model(period="DAY")
        assert model.period == Period.DAY

    def test_period_field_case_insensitive(self):
        """Test PeriodField accepts lowercase strings."""

        class Model(BaseModel):
            period: PeriodField

        model = Model(period="week")
        assert model.period == Period.WEEK

    def test_period_field_invalid_string(self):
        """Test PeriodField rejects invalid period names."""

        class Model(BaseModel):
            period: PeriodField

        with pytest.raises(ValidationError, match="Unknown period"):
            Model(period="INVALID_PERIOD")

    def test_period_field_invalid_type(self):
        """Test PeriodField rejects invalid types."""

        class Model(BaseModel):
            period: PeriodField

        with pytest.raises(ValidationError):
            Model(period=123)

    def test_period_field_json_schema(self):
        """Test PeriodField JSON schema generation."""

        class Model(BaseModel):
            period: PeriodField

        schema = Model.model_json_schema()
        period_schema = schema["properties"]["period"]
        assert period_schema["type"] == "string"
        assert "MINUTE" in period_schema["enum"]
        assert "DAY" in period_schema["enum"]
        assert "YEAR" in period_schema["enum"]


class TestComplexModels:
    """Test complex models using multiple carbonic field types."""

    def test_event_model(self):
        """Test a complex event model with multiple field types."""

        class Event(BaseModel):
            name: str
            date: DateField
            start_time: DateTimeField
            duration: DurationField
            time_slot: IntervalField
            frequency: PeriodField

        event_data = {  # type: ignore[var-annotated]
            "name": "Meeting",
            "date": "2024-01-15",
            "start_time": "2024-01-15T14:00:00Z",
            "duration": "PT2H",
            "time_slot": {
                "start": "2024-01-15T14:00:00Z",
                "end": "2024-01-15T16:00:00Z",
            },
            "frequency": "WEEK",
        }

        event = Event(**event_data)  # type: ignore[arg-type]
        assert isinstance(event.date, Date)
        assert isinstance(event.start_time, DateTime)
        assert isinstance(event.duration, Duration)
        assert isinstance(event.time_slot, Interval)
        assert isinstance(event.frequency, Period)

    def test_event_model_json_roundtrip(self):
        """Test JSON serialization and deserialization of complex model."""

        class Event(BaseModel):
            name: str
            date: DateField
            start_time: DateTimeField
            duration: DurationField

        # Create event
        event = Event(
            name="Meeting",
            date="2024-01-15",
            start_time="2024-01-15T14:00:00Z",
            duration="PT2H",
        )

        # Serialize to JSON
        json_str = event.model_dump_json()

        # Deserialize from JSON
        event_data = json.loads(json_str)
        event2 = Event(**event_data)

        # Should be equivalent
        assert event.name == event2.name
        assert event.date == event2.date
        assert event.start_time == event2.start_time
        assert event.duration == event2.duration

    def test_nested_model_validation(self):
        """Test validation with nested models."""

        class TimeSlot(BaseModel):
            start: DateTimeField
            end: DateTimeField

        class Event(BaseModel):
            name: str
            slot: TimeSlot

        event = Event(
            name="Meeting",
            slot={"start": "2024-01-15T14:00:00Z", "end": "2024-01-15T16:00:00Z"},
        )

        assert isinstance(event.slot.start, DateTime)
        assert isinstance(event.slot.end, DateTime)


class TestValidationErrors:
    """Test detailed validation error scenarios."""

    def test_date_validation_error_details(self):
        """Test that date validation errors include helpful details."""

        class Model(BaseModel):
            date: DateField

        with pytest.raises(ValidationError) as exc_info:
            Model(date="2024-13-01")  # Invalid month

        error = exc_info.value.errors()[0]
        assert "Invalid date string" in error["msg"]

    def test_datetime_validation_error_details(self):
        """Test that datetime validation errors include helpful details."""

        class Model(BaseModel):
            dt: DateTimeField

        with pytest.raises(ValidationError) as exc_info:
            Model(dt="2024-01-15T25:00:00Z")  # Invalid hour

        error = exc_info.value.errors()[0]
        assert "Invalid datetime string" in error["msg"]

    def test_duration_validation_error_details(self):
        """Test that duration validation errors include helpful details."""

        class Model(BaseModel):
            duration: DurationField

        with pytest.raises(ValidationError) as exc_info:
            Model(duration="INVALID")

        error = exc_info.value.errors()[0]
        assert "Invalid ISO 8601 duration format" in error["msg"]


class TestFieldAliases:
    """Test type alias imports."""

    def test_carbonic_aliases_import(self):
        """Test that type aliases can be imported."""
        from carbonic.integrations.pydantic import (
            CarbonicDate,
            CarbonicDateTime,
            CarbonicDuration,
            CarbonicInterval,
            CarbonicPeriod,
        )

        # Aliases should be the same as main classes
        assert CarbonicDate is DateField
        assert CarbonicDateTime is DateTimeField
        assert CarbonicDuration is DurationField
        assert CarbonicInterval is IntervalField
        assert CarbonicPeriod is PeriodField

    def test_carbonic_aliases_usage(self):
        """Test using type aliases in models."""
        from carbonic.integrations.pydantic import CarbonicDate, CarbonicDateTime

        class Event(BaseModel):
            date: CarbonicDate
            start_time: CarbonicDateTime

        event = Event(date="2024-01-15", start_time="2024-01-15T14:00:00Z")

        assert isinstance(event.date, Date)
        assert isinstance(event.start_time, DateTime)
