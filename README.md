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

### Basic Usage

```python
from SVGColorizer import colorize_icon

# Colorize an SVG icon
svg_string = colorize_icon(
    icon_name="path/to/icon.svg",
    color_primary="#ff0000",      # Red for elements with class="primary"
    color_secondary="#00ff00",    # Green for elements with class="secondary"
    color_tertiary="#0000ff"      # Blue for elements with class="tertiary"
)

# Now you can use the svg_string in your application
```

### Using with Qt

```python
from SVGColorizer import colorize_icon
from qtpy.QtWidgets import QApplication, QPushButton
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPainter

# Colorize the SVG
svg_data = colorize_icon("icon.svg", "#fafafa", "#44DEB0", "#ff0000")

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

For SVG Colorizer to work properly, your SVG files should have class attributes on the elements you want to colorize:

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

#### Methods

- `__init__(svg_path)`: Initialize with the path to an SVG file
- `change_fill_color_by_class(class_name, new_color)`: Change the fill color of all elements with the specified class
- `save_to_string()`: Convert the modified SVG to a string
- `save_to_file(output_path)`: Save the modified SVG to a file

### `colorize_icon` Function

```python
def colorize_icon(
    icon_name: str,
    color_primary: str,
    color_secondary: str = "",
    color_tertiary: str = "",
):
    """
    Colorize an SVG icon by replacing fill colors for elements with specific classes.
    
    Parameters
    ----------
    icon_name : str
        Path to the SVG file
    color_primary : str
        Color to apply to elements with class="primary"
    color_secondary : str, optional
        Color to apply to elements with class="secondary"
    color_tertiary : str, optional
        Color to apply to elements with class="tertiary"
        
    Returns
    -------
    str or None
        The colorized SVG as a string, or None if there was an error
    """
```

## Examples

The repository includes example SVG files that you can use to test the colorizer:

- `example.svg`: An SVG with primary and secondary class elements
- `example2.svg`: An SVG with primary and tertiary class elements

To run the demo:

```bash
python SVGColorizer.py
```

## Integration with Spyder

This utility is a work in progress designed to be integrated with [Spyder IDE](https://www.spyder-ide.org) for theme-based icon colorization. It is the first in several steps to create full color theme support at the UI level for our beloved Python IDE.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
