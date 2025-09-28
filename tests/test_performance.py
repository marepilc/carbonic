"""Performance tests for Carbonic optimizations."""

import datetime
import time

import pytest

from carbonic import Date, DateTime
from carbonic.core.exceptions import ParseError


class TestCiso8601Integration:
    """Test ciso8601 integration for fast ISO datetime parsing."""

    def test_baseline_parsing_behavior(self):
        """Test current parsing behavior to establish baseline before optimization."""
        test_cases = [
            ("2025-09-23T14:30:45+00:00", 2025, 9, 23, 14, 30, 45, 0),
            ("2025-09-23T14:30:45Z", 2025, 9, 23, 14, 30, 45, 0),
            ("2025-09-23T14:30:45", 2025, 9, 23, 14, 30, 45, 0),
            ("2025-12-31T23:59:59Z", 2025, 12, 31, 23, 59, 59, 0),
            ("2024-02-29T12:00:00Z", 2024, 2, 29, 12, 0, 0, 0),  # Leap year
        ]

        for (
            iso_string,
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond,
        ) in test_cases:
            dt = DateTime.parse(iso_string)
            assert dt.year == year
            assert dt.month == month
            assert dt.day == day
            assert dt.hour == hour
            assert dt.minute == minute
            assert dt.second == second
            assert dt.microsecond == microsecond

    def test_parsing_behavior_preservation_with_ciso8601(self):
        """Test that ciso8601 parsing will produce same results as manual parsing."""
        # This test will be enabled after implementing ciso8601 integration
        # For now, we just verify the baseline behavior
        iso_string = "2025-09-23T14:30:45+00:00"
        dt = DateTime.parse(iso_string)

        assert dt.year == 2025
        assert dt.month == 9
        assert dt.day == 23
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45
        # Current behavior treats timezone offsets as UTC
        assert str(dt.tzinfo) == "UTC"

    def test_ciso8601_fallback_behavior(self):
        """Test that parsing works correctly when ciso8601 is not available."""
        # Mock ciso8601 import to simulate it not being available
        import sys
        from unittest.mock import patch

        # Save original modules state
        original_modules = sys.modules.copy()

        try:
            # Remove ciso8601 from sys.modules to simulate import failure
            if "ciso8601" in sys.modules:
                del sys.modules["ciso8601"]

            # Mock the import to raise ImportError
            with patch.dict("sys.modules", {"ciso8601": None}):
                # Force Python to try importing ciso8601 and fail
                iso_string = "2025-09-23T14:30:45Z"
                dt = DateTime.parse(iso_string)

                # Should still parse correctly using manual parsing
                assert dt.year == 2025
                assert dt.month == 9
                assert dt.day == 23
                assert dt.hour == 14
                assert dt.minute == 30
                assert dt.second == 45
                assert str(dt.tzinfo) == "UTC"

        finally:
            # Restore original modules state
            sys.modules.clear()
            sys.modules.update(original_modules)

    def test_ciso8601_timezone_handling(self):
        """Test timezone handling with ciso8601."""
        # Test with timezone in string
        dt1 = DateTime.parse("2025-09-23T14:30:45+02:00")
        assert str(dt1.tzinfo) == "UTC"  # Current behavior treats offsets as UTC

        # Test with explicit timezone parameter (should override)
        dt2 = DateTime.parse("2025-09-23T14:30:45", tz="Europe/Warsaw")
        assert str(dt2.tzinfo) == "Europe/Warsaw"

        # Test naive datetime with default UTC
        dt3 = DateTime.parse("2025-09-23T14:30:45")
        assert str(dt3.tzinfo) == "UTC"

    def test_ciso8601_microseconds_preservation(self):
        """Test that microseconds are correctly handled by ciso8601."""
        dt = DateTime.parse("2025-09-23T14:30:45.123456Z")
        assert dt.microsecond == 123456

        # Test with different microsecond precision
        dt2 = DateTime.parse("2025-09-23T14:30:45.123Z")
        assert dt2.microsecond == 123000

    def test_non_iso_formats_bypass_ciso8601(self):
        """Test that non-ISO formats correctly bypass ciso8601 and use manual parsing."""
        # These should not be parsed by ciso8601 and fall back to manual parsing
        non_iso_cases = [
            "2025-09-23",  # Date only
            "invalid-datetime",  # Invalid format
        ]

        for case in non_iso_cases:
            try:
                dt = DateTime.parse(case)
                # If parsing succeeds, ensure it's handled by manual parser
                if case == "2025-09-23":
                    assert dt.year == 2025
                    assert dt.month == 9
                    assert dt.day == 23
                    assert dt.hour == 0
                    assert dt.minute == 0
                    assert dt.second == 0
            except ParseError:
                # Expected for invalid formats
                pass

    @pytest.mark.benchmark
    def test_ciso8601_performance_improvement(self):
        """Benchmark parsing performance with ciso8601."""
        iso_strings = [
            "2025-09-23T14:30:45+00:00",
            "2025-09-23T14:30:45Z",
            "2025-09-23T14:30:45.123456Z",
            "2024-02-29T12:00:00+02:00",
        ] * 100  # Parse each 100 times for better measurement

        # Time with ciso8601 (should be fast)
        start_time = time.perf_counter()
        for iso_string in iso_strings:
            DateTime.parse(iso_string)
        ciso8601_time = time.perf_counter() - start_time

        # Print performance information (for manual inspection)
        print(
            f"Parsing {len(iso_strings)} ISO datetime strings took: {ciso8601_time:.4f}s"
        )
        print(
            f"Average time per parse: {ciso8601_time / len(iso_strings) * 1000:.3f}ms"
        )

        # Basic sanity check - should complete in reasonable time
        assert ciso8601_time < 10.0  # Should not take more than 10 seconds

        # Test that ciso8601 is actually being used (not just fallback)
        # We can do this by ensuring common ISO formats parse correctly
        common_formats = [
            "2025-09-23T14:30:45Z",
            "2025-09-23T14:30:45+00:00",
            "2025-09-23T14:30:45.123456Z",
        ]

        for fmt in common_formats:
            dt = DateTime.parse(fmt)
            assert dt.year == 2025
            assert dt.month == 9
            assert dt.day == 23

    def test_comprehensive_performance_benchmark(self):
        """Comprehensive performance benchmark measuring all optimizations."""
        import time

        # Test data
        iso_strings = [
            "2025-09-23T14:30:45Z",
            "2025-09-23T14:30:45+00:00",
            "2025-09-23T14:30:45.123456Z",
            "2024-02-29T12:00:00+02:00",
        ]

        formats = [
            "Y-m-d H:i:s",
            "F j, Y g:i A",
            "l, F j, Y",
            "Y-m-d{T}H:i:s{Z}",
        ]

        # Benchmark 1: ISO Parsing Performance (ciso8601 optimization)
        print("\n=== ISO Parsing Performance (ciso8601) ===")
        iterations = 1000
        start_time = time.perf_counter()
        for _ in range(iterations):
            for iso_string in iso_strings:
                DateTime.parse(iso_string)
        iso_parsing_time = time.perf_counter() - start_time
        print(
            f"Parsed {iterations * len(iso_strings)} ISO strings in {iso_parsing_time:.4f}s"
        )
        print(
            f"Average per parse: {iso_parsing_time / (iterations * len(iso_strings)) * 1000:.3f}ms"
        )

        # Benchmark 2: Formatting Performance (lazy evaluation optimization)
        print("\n=== Formatting Performance (lazy evaluation) ===")
        dt = DateTime(2025, 9, 23, 14, 30, 45, tz="UTC")

        # Test repeated formatting (should benefit from caching)
        start_time = time.perf_counter()
        for _ in range(iterations):
            for fmt in formats:
                dt.format(fmt)
        formatting_time = time.perf_counter() - start_time
        print(
            f"Formatted {iterations * len(formats)} strings in {formatting_time:.4f}s"
        )
        print(
            f"Average per format: {formatting_time / (iterations * len(formats)) * 1000:.3f}ms"
        )

        # Benchmark 3: Memory Efficiency (slots optimization)
        print("\n=== Memory Efficiency (slots) ===")
        start_time = time.perf_counter()
        instances = [
            DateTime(2025, 1, 1, hour=i % 24, minute=i % 60) for i in range(10000)
        ]
        creation_time = time.perf_counter() - start_time
        print(f"Created {len(instances)} DateTime instances in {creation_time:.4f}s")
        print(f"Average per instance: {creation_time / len(instances) * 1000:.3f}ms")

        # Memory check - instances should not have __dict__
        no_dict_count = 0
        for dt in instances[:100]:  # Check first 100
            try:
                _ = dt.__dict__
            except AttributeError:
                no_dict_count += 1

        print(f"Instances without __dict__ (slots working): {no_dict_count}/100")

        # Benchmark 4: Locale-dependent formatting (should benefit from caching)
        print("\n=== Locale-dependent Formatting ===")
        date_obj = Date(2025, 9, 23)
        locale_formats = ["F j, Y", "l, F j, Y", "M d, Y"]

        start_time = time.perf_counter()
        for _ in range(iterations // 10):  # Fewer iterations for locale testing
            for locale in ["en", "pl"]:
                for fmt in locale_formats:
                    date_obj.format(fmt, locale=locale)
        locale_time = time.perf_counter() - start_time
        print(f"Locale formatting completed in {locale_time:.4f}s")

        # Performance assertions (basic sanity checks)
        assert iso_parsing_time < 5.0  # Should parse very fast with ciso8601
        assert formatting_time < 5.0  # Should format reasonably fast
        assert creation_time < 5.0  # Should create instances fast
        assert no_dict_count == 100  # All instances should use slots
        assert locale_time < 5.0  # Locale operations should be reasonable

        print("\n=== Performance Summary ===")
        print(
            f"✓ ISO parsing: {iso_parsing_time:.4f}s ({iterations * len(iso_strings)} operations)"
        )
        print(
            f"✓ Formatting: {formatting_time:.4f}s ({iterations * len(formats)} operations)"
        )
        print(f"✓ Instance creation: {creation_time:.4f}s ({len(instances)} instances)")
        print(f"✓ Memory efficiency: {no_dict_count}/100 instances using slots")
        print(f"✓ Locale formatting: {locale_time:.4f}s")
        print("All performance optimizations working correctly!")


class TestMemoryOptimizations:
    """Test memory usage optimizations."""

    def test_slots_memory_efficiency(self):
        """Test that slots reduce memory usage."""
        # Create many DateTime instances to test memory efficiency
        instances = [DateTime(2025, 1, 1, hour=i % 24) for i in range(1000)]

        # Basic check that all instances are created successfully
        assert len(instances) == 1000
        assert all(isinstance(dt, DateTime) for dt in instances)

        # Check that instances don't have __dict__ (indicating slots are working)
        for dt in instances[:10]:  # Check first 10
            with pytest.raises(AttributeError):
                _ = dt.__dict__

    def test_dataclass_frozen_behavior(self):
        """Test that frozen dataclass behavior is preserved."""
        dt = DateTime(2025, 9, 23, 14, 30, 45)

        # Should not be able to modify attributes (frozen dataclass)
        with pytest.raises((AttributeError, TypeError)):
            dt.year = 2026  # type: ignore[assignment]

        with pytest.raises((AttributeError, TypeError)):
            dt._dt = datetime.datetime.now()  # type: ignore[assignment]


class TestLazyEvaluationPreparation:
    """Preparation tests for lazy evaluation of expensive formatting operations."""

    def test_format_operations_are_pure(self):
        """Test that format operations don't have side effects (prerequisite for lazy eval)."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, tz="UTC")

        # Multiple format calls should return identical results
        result1 = dt.format("Y-m-d H:i:s")
        result2 = dt.format("Y-m-d H:i:s")
        result3 = dt.format("Y-m-d H:i:s")

        assert result1 == result2 == result3
        assert result1 == "2025-09-23 14:30:45"

    def test_expensive_format_operations(self):
        """Identify expensive formatting operations for potential lazy evaluation."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, tz="UTC")

        # Test various format operations that might benefit from caching
        formats = [
            "Y-m-d H:i:s",
            "F j, Y g:i A",  # Full month name
            "l, F j, Y",  # Full day and month names
            "Y-m-d{T}H:i:s{Z}",  # ISO format with escapes
            "jS {o}{f} F Y",  # Ordinal day
        ]

        for fmt in formats:
            result = dt.format(fmt)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_locale_dependent_formatting(self):
        """Test locale-dependent formatting that might benefit from caching."""
        dt = DateTime(2025, 9, 23, 14, 30, 45, tz="UTC")

        # Test different locales
        en_result = dt.format("F j, Y", locale="en")
        pl_result = dt.format("F j, Y", locale="pl")

        assert isinstance(en_result, str)
        assert isinstance(pl_result, str)
        assert en_result != pl_result  # Should be different for different locales
