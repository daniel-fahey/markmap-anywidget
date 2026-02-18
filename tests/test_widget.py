"""Tests for MarkmapWidget."""

from markmap_anywidget import MarkmapWidget


def test_widget():
    w = MarkmapWidget()
    assert w.markdown_content == ""
    assert hasattr(w, "_esm")


def test_widget_with_markdown():
    w = MarkmapWidget(markdown_content="# Test")
    assert w.markdown_content == "# Test"
