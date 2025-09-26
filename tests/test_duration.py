from carbonic import Duration


class TestDurationConstructor:
    def test_basic_components(self):
        """Test Duration constructor with basic time components."""
        duration = Duration(days=5, hours=2, minutes=30, seconds=45)

        assert duration.days == 5
        assert duration.storage_seconds == 2 * 3600 + 30 * 60 + 45  # 9045 seconds
        assert duration.microseconds == 0
        assert duration.months == 0
        assert duration.years == 0

    def test_weeks_conversion(self):
        """Test Duration constructor converts weeks to days."""
        duration = Duration(weeks=2, days=3)

        assert duration.days == 17  # 2*7 + 3
        assert duration.storage_seconds == 0
        assert duration.months == 0
        assert duration.years == 0

    def test_microseconds(self):
        """Test Duration constructor with microseconds."""
        duration = Duration(seconds=1, microseconds=500000)

        assert duration.days == 0
        assert duration.storage_seconds == 1
        assert duration.microseconds == 500000

    def test_calendar_components(self):
        """Test Duration constructor with calendar components."""
        duration = Duration(years=2, months=6, days=15)

        assert duration.years == 2
        assert duration.months == 6
        assert duration.days == 15
        assert duration.storage_seconds == 0
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
        assert duration.storage_seconds == 5 * 3600 + 6 * 60 + 7  # 18367
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


