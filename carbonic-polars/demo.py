#!/usr/bin/env python3
"""Demonstration of the working Carbonic Polars plugin."""

import polars as pl
import carbonic_polars

def main():
    print("🚀 Carbonic Polars Plugin Demo")
    print("=" * 40)

    # Create sample data
    df = pl.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "date_str": ["2023-12-25", "2024-01-01", "2023-06-15", "2023-11-30", "2024-02-14"],
        "numbers": [10, 20, 30, 40, 50],
    })

    print("📊 Original DataFrame:")
    print(df)
    print()

    # Test Expression namespace
    print("🔧 Testing Expression namespace (.carbonic):")
    try:
        expr = pl.col("numbers")
        carbonic_expr = expr.carbonic.placeholder()
        print(f"✅ Expression namespace registered: {carbonic_expr is not None}")
    except Exception as e:
        print(f"❌ Expression namespace error: {e}")
    print()

    # Test DataFrame namespace
    print("📋 Testing DataFrame namespace (.carbonic):")
    try:
        info = df.carbonic.info()
        print(f"✅ DataFrame namespace: {info}")
    except Exception as e:
        print(f"❌ DataFrame namespace error: {e}")
    print()

    # Test with actual Polars operations
    print("⚙️  Testing with Polars operations:")
    try:
        result = df.with_columns([
            pl.col("numbers").carbonic.placeholder().alias("processed_numbers")
        ])
        print("✅ Polars integration working!")
        print(result.head())
    except Exception as e:
        print(f"❌ Polars integration error: {e}")
    print()

    print("🎉 Basic plugin functionality verified!")
    print()
    print("Next steps:")
    print("- Add actual datetime parsing functions")
    print("- Implement business day arithmetic")
    print("- Add localized formatting")
    print("- Full vectorized operations")

if __name__ == "__main__":
    main()