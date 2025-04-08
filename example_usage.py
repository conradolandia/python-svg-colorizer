#!/usr/bin/env python

import sys
from qtpy.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPainter
import qdarkstyle

# Import the colorizer class
from svg_colorizer import SVGColorize

# Create a Qt application
app = QApplication(sys.argv)

# Set the dark style
dark_stylesheet = qdarkstyle.load_stylesheet(qt_api="pyqt5")
app.setStyleSheet(dark_stylesheet)

# Example files to colorize
examples = ["example.svg", "example2.svg"]

# Create a window
window = QWidget()
window.setWindowTitle("SVG Icon Examples")
layout = QVBoxLayout()

for example in examples:
    # Get SVG data using the class method
    svg_data = SVGColorize.colorize_icon(example, "#fafafa", "#44DEB0", "#ff0000")
    if svg_data is None:
        print(f"Could not colorize {example}. Skipping.")
        continue
        
    svg_bytes = QByteArray(svg_data.encode())  # Convert SVG data to bytes

    # Create QPixmap from SVG data
    pixmap = QPixmap(256, 256)  # Specify the size of the icon
    renderer = QSvgRenderer(svg_bytes)
    pixmap.fill(Qt.transparent)  # Fill with transparency
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()  # End painting before creating QIcon

    # Create QIcon from QPixmap
    icon = QIcon(pixmap)

    # Create a button with the icon and filename
    button = QPushButton(example)
    button.setIcon(icon)
    button.setIconSize(pixmap.size())  # Set icon size to match the pixmap size
    layout.addWidget(button)

window.setLayout(layout)
window.show()

# Run the application
sys.exit(app.exec_()) 