class TestDurationConversionProperties:
    def test_in_seconds(self):
        """Test in_seconds property (alias for total_seconds)."""
        duration = Duration(hours=1, minutes=30, seconds=45)

        expected = 1 * 3600 + 30 * 60 + 45  # 5445
        assert duration.in_seconds() == expected
        assert duration.in_seconds() == duration.total_seconds()

    def test_in_minutes(self):
        """Test in_minutes method."""
        duration = Duration(hours=2, minutes=30)

        expected = (2 * 60) + 30  # 150 minutes
        assert duration.in_minutes() == expected

    def test_in_hours(self):
        """Test in_hours method."""
        duration = Duration(days=1, hours=6, minutes=30)

        expected = 24 + 6 + 0.5  # 30.5 hours
        assert duration.in_hours() == expected

    def test_in_days(self):
        """Test in_days method."""
        duration = Duration(days=2, hours=12)

        expected = 2 + 0.5  # 2.5 days
        assert duration.in_days() == expected

    def test_in_weeks(self):
        """Test in_weeks method."""
        duration = Duration(weeks=1, days=3, hours=12)

        # 1 week + 3.5 days = 10.5 days = 1.5 weeks
        expected = 10.5 / 7
        assert duration.in_weeks() == expected

    def test_in_milliseconds(self):
        """Test in_milliseconds method."""
        duration = Duration(seconds=2, microseconds=500000)

        expected = 2.5 * 1000  # 2500 milliseconds
        assert duration.in_milliseconds() == expected

    def test_in_microseconds(self):
        """Test in_microseconds method."""
        duration = Duration(seconds=1, microseconds=500000)

        expected = 1.5 * 1_000_000  # 1,500,000 microseconds
        assert duration.in_microseconds() == expected

    def test_fractional_conversions(self):
        """Test conversion properties with fractional results."""
        duration = Duration(seconds=90)  # 1.5 minutes

        assert duration.in_seconds() == 90
        assert duration.in_minutes() == 1.5
        assert duration.in_hours() == 0.025  # 90/3600
        assert duration.in_days() == 90 / 86400
        assert duration.in_weeks() == (90 / 86400) / 7

    def test_zero_duration_conversions(self):
        """Test conversion properties for zero duration."""
        duration = Duration()

        assert duration.in_seconds() == 0
        assert duration.in_minutes() == 0
        assert duration.in_hours() == 0
        assert duration.in_days() == 0
        assert duration.in_weeks() == 0
        assert duration.in_milliseconds() == 0
        assert duration.in_microseconds() == 0

    def test_negative_duration_conversions(self):
        """Test conversion properties for negative durations."""
        duration = Duration(hours=-2, minutes=-30)

        expected_seconds = -(2 * 3600 + 30 * 60)  # -9000
        assert duration.in_seconds() == expected_seconds
        assert duration.in_minutes() == expected_seconds / 60
        assert duration.in_hours() == expected_seconds / 3600
        assert duration.in_days() == expected_seconds / 86400

    def test_calendar_components_excluded_from_conversions(self):
        """Test that calendar components (months/years) don't affect time conversions."""
        duration = Duration(years=1, months=6, hours=24)

        # Should only count the 24 hours, not the years/months
        expected_seconds = 24 * 3600  # 86400
        assert duration.in_seconds() == expected_seconds
        assert duration.in_hours() == 24
        assert duration.in_days() == 1

    def test_large_duration_conversions(self):
        """Test conversion properties with large durations."""
        duration = Duration(days=365, hours=12)  # 1 year + 12 hours

        total_hours = 365 * 24 + 12  # 8772 hours
        assert duration.in_hours() == total_hours
        assert duration.in_days() == 365.5
        assert duration.in_weeks() == 365.5 / 7

    def test_whole_parameter_behavior(self):
        """Test the whole parameter for in_* methods."""
        duration = Duration(hours=2, minutes=30, seconds=45, microseconds=500000)

        # Test in_seconds with whole=False (default) and whole=True
        assert duration.in_seconds() == 9045.5  # 2.5 hours + 30 minutes + 45.5 seconds
        assert duration.in_seconds(whole=True) == 9045

        # Test in_minutes with whole parameter
        expected_minutes = (
            150.75833333333333  # Approximately 150 minutes and 45.5 seconds
        )
        assert abs(duration.in_minutes() - expected_minutes) < 0.001
        assert duration.in_minutes(whole=True) == 150

        # Test in_hours with whole parameter
        expected_hours = 2.5125  # 2 hours, 30 minutes, 45.5 seconds
        assert abs(duration.in_hours() - expected_hours) < 0.001
        assert duration.in_hours(whole=True) == 2

        # Test with fractional days
        long_duration = Duration(days=5, hours=18, minutes=30)
        assert long_duration.in_days() == 5.770833333333333
        assert long_duration.in_days(whole=True) == 5

    def test_whole_parameter_with_negative_duration(self):
        """Test whole parameter with negative durations."""
        duration = Duration(hours=-2, minutes=-30, seconds=-15)

        expected_seconds = -(2 * 3600 + 30 * 60 + 15)  # -9015
        assert duration.in_seconds() == expected_seconds
        assert duration.in_seconds(whole=True) == -9015

        expected_minutes = expected_seconds / 60  # -150.25
        assert duration.in_minutes() == expected_minutes
        assert duration.in_minutes(whole=True) == -150


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
        assert result.storage_seconds == 6 * 3600  # 2 + 4 hours

    def test_addition_overflow(self):
        """Test Duration addition with time overflow."""
        d1 = Duration(hours=20)
        d2 = Duration(hours=10)

        result = d1 + d2

        # Should normalize: 30 hours = 1 day + 6 hours
        assert result.days == 1
        assert result.storage_seconds == 6 * 3600

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
        assert (
            result.storage_seconds == 9 * 3600 + 90 * 60
        )  # 3 * (3 hours + 30 minutes)

    def test_multiplication_float(self):
        """Test Duration multiplication by float."""
        duration = Duration(hours=2)

        result = duration * 1.5

        assert result.storage_seconds == 3 * 3600  # 2 * 1.5 = 3 hours

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
        assert result.storage_seconds == -(2 * 3600 + 30 * 60)

    def test_subtraction(self):
        """Test Duration subtraction."""
        d1 = Duration(days=10, hours=5)
        d2 = Duration(days=3, hours=2)

        result = d1 - d2

        assert result.days == 7
        assert result.storage_seconds == 3 * 3600  # 5 - 2 hours

    def test_absolute_value(self):
        """Test Duration absolute value."""
        duration = Duration(days=-5, hours=-2)

        result = abs(duration)

        assert result.days == 5
        assert result.storage_seconds == 2 * 3600


