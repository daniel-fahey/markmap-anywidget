"""Test that the package artifacts are correct."""

import zipfile
from pathlib import Path


def test_wheel_contains_static_files():
    """Test that the built wheel contains static JavaScript files."""
    # Find the wheel (assumes package was built by make/CI)
    wheel_files = list(Path("dist").glob("*.whl"))
    assert wheel_files, "No wheel file found - run 'make build' first"
    
    wheel_file = wheel_files[-1]
    
    # Check wheel contents
    with zipfile.ZipFile(wheel_file, 'r') as zf:
        file_list = zf.namelist()
        
        # Verify static files are included
        static_files = [f for f in file_list if 'static/' in f and f.endswith('.js')]
        assert static_files, f"No static JS files found in wheel. Contents: {file_list}"
        
        # Verify the main widget.js exists
        widget_js_files = [f for f in static_files if f.endswith('widget.js')]
        assert widget_js_files, f"widget.js not found in wheel. Static files: {static_files}"
        
        print(f"✅ Found static files in wheel: {static_files}")


def test_source_static_files_exist():
    """Test that static files exist in source after build."""
    static_dir = Path("src/markmap_anywidget/static")
    assert static_dir.exists(), "Static directory missing - run 'make build' first"
    
    widget_js = static_dir / "widget.js"
    assert widget_js.exists(), "widget.js missing from static directory"
    assert widget_js.stat().st_size > 100000, "widget.js seems too small (< 100KB)"
    
    print(f"✅ Static files exist: {list(static_dir.glob('*'))}")
