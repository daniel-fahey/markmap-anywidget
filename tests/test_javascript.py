"""Tests for the JavaScript bundle."""

from pathlib import Path


def test_bundle():
    path = Path("src/markmap_anywidget/static/widget.js")
    assert path.exists(), "Run 'bun run build' first"
    content = path.read_text()
    assert len(content) > 1000
    assert "markmap" in content.lower()
    assert "render" in content
    assert "katex" in content.lower()
