"""Interval implementation for Carbonic.

This module provides the Interval class for representing time intervals
with start and end points, supporting both Date and DateTime intervals
with comprehensive operations like intersection, union, and overlap detection.
"""

from __future__ import annotations

from dataclasses import dataclass

from carbonic.core.date import Date
from carbonic.core.datetime import DateTime
from carbonic.core.duration import Duration


@dataclass(frozen=True, slots=True)
class Interval:
    """Represents a time interval with start and end points.

    Intervals are half-open: [start, end) - inclusive start, exclusive end.
    Supports both Date and DateTime intervals with comprehensive operations.

    Examples:
        # Create intervals
        meeting = Interval(start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 10, 30))
        vacation = Interval(start=Date(2024, 7, 1), end=Date(2024, 7, 15))

        # Operations
        meeting.contains(DateTime(2024, 1, 15, 9, 30))  # True
        meeting.overlaps(lunch_interval)                # True/False
        meeting.intersection(lunch_interval)            # Overlapping part
        meeting.union(lunch_interval)                   # Combined intervals
        meeting.duration()                              # Duration object
    """

    start: Date | DateTime
    end: Date | DateTime

    def __post_init__(self):
        """Validate and normalize the interval after construction."""
        # Normalize mixed Date/DateTime to DateTime first for comparison
        if type(self.start) is not type(self.end):
            # Convert both to DateTime for consistency
            new_start = self.start
            new_end = self.end

            if isinstance(self.start, Date) and isinstance(self.end, DateTime):
                # Convert Date start to DateTime (start of day)
                # Use same timezone as the DateTime end
                tz_str = None
                if self.end.tzinfo is not None:
                    # Extract timezone string from tzinfo
                    tz_str = str(self.end.tzinfo)
                    if tz_str == "UTC":
                        tz_str = "UTC"
                    else:
                        tz_str = "UTC"  # Default fallback
                new_start = DateTime(
                    self.start.year,
                    self.start.month,
                    self.start.day,
                    0,
                    0,
                    0,
                    0,
                    tz_str,
                )
            elif isinstance(self.start, DateTime) and isinstance(self.end, Date):
                # Convert Date end to DateTime (start of day)
                tz_str = None
                if self.start.tzinfo is not None:
                    tz_str = str(self.start.tzinfo)
                    if tz_str == "UTC":
                        tz_str = "UTC"
                    else:
                        tz_str = "UTC"  # Default fallback
                new_end = DateTime(
                    self.end.year, self.end.month, self.end.day, 0, 0, 0, 0, tz_str
                )

            # Use object.__setattr__ since the dataclass is frozen
            object.__setattr__(self, "start", new_start)
            object.__setattr__(self, "end", new_end)

        # Now validate that end >= start
        # After normalization, both should be the same type
        if type(self.start) is type(self.end):
            if self.end < self.start:  # type: ignore
                raise ValueError("End must be after or equal to start")
        else:
            raise RuntimeError(
                "Normalization failed - start and end are different types"
            )

        # Validate timezone consistency for DateTime objects only
        if isinstance(self.start, DateTime) and isinstance(self.end, DateTime):
            if self.start.tzinfo != self.end.tzinfo:
                raise ValueError("Start and end timezones must match")

    def _safe_compare(self, a: Date | DateTime, op: str, b: Date | DateTime) -> bool:
        """Safely compare Date/DateTime objects after normalization.

        After __post_init__, both endpoints are guaranteed to be the same type.
        """
        # After __post_init__, both a and b should be the same type
        if type(a) is type(b):
            if op == "<":
                return a < b  # type: ignore
            elif op == "<=":
                return a <= b  # type: ignore
            elif op == ">":
                return a > b  # type: ignore
            elif op == ">=":
                return a >= b  # type: ignore
            else:
                raise ValueError(f"Unsupported operator: {op}")
        else:
            # This should not happen after __post_init__ normalization
            raise TypeError(
                f"Cannot compare {type(a)} with {type(b)} after normalization"
            )

    def duration(self) -> Duration:
        """Get the Duration of this interval.

        Returns:
            Duration object representing the time span
        """
        # After __post_init__, both are same type, so subtraction is safe
        return self.end - self.start  # type: ignore

    def is_empty(self) -> bool:
        """Check if this interval is empty (zero duration).

        Returns:
            True if start == end, False otherwise
        """
        # After __post_init__, both are same type, so direct comparison is safe
        return self.start == self.end  # type: ignore

    def contains(self, point: Date | DateTime) -> bool:
        """Check if this interval contains a time point.

        Uses half-open interval logic: [start, end)
        - start is inclusive
        - end is exclusive

        Args:
            point: Date or DateTime to check

        Returns:
            True if point is within the interval
        """
        # Handle mixed types by converting to common type
        if type(point) is not type(self.start):
            # Convert Date to DateTime for comparison
            if hasattr(self.start, "hour"):  # DateTime interval
                if not hasattr(point, "hour"):  # Date point
                    # Convert Date point to DateTime (start of day) with same timezone
                    from zoneinfo import ZoneInfo

                    tz_str = None
                    if hasattr(self.start, "tzinfo") and self.start.tzinfo is not None:  # type: ignore
                        if isinstance(self.start.tzinfo, ZoneInfo):  # type: ignore
                            tz_str = self.start.tzinfo.key  # type: ignore
                        else:
                            tz_str = "UTC"  # fallback
                    point = DateTime(
                        point.year, point.month, point.day, 0, 0, 0, 0, tz_str
                    )

        return self._safe_compare(self.start, "<=", point) and self._safe_compare(
            point, "<", self.end
        )

    def overlaps(self, other: Interval) -> bool:
        """Check if this interval overlaps with another interval.

        Args:
            other: Another Interval to check

        Returns:
            True if intervals overlap, False otherwise
        """

        # Two intervals overlap if:
        # self.start < other.end AND other.start < self.end
        return self._safe_compare(self.start, "<", other.end) and self._safe_compare(
            other.start, "<", self.end
        )

    def intersection(self, other: Interval) -> Interval | None:
        """Get the intersection (overlapping part) of two intervals.

        Args:
            other: Another Interval to intersect with

        Returns:
            Interval representing the overlap, or None if no overlap
        """

        if not self.overlaps(other):
            return None

        # Intersection start = max(self.start, other.start)
        # Intersection end = min(self.end, other.end)
        # Use safe comparison to determine max/min
        intersection_start = (
            self.start
            if self._safe_compare(self.start, ">=", other.start)
            else other.start
        )
        intersection_end = (
            self.end if self._safe_compare(self.end, "<=", other.end) else other.end
        )

        return Interval(start=intersection_start, end=intersection_end)

    def union(self, other: Interval) -> Interval | list[Interval]:
        """Get the union of two intervals.

        Args:
            other: Another Interval to union with

        Returns:
            Single Interval if they overlap or are adjacent,
            List of Intervals if they are separate
        """

        # Check if intervals overlap or are adjacent
        if self.overlaps(other) or self._is_adjacent_to(other):
            # Return merged interval
            union_start = (
                self.start
                if self._safe_compare(self.start, "<=", other.start)
                else other.start
            )
            union_end = (
                self.end if self._safe_compare(self.end, ">=", other.end) else other.end
            )
            return Interval(start=union_start, end=union_end)
        else:
            # Return both intervals as separate list
            return [self, other]

    def _is_adjacent_to(self, other: Interval) -> bool:
        """Check if this interval is adjacent to another (touching at boundary)."""
        # After __post_init__, both intervals have same-type endpoints
        return self.end == other.start or other.end == self.start  # type: ignore

    def __eq__(self, other: object) -> bool:
        """Check equality with another Interval."""
        if not isinstance(other, Interval):
            return False
        # After __post_init__, both intervals have same-type endpoints
        return self.start == other.start and self.end == other.end  # type: ignore

    def __lt__(self, other: object) -> bool:
        """Compare intervals by start time."""
        if not isinstance(other, Interval):
            return NotImplemented
        return self._safe_compare(self.start, "<", other.start)

    def __le__(self, other: object) -> bool:
        """Compare intervals by start time."""
        if not isinstance(other, Interval):
            return NotImplemented
        return self._safe_compare(self.start, "<=", other.start)

    def __gt__(self, other: object) -> bool:
        """Compare intervals by start time."""
        if not isinstance(other, Interval):
            return NotImplemented
        return self._safe_compare(self.start, ">", other.start)

    def __ge__(self, other: object) -> bool:
        """Compare intervals by start time."""
        if not isinstance(other, Interval):
            return NotImplemented
        return self._safe_compare(self.start, ">=", other.start)

    def __hash__(self) -> int:
        """Return hash for use in sets and dicts."""
        return hash((self.start, self.end))

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return f"[{self.start}, {self.end})"

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"Interval(start={self.start!r}, end={self.end!r})"
