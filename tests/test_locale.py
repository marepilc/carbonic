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
        result = dt.format("l, F j, Y {a}{t} G:i:s", locale="en")
        assert result == "Monday, December 25, 2023 at 14:30:15"

        # Polish
        result = dt.format("l, F j, Y {o} G:i:s", locale="pl")
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


class TestSpanishLocalization:
    def test_spanish_locale_basic(self):
        """Test basic Spanish locale functionality."""
        locale = get_locale("es")
        assert locale.code == "es"
        assert locale.name == "Español"

    def test_duration_humanize_spanish_basic(self):
        """Test Duration.humanize() with Spanish locale."""
        # Singular forms
        assert Duration(seconds=1).humanize(locale="es") == "1 segundo"
        assert Duration(minutes=1).humanize(locale="es") == "1 minuto"
        assert Duration(hours=1).humanize(locale="es") == "1 hora"
        assert Duration(days=1).humanize(locale="es") == "1 día"
        assert Duration(weeks=1).humanize(locale="es") == "1 semana"
        assert Duration(months=1).humanize(locale="es") == "1 mes"
        assert Duration(years=1).humanize(locale="es") == "1 año"

        # Plural forms
        assert Duration(seconds=2).humanize(locale="es") == "2 segundos"
        assert Duration(minutes=2).humanize(locale="es") == "2 minutos"
        assert Duration(hours=2).humanize(locale="es") == "2 horas"
        assert Duration(days=2).humanize(locale="es") == "2 días"
        assert Duration(weeks=2).humanize(locale="es") == "2 semanas"
        assert Duration(months=2).humanize(locale="es") == "2 meses"
        assert Duration(years=2).humanize(locale="es") == "2 años"

    def test_duration_humanize_spanish_zero_and_negative(self):
        """Test zero and negative durations in Spanish."""
        assert Duration().humanize(locale="es") == "0 segundos"
        assert Duration(days=-1).humanize(locale="es") == "-1 día"
        assert Duration(days=-2).humanize(locale="es") == "-2 días"

    def test_duration_humanize_spanish_fractional(self):
        """Test fractional durations in Spanish (decimal comma)."""
        duration = Duration(microseconds=500000)  # 0.5 seconds
        result = duration.humanize(locale="es")
        assert result == "0,5 segundos"  # Spanish uses comma decimal

    def test_date_format_spanish_month_names(self):
        """Test Spanish month names in date formatting."""
        date = Date(2023, 12, 25)

        # Full month name
        result = date.format("F j, Y", locale="es")
        assert result == "diciembre 25, 2023"

        # Short month name
        result = date.format("M j, Y", locale="es")
        assert result == "dic 25, 2023"

        # Test all months
        expected_full = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        expected_short = [
            "ene", "feb", "mar", "abr", "may", "jun",
            "jul", "ago", "sep", "oct", "nov", "dic"
        ]

        for month in range(1, 13):
            date = Date(2023, month, 1)
            assert date.format("F", locale="es") == expected_full[month - 1]
            assert date.format("M", locale="es") == expected_short[month - 1]

    def test_date_format_spanish_day_names(self):
        """Test Spanish day names in date formatting."""
        # Test a known Monday (2023-12-25)
        date = Date(2023, 12, 25)

        # Full day name
        result = date.format("l, F j, Y", locale="es")
        assert result == "lunes, diciembre 25, 2023"

        # Short day name
        result = date.format("D, M j, Y", locale="es")
        assert result == "lun, dic 25, 2023"

        # Test all days of the week (starting with Monday 2023-12-25)
        expected_full = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        expected_short = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]

        for day_offset in range(7):
            test_date = Date(2023, 12, 25 + day_offset)
            assert test_date.format("l", locale="es") == expected_full[day_offset]
            assert test_date.format("D", locale="es") == expected_short[day_offset]

    def test_datetime_format_spanish(self):
        """Test localized DateTime formatting in Spanish."""
        dt = DateTime(2023, 12, 25, 14, 30, 15, tz="UTC")

        result = dt.format("l, F j, Y {a} {l}{a}{s} G:i:s", locale="es")
        assert result == "lunes, diciembre 25, 2023 a las 14:30:15"

    def test_spanish_number_formatting(self):
        """Test Spanish number formatting (decimal comma)."""
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize(locale="es")
        assert "," in result  # Spanish uses decimal comma

    def test_spanish_pluralization_edge_cases(self):
        """Test Spanish pluralization edge cases."""
        # Test zero duration (shows as seconds)
        assert Duration().humanize(locale="es") == "0 segundos"

        # Test negative numbers
        assert Duration(days=-1).humanize(locale="es") == "-1 día"
        assert Duration(days=-2).humanize(locale="es") == "-2 días"

        # Test fractional numbers (should be plural)
        assert Duration(days=1.5).humanize(locale="es") == "1 día 12 horas"


