"""Tests for the MarkmapWidget class."""

import pytest
from markmap_anywidget import MarkmapWidget


@pytest.fixture
def widget():
    """Return a default MarkmapWidget instance."""
    return MarkmapWidget()


class TestMarkmapWidget:
    """Test cases for MarkmapWidget."""

    def test_widget_creation(self, widget):
        """Test that widget can be created with default values."""
        assert widget.markdown_content == ""
        assert hasattr(widget, "_esm")
        assert hasattr(widget, "_css")

    def test_widget_with_markdown(self):
        """Test that widget can be created with markdown content."""
        markdown = "# Test\n\nThis is a test."
        widget = MarkmapWidget(markdown_content=markdown)
        assert widget.markdown_content == markdown

    def test_widget_attributes(self, widget):
        """Test that widget has required anywidget attributes."""

        # Check that required anywidget attributes exist
        assert hasattr(widget, "_esm")
        assert hasattr(widget, "_css")
        assert hasattr(widget, "markdown_content")

        # Check that _esm contains bundled JavaScript content
        esm_content = str(widget._esm)
        assert len(esm_content) > 1000  # Should be substantial bundled content
        assert (
            "function" in esm_content or "var" in esm_content
        )  # Should contain JavaScript

    def test_markdown_content_trait(self, widget):
        """Test that markdown_content trait works correctly."""

        # Test setting markdown content
        test_content = "# New Content\n\nUpdated markdown."
        widget.markdown_content = test_content
        assert widget.markdown_content == test_content

        # Test that it's a traitlets trait
        assert isinstance(widget.markdown_content, str)

    def test_empty_markdown(self):
        """Test widget behavior with empty markdown."""
        widget = MarkmapWidget(markdown_content="")
        assert widget.markdown_content == ""

    def test_complex_markdown(self):
        """Test widget with complex markdown including frontmatter."""
        complex_markdown = """---
markmap:
  color:
    - '#d62728'
    - '#2ca02c'
  maxWidth: 300
---

# Complex Test

## Section 1
- Item 1
- Item 2

## Section 2
![Image](test.png)

### Subsection
`code` and **bold** text
"""
        widget = MarkmapWidget(markdown_content=complex_markdown)
        assert widget.markdown_content == complex_markdown

    def test_special_characters(self):
        """Test widget with special characters in markdown."""
        special_markdown = "# Test with special chars: äöüß\n\n*Emphasis* and `code`"
        widget = MarkmapWidget(markdown_content=special_markdown)
        assert widget.markdown_content == special_markdown

    def test_long_markdown(self):
        """Test widget with very long markdown content."""
        long_content = "# " + "A" * 1000 + "\n\n" + "B" * 1000
        widget = MarkmapWidget(markdown_content=long_content)
        assert widget.markdown_content == long_content
        assert len(widget.markdown_content) > 2000

    def test_widget_repr(self):
        """Test widget string representation."""
        widget = MarkmapWidget(markdown_content="# Test")
        repr_str = repr(widget)
        assert "MarkmapWidget" in repr_str
        assert "markdown_content" in repr_str

    def test_widget_equality(self):
        """Test widget equality comparison."""
        widget1 = MarkmapWidget(markdown_content="# Test")
        widget2 = MarkmapWidget(markdown_content="# Test")
        widget3 = MarkmapWidget(markdown_content="# Different")

        # Widgets with same content should be equal
        assert widget1.markdown_content == widget2.markdown_content
        # Widgets with different content should not be equal
        assert widget1.markdown_content != widget3.markdown_content
