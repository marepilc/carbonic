from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Duration:
    # Uses months/years only when explicitly constructed that way.
    days: int
    seconds: int
    microseconds: int
    months: int = 0
    years: int = 0  # optional, for calendar durations

    # Constructors
    @classmethod
    def parse(cls, s: str) -> "Duration": ...  # ISO 8601 / token forms
    @classmethod
    def of(
        cls,
        *,
        years=0,
        months=0,
        weeks=0,
        days=0,
        hours=0,
        minutes=0,
        seconds=0,
        microseconds=0,
    ) -> "Duration": ...

    # Ops
    def total_seconds(self) -> float: ...
    def humanize(self, *, max_units=2, locale: str | None = None) -> str: ...
    def __add__(self, other: "Duration") -> "Duration": ...
    def __mul__(self, k: int | float) -> "Duration": ...
