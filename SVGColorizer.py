#!/usr/bin/env python

# This probably should be implemented in
# spyder/utils/icon_manager.py

import re
from qtpy.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtCore import QByteArray, Qt, QSize
from PyQt5.QtGui import QPainter
import qdarkstyle
import sys


class SVGColorize:
    """
    Class for colorizing SVG icons using class-based targeting.
    This class uses regex-based string manipulation which is more reliable
    than DOM-based manipulation for this specific use case.
    """
    def __init__(self, svg_path):
        """Initialize with the path to an SVG file."""
        try:
            with open(svg_path, 'r') as f:
                self.svg_content = f.read()
        except Exception as e:
            print(f"Error reading SVG file: {e}")
            self.svg_content = None

    def change_fill_color_by_class(self, class_name, new_color):
        """Change the fill color of all elements with the specified class."""
        if self.svg_content is None:
            return
        
        # Find elements with the specified class
        class_pattern = f'class="{class_name}"'
        if class_pattern in self.svg_content:
            # Replace fill attribute if it exists
            pattern_fill = f'(class="{class_name}"[^>]*?)(fill="[^"]*?)(")'
            if re.search(pattern_fill, self.svg_content):
                self.svg_content = re.sub(pattern_fill, f'\\1fill="{new_color}"\\3', self.svg_content)
            # Add fill attribute if it doesn't exist
            else:
                pattern_add = f'(class="{class_name}")'
                self.svg_content = re.sub(pattern_add, f'\\1 fill="{new_color}"', self.svg_content)
                
            # Remove any additional fill="none" that might be present elsewhere in the element
            pattern_none = f'(<[^>]*class="{class_name}"[^>]*?)fill="none"([^>]*?>)'
            self.svg_content = re.sub(pattern_none, '\\1\\2', self.svg_content)

    def save_to_string(self):
        """Return the colorized SVG as a string."""
        if self.svg_content is None:
            return None
        return self.svg_content

    def save_to_file(self, output_path):
        """Save the colorized SVG to a file."""
        if self.svg_content is None or output_path is None:
            return
        with open(output_path, 'w') as f:
            f.write(self.save_to_string())


def colorize_icon(
    icon_name: str,
    color_primary: str,
    color_secondary: str = "",
    color_tertiary: str = "",
):
    """
    Colorize an SVG icon by replacing fill colors for elements with specific classes.
    
    Args:
        icon_name: Path to the SVG file
        color_primary: Color to apply to elements with class="primary"
        color_secondary: Color to apply to elements with class="secondary"
        color_tertiary: Color to apply to elements with class="tertiary"
        
    Returns:
        The colorized SVG as a string, or None if there was an error
    """
    icon = SVGColorize(icon_name)
    icon.change_fill_color_by_class("primary", color_primary)

    if color_secondary:
        icon.change_fill_color_by_class("secondary", color_secondary)

    if color_tertiary:
        icon.change_fill_color_by_class("tertiary", color_tertiary)

    return icon.save_to_string()


# Test function
def test_icon_colorization():
    """Test the SVG colorization with a visual demo."""
    # Create a Qt application
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    # Create a window
    window = QWidget()
    window.setWindowTitle("SVG Colorizer Test")
    layout = QVBoxLayout()
    
    # Create a horizontal layout for the icons
    icons_layout = QHBoxLayout()
    
    # Test both example files
    for file_name in ["example.svg", "example2.svg"]:
        # Create a layout for this example
        example_layout = QVBoxLayout()
        
        # Add a label for the file name
        label = QLabel(file_name)
        label.setAlignment(Qt.AlignCenter)
        example_layout.addWidget(label)
        
        # Get SVG data
        svg_data = colorize_icon(file_name, "#ff0000", "#00ff00", "#0000ff")
        
        if svg_data:
            # Convert SVG data to bytes
            svg_bytes = QByteArray(svg_data.encode())
            
            # Create renderer and pixmap
            renderer = QSvgRenderer(svg_bytes)
            pixmap = QPixmap(128, 128)
            pixmap.fill(Qt.transparent)
            
            # Render SVG to pixmap
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            
            # Create icon and button
            button = QPushButton()
            button.setFixedSize(150, 150)
            button.setIconSize(QSize(128, 128))
            button.setIcon(QIcon(pixmap))
            example_layout.addWidget(button)
        else:
            error_label = QLabel("Failed to load icon")
            error_label.setStyleSheet("color: red")
            example_layout.addWidget(error_label)
        
        # Add this example to the icons layout
        icons_layout.addLayout(example_layout)
    
    layout.addLayout(icons_layout)
    window.setLayout(layout)
    window.show()
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_icon_colorization()