class TestFrenchLocalization:
    def test_french_locale_basic(self):
        """Test basic French locale functionality."""
        locale = get_locale("fr")
        assert locale.code == "fr"
        assert locale.name == "Français"

    def test_duration_humanize_french_basic(self):
        """Test Duration.humanize() with French locale."""
        # Singular forms
        assert Duration(seconds=1).humanize(locale="fr") == "1 seconde"
        assert Duration(minutes=1).humanize(locale="fr") == "1 minute"
        assert Duration(hours=1).humanize(locale="fr") == "1 heure"
        assert Duration(days=1).humanize(locale="fr") == "1 jour"
        assert Duration(weeks=1).humanize(locale="fr") == "1 semaine"
        assert Duration(months=1).humanize(locale="fr") == "1 mois"
        assert Duration(years=1).humanize(locale="fr") == "1 an"

        # Plural forms
        assert Duration(seconds=2).humanize(locale="fr") == "2 secondes"
        assert Duration(minutes=2).humanize(locale="fr") == "2 minutes"
        assert Duration(hours=2).humanize(locale="fr") == "2 heures"
        assert Duration(days=2).humanize(locale="fr") == "2 jours"
        assert Duration(weeks=2).humanize(locale="fr") == "2 semaines"
        assert Duration(months=2).humanize(locale="fr") == "2 mois"
        assert Duration(years=2).humanize(locale="fr") == "2 ans"

    def test_duration_humanize_french_zero_and_negative(self):
        """Test zero and negative durations in French."""
        assert Duration().humanize(locale="fr") == "0 secondes"
        assert Duration(days=-1).humanize(locale="fr") == "-1 jour"
        assert Duration(days=-2).humanize(locale="fr") == "-2 jours"

    def test_duration_humanize_french_fractional(self):
        """Test fractional durations in French (decimal comma)."""
        duration = Duration(microseconds=500000)  # 0.5 seconds
        result = duration.humanize(locale="fr")
        assert result == "0,5 secondes"  # French uses comma decimal

    def test_date_format_french_month_names(self):
        """Test French month names in date formatting."""
        date = Date(2023, 12, 25)

        # Full month name
        result = date.format("F j, Y", locale="fr")
        assert result == "décembre 25, 2023"

        # Short month name
        result = date.format("M j, Y", locale="fr")
        assert result == "déc 25, 2023"

        # Test all months
        expected_full = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        expected_short = [
            "jan", "fév", "mar", "avr", "mai", "jun",
            "jul", "aoû", "sep", "oct", "nov", "déc"
        ]

        for month in range(1, 13):
            date = Date(2023, month, 1)
            assert date.format("F", locale="fr") == expected_full[month - 1]
            assert date.format("M", locale="fr") == expected_short[month - 1]

    def test_date_format_french_day_names(self):
        """Test French day names in date formatting."""
        # Test a known Monday (2023-12-25)
        date = Date(2023, 12, 25)

        # Full day name
        result = date.format("l, F j, Y", locale="fr")
        assert result == "lundi, décembre 25, 2023"

        # Short day name
        result = date.format("D, M j, Y", locale="fr")
        assert result == "lun, déc 25, 2023"

        # Test all days of the week (starting with Monday 2023-12-25)
        expected_full = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        expected_short = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"]

        for day_offset in range(7):
            test_date = Date(2023, 12, 25 + day_offset)
            assert test_date.format("l", locale="fr") == expected_full[day_offset]
            assert test_date.format("D", locale="fr") == expected_short[day_offset]

    def test_datetime_format_french(self):
        """Test localized DateTime formatting in French."""
        dt = DateTime(2023, 12, 25, 14, 30, 15, tz="UTC")

        result = dt.format("l, F j, Y {à} G:i:s", locale="fr")
        assert result == "lundi, décembre 25, 2023 à 14:30:15"

    def test_french_number_formatting(self):
        """Test French number formatting (decimal comma)."""
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize(locale="fr")
        assert "," in result  # French uses decimal comma

    def test_french_pluralization_edge_cases(self):
        """Test French pluralization edge cases."""
        # Test zero duration (shows as seconds)
        assert Duration().humanize(locale="fr") == "0 secondes"

        # Test negative numbers
        assert Duration(days=-1).humanize(locale="fr") == "-1 jour"
        assert Duration(days=-2).humanize(locale="fr") == "-2 jours"

        # Test fractional numbers (should be plural)
        assert Duration(days=1.5).humanize(locale="fr") == "1 jour 12 heures"


