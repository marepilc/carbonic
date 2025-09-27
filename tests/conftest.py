"""Pytest configuration for documentation tests."""

import pytest
import sys
from pathlib import Path
from typing import Generator, Any

# Add the project root to Python path to ensure imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(autouse=True)
def setup_carbonic_for_docs() -> Generator[None, None, None]:
    """Ensure carbonic is available for documentation examples."""
    # This fixture automatically sets up the environment for each test
    # ensuring that imports like `from carbonic import DateTime` work
    yield

@pytest.fixture
def sample_datetime() -> Any:
    """Provide a sample DateTime for testing."""
    from carbonic import DateTime
    return DateTime(2024, 1, 15, 14, 30, 0, tz="UTC")

@pytest.fixture
def sample_date() -> Any:
    """Provide a sample Date for testing."""
    from carbonic import Date
    return Date(2024, 1, 15)