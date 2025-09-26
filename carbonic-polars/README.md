# Carbonic Polars Extension

High-performance Polars plugin providing Carbonic datetime functionality with vectorized operations.

## Features

### Custom Parsing with Carbonic Format Tokens
```python
import polars as pl
import carbonic_polars  # Registers the .carbonic namespace

# Parse datetime strings with Carbonic format tokens
df = df.with_columns([
    pl.col("date_str").carbonic.parse_format("Y-m-d H:i:s"),
    pl.col("iso_date").carbonic.parse_format("c"),  # ISO 8601
    pl.col("custom_date").carbonic.parse_format("F j, Y", locale="en"),
])
```

### Business Day Arithmetic
```python
# Add business days (skipping weekends by default)
df = df.with_columns([
    pl.col("start_date").carbonic.add_business_days(5),
    pl.col("due_date").carbonic.subtract_business_days(pl.col("offset_days")),
])

# Custom weekends and holidays
df = df.with_columns([
    pl.col("date").carbonic.add_business_days(
        10,
        weekends=["Friday", "Saturday"],  # Different weekend
        holidays=["2023-12-25", "2023-01-01"]
    )
])
```

### Localized Formatting
```python
# Format with localized month/day names
df = df.with_columns([
    pl.col("date").carbonic.format_localized("F j, Y", locale="pl"),  # "grudzień 25, 2023"
    pl.col("date").carbonic.format_localized("l, F j", locale="en"),  # "Monday, December 25"
])
```

### Bulk Operations
```python
# Parse multiple columns with same format
df = df.carbonic.parse_datetime_columns(
    ["start_date", "end_date", "created_at"],
    format="Y-m-d H:i:s"
)

# Business day calculations across multiple columns
df = df.carbonic.add_business_days_bulk(
    date_columns=["start", "middle", "end"],
    days=[1, 5, 10]
)
```

## Performance Benefits

- **Vectorized Operations**: All operations work on entire Series at once
- **Zero-Copy**: Efficient memory usage with Polars' internal data structures
- **Native Speed**: Rust implementation without Python GIL overhead
- **Null Handling**: Proper null propagation in vectorized operations

## Installation

```bash
# Install from PyPI (when published)
pip install carbonic-polars

# Or install in development mode
cd carbonic-polars
pip install -e .
```

## Comparison with Standard Polars

| Operation | Standard Polars | Carbonic Plugin |
|-----------|----------------|-----------------|
| Parse custom format | `pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")` | `pl.col("date").carbonic.parse_format("Y-m-d")` |
| Business days | Not available | `pl.col("date").carbonic.add_business_days(5)` |
| Localized output | Not available | `pl.col("date").carbonic.format_localized("F j, Y", "pl")` |
| Format tokens | strftime only | Carbon-style + strftime + custom |