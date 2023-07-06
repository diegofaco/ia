# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QFileDialog, QProgressBar, QCheckBox
from PyQt5.QtGui import QFont, QIcon
from random import choice, shuffle, randint
import sys
import os
import json
import logging
from datetime import datetime
import utils

# CB: 1.1 - Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# CB: 1.2 - Define constants
NUM_OPTIONS = ["0"] + [str(i) for i in range(1, 100)]  # Max files set to 99
ASPECT_RATIO_OPTIONS = ["--ar 16:9", "--ar 4:5", "--ar 1:1", "--ar 3:4", "--ar 4:3", "--ar 5:4", "--ar 3:4", "--ar 4:7", "--ar 7:4", "--ar 2:1", "--ar 1:2", "--ar 3:1", "--ar 1:3", "--ar 9:16"]
CHAOS_OPTIONS = ["--c 0", "--c 5", "--c 10", "--c 20", "--c 25", "--c 35", "--c 40", "--c 50", "--c 60", "--c 75", "--c 90", "--c 95", "--c 100"]
STYLIZE_OPTIONS = ["--s 0", "--s 10", "--s 50", "--s 100", "--s 200", "--s 300", "--s 500", "--s 700", "--s 800", "--s 900", "--s 950", "--s 990", "--s 1000"]
TILE_OPTIONS = ["--tile", ""]
WEIRD_OPTIONS = ["--weird " + str(i) for i in [0, 10, 25, 50, 75, 100, 150, 250, 350, 500, 750, 1000, 1500, 2000, 2500, 3000]]

# CB: 3.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")
        self.categories = utils.load_categories("categories.json")

        # CB: 3.1 - Create widgets
        self.create_widgets()

        # CB: 3.2 - Arrange widgets in a grid layout
        self.arrange_widgets()

        # CB: 3.3 - Add a status bar
        self.statusBar().showMessage('Ready')

    # CB: 3.4 - Create widgets
    def create_widgets(self):
        self.file_label = QLabel("Number of Files:")
        self.file_selector = QComboBox()
        self.file_selector.addItems(NUM_OPTIONS)
        self.category_selectors = {category: (QComboBox(), QCheckBox("Range?")) for category in self.categories.keys()}
        for selector, _ in self.category_selectors.values():
            selector.addItems(NUM_OPTIONS)
        self.aspect_ratio_selector = QComboBox()
        self.aspect_ratio_selector.addItems(ASPECT_RATIO_OPTIONS)
        self.aspect_ratio_selector.setCurrentIndex(ASPECT_RATIO_OPTIONS.index("--ar 16:9"))  # Set default value
        self.chaos_selector = QComboBox()
        self.chaos_selector.addItems(CHAOS_OPTIONS)
        self.chaos_selector.setCurrentIndex(CHAOS_OPTIONS.index("--c 0"))  # Set default value
        self.stylize_selector = QComboBox()
        self.stylize_selector.addItems(STYLIZE_OPTIONS)
        self.stylize_selector.setCurrentIndex(STYLIZE_OPTIONS.index("--s 100"))  # Set default value
        self.tile_selector = QComboBox()
        self.tile_selector.addItems(TILE_OPTIONS)
        self.tile_selector.setCurrentIndex(TILE_OPTIONS.index(""))  # Set default value
        self.start_button = QPushButton("Generate Files")
        self.start_button.setStyleSheet("QPushButton { background-color: #2ecc71; font-weight: bold; color: white; } QPushButton:hover { background-color: #27ae60; }")
        self.start_button.setIcon(QIcon('start_icon.png'))  # Add icon to the start button
        self.start_button.clicked.connect(self.start_process)
        self.result_box = QTextEdit()
        self.progress_bar = QProgressBar(self)
        self.category_selectors["weird"] = (QComboBox(), QCheckBox("Range?"))
        self.category_selectors["weird"][0].addItems(WEIRD_OPTIONS)

    # CB: 3.5 - Arrange widgets in a grid layout
    def arrange_widgets(self):
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.file_label, 0, 0)
        layout.addWidget(self.file_selector, 0, 1)
        row = 1
        for category, (selector, checkbox) in self.category_selectors.items():
            layout.addWidget(QLabel(f"{category} Items:"), row, 0)
            layout.addWidget(selector, row, 1)
            layout.addWidget(checkbox, row, 2)
            row += 1
        layout.addWidget(QLabel("Aspect Ratio:"), row, 0)
        layout.addWidget(self.aspect_ratio_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Chaos:"), row, 0)
        layout.addWidget(self.chaos_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Stylize:"), row, 0)
        layout.addWidget(self.stylize_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Tile:"), row, 0)
        layout.addWidget(self.tile_selector, row, 1)
        row += 1
        layout.addWidget(self.start_button, row, 0, 1, 2)
        layout.addWidget(self.result_box, row+1, 0, 1, 2)
        layout.addWidget(self.progress_bar, row+2, 0, 1, 2)

        # CB: 3.6 - Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 3.7 - Define start_process function
    def start_process(self):
        num_files = int(self.file_selector.currentText())
        category_counts = {category: (int(selector.currentText()), checkbox.isChecked()) for category, (selector, checkbox) in self.category_selectors.items()}
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        aspect_ratio = self.aspect_ratio_selector.currentText()
        chaos = self.chaos_selector.currentText()
        stylize = self.stylize_selector.currentText()
        tile = self.tile_selector.currentText()
        utils.select_items(num_files, category_counts, self.categories, output_dir, self.progress_bar, aspect_ratio, chaos, stylize, tile)
        self.statusBar().showMessage('Files generated successfully')

# CB: 4.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 5.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())