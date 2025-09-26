#!/bin/bash
# Clean build artifacts from Carbonic project

echo "🧹 Cleaning Carbonic build artifacts..."

# Clean main project artifacts
echo "Cleaning main project..."
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/
rm -rf .pytest_cache/
rm -rf .mypy_cache/
rm -rf .ruff_cache/
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Clean Polars plugin artifacts
if [ -d "carbonic-polars" ]; then
    echo "Cleaning Polars plugin..."
    cd carbonic-polars

    # Clean Rust artifacts
    if [ -f "Cargo.toml" ]; then
        cargo clean 2>/dev/null || echo "Cargo clean failed (this is okay)"
    fi
    rm -rf target/
    rm -f Cargo.lock

    # Clean Python artifacts
    rm -rf .venv/
    rm -rf dist/
    rm -rf build/
    rm -rf *.egg-info/
    rm -rf .pytest_cache/
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
    find . -name "*.pyc" -delete 2>/dev/null
    find . -name "*.abi3.so" -delete 2>/dev/null
    find . -name "*.pyd" -delete 2>/dev/null

    cd ..
fi

echo "✅ Build artifacts cleaned!"
echo ""
echo "📊 File count after cleanup:"
find . -type f | wc -l
echo ""
echo "📋 Git status:"
git status --porcelain | wc -l
echo "files changed according to git"