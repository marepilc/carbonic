import datetime
from dataclasses import dataclass
from typing import Literal

from carbonic.core.datetime import DateTime
from carbonic.core.duration import Duration


@dataclass(frozen=True, slots=True)
class Date:
    _date: datetime.date

    # Constructors
    @classmethod
    def today(cls, tz: str | None = None) -> "Date": ...
    @classmethod
    def create(cls, year: int, month: int, day: int) -> "Date": ...
    @classmethod
    def parse(cls, s: str, fmt: str | None = None) -> "Date": ...
    @classmethod
    def from_date(cls, d: datetime.date) -> "Date": ...

    # Properties
    year: int
    month: int
    day: int
    weekday: int  # Mon=0..Sun=6
    iso_week: tuple[int, int]  # (year, week)

    # Operations
    def add(self, *, years=0, months=0, days=0) -> "Date": ...
    def subtract(self, *, years=0, months=0, days=0) -> "Date": ...
    def diff(self, other: "Date", *, absolute=False) -> "Duration": ...

    # Anchors
    def start_of(self, unit: Literal["month", "year", "quarter", "week"]) -> "Date": ...
    def end_of(self, unit: Literal["month", "year", "quarter", "week"]) -> "Date": ...

    # Interop
    def to_datetime(self, tz: str | None = None) -> "DateTime": ...
    def to_date(self) -> datetime.date: ...
