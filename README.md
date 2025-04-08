# SVG Colorizer

A Python utility for dynamically colorizing SVG icons by targeting elements with specific class attributes.

## Overview

SVG Colorizer allows you to modify SVG files by changing the fill colors of elements with specific class attributes. This is particularly useful for theming UI elements in applications where you need to dynamically change icon colors based on the application theme or user preferences.

The implementation uses `lxml` for XML parsing and XPath for element selection, providing a reliable and maintainable way to manipulate SVG files.

## Requirements

- Python 3.6+
- lxml
- For the demo:
  - PyQt5 / PySide2 (via qtpy)
  - qdarkstyle

## Installation

```bash
# Install required packages
pip install lxml qtpy PyQt5 qdarkstyle
```

## Usage

### Basic Usage - Instance Method

If you need more control or want to perform multiple operations on the same SVG:

```python
from svg_colorizer import SVGColorize

# Create an instance
icon_colorizer = SVGColorize("path/to/icon.svg")

# Apply colors
icon_colorizer.change_fill_color_by_class("primary", "#ff0000")
icon_colorizer.change_fill_color_by_class("secondary", "#00ff00")

# Get the SVG string or save to file
svg_string = icon_colorizer.save_to_string()
# or
# icon_colorizer.save_to_file("output.svg")
```

### Basic Usage - Class Method (Convenience)

For quick, one-line colorization:

```python
from svg_colorizer import SVGColorize

# Colorize an SVG icon using the class method
svg_string = SVGColorize.colorize_icon(
    icon_path="path/to/icon.svg",
    color_primary="#ff0000",      # Red for elements with class="primary"
    color_secondary="#00ff00",    # Green for elements with class="secondary"
    color_tertiary="#0000ff"      # Blue for elements with class="tertiary"
)

# Now you can use the svg_string in your application
```

### Using with Qt

```python
from svg_colorizer import SVGColorize
from qtpy.QtWidgets import QApplication, QPushButton
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPainter

# Colorize the SVG using the class method
svg_data = SVGColorize.colorize_icon("icon.svg", "#fafafa", "#44DEB0", "#ff0000")

# Convert to QIcon
svg_bytes = QByteArray(svg_data.encode())
pixmap = QPixmap(256, 256)
renderer = QSvgRenderer(svg_bytes)
pixmap.fill(Qt.transparent)
painter = QPainter(pixmap)
renderer.render(painter)
painter.end()
icon = QIcon(pixmap)

# Use in a button
button = QPushButton()
button.setIcon(icon)
button.setIconSize(pixmap.size())
```

## SVG File Requirements

For SVG Colorizer to work properly, your SVG files should have class attributes on the elements you want to colorize, and no `fill` attributes:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24">
  <path class="primary" d="M4 6h16v4.982h2V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h6v-2H4Z"/>
  <path class="secondary" d="M19.714 13.033h-1.428v7h1.428zm3 0h-1.428v7h1.428z"/>
  <path class="tertiary" d="M11.881 13.033l5.238 3.5-5.238 3.5z"/>
</svg>
```

## API Reference

### `SVGColorize` Class

A class for modifying SVG files by changing the fill colors of elements with specific class attributes.

#### Instance Methods

-   `__init__(svg_path)`: Initialize with the path to an SVG file.
-   `change_fill_color_by_class(class_name, new_color)`: Change the fill color of all elements with the specified class.
-   `colorize(color_primary, color_secondary="", color_tertiary="")`: Apply colors to primary, secondary, and tertiary classes and return the SVG as a string.
-   `save_to_string()`: Convert the modified SVG to a string.
-   `save_to_file(output_path)`: Save the modified SVG to a file.

#### Class Method

-   `colorize_icon(icon_path, color_primary, color_secondary="", color_tertiary="")`: A convenience method to load an SVG, apply colors, and return the SVG string in one call.

## Examples

The repository includes example SVG files that you can use to test the colorizer:

- `example.svg`: An SVG with primary and secondary class elements
- `example2.svg`: An SVG with primary and tertiary class elements

A Qt-based visual demo is available in `example_usage.py`.

To run the demo:

```bash
python example_usage.py
```

## Integration with Spyder

This utility is a work in progress designed to be integrated with [Spyder IDE](https://www.spyder-ide.org) for theme-based icon colorization. It is the first in several steps to create full color theme support at the UI level for our beloved Python IDE.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
