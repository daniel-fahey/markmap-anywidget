"""Tests for the Python package structure and metadata."""

import pytest
from pathlib import Path


class TestPackageStructure:
    """Test cases for package structure."""

    def test_package_init_exists(self):
        """Test that package __init__.py exists and is importable."""
        init_path = Path("src/markmap_anywidget/__init__.py")
        assert init_path.exists(), "Package __init__.py should exist"

        # Should be able to import the package
        try:
            import markmap_anywidget

            assert hasattr(markmap_anywidget, "MarkmapWidget"), (
                "Should export MarkmapWidget"
            )
        except ImportError as e:
            pytest.fail(f"Failed to import package: {e}")

    def test_package_metadata(self):
        """Test that package has correct metadata."""
        try:
            import markmap_anywidget

            assert markmap_anywidget.__name__ == "markmap_anywidget"

            # Check that MarkmapWidget is available
            from markmap_anywidget import MarkmapWidget

            assert MarkmapWidget.__name__ == "MarkmapWidget"

        except ImportError as e:
            pytest.fail(f"Failed to import package metadata: {e}")
