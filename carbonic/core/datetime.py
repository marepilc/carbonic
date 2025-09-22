import datetime
from dataclasses import dataclass
from typing import Literal

from carbonic.core.date import Date
from carbonic.core.duration import Duration


@dataclass(frozen=True, slots=True)
class DateTime:
    _dt: datetime.datetime

    # Constructors
    @classmethod
    def now(cls, tz: str | None = "UTC") -> "DateTime": ...
    @classmethod
    def create(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tz: str | None = "UTC",
    ) -> "DateTime": ...
    @classmethod
    def parse(
        cls, s: str, fmt: str | None = None, tz: str | None = None
    ) -> "DateTime": ...
    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> "DateTime": ...

    # Properties
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    tzinfo: datetime.tzinfo

    # Ops
    def add(
        self, *, days=0, hours=0, minutes=0, seconds=0, months=0, years=0
    ) -> "DateTime": ...
    def subtract(self, **kwargs) -> "DateTime": ...
    def diff(self, other: "DateTime", *, absolute=False) -> "Duration": ...

    # Anchors
    def start_of(
        self, unit: Literal["minute", "hour", "day", "month", "year", "week"]
    ) -> "DateTime": ...
    def end_of(
        self, unit: Literal["minute", "hour", "day", "month", "year", "week"]
    ) -> "DateTime": ...

    # Conversions
    def to_date(self) -> Date: ...
    def to_datetime(self) -> datetime.datetime: ...
