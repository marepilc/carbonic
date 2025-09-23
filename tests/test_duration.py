from carbonic.core.duration import Duration


class TestDurationConstructor:
    def test_basic_components(self):
        """Test Duration constructor with basic time components."""
        duration = Duration(days=5, hours=2, minutes=30, seconds=45)

        assert duration.days == 5
        assert duration.seconds == 2 * 3600 + 30 * 60 + 45  # 9045 seconds
        assert duration.microseconds == 0
        assert duration.months == 0
        assert duration.years == 0

    def test_weeks_conversion(self):
        """Test Duration constructor converts weeks to days."""
        duration = Duration(weeks=2, days=3)

        assert duration.days == 17  # 2*7 + 3
        assert duration.seconds == 0
        assert duration.months == 0
        assert duration.years == 0

    def test_microseconds(self):
        """Test Duration constructor with microseconds."""
        duration = Duration(seconds=1, microseconds=500000)

        assert duration.days == 0
        assert duration.seconds == 1
        assert duration.microseconds == 500000

    def test_calendar_components(self):
        """Test Duration constructor with calendar components."""
        duration = Duration(years=2, months=6, days=15)

        assert duration.years == 2
        assert duration.months == 6
        assert duration.days == 15
        assert duration.seconds == 0
        assert duration.microseconds == 0

    def test_all_components(self):
        """Test Duration constructor with all possible components."""
        duration = Duration(
            years=1,
            months=2,
            weeks=3,
            days=4,
            hours=5,
            minutes=6,
            seconds=7,
            microseconds=123456,
        )

        assert duration.years == 1
        assert duration.months == 2
        assert duration.days == 25  # 3*7 + 4
        assert duration.seconds == 5 * 3600 + 6 * 60 + 7  # 18367
        assert duration.microseconds == 123456


class TestDurationProperties:
    def test_total_seconds_basic(self):
        """Test total_seconds() for basic durations."""
        duration = Duration(days=1, hours=2, minutes=30, seconds=45)

        expected = 1 * 86400 + 2 * 3600 + 30 * 60 + 45  # 93645
        assert duration.total_seconds() == expected

    def test_total_seconds_with_microseconds(self):
        """Test total_seconds() includes microseconds as fractional seconds."""
        duration = Duration(seconds=1, microseconds=500000)

        assert duration.total_seconds() == 1.5

    def test_total_seconds_calendar_components_excluded(self):
        """Test total_seconds() excludes calendar components (months/years)."""
        duration = Duration(years=1, months=6, days=2, hours=3)

        # Should only count days and hours, not years/months
        expected = 2 * 86400 + 3 * 3600  # 183600
        assert duration.total_seconds() == expected


class TestDurationStringRepresentation:
    def test_repr(self):
        """Test Duration repr."""
        duration = Duration(days=5, hours=2, minutes=30)
        result = repr(duration)

        assert "Duration" in result
        assert "days=5" in result

    def test_str_basic(self):
        """Test Duration string representation."""
        duration = Duration(days=5, hours=2, minutes=30)
        result = str(duration)

        # Should be human-readable
        assert "5 days" in result or "5d" in result


class TestDurationComparison:
    def test_equality(self):
        """Test Duration equality comparison."""
        d1 = Duration(days=5, hours=2, minutes=30)
        d2 = Duration(days=5, hours=2, minutes=30)
        d3 = Duration(days=5, hours=2, minutes=31)

        assert d1 == d2
        assert d1 != d3
        assert not (d1 == "not a duration")

    def test_equality_equivalent_durations(self):
        """Test equality for equivalent durations (same total time)."""
        d1 = Duration(hours=24)
        d2 = Duration(days=1)

        assert d1 == d2  # 24 hours = 1 day

    def test_ordering(self):
        """Test Duration ordering comparisons."""
        d1 = Duration(hours=1)
        d2 = Duration(hours=2)
        d3 = Duration(minutes=30)

        assert d3 < d1 < d2
        assert d3 <= d1 <= d2
        assert d2 > d1 > d3
        assert d2 >= d1 >= d3

    def test_hash(self):
        """Test Duration hashing for use in sets and dicts."""
        d1 = Duration(days=5, hours=2)
        d2 = Duration(days=5, hours=2)
        d3 = Duration(days=5, hours=3)

        assert hash(d1) == hash(d2)
        assert hash(d1) != hash(d3)

        # Should work in sets
        duration_set = {d1, d2, d3}
        assert len(duration_set) == 2  # d1 and d2 should be the same

    def test_calendar_component_comparison(self):
        """Test comparison with calendar components (months/years)."""
        # Calendar components should compare separately from time components
        d1 = Duration(months=12)
        d2 = Duration(years=1)
        d3 = Duration(months=6)

        assert d1 == d2  # 12 months = 1 year
        assert d1 > d3
        assert d3 < d1


class TestDurationArithmetic:
    def test_addition_basic(self):
        """Test basic Duration addition."""
        d1 = Duration(days=5, hours=2)
        d2 = Duration(days=3, hours=4)

        result = d1 + d2

        assert result.days == 8
        assert result.seconds == 6 * 3600  # 2 + 4 hours

    def test_addition_overflow(self):
        """Test Duration addition with time overflow."""
        d1 = Duration(hours=20)
        d2 = Duration(hours=10)

        result = d1 + d2

        # Should normalize: 30 hours = 1 day + 6 hours
        assert result.days == 1
        assert result.seconds == 6 * 3600

    def test_addition_calendar_components(self):
        """Test Duration addition with calendar components."""
        d1 = Duration(years=2, months=6, days=15)
        d2 = Duration(years=1, months=8, days=20)

        result = d1 + d2

        # Should handle month overflow: 6 + 8 = 14 months = 1 year + 2 months
        assert result.years == 4  # 2 + 1 + 1
        assert result.months == 2  # 14 - 12
        assert result.days == 35

    def test_multiplication_basic(self):
        """Test Duration multiplication by integer."""
        duration = Duration(days=2, hours=3, minutes=30)

        result = duration * 3

        assert result.days == 6
        assert result.seconds == 9 * 3600 + 90 * 60  # 3 * (3 hours + 30 minutes)

    def test_multiplication_float(self):
        """Test Duration multiplication by float."""
        duration = Duration(hours=2)

        result = duration * 1.5

        assert result.seconds == 3 * 3600  # 2 * 1.5 = 3 hours

    def test_multiplication_calendar_components(self):
        """Test Duration multiplication with calendar components."""
        duration = Duration(years=1, months=6, days=10)

        result = duration * 2

        assert result.years == 2
        assert result.months == 12
        assert result.days == 20

    def test_negation(self):
        """Test Duration negation."""
        duration = Duration(days=5, hours=2, minutes=30)

        result = -duration

        assert result.days == -5
        assert result.seconds == -(2 * 3600 + 30 * 60)

    def test_subtraction(self):
        """Test Duration subtraction."""
        d1 = Duration(days=10, hours=5)
        d2 = Duration(days=3, hours=2)

        result = d1 - d2

        assert result.days == 7
        assert result.seconds == 3 * 3600  # 5 - 2 hours

    def test_absolute_value(self):
        """Test Duration absolute value."""
        duration = Duration(days=-5, hours=-2)

        result = abs(duration)

        assert result.days == 5
        assert result.seconds == 2 * 3600
