import pytest
from zoneinfo import ZoneInfo

from carbonic import Date, DateTime, Duration, Interval


class TestIntervalConstructor:
    def test_datetime_interval_constructor(self):
        """Test creating Interval with DateTime start/end."""
        start = DateTime(2024, 1, 15, 9, 0)
        end = DateTime(2024, 1, 15, 17, 0)

        interval = Interval(start=start, end=end)

        assert interval.start == start
        assert interval.end == end

    def test_date_interval_constructor(self):
        """Test creating Interval with Date start/end."""
        start = Date(2024, 1, 15)
        end = Date(2024, 1, 20)

        interval = Interval(start=start, end=end)

        assert interval.start == start
        assert interval.end == end

    def test_mixed_date_datetime_interval(self):
        """Test creating Interval with mixed Date/DateTime."""
        date_start = Date(2024, 1, 15)
        datetime_end = DateTime(2024, 1, 20, 17, 0)

        interval = Interval(start=date_start, end=datetime_end)

        # Should convert Date to DateTime for consistency
        assert isinstance(interval.start, DateTime)
        assert isinstance(interval.end, DateTime)
        assert interval.start == DateTime(2024, 1, 15, 0, 0, 0)
        assert interval.end == datetime_end

    def test_invalid_interval_end_before_start(self):
        """Test that creating interval with end before start raises error."""
        start = DateTime(2024, 1, 20, 9, 0)
        end = DateTime(2024, 1, 15, 9, 0)  # Before start

        with pytest.raises(ValueError, match="End must be after or equal to start"):
            Interval(start=start, end=end)

    def test_zero_length_interval(self):
        """Test creating zero-length interval (start == end)."""
        dt = DateTime(2024, 1, 15, 9, 0)

        interval = Interval(start=dt, end=dt)

        assert interval.start == dt
        assert interval.end == dt
        assert interval.is_empty()


class TestIntervalProperties:
    def test_duration_property(self):
        """Test getting Duration of an interval."""
        start = DateTime(2024, 1, 15, 9, 0)
        end = DateTime(2024, 1, 15, 17, 0)
        interval = Interval(start=start, end=end)

        duration = interval.duration()

        assert isinstance(duration, Duration)
        assert duration.in_hours() == 8

    def test_duration_with_date_interval(self):
        """Test Duration of Date interval."""
        start = Date(2024, 1, 15)
        end = Date(2024, 1, 20)
        interval = Interval(start=start, end=end)

        duration = interval.duration()

        assert isinstance(duration, Duration)
        assert duration.days == 5

    def test_is_empty_property(self):
        """Test is_empty() method."""
        dt = DateTime(2024, 1, 15, 9, 0)

        # Empty interval
        empty_interval = Interval(start=dt, end=dt)
        assert empty_interval.is_empty()

        # Non-empty interval
        non_empty = Interval(start=dt, end=dt.add(hours=1))
        assert not non_empty.is_empty()


class TestIntervalContains:
    def test_contains_datetime_point(self):
        """Test contains() with DateTime point."""
        start = DateTime(2024, 1, 15, 9, 0)
        end = DateTime(2024, 1, 15, 17, 0)
        interval = Interval(start=start, end=end)

        # Inside interval
        assert interval.contains(DateTime(2024, 1, 15, 12, 30))

        # At start (inclusive)
        assert interval.contains(start)

        # At end (exclusive)
        assert not interval.contains(end)

        # Before start
        assert not interval.contains(DateTime(2024, 1, 15, 8, 0))

        # After end
        assert not interval.contains(DateTime(2024, 1, 15, 18, 0))

    def test_contains_date_point(self):
        """Test contains() with Date point."""
        start = Date(2024, 1, 15)
        end = Date(2024, 1, 20)
        interval = Interval(start=start, end=end)

        # Inside interval
        assert interval.contains(Date(2024, 1, 17))

        # At start (inclusive)
        assert interval.contains(start)

        # At end (exclusive)
        assert not interval.contains(end)

        # Before/after
        assert not interval.contains(Date(2024, 1, 14))
        assert not interval.contains(Date(2024, 1, 21))

    def test_contains_mixed_types(self):
        """Test contains() with mixed Date/DateTime."""
        # DateTime interval containing Date point
        dt_start = DateTime(2024, 1, 15, 9, 0)
        dt_end = DateTime(2024, 1, 20, 17, 0)
        interval = Interval(start=dt_start, end=dt_end)

        assert interval.contains(Date(2024, 1, 17))
        assert not interval.contains(Date(2024, 1, 21))


