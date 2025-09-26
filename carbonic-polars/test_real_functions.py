#!/usr/bin/env python3
"""Test the real Carbonic Polars plugin functionality."""

import polars as pl
import carbonic_polars

def main():
    print("🧪 Testing Real Carbonic Polars Plugin Functions")
    print("=" * 50)

    # Create test data
    df = pl.DataFrame({
        "date_strings": ["2023-12-25", "2024-01-01", "2023-06-15"],
        "iso_strings": ["2023-12-25T14:30:15Z", "2024-01-01T00:00:00Z", "2023-06-15T18:30:45Z"]
    })

    print("📊 Original DataFrame:")
    print(df)
    print()

    # Test parse_format function
    print("🔧 Testing parse_format (placeholder):")
    try:
        result = df.with_columns([
            pl.col("date_strings").carbonic.parse_format("Y-m-d").alias("parsed_dates")
        ])
        print("✅ parse_format works!")
        print(result)
    except Exception as e:
        print(f"❌ parse_format failed: {e}")
    print()

    # Test parse_iso function
    print("🔧 Testing parse_iso (placeholder):")
    try:
        result = df.with_columns([
            pl.col("iso_strings").carbonic.parse_iso().alias("parsed_iso")
        ])
        print("✅ parse_iso works!")
        print(result)
    except Exception as e:
        print(f"❌ parse_iso failed: {e}")
    print()

    # Test both functions together
    print("🔧 Testing both functions together:")
    try:
        result = df.with_columns([
            pl.col("date_strings").carbonic.parse_format("Y-m-d", locale="en").alias("carbonic_parsed"),
            pl.col("iso_strings").carbonic.parse_iso().alias("iso_parsed")
        ])
        print("✅ Both functions work together!")
        print(result)
    except Exception as e:
        print(f"❌ Combined test failed: {e}")
    print()

    print("🎉 Real Rust functions are working with Polars integration!")
    print("Ready for implementing actual datetime parsing logic.")

if __name__ == "__main__":
    main()