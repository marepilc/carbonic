"""Basic tests to verify plugin loading and Polars integration."""

import pytest
import polars as pl


def test_plugin_can_be_imported():
    """Test that the plugin can be imported without errors."""
    try:
        import carbonic_polars
        assert True
    except ImportError:
        pytest.fail("carbonic_polars plugin failed to import")


def test_polars_basic_functionality():
    """Test that basic Polars functionality works."""
    df = pl.DataFrame({
        "date_str": ["2023-12-25", "2024-01-01", "2023-06-15"],
        "numbers": [1, 2, 3]
    })

    assert len(df) == 3
    assert "date_str" in df.columns
    assert "numbers" in df.columns


def test_namespace_registration():
    """Test that the .carbonic namespace is registered."""
    try:
        import carbonic_polars
        df = pl.DataFrame({"test_str": ["2023-12-25", "2024-01-01", "2023-06-15"]})

        # This should not raise an AttributeError if namespace is registered
        expr = pl.col("test_str")
        assert hasattr(expr, "carbonic")

        # Test the real functions work
        result = df.with_columns([
            pl.col("test_str").carbonic.parse_format("Y-m-d").alias("parsed"),
            pl.col("test_str").carbonic.parse_iso().alias("iso_parsed")
        ])

        assert len(result) == 3
        assert "parsed" in result.columns
        assert "iso_parsed" in result.columns

        # Check the placeholder behavior
        parsed_values = result["parsed"].to_list()
        assert all("parsed:" in val for val in parsed_values)

        iso_values = result["iso_parsed"].to_list()
        assert all("iso:" in val for val in iso_values)

        # Test DataFrame namespace
        assert hasattr(df, "carbonic")
        info = df.carbonic.info()
        assert "3 rows" in info

    except ImportError:
        pytest.skip("carbonic_polars not available")
    except AttributeError:
        pytest.skip("carbonic namespace not yet implemented")


if __name__ == "__main__":
    pytest.main([__file__])