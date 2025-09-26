# Carbonic Polars Plugin Development

## Project Structure

```
carbonic-polars/
├── src/                    # Rust source code
│   ├── lib.rs             # Main plugin entry point
│   └── *.rs.bak           # Backup of complex modules (temporarily disabled)
├── carbonic_polars/       # Python package
│   ├── __init__.py        # Main Python module with namespace registration
│   └── _internal.abi3.so  # Compiled Rust library (generated)
├── tests/                 # Test suite
├── Cargo.toml            # Rust dependencies and build config
├── pyproject.toml        # Python package metadata and build system
├── uv.lock              # UV dependency lock file (tracked for reproducibility)
└── demo.py              # Working demonstration script
```

## Development Workflow

### 1. Setup Environment
```bash
cd carbonic-polars
uv sync  # Install Python dependencies and create virtual environment
```

### 2. Build Plugin
```bash
uv run maturin develop  # Compile Rust code and install Python package
```

### 3. Run Tests
```bash
uv run pytest tests/ -v  # Run test suite
uv run python demo.py    # Run demonstration
```

### 4. Development Cycle
1. Modify Rust code in `src/`
2. Update Python bindings in `carbonic_polars/__init__.py` if needed
3. Run `uv run maturin develop` to rebuild
4. Test changes with `uv run pytest`

## Build System

- **maturin**: Builds Rust extension and creates Python wheel
- **PyO3**: Provides Rust-Python bindings
- **pyo3-polars**: Polars-specific plugin framework
- **UV**: Manages Python dependencies and virtual environment

## Current Status

✅ **Working:**
- Basic Rust plugin compilation
- Python namespace registration (`pl.col("x").carbonic`)
- Polars integration (`df.carbonic`)
- Test suite passing
- Build pipeline established

🚧 **In Development:**
- Actual datetime parsing functions
- Business day arithmetic
- Localized formatting
- Vectorized operations

## File Management

### Tracked Files
- Source code (`src/`, `carbonic_polars/`)
- Configuration (`*.toml`)
- Tests and documentation
- `uv.lock` (for reproducible builds)

### Ignored Files
- Build artifacts (`target/`, `*.abi3.so`)
- Python cache (`__pycache__/`, `.pytest_cache/`)
- Virtual environment (`.venv/`)
- Backup files (`*.rs.bak`)
- Distribution files (`dist/`, `build/`)

## Next Steps

1. **Restore Full Functionality**: Move `*.rs.bak` files back and fix compilation errors
2. **Implement Core Features**: Add parsing, business days, and formatting
3. **Performance Testing**: Benchmark against pure Polars operations
4. **Documentation**: Complete API documentation and examples

## Dependencies

### Rust Dependencies
- `polars`: Core Polars functionality
- `pyo3`: Python bindings
- `pyo3-polars`: Polars plugin framework
- `chrono`: Date/time handling
- `serde`: Serialization

### Python Dependencies
- `polars>=0.20.0`: Core Polars library
- `carbonic>=0.1.0`: Main Carbonic datetime library
- `maturin`: Build system (dev)
- `pytest`: Testing framework (dev)