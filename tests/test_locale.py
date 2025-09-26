"""Tests for localization functionality."""

import pytest

from carbonic import Date, DateTime, Duration
from carbonic.locale import get_locale, is_locale_available


class TestLocaleInfrastructure:
    def test_get_locale_english(self):
        """Test getting English locale."""
        locale = get_locale("en")
        assert locale.code == "en"
        assert locale.name == "English"

    def test_get_locale_polish(self):
        """Test getting Polish locale."""
        locale = get_locale("pl")
        assert locale.code == "pl"
        assert locale.name == "Polski"

    def test_get_locale_invalid(self):
        """Test getting invalid locale raises error."""
        with pytest.raises(ValueError, match="Unsupported locale"):
            get_locale("invalid")

    def test_get_locale_none_defaults_english(self):
        """Test that None locale defaults to English."""
        locale = get_locale(None)
        assert locale.code == "en"

    def test_locale_registration(self):
        """Test locale registration system."""

        # Should have at least English and Polish
        assert is_locale_available("en")
        assert is_locale_available("pl")


class TestDurationHumanizeLocalization:
    def test_duration_humanize_english_basic(self):
        """Test Duration.humanize() with English locale."""
        duration = Duration(days=2, hours=3, minutes=15)

        # Default should be English
        result = duration.humanize()
        assert result == "2 days 3 hours"

        # Explicit English
        result = duration.humanize(locale="en")
        assert result == "2 days 3 hours"

    def test_duration_humanize_polish_basic(self):
        """Test Duration.humanize() with Polish locale."""
        duration = Duration(days=2, hours=3, minutes=15)

        result = duration.humanize(locale="pl")
        assert result == "2 dni 3 godziny"

    def test_duration_humanize_polish_singular_plural(self):
        """Test Polish pluralization rules."""
        # Singular forms
        assert Duration(days=1).humanize(locale="pl") == "1 dzień"
        assert Duration(hours=1).humanize(locale="pl") == "1 godzina"
        assert Duration(minutes=1).humanize(locale="pl") == "1 minuta"
        assert Duration(seconds=1).humanize(locale="pl") == "1 sekunda"

        # Plural forms (2-4)
        assert Duration(days=2).humanize(locale="pl") == "2 dni"
        assert Duration(days=3).humanize(locale="pl") == "3 dni"
        assert Duration(days=4).humanize(locale="pl") == "4 dni"

        assert Duration(hours=2).humanize(locale="pl") == "2 godziny"
        assert Duration(hours=3).humanize(locale="pl") == "3 godziny"
        assert Duration(hours=4).humanize(locale="pl") == "4 godziny"

        # Many forms (5+)
        assert Duration(days=5).humanize(locale="pl") == "5 dni"
        assert Duration(days=10).humanize(locale="pl") == "10 dni"
        assert Duration(hours=5).humanize(locale="pl") == "5 godzin"
        assert Duration(hours=10).humanize(locale="pl") == "10 godzin"

    def test_duration_humanize_polish_complex_plurals(self):
        """Test Polish complex pluralization rules."""
        # Numbers ending in 2-4 but not 12-14 use plural2 form
        assert Duration(days=12).humanize(locale="pl") == "12 dni"  # many form
        assert Duration(days=22).humanize(locale="pl") == "22 dni"  # plural2 form
        assert Duration(days=32).humanize(locale="pl") == "32 dni"  # plural2 form

        # Numbers ending in 5-9, 0, or teens use many form
        assert Duration(days=15).humanize(locale="pl") == "15 dni"
        assert Duration(days=20).humanize(locale="pl") == "20 dni"

    def test_duration_humanize_polish_calendar_units(self):
        """Test Polish calendar units."""
        # Years
        assert Duration(years=1).humanize(locale="pl") == "1 rok"
        assert Duration(years=2).humanize(locale="pl") == "2 lata"
        assert Duration(years=5).humanize(locale="pl") == "5 lat"

        # Months
        assert Duration(months=1).humanize(locale="pl") == "1 miesiąc"
        assert Duration(months=2).humanize(locale="pl") == "2 miesiące"
        assert Duration(months=5).humanize(locale="pl") == "5 miesięcy"

        # Weeks
        assert Duration(weeks=1).humanize(locale="pl") == "1 tydzień"
        assert (
            Duration(weeks=2).humanize(locale="pl") == "14 dni"
        )  # Shows as days due to grammar conflicts
        assert Duration(weeks=5).humanize(locale="pl") == "5 tygodni"

    def test_duration_humanize_negative_polish(self):
        """Test negative durations in Polish."""
        assert Duration(days=-1).humanize(locale="pl") == "-1 dzień"
        assert Duration(days=-2).humanize(locale="pl") == "-2 dni"
        assert Duration(hours=-3).humanize(locale="pl") == "-3 godziny"

    def test_duration_humanize_zero_polish(self):
        """Test zero duration in Polish."""
        assert Duration().humanize(locale="pl") == "0 sekund"

    def test_duration_humanize_fractional_polish(self):
        """Test fractional durations in Polish."""
        duration = Duration(microseconds=500000)  # 0.5 seconds
        assert (
            duration.humanize(locale="pl") == "0,5 sekundy"
        )  # Polish uses comma decimal