class TestIntervalOverlaps:
    def test_overlapping_intervals(self):
        """Test overlaps() with overlapping intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 15, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 12, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        assert interval1.overlaps(interval2)
        assert interval2.overlaps(interval1)  # Symmetric

    def test_non_overlapping_intervals(self):
        """Test overlaps() with non-overlapping intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 12, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 15, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        assert not interval1.overlaps(interval2)
        assert not interval2.overlaps(interval1)

    def test_adjacent_intervals(self):
        """Test overlaps() with adjacent intervals (touching at boundary)."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 12, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 12, 0),  # Starts exactly where interval1 ends
            end=DateTime(2024, 1, 15, 15, 0),
        )

        # Adjacent intervals don't overlap (end is exclusive)
        assert not interval1.overlaps(interval2)
        assert not interval2.overlaps(interval1)

    def test_overlaps_with_date_intervals(self):
        """Test overlaps() with Date intervals."""
        interval1 = Interval(start=Date(2024, 1, 15), end=Date(2024, 1, 20))
        interval2 = Interval(start=Date(2024, 1, 18), end=Date(2024, 1, 25))

        assert interval1.overlaps(interval2)
        assert interval2.overlaps(interval1)


class TestIntervalIntersection:
    def test_intersection_overlapping_intervals(self):
        """Test intersection() with overlapping intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 15, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 12, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        intersection = interval1.intersection(interval2)

        assert intersection is not None
        assert intersection.start == DateTime(2024, 1, 15, 12, 0)
        assert intersection.end == DateTime(2024, 1, 15, 15, 0)

    def test_intersection_non_overlapping_intervals(self):
        """Test intersection() with non-overlapping intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 12, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 15, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        intersection = interval1.intersection(interval2)
        assert intersection is None

    def test_intersection_identical_intervals(self):
        """Test intersection() with identical intervals."""
        interval = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 15, 0)
        )

        intersection = interval.intersection(interval)

        assert intersection is not None
        assert intersection.start == interval.start
        assert intersection.end == interval.end


class TestIntervalUnion:
    def test_union_overlapping_intervals(self):
        """Test union() with overlapping intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 15, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 12, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        union = interval1.union(interval2)

        # Should return single merged interval
        assert isinstance(union, Interval)
        assert union.start == DateTime(2024, 1, 15, 9, 0)
        assert union.end == DateTime(2024, 1, 15, 18, 0)

    def test_union_adjacent_intervals(self):
        """Test union() with adjacent intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 12, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 12, 0), end=DateTime(2024, 1, 15, 15, 0)
        )

        union = interval1.union(interval2)

        # Adjacent intervals should merge
        assert isinstance(union, Interval)
        assert union.start == DateTime(2024, 1, 15, 9, 0)
        assert union.end == DateTime(2024, 1, 15, 15, 0)

    def test_union_non_overlapping_intervals(self):
        """Test union() with non-overlapping intervals."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 12, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 15, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        union = interval1.union(interval2)

        # Should return list of intervals
        assert isinstance(union, list)
        assert len(union) == 2
        assert interval1 in union
        assert interval2 in union


class TestIntervalComparison:
    def test_interval_equality(self):
        """Test Interval equality comparison."""
        start = DateTime(2024, 1, 15, 9, 0)
        end = DateTime(2024, 1, 15, 17, 0)

        interval1 = Interval(start=start, end=end)
        interval2 = Interval(start=start, end=end)
        interval3 = Interval(start=start, end=start.add(hours=1))

        assert interval1 == interval2
        assert interval1 != interval3
        assert not (interval1 == "not an interval")

    def test_interval_ordering(self):
        """Test Interval ordering (by start time)."""
        early = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 12, 0)
        )
        late = Interval(
            start=DateTime(2024, 1, 15, 15, 0), end=DateTime(2024, 1, 15, 18, 0)
        )

        assert early < late
        assert late > early
        assert early <= late
        assert late >= early

    def test_interval_hash(self):
        """Test Interval hashing for use in sets."""
        interval1 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 17, 0)
        )
        interval2 = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 17, 0)
        )

        assert hash(interval1) == hash(interval2)

        # Should work in sets
        interval_set = {interval1, interval2}
        assert len(interval_set) == 1


class TestIntervalStringRepresentation:
    def test_interval_str(self):
        """Test Interval string representation."""
        interval = Interval(
            start=DateTime(2024, 1, 15, 9, 0), end=DateTime(2024, 1, 15, 17, 0)
        )

        result = str(interval)

        # Should be human readable
        assert "2024-01-15T09:00:00" in result
        assert "2024-01-15T17:00:00" in result

    def test_interval_repr(self):
        """Test Interval repr."""
        interval = Interval(start=Date(2024, 1, 15), end=Date(2024, 1, 20))

        result = repr(interval)

        assert "Interval" in result
        assert "start=" in result
        assert "end=" in result


class TestIntervalEdgeCases:
    def test_interval_with_timezone_aware_datetime(self):
        """Test Interval with timezone-aware DateTime objects."""
        start = DateTime(2024, 1, 15, 9, 0, tz="UTC")
        end = DateTime(2024, 1, 15, 17, 0, tz="UTC")

        interval = Interval(start=start, end=end)

        # After normalization, both should be DateTime objects
        assert isinstance(interval.start, DateTime)
        assert isinstance(interval.end, DateTime)
        assert interval.start.tzinfo == ZoneInfo("UTC")
        assert interval.end.tzinfo == ZoneInfo("UTC")

    def test_interval_mixed_timezones(self):
        """Test Interval with different timezones (should normalize)."""
        start_utc = DateTime(2024, 1, 15, 9, 0, tz="UTC")
        end_ny = DateTime(2024, 1, 15, 17, 0, tz="America/New_York")

        # Should either normalize to same timezone or raise error
        # Implementation decision needed
        with pytest.raises(ValueError, match="timezones must match"):
            Interval(start=start_utc, end=end_ny)

    def test_very_short_interval(self):
        """Test very short intervals (microseconds)."""
        start = DateTime(2024, 1, 15, 9, 0, 0, 0)
        end = DateTime(2024, 1, 15, 9, 0, 0, 1)  # 1 microsecond later

        interval = Interval(start=start, end=end)

        assert not interval.is_empty()
        duration = interval.duration()
        assert duration.microseconds == 1
