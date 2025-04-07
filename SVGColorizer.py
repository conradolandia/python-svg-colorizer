#!/usr/bin/env python

# This probably should be implemented in
# spyder/utils/icon_manager.py

from lxml import etree
from qtpy.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPainter
import qdarkstyle


# Methods for colorization.
class SVGColorize:
    def __init__(self, svg_path):
        try:
            self.tree = etree.parse(svg_path)
            self.root = self.tree.getroot()
        except etree.XMLSyntaxError as e:
            print(f"Error parsing SVG file: {e}")
            self.tree = None
            self.root = None

    def change_fill_color_by_class(self, class_name, new_color):
        if self.root is None:
            print("No SVG data to modify.")
            return
        ns = {"svg": "http://www.w3.org/2000/svg"}
        elements = self.root.xpath(f"//svg:*[@class='{class_name}']", namespaces=ns)
        for element in elements:
            element.attrib["fill"] = new_color

    def save_to_string(self):
        if self.root is None:
            print("No SVG data to save.")
            return None
        return etree.tostring(self.root).decode()

    def save_to_file(self, output_path):
        if self.tree is None:
            print("No SVG data to save.")
            return
        if output_path is None:
            print("Empty path.")
            return
        self.tree.write(output_path, pretty_print=True)


# Colorize an icon taking the name and a set of colors.
# Only the name and the primary color are mandatory.
# Returns a string with the unformatted SVG markup.

def colorize_icon(
    icon_name: str,
    color_primary: str,
    color_secondary: str = "",
    color_tertiary: str = "",
):
    icon = SVGColorize(icon_name)
    icon.change_fill_color_by_class("primary", color_primary)

    if color_secondary:
        icon.change_fill_color_by_class("secondary", color_secondary)

    if color_tertiary:
        icon.change_fill_color_by_class("tertiary", color_tertiary)

    svg_string = icon.save_to_string()
    return svg_string


# usage example

# Create a Qt application
app = QApplication([])

# Set the dark style
dark_stylesheet = qdarkstyle.load_stylesheet(qt_api='pyqt5')
app.setStyleSheet(dark_stylesheet)

# Create a window
window = QWidget()
layout = QVBoxLayout()

# Get SVG data from colorize_icon
svg_data = colorize_icon("example.svg", "#fafafa", "#44DEB0", "#ff0000")
svg_bytes = QByteArray(svg_data.encode())  # Convert SVG data to bytes

# Create QPixmap from SVG data
pixmap = QPixmap(256, 256)  # Specify the size of the icon
renderer = QSvgRenderer(svg_bytes)
pixmap.fill(Qt.transparent)  # Fill with transparency
painter = QPainter(pixmap)
renderer.render(painter)

# Create QIcon from QPixmap
icon = QIcon(pixmap)

# Create a button with the icon
button = QPushButton()
button.setIcon(icon)
button.setIconSize(pixmap.size())  # Set icon size to match the pixmap size
layout.addWidget(button)

window.setLayout(layout)
window.show()

# Run the application
app.exec_()