class TestDurationParsing:
    def test_parse_basic_iso8601_date_only(self):
        """Test parsing ISO 8601 date-only duration strings."""
        # P1Y2M3D - 1 year, 2 months, 3 days
        duration = Duration.parse("P1Y2M3D")
        assert duration.years == 1
        assert duration.months == 2
        assert duration.days == 3
        assert duration.storage_seconds == 0

    def test_parse_basic_iso8601_time_only(self):
        """Test parsing ISO 8601 time-only duration strings."""
        # PT4H5M6S - 4 hours, 5 minutes, 6 seconds
        duration = Duration.parse("PT4H5M6S")
        assert duration.years == 0
        assert duration.months == 0
        assert duration.days == 0
        assert duration.storage_seconds == 4 * 3600 + 5 * 60 + 6  # 14706

    def test_parse_iso8601_combined(self):
        """Test parsing ISO 8601 combined date and time duration."""
        # P1Y2M3DT4H5M6S - 1 year, 2 months, 3 days, 4 hours, 5 minutes, 6 seconds
        duration = Duration.parse("P1Y2M3DT4H5M6S")
        assert duration.years == 1
        assert duration.months == 2
        assert duration.days == 3
        assert duration.storage_seconds == 4 * 3600 + 5 * 60 + 6  # 14706

    def test_parse_iso8601_weeks(self):
        """Test parsing ISO 8601 week duration."""
        # P2W - 2 weeks
        duration = Duration.parse("P2W")
        assert duration.years == 0
        assert duration.months == 0
        assert duration.days == 14  # 2 weeks = 14 days
        assert duration.storage_seconds == 0

    def test_parse_iso8601_fractional_weeks(self):
        """Test parsing ISO 8601 fractional week duration."""
        # P1.5W - 1.5 weeks = 1 week + 3.5 days = 1 week + 3 days
        duration = Duration.parse("P1.5W")
        assert duration.years == 0
        assert duration.months == 0
        assert duration.days == 10  # 1 week (7 days) + 3 days from 0.5 week
        assert duration.storage_seconds == 0

    def test_parse_iso8601_fractional_seconds(self):
        """Test parsing ISO 8601 duration with fractional seconds."""
        # PT1.5S - 1.5 seconds
        duration = Duration.parse("PT1.5S")
        assert duration.days == 0
        assert duration.storage_seconds == 1
        assert duration.microseconds == 500000  # 0.5 seconds = 500000 microseconds

    def test_parse_iso8601_fractional_minutes(self):
        """Test parsing ISO 8601 duration with fractional minutes."""
        # PT2.5M - 2.5 minutes = 2 minutes 30 seconds
        duration = Duration.parse("PT2.5M")
        assert duration.days == 0
        assert duration.storage_seconds == 2 * 60 + 30  # 150 seconds

    def test_parse_iso8601_fractional_hours(self):
        """Test parsing ISO 8601 duration with fractional hours."""
        # PT1.5H - 1.5 hours = 1 hour 30 minutes
        duration = Duration.parse("PT1.5H")
        assert duration.days == 0
        assert duration.storage_seconds == 1 * 3600 + 30 * 60  # 5400 seconds

    def test_parse_iso8601_partial_components(self):
        """Test parsing ISO 8601 duration with missing components."""
        # P1Y3D - 1 year, 3 days (no months)
        duration = Duration.parse("P1Y3D")
        assert duration.years == 1
        assert duration.months == 0
        assert duration.days == 3

        # PT30M - 30 minutes (no hours or seconds)
        duration = Duration.parse("PT30M")
        assert duration.storage_seconds == 30 * 60

    def test_parse_iso8601_zero_values(self):
        """Test parsing ISO 8601 duration with explicit zero values."""
        # P0Y0M1DT0H0M0S - only 1 day
        duration = Duration.parse("P0Y0M1DT0H0M0S")
        assert duration.years == 0
        assert duration.months == 0
        assert duration.days == 1
        assert duration.storage_seconds == 0

    def test_parse_iso8601_negative_duration(self):
        """Test parsing ISO 8601 negative duration."""
        # -P1DT2H - negative 1 day 2 hours
        duration = Duration.parse("-P1DT2H")
        # The constructor normalizes -1 day -2 hours into -2 days + 22 hours
        assert duration.days == -2
        assert duration.storage_seconds == 22 * 3600  # 79200 seconds
        # But the total should still be the expected negative value
        assert duration.total_seconds() == -(1 * 86400 + 2 * 3600)  # -93600

    def test_parse_iso8601_case_insensitive(self):
        """Test parsing ISO 8601 duration is case insensitive for designators."""
        # p1y2m3dt4h5m6s - lowercase should work
        duration = Duration.parse("p1y2m3dt4h5m6s")
        assert duration.years == 1
        assert duration.months == 2
        assert duration.days == 3
        assert duration.storage_seconds == 4 * 3600 + 5 * 60 + 6

    def test_parse_iso8601_invalid_format(self):
        """Test parsing invalid ISO 8601 duration strings raises ValueError."""
        import pytest

        # Missing P prefix
        with pytest.raises(ValueError, match="Invalid ISO 8601 duration format"):
            Duration.parse("1Y2M3D")

        # Invalid order
        with pytest.raises(ValueError, match="Invalid ISO 8601 duration format"):
            Duration.parse("P3D2M1Y")

        # T without time components
        with pytest.raises(ValueError, match="Invalid ISO 8601 duration format"):
            Duration.parse("P1DT")

        # Missing T for time components
        with pytest.raises(ValueError, match="Invalid ISO 8601 duration format"):
            Duration.parse("P1D2H")

        # Empty string
        with pytest.raises(ValueError, match="Invalid ISO 8601 duration format"):
            Duration.parse("")

        # Invalid characters
        with pytest.raises(ValueError, match="Invalid ISO 8601 duration format"):
            Duration.parse("P1X")

    def test_parse_iso8601_edge_cases(self):
        """Test parsing ISO 8601 duration edge cases."""
        # Just P should be invalid
        import pytest

        with pytest.raises(ValueError):
            Duration.parse("P")

        # Zero duration
        duration = Duration.parse("PT0S")
        assert duration.total_seconds() == 0

        # Large values - constructor will normalize overflow
        duration = Duration.parse("P999Y999M999DT999H999M999.999S")
        assert duration.years == 999
        assert duration.months == 999
        # 999 days + 999 hours (41 days) + 999 minutes (16 hours 39 minutes) + 999.999 seconds
        # = 999 + 41 + 16/24 days + (39*60 + 999.999)/86400 seconds
        # The constructor normalizes all time overflow into days
        assert duration.days > 999  # Will be larger due to time component overflow


