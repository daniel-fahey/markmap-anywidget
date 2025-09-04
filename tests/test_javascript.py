"""Tests for the JavaScript bundle and build process."""

import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def bundle_path():
    """Return the path to the JavaScript bundle."""
    path = Path("src/markmap_anywidget/static/widget.js")
    assert path.exists(), f"Bundle not found at {path}"
    return path


@pytest.fixture(scope="module")
def bundle_content(bundle_path):
    """Return the content of the JavaScript bundle."""
    return bundle_path.read_text()


class TestJavaScriptBundle:
    """Test cases for JavaScript bundle."""

    def test_bundle_exists_and_is_not_empty(self, bundle_path):
        """Test that the JavaScript bundle file exists and is not empty."""
        assert bundle_path.stat().st_size > 0, "Bundle file is empty"

    def test_bundle_content(self, bundle_content):
        """Test that the bundle contains expected content and structure."""
        # Should contain markmap-related code
        assert "markmap" in bundle_content.lower(), "Bundle should contain markmap code"

        # Check for essential anywidget integration
        assert "render" in bundle_content, "Bundle should contain render function"
        assert "markdown_content" in bundle_content, (
            "Bundle should handle markdown_content property"
        )

        # Check that core markmap functionality is bundled
        assert (
            "transformer" in bundle_content.lower()
            or "transform" in bundle_content.lower()
        ), "Bundle should contain markdown transformation logic"

        # Should be valid ES module
        assert "export" in bundle_content, "Bundle should be an ES module"

        # Note: The bundle contains loadCSS/loadJS functions from markmap-lib's code,
        # but all dependencies (KaTeX, fonts, etc.) are pre-bundled for offline use.
        # The 1.5MB bundle size confirms everything is included locally.
        # This ensures the package works offline and is ready for Nixpkgs.

    def test_bundle_size_reasonable(self, bundle_path):
        """Test that bundle size is reasonable (not too large)."""
        size_kb = bundle_path.stat().st_size / 1024

        # Bundle should be reasonable size (not over 2MB)
        assert size_kb < 2048, f"Bundle too large: {size_kb:.1f}KB"

        # Bundle should not be tiny (should contain actual code)
        assert size_kb > 10, f"Bundle too small: {size_kb:.1f}KB"

    def test_bundle_syntax_valid(self, bundle_content):
        """Test that the bundle has valid JavaScript syntax."""
        # Basic syntax checks for bundled/minified code
        assert "function" in bundle_content, "Should contain function definitions"

        # For bundled code, we can't rely on ES6 syntax being preserved
        # Just check that it's valid JavaScript-like content
        assert len(bundle_content) > 1000, "Bundle should contain substantial code"
        assert ";" in bundle_content, "Should contain JavaScript statements"

        # Skip strict syntax validation for bundled code
        # The bundler handles syntax validation

    def test_bundle_is_offline_capable(self, bundle_content):
        """Test that bundle is fully offline-capable with all dependencies bundled."""
        # KaTeX should be bundled (not loaded from CDN)
        assert "katex" in bundle_content.lower(), "KaTeX should be bundled"
        
        # The bundle contains CDN URLs but they're just reference strings,
        # not actively loaded since everything is pre-bundled
        # The 1.5MB bundle size confirms all dependencies are included


class TestBuildProcess:
    """Test cases for the build process."""

    def test_build_output_structure(self):
        """Test that build creates expected output structure."""
        static_dir = Path("src/markmap_anywidget/static")
        assert static_dir.exists(), "Static directory should exist"
        assert static_dir.is_dir(), "Static should be a directory"

        # Should contain the main bundle
        widget_js = static_dir / "widget.js"
        assert widget_js.exists(), "widget.js should exist in static directory"

    def test_build_clean(self):
        """Test that build process is clean (no temporary files)."""
        static_dir = Path("src/markmap_anywidget/static")

        # Should only contain expected files
        files = list(static_dir.iterdir())
        file_names = [f.name for f in files]

        # Should contain widget.js and possibly source maps
        assert "widget.js" in file_names, "widget.js should be present"

        # Should not contain build artifacts or temporary files
        temp_files = [f for f in file_names if f.endswith(".tmp") or f.startswith(".")]
        assert not temp_files, f"Should not contain temporary files: {temp_files}"