class TestGermanLocalization:
    def test_german_locale_basic(self):
        """Test basic German locale functionality."""
        locale = get_locale("de")
        assert locale.code == "de"
        assert locale.name == "Deutsch"

    def test_duration_humanize_german_basic(self):
        """Test Duration.humanize() with German locale."""
        # Singular forms
        assert Duration(seconds=1).humanize(locale="de") == "1 Sekunde"
        assert Duration(minutes=1).humanize(locale="de") == "1 Minute"
        assert Duration(hours=1).humanize(locale="de") == "1 Stunde"
        assert Duration(days=1).humanize(locale="de") == "1 Tag"
        assert Duration(weeks=1).humanize(locale="de") == "1 Woche"
        assert Duration(months=1).humanize(locale="de") == "1 Monat"
        assert Duration(years=1).humanize(locale="de") == "1 Jahr"

        # Plural forms
        assert Duration(seconds=2).humanize(locale="de") == "2 Sekunden"
        assert Duration(minutes=2).humanize(locale="de") == "2 Minuten"
        assert Duration(hours=2).humanize(locale="de") == "2 Stunden"
        assert Duration(days=2).humanize(locale="de") == "2 Tage"
        assert Duration(weeks=2).humanize(locale="de") == "2 Wochen"
        assert Duration(months=2).humanize(locale="de") == "2 Monate"
        assert Duration(years=2).humanize(locale="de") == "2 Jahre"

    def test_duration_humanize_german_zero_and_negative(self):
        """Test zero and negative durations in German."""
        assert Duration().humanize(locale="de") == "0 Sekunden"
        assert Duration(days=-1).humanize(locale="de") == "-1 Tag"
        assert Duration(days=-2).humanize(locale="de") == "-2 Tage"

    def test_duration_humanize_german_fractional(self):
        """Test fractional durations in German (decimal comma)."""
        duration = Duration(microseconds=500000)  # 0.5 seconds
        result = duration.humanize(locale="de")
        assert result == "0,5 Sekunden"  # German uses comma decimal

    def test_date_format_german_month_names(self):
        """Test German month names in date formatting."""
        date = Date(2023, 12, 25)

        # Full month name
        result = date.format("F j, Y", locale="de")
        assert result == "Dezember 25, 2023"

        # Short month name
        result = date.format("M j, Y", locale="de")
        assert result == "Dez 25, 2023"

        # Test all months
        expected_full = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ]
        expected_short = [
            "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
            "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"
        ]

        for month in range(1, 13):
            date = Date(2023, month, 1)
            assert date.format("F", locale="de") == expected_full[month - 1]
            assert date.format("M", locale="de") == expected_short[month - 1]

    def test_date_format_german_day_names(self):
        """Test German day names in date formatting."""
        # Test a known Monday (2023-12-25)
        date = Date(2023, 12, 25)

        # Full day name
        result = date.format("l, F j, Y", locale="de")
        assert result == "Montag, Dezember 25, 2023"

        # Short day name
        result = date.format("D, M j, Y", locale="de")
        assert result == "Mo, Dez 25, 2023"

        # Test all days of the week (starting with Monday 2023-12-25)
        expected_full = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        expected_short = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

        for day_offset in range(7):
            test_date = Date(2023, 12, 25 + day_offset)
            assert test_date.format("l", locale="de") == expected_full[day_offset]
            assert test_date.format("D", locale="de") == expected_short[day_offset]

    def test_datetime_format_german(self):
        """Test localized DateTime formatting in German."""
        dt = DateTime(2023, 12, 25, 14, 30, 15, tz="UTC")

        result = dt.format("l, F j, Y {u}{m} G:i:s", locale="de")
        assert result == "Montag, Dezember 25, 2023 um 14:30:15"

    def test_german_number_formatting(self):
        """Test German number formatting (decimal comma)."""
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize(locale="de")
        assert "," in result  # German uses decimal comma

    def test_german_pluralization_edge_cases(self):
        """Test German pluralization edge cases."""
        # Test zero duration (shows as seconds)
        assert Duration().humanize(locale="de") == "0 Sekunden"

        # Test negative numbers
        assert Duration(days=-1).humanize(locale="de") == "-1 Tag"
        assert Duration(days=-2).humanize(locale="de") == "-2 Tage"

        # Test fractional numbers (should be plural)
        assert Duration(days=1.5).humanize(locale="de") == "1 Tag 12 Stunden"