class TestDurationHumanize:
    def test_humanize_basic_units(self):
        """Test humanizing basic time units."""
        # Single units
        assert Duration(seconds=1).humanize() == "1 second"
        assert Duration(seconds=2).humanize() == "2 seconds"
        assert Duration(minutes=1).humanize() == "1 minute"
        assert Duration(minutes=2).humanize() == "2 minutes"
        assert Duration(hours=1).humanize() == "1 hour"
        assert Duration(hours=2).humanize() == "2 hours"
        assert Duration(days=1).humanize() == "1 day"
        assert Duration(days=2).humanize() == "2 days"
        assert Duration(weeks=1).humanize() == "1 week"
        assert Duration(weeks=2).humanize() == "2 weeks"
        assert Duration(months=1).humanize() == "1 month"
        assert Duration(months=2).humanize() == "2 months"
        assert Duration(years=1).humanize() == "1 year"
        assert Duration(years=2).humanize() == "2 years"

    def test_humanize_zero_duration(self):
        """Test humanizing zero duration."""
        assert Duration().humanize() == "0 seconds"

    def test_humanize_multiple_units_default(self):
        """Test humanizing multiple units with default max_units=2."""
        # Two units (default)
        duration = Duration(days=1, hours=2, minutes=30, seconds=45)
        assert duration.humanize() == "1 day 2 hours"

        duration = Duration(hours=3, minutes=45, seconds=30)
        assert duration.humanize() == "3 hours 45 minutes"

        duration = Duration(minutes=5, seconds=30)
        assert duration.humanize() == "5 minutes 30 seconds"

    def test_humanize_max_units_parameter(self):
        """Test humanizing with different max_units values."""
        duration = Duration(days=2, hours=3, minutes=45, seconds=30)

        # max_units=1
        assert duration.humanize(max_units=1) == "2 days"

        # max_units=2 (default)
        assert duration.humanize(max_units=2) == "2 days 3 hours"

        # max_units=3
        assert duration.humanize(max_units=3) == "2 days 3 hours 45 minutes"

        # max_units=4
        assert duration.humanize(max_units=4) == "2 days 3 hours 45 minutes 30 seconds"

    def test_humanize_with_calendar_components(self):
        """Test humanizing durations with calendar components (years/months)."""
        # Years and months should appear first
        duration = Duration(years=2, months=3, days=5, hours=4)
        assert duration.humanize() == "2 years 3 months"

        duration = Duration(years=1, days=10, hours=5)
        assert duration.humanize() == "1 year 10 days"

        duration = Duration(months=6, hours=12, minutes=30)
        assert duration.humanize() == "6 months 12 hours"

    def test_humanize_negative_durations(self):
        """Test humanizing negative durations."""
        assert Duration(days=-1).humanize() == "-1 day"
        assert Duration(hours=-2, minutes=-30).humanize() == "-2 hours 30 minutes"
        assert Duration(days=-1, hours=-3).humanize() == "-1 day 3 hours"

    def test_humanize_fractional_seconds(self):
        """Test humanizing durations with fractional seconds."""
        # Sub-second durations should show as fractional seconds
        duration = Duration(microseconds=500000)  # 0.5 seconds
        assert duration.humanize() == "0.5 seconds"

        duration = Duration(seconds=1, microseconds=250000)  # 1.25 seconds
        assert duration.humanize() == "1.25 seconds"

        duration = Duration(minutes=2, microseconds=750000)  # 2 minutes 0.75 seconds
        assert duration.humanize() == "2 minutes 0.75 seconds"

    def test_humanize_very_small_durations(self):
        """Test humanizing very small durations."""
        # Microseconds only
        assert Duration(microseconds=1).humanize() == "0.000001 seconds"
        assert (
            Duration(microseconds=1000).humanize() == "0.001 seconds"
        )  # 1 millisecond
        assert Duration(microseconds=10000).humanize() == "0.01 seconds"

    def test_humanize_large_durations(self):
        """Test humanizing large durations."""
        duration = Duration(years=100, months=6, days=15, hours=8)
        assert duration.humanize() == "100 years 6 months"

        # Very large time-based duration
        duration = Duration(days=365, hours=12)
        assert duration.humanize() == "365 days 12 hours"

    def test_humanize_locale_parameter(self):
        """Test humanizing with different locales."""
        duration = Duration(days=2, hours=3)

        # English (default)
        assert duration.humanize() == "2 days 3 hours"
        assert duration.humanize(locale="en") == "2 days 3 hours"

        # Polish locale (when implemented)
        # For now, should either work or raise NotImplementedError
        try:
            result = duration.humanize(locale="pl")
            # If implemented, should be Polish
            assert "dni" in result or "godzin" in result
        except NotImplementedError:
            # Expected if Polish locale not yet implemented
            pass

    def test_humanize_edge_cases(self):
        """Test humanizing edge cases."""
        # Only calendar components
        duration = Duration(years=1, months=2)
        assert duration.humanize() == "1 year 2 months"

        # Mixed positive and negative (after normalization)
        # This tests the constructor's normalization behavior
        duration = Duration(days=1, hours=-25)  # Should normalize to -1 day + 23 hours
        result = duration.humanize()
        # The actual result after normalization shows the net effect
        assert result.startswith("-") and ("hour" in result or "day" in result)

    def test_humanize_precision_control(self):
        """Test humanizing with precision control for sub-second values."""
        # Test that very small microseconds are handled reasonably
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize()
        assert (
            result == "0.123456 seconds" or result == "0.123 seconds"
        )  # Allow rounding

        # Test rounding behavior for display
        duration = Duration(microseconds=999999)  # 0.999999 seconds
        result = duration.humanize()
        assert "second" in result

    def test_humanize_invalid_parameters(self):
        """Test humanizing with invalid parameters."""
        import pytest

        duration = Duration(hours=2)

        # Invalid max_units values
        with pytest.raises(ValueError):
            duration.humanize(max_units=0)

        with pytest.raises(ValueError):
            duration.humanize(max_units=-1)

        # Invalid locale (should raise ValueError or NotImplementedError)
        with pytest.raises((ValueError, NotImplementedError)):
            duration.humanize(locale="invalid_locale")