class TestDateLocalization:
    def test_date_format_english_month_names(self):
        """Test English month names in date formatting."""
        date = Date(2023, 12, 25)

        # Full month name
        result = date.format("F j, Y", locale="en")
        assert result == "December 25, 2023"

        # Short month name
        result = date.format("M j, Y", locale="en")
        assert result == "Dec 25, 2023"

    def test_date_format_polish_month_names(self):
        """Test Polish month names in date formatting."""
        date = Date(2023, 12, 25)

        # Full month name
        result = date.format("F j, Y", locale="pl")
        assert result == "grudzień 25, 2023"

        # Short month name
        result = date.format("M j, Y", locale="pl")
        assert result == "gru 25, 2023"

    def test_date_format_english_day_names(self):
        """Test English day names in date formatting."""
        date = Date(2023, 12, 25)  # Monday

        # Full day name
        result = date.format("l, F j, Y", locale="en")
        assert result == "Monday, December 25, 2023"

        # Short day name
        result = date.format("D, M j, Y", locale="en")
        assert result == "Mon, Dec 25, 2023"

    def test_date_format_polish_day_names(self):
        """Test Polish day names in date formatting."""
        date = Date(2023, 12, 25)  # Monday

        # Full day name
        result = date.format("l, F j, Y", locale="pl")
        assert result == "poniedziałek, grudzień 25, 2023"

        # Short day name
        result = date.format("D, M j, Y", locale="pl")
        assert result == "pon, gru 25, 2023"

    def test_date_format_polish_case_handling(self):
        """Test Polish case handling in date formatting."""
        date = Date(2023, 1, 15)

        # Different cases for Polish months might be needed
        # This tests the framework is ready for grammatical cases
        result = date.format("F", locale="pl")
        assert result == "styczeń"


class TestDateTimeLocalization:
    def test_datetime_format_localized(self):
        """Test localized DateTime formatting."""
        dt = DateTime(2023, 12, 25, 14, 30, 15, tz="UTC")

        # English
        result = dt.format("l, F j, Y \\a\\t G:i:s", locale="en")
        assert result == "Monday, December 25, 2023 at 14:30:15"

        # Polish
        result = dt.format("l, F j, Y \\o G:i:s", locale="pl")
        assert result == "poniedziałek, grudzień 25, 2023 o 14:30:15"


class TestLocaleSpecificFormatting:
    def test_english_number_formatting(self):
        """Test English number formatting (decimal point)."""
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize(locale="en")
        assert "." in result  # English uses decimal point

    def test_polish_number_formatting(self):
        """Test Polish number formatting (decimal comma)."""
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize(locale="pl")
        assert "," in result  # Polish uses decimal comma

    def test_locale_specific_pluralization_edge_cases(self):
        """Test edge cases in pluralization."""
        # Test teens in Polish (should use 'many' form)
        for i in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
            result = Duration(days=i).humanize(locale="pl")
            assert result == f"{i} dni"  # Always 'dni' for teens

        # Test 21, 22, 23, 24 in Polish (should use plural2 form)
        for i in [21, 22, 23, 24]:
            result = Duration(days=i).humanize(locale="pl")
            assert result == f"{i} dni"


class TestLocaleErrors:
    def test_invalid_locale_in_duration_humanize(self):
        """Test invalid locale in Duration.humanize()."""
        duration = Duration(hours=2)

        with pytest.raises(ValueError, match="Unsupported locale"):
            duration.humanize(locale="invalid")

    def test_invalid_locale_in_date_format(self):
        """Test invalid locale in Date.format()."""
        date = Date(2023, 12, 25)

        with pytest.raises(ValueError, match="Unsupported locale"):
            date.format("F j, Y", locale="invalid")

    def test_invalid_locale_in_datetime_format(self):
        """Test invalid locale in DateTime.format()."""
        dt = DateTime(2023, 12, 25, 14, 30, 15)

        with pytest.raises(ValueError, match="Unsupported locale"):
            dt.format("l, F j, Y", locale="invalid")
