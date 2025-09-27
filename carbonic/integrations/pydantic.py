"""Pydantic field types and validators for Carbonic datetime classes.

This module provides custom pydantic field types for all core Carbonic classes:
- DateField: Validates and converts to carbonic.Date
- DateTimeField: Validates and converts to carbonic.DateTime with timezone support
- DurationField: Validates and converts to carbonic.Duration
- IntervalField: Validates time ranges
- PeriodField: Validates named periods

Usage:
    from pydantic import BaseModel
    from carbonic.integrations.pydantic import DateField, DateTimeField

    class Event(BaseModel):
        start_date: DateField
        start_time: DateTimeField

    event = Event(
        start_date="2024-01-15",
        start_time="2024-01-15T14:30:00Z"
    )
"""

from __future__ import annotations

from typing import Any, Union

# Check if pydantic is available
try:
    from pydantic import GetCoreSchemaHandler
    from pydantic.annotated_handlers import GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import CoreSchema, core_schema
except ImportError as e:
    raise ImportError(
        "Pydantic is required for carbonic.integrations.pydantic. "
        "Install it with: pip install carbonic[pydantic]"
    ) from e

from carbonic import Date, DateTime, Duration, Interval, Period
from carbonic.core.exceptions import ParseError


def validate_date(value: Any) -> Date:
    """Validate and convert input to Date."""
    if isinstance(value, Date):
        return value
    elif isinstance(value, str):
        try:
            return Date.parse(value)
        except ParseError as e:
            raise ValueError(f"Invalid date string: {value}") from e
    elif isinstance(value, dict):  # type: ignore[arg-type]
        try:
            return Date(**value)  # type: ignore[arg-type]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid date dict: {value}") from e
    else:
        raise ValueError(f"Expected Date, str, or dict, got {type(value)}")


def validate_datetime(value: Any) -> DateTime:
    """Validate and convert input to DateTime."""
    if isinstance(value, DateTime):
        return value
    elif isinstance(value, str):
        try:
            return DateTime.parse(value)
        except ParseError as e:
            raise ValueError(f"Invalid datetime string: {value}") from e
    elif isinstance(value, dict):  # type: ignore[arg-type]
        try:
            return DateTime(**value)  # type: ignore[arg-type]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid datetime dict: {value}") from e
    else:
        raise ValueError(f"Expected DateTime, str, or dict, got {type(value)}")


def validate_duration(value: Any) -> Duration:
    """Validate and convert input to Duration."""
    if isinstance(value, Duration):
        return value
    elif isinstance(value, str):
        try:
            return Duration.parse(value)
        except ParseError as e:
            raise ValueError(f"Invalid duration string: {value}") from e
    elif isinstance(value, (int, float)):
        if isinstance(value, float):
            # Convert float seconds to int seconds + microseconds
            int_seconds = int(value)
            microseconds = int((value - int_seconds) * 1_000_000)
            return Duration(seconds=int_seconds, microseconds=microseconds)
        else:
            return Duration(seconds=value)
    elif isinstance(value, dict):  # type: ignore[arg-type]
        try:
            return Duration(**value)  # type: ignore[arg-type]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid duration dict: {value}") from e
    else:
        raise ValueError(f"Expected Duration, str, number, or dict, got {type(value)}")


def serialize_duration(value: Duration) -> str:
    """Serialize Duration to ISO 8601 format."""
    # Convert Duration back to ISO 8601 format
    parts: list[str] = []

    # Years and months
    if value.years:
        parts.append(f"{value.years}Y")
    if value.months:
        parts.append(f"{value.months}M")

    # Days
    if value.days:
        parts.append(f"{value.days}D")

    # Time part - extract from storage_seconds
    time_parts: list[str] = []
    remaining_seconds = value.storage_seconds

    hours = remaining_seconds // 3600
    remaining_seconds %= 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    # Add microseconds
    fractional_seconds: float = float(seconds)
    if value.microseconds:
        fractional_seconds += value.microseconds / 1_000_000

    if hours:
        time_parts.append(f"{hours}H")
    if minutes:
        time_parts.append(f"{minutes}M")
    if fractional_seconds or (
        not time_parts and not parts
    ):  # Always include seconds if no other parts
        if fractional_seconds == int(fractional_seconds):
            time_parts.append(f"{int(fractional_seconds)}S")
        else:
            time_parts.append(f"{fractional_seconds}S")

    result = "P"
    result += "".join(parts)
    if time_parts:
        result += "T" + "".join(time_parts)

    return result if result != "P" else "PT0S"