class TestPortugueseLocalization:
    def test_portuguese_locale_basic(self):
        """Test basic Portuguese locale functionality."""
        locale = get_locale("pt")
        assert locale.code == "pt"
        assert locale.name == "Português"

    def test_duration_humanize_portuguese_basic(self):
        """Test Duration.humanize() with Portuguese locale."""
        # Singular forms
        assert Duration(seconds=1).humanize(locale="pt") == "1 segundo"
        assert Duration(minutes=1).humanize(locale="pt") == "1 minuto"
        assert Duration(hours=1).humanize(locale="pt") == "1 hora"
        assert Duration(days=1).humanize(locale="pt") == "1 dia"
        assert Duration(weeks=1).humanize(locale="pt") == "1 semana"
        assert Duration(months=1).humanize(locale="pt") == "1 mês"
        assert Duration(years=1).humanize(locale="pt") == "1 ano"

        # Plural forms
        assert Duration(seconds=2).humanize(locale="pt") == "2 segundos"
        assert Duration(minutes=2).humanize(locale="pt") == "2 minutos"
        assert Duration(hours=2).humanize(locale="pt") == "2 horas"
        assert Duration(days=2).humanize(locale="pt") == "2 dias"
        assert Duration(weeks=2).humanize(locale="pt") == "2 semanas"
        assert Duration(months=2).humanize(locale="pt") == "2 meses"
        assert Duration(years=2).humanize(locale="pt") == "2 anos"

    def test_duration_humanize_portuguese_zero_and_negative(self):
        """Test zero and negative durations in Portuguese."""
        assert Duration().humanize(locale="pt") == "0 segundos"
        assert Duration(days=-1).humanize(locale="pt") == "-1 dia"
        assert Duration(days=-2).humanize(locale="pt") == "-2 dias"

    def test_duration_humanize_portuguese_fractional(self):
        """Test fractional durations in Portuguese (decimal comma)."""
        duration = Duration(microseconds=500000)  # 0.5 seconds
        result = duration.humanize(locale="pt")
        assert result == "0,5 segundos"  # Portuguese uses comma decimal

    def test_date_format_portuguese_month_names(self):
        """Test Portuguese month names in date formatting."""
        date = Date(2023, 12, 25)

        # Full month name
        result = date.format("F j, Y", locale="pt")
        assert result == "dezembro 25, 2023"

        # Short month name
        result = date.format("M j, Y", locale="pt")
        assert result == "dez 25, 2023"

        # Test all months
        expected_full = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        expected_short = [
            "jan", "fev", "mar", "abr", "mai", "jun",
            "jul", "ago", "set", "out", "nov", "dez"
        ]

        for month in range(1, 13):
            date = Date(2023, month, 1)
            assert date.format("F", locale="pt") == expected_full[month - 1]
            assert date.format("M", locale="pt") == expected_short[month - 1]

    def test_date_format_portuguese_day_names(self):
        """Test Portuguese day names in date formatting."""
        # Test a known Monday (2023-12-25)
        date = Date(2023, 12, 25)

        # Full day name
        result = date.format("l, F j, Y", locale="pt")
        assert result == "segunda-feira, dezembro 25, 2023"

        # Short day name
        result = date.format("D, M j, Y", locale="pt")
        assert result == "seg, dez 25, 2023"

        # Test all days of the week (starting with Monday 2023-12-25)
        expected_full = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        expected_short = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

        for day_offset in range(7):
            test_date = Date(2023, 12, 25 + day_offset)
            assert test_date.format("l", locale="pt") == expected_full[day_offset]
            assert test_date.format("D", locale="pt") == expected_short[day_offset]

    def test_datetime_format_portuguese(self):
        """Test localized DateTime formatting in Portuguese."""
        dt = DateTime(2023, 12, 25, 14, 30, 15, tz="UTC")

        result = dt.format("l, F j, Y {à}{s} G:i:s", locale="pt")
        assert result == "segunda-feira, dezembro 25, 2023 às 14:30:15"

    def test_portuguese_number_formatting(self):
        """Test Portuguese number formatting (decimal comma)."""
        duration = Duration(microseconds=123456)  # 0.123456 seconds
        result = duration.humanize(locale="pt")
        assert "," in result  # Portuguese uses decimal comma

    def test_portuguese_pluralization_edge_cases(self):
        """Test Portuguese pluralization edge cases."""
        # Test zero duration (shows as seconds)
        assert Duration().humanize(locale="pt") == "0 segundos"

        # Test negative numbers
        assert Duration(days=-1).humanize(locale="pt") == "-1 dia"
        assert Duration(days=-2).humanize(locale="pt") == "-2 dias"

        # Test fractional numbers (should be plural)
        assert Duration(days=1.5).humanize(locale="pt") == "1 dia 12 horas"


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