def validate_interval(value: Any) -> Interval:
    """Validate and convert input to Interval."""
    if isinstance(value, Interval):
        return value
    elif isinstance(value, dict):  # type: ignore[arg-type]
        if "start" in value and "end" in value:
            try:
                start_value: Any = value["start"]  # type: ignore[assignment]
                end_value: Any = value["end"]  # type: ignore[assignment]

                # Convert string dates/datetimes to proper objects
                if isinstance(start_value, str):
                    start_obj: Union[Date, DateTime] = (
                        DateTime.parse(start_value)
                        if "T" in start_value
                        else Date.parse(start_value)
                    )
                elif isinstance(start_value, (Date, DateTime)):
                    start_obj = start_value
                else:
                    raise TypeError("Invalid start type")

                if isinstance(end_value, str):
                    end_obj: Union[Date, DateTime] = (
                        DateTime.parse(end_value)
                        if "T" in end_value
                        else Date.parse(end_value)
                    )
                elif isinstance(end_value, (Date, DateTime)):
                    end_obj = end_value
                else:
                    raise TypeError("Invalid end type")

                return Interval(start_obj, end_obj)
            except (ParseError, TypeError, ValueError) as e:
                raise ValueError(f"Invalid interval dict: {value}") from e
        else:
            raise ValueError("Interval dict must have 'start' and 'end' keys")
    elif isinstance(value, (list, tuple)) and len(value) == 2:  # type: ignore[arg-type]
        try:
            start_item: Any = value[0]  # type: ignore[assignment]
            end_item: Any = value[1]  # type: ignore[assignment]

            if isinstance(start_item, str):
                start_parsed: Union[Date, DateTime] = (
                    DateTime.parse(start_item)
                    if "T" in start_item
                    else Date.parse(start_item)
                )
            elif isinstance(start_item, (Date, DateTime)):
                start_parsed = start_item
            else:
                raise TypeError("Invalid start type")

            if isinstance(end_item, str):
                end_parsed: Union[Date, DateTime] = (
                    DateTime.parse(end_item)
                    if "T" in end_item
                    else Date.parse(end_item)
                )
            elif isinstance(end_item, (Date, DateTime)):
                end_parsed = end_item
            else:
                raise TypeError("Invalid end type")

            return Interval(start_parsed, end_parsed)
        except (ParseError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid interval tuple/list: {value}") from e
    else:
        raise ValueError("Expected Interval, dict with start/end, or tuple/list")


def validate_period(value: Any) -> Period:
    """Validate and convert input to Period."""
    if isinstance(value, Period):
        return value
    elif isinstance(value, str):
        # Try to get period constant by name
        period_name = value.upper()
        for attr_name in dir(Period):
            attr_value = getattr(Period, attr_name)
            if attr_name == period_name and isinstance(attr_value, Period):
                return attr_value
        raise ValueError(f"Unknown period: {value}")
    else:
        raise ValueError(f"Expected Period or str, got {type(value)}")


def _get_date_core_schema(
    source_type: Any, handler: GetCoreSchemaHandler
) -> CoreSchema:
    """Generate pydantic-core schema for Date field type."""

    def validate_date(value: Any) -> Date:
        if isinstance(value, Date):
            return value
        elif isinstance(value, str):
            try:
                return Date.parse(value)
            except ParseError as e:
                raise ValueError(f"Invalid date string: {value}") from e
        elif isinstance(value, dict):  # type: ignore[arg-type]
            try:
                return Date(**value)  # type: ignore[arg-type]
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid date dict: {value}") from e
        else:
            raise ValueError(f"Expected Date, str, or dict, got {type(value)}")

    return core_schema.no_info_plain_validator_function(
        validate_date, serialization=core_schema.to_string_ser_schema(when_used="json")
    )


def _get_datetime_core_schema(
    source_type: Any, handler: GetCoreSchemaHandler
) -> CoreSchema:
    """Generate pydantic-core schema for DateTime field type."""

    def validate_datetime(value: Any) -> DateTime:
        if isinstance(value, DateTime):
            return value
        elif isinstance(value, str):
            try:
                return DateTime.parse(value)
            except ParseError as e:
                raise ValueError(f"Invalid datetime string: {value}") from e
        elif isinstance(value, dict):  # type: ignore[arg-type]
            try:
                return DateTime(**value)  # type: ignore[arg-type]
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid datetime dict: {value}") from e
        else:
            raise ValueError(f"Expected DateTime, str, or dict, got {type(value)}")

    return core_schema.no_info_plain_validator_function(
        validate_datetime,
        serialization=core_schema.to_string_ser_schema(when_used="json"),
    )


def _get_duration_core_schema(
    source_type: Any, handler: GetCoreSchemaHandler
) -> CoreSchema:
    """Generate pydantic-core schema for Duration field type."""

    def validate_duration(value: Any) -> Duration:
        if isinstance(value, Duration):
            return value
        elif isinstance(value, str):
            try:
                return Duration.parse(value)
            except ParseError as e:
                raise ValueError(f"Invalid duration string: {value}") from e
        elif isinstance(value, (int, float)):
            if isinstance(value, float):
                # Convert float seconds to int seconds + microseconds
                int_seconds = int(value)
                microseconds = int((value - int_seconds) * 1_000_000)
                return Duration(seconds=int_seconds, microseconds=microseconds)
            else:
                return Duration(seconds=value)
        elif isinstance(value, dict):  # type: ignore[arg-type]
            try:
                return Duration(**value)  # type: ignore[arg-type]
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid duration dict: {value}") from e
        else:
            raise ValueError(
                f"Expected Duration, str, number, or dict, got {type(value)}"
            )

    def serialize_duration(value: Duration) -> str:
        """Serialize Duration to ISO 8601 format."""
        # Convert Duration back to ISO 8601 format
        parts: list[str] = []

        # Years and months
        if value.years:
            parts.append(f"{value.years}Y")
        if value.months:
            parts.append(f"{value.months}M")

        # Days
        if value.days:
            parts.append(f"{value.days}D")

        # Time part - extract from storage_seconds
        time_parts: list[str] = []
        remaining_seconds = value.storage_seconds

        hours = remaining_seconds // 3600
        remaining_seconds %= 3600

        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        # Add microseconds
        fractional_seconds: float = float(seconds)
        if value.microseconds:
            fractional_seconds += value.microseconds / 1_000_000

        if hours:
            time_parts.append(f"{hours}H")
        if minutes:
            time_parts.append(f"{minutes}M")
        if fractional_seconds or (
            not time_parts and not parts
        ):  # Always include seconds if no other parts
            if fractional_seconds == int(fractional_seconds):
                time_parts.append(f"{int(fractional_seconds)}S")
            else:
                time_parts.append(f"{fractional_seconds}S")

        result = "P"
        result += "".join(parts)
        if time_parts:
            result += "T" + "".join(time_parts)

        return result if result != "P" else "PT0S"

    return core_schema.no_info_plain_validator_function(
        validate_duration,
        serialization=core_schema.plain_serializer_function_ser_schema(
            serialize_duration, when_used="json"
        ),
    )


def _get_interval_core_schema(
    source_type: Any, handler: GetCoreSchemaHandler
) -> CoreSchema:
    """Generate pydantic-core schema for Interval field type."""

    def validate_interval(value: Any) -> Interval:
        if isinstance(value, Interval):
            return value
        elif isinstance(value, dict):  # type: ignore[arg-type]
            if "start" in value and "end" in value:
                try:
                    start_value: Any = value["start"]  # type: ignore[assignment]
                    end_value: Any = value["end"]  # type: ignore[assignment]

                    # Convert string dates/datetimes to proper objects
                    if isinstance(start_value, str):
                        start_obj: Union[Date, DateTime] = (
                            DateTime.parse(start_value)
                            if "T" in start_value
                            else Date.parse(start_value)
                        )
                    elif isinstance(start_value, (Date, DateTime)):
                        start_obj = start_value
                    else:
                        raise TypeError("Invalid start type")

                    if isinstance(end_value, str):
                        end_obj: Union[Date, DateTime] = (
                            DateTime.parse(end_value)
                            if "T" in end_value
                            else Date.parse(end_value)
                        )
                    elif isinstance(end_value, (Date, DateTime)):
                        end_obj = end_value
                    else:
                        raise TypeError("Invalid end type")

                    return Interval(start_obj, end_obj)
                except (ParseError, TypeError, ValueError) as e:
                    raise ValueError(f"Invalid interval dict: {value}") from e
            else:
                raise ValueError("Interval dict must have 'start' and 'end' keys")
        elif isinstance(value, (list, tuple)) and len(value) == 2:  # type: ignore[arg-type]
            try:
                start_item: Any = value[0]  # type: ignore[assignment]
                end_item: Any = value[1]  # type: ignore[assignment]

                if isinstance(start_item, str):
                    start_parsed: Union[Date, DateTime] = (
                        DateTime.parse(start_item)
                        if "T" in start_item
                        else Date.parse(start_item)
                    )
                elif isinstance(start_item, (Date, DateTime)):
                    start_parsed = start_item
                else:
                    raise TypeError("Invalid start type")

                if isinstance(end_item, str):
                    end_parsed: Union[Date, DateTime] = (
                        DateTime.parse(end_item)
                        if "T" in end_item
                        else Date.parse(end_item)
                    )
                elif isinstance(end_item, (Date, DateTime)):
                    end_parsed = end_item
                else:
                    raise TypeError("Invalid end type")

                return Interval(start_parsed, end_parsed)
            except (ParseError, TypeError, ValueError) as e:
                raise ValueError(f"Invalid interval tuple/list: {value}") from e
        else:
            raise ValueError("Expected Interval, dict with start/end, or tuple/list")

    return core_schema.no_info_plain_validator_function(
        validate_interval,
        serialization=core_schema.to_string_ser_schema(when_used="json"),
    )


def _get_period_core_schema(
    source_type: Any, handler: GetCoreSchemaHandler
) -> CoreSchema:
    """Generate pydantic-core schema for Period field type."""

    def validate_period(value: Any) -> Period:
        if isinstance(value, Period):
            return value
        elif isinstance(value, str):
            # Try to get period constant by name
            period_name = value.upper()
            for attr_name in dir(Period):
                attr_value = getattr(Period, attr_name)
                if attr_name == period_name and isinstance(attr_value, Period):
                    return attr_value
            raise ValueError(f"Unknown period: {value}")
        else:
            raise ValueError(f"Expected Period or str, got {type(value)}")

    return core_schema.no_info_plain_validator_function(
        validate_period,
        serialization=core_schema.to_string_ser_schema(when_used="json"),
    )


class DateField:
    """Pydantic field type for carbonic.Date.

    Accepts:
    - carbonic.Date instances
    - ISO 8601 date strings ("2024-01-15")
    - Dict with year, month, day keys

    Examples:
        >>> from pydantic import BaseModel
        >>> from carbonic.integrations.pydantic import DateField
        >>>
        >>> class Event(BaseModel):
        ...     date: DateField
        >>>
        >>> event = Event(date="2024-01-15")
        >>> event.date
        Date(2024, 1, 15)
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _get_date_core_schema(source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "date",
            "description": "ISO 8601 date string (YYYY-MM-DD)",
            "examples": ["2024-01-15", "2023-12-31"],
        }


class DateTimeField:
    """Pydantic field type for carbonic.DateTime.

    Accepts:
    - carbonic.DateTime instances
    - ISO 8601 datetime strings with timezone
    - Dict with year, month, day, hour, minute, second, tz keys

    Examples:
        >>> from pydantic import BaseModel
        >>> from carbonic.integrations.pydantic import DateTimeField
        >>>
        >>> class Event(BaseModel):
        ...     start_time: DateTimeField
        >>>
        >>> event = Event(start_time="2024-01-15T14:30:00Z")
        >>> event.start_time
        DateTime(2024, 1, 15, 14, 30, 0, tz='UTC')
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _get_datetime_core_schema(source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 datetime string with timezone",
            "examples": ["2024-01-15T14:30:00Z", "2024-01-15T14:30:00+02:00"],
        }


class DurationField:
    """Pydantic field type for carbonic.Duration.

    Accepts:
    - carbonic.Duration instances
    - ISO 8601 duration strings ("P1DT2H30M")
    - Numbers (seconds)
    - Dict with duration components

    Examples:
        >>> from pydantic import BaseModel
        >>> from carbonic.integrations.pydantic import DurationField
        >>>
        >>> class Task(BaseModel):
        ...     duration: DurationField
        >>>
        >>> task = Task(duration="PT2H30M")
        >>> task.duration
        Duration(days=0, storage_seconds=9000, microseconds=0, months=0, years=0)
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _get_duration_core_schema(source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "anyOf": [
                {
                    "type": "string",
                    "description": "ISO 8601 duration string",
                    "examples": ["PT2H30M", "P1DT6H", "PT45S"],
                },
                {
                    "type": "number",
                    "description": "Duration in seconds",
                    "examples": [3600, 86400, 0.5],
                },
            ]
        }


class IntervalField:
    """Pydantic field type for carbonic.Interval.

    Accepts:
    - carbonic.Interval instances
    - Dict with 'start' and 'end' keys
    - Tuple/list with [start, end] elements

    Examples:
        >>> from pydantic import BaseModel
        >>> from carbonic.integrations.pydantic import IntervalField
        >>>
        >>> class Meeting(BaseModel):
        ...     time_slot: IntervalField
        >>>
        >>> meeting = Meeting(time_slot={
        ...     "start": "2024-01-15T14:00:00Z",
        ...     "end": "2024-01-15T15:00:00Z"
        ... })
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _get_interval_core_schema(source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "object",
            "properties": {
                "start": {
                    "anyOf": [
                        {"type": "string", "format": "date"},
                        {"type": "string", "format": "date-time"},
                    ]
                },
                "end": {
                    "anyOf": [
                        {"type": "string", "format": "date"},
                        {"type": "string", "format": "date-time"},
                    ]
                },
            },
            "required": ["start", "end"],
            "description": "Time interval with start and end dates/datetimes",
        }


class PeriodField:
    """Pydantic field type for carbonic.Period.

    Accepts:
    - carbonic.Period instances
    - String period names ("DAY", "WEEK", "MONTH", etc.)

    Examples:
        >>> from pydantic import BaseModel
        >>> from carbonic.integrations.pydantic import PeriodField
        >>>
        >>> class Schedule(BaseModel):
        ...     frequency: PeriodField
        >>>
        >>> schedule = Schedule(frequency="WEEK")
        >>> schedule.frequency
        Period.WEEK
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _get_period_core_schema(source_type, handler)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "enum": ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR"],
            "description": "Named period constant",
        }


# Type aliases for easier imports
CarbonicDate = DateField
CarbonicDateTime = DateTimeField
CarbonicDuration = DurationField
CarbonicInterval = IntervalField
CarbonicPeriod = PeriodField

# Export all field types
__all__ = [
    "DateField",
    "DateTimeField",
    "DurationField",
    "IntervalField",
    "PeriodField",
    "CarbonicDate",
    "CarbonicDateTime",
    "CarbonicDuration",
    "CarbonicInterval",
    "CarbonicPeriod",
]
