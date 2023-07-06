from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QFileDialog, QProgressBar, QCheckBox
from PyQt5.QtGui import QFont, QIcon
import sys
import os
import json
import logging
from datetime import datetime
import utils

logging.basicConfig(filename='app.log', level=logging.INFO)

OPTIONS = {
    "NUM": ["0"] + [str(i) for i in range(1, 100)],
    "ASPECT_RATIO": ["--ar 16:9", "--ar 4:5", "--ar 1:1", "--ar 3:4", "--ar 4:3", "--ar 5:4", "--ar 3:4", "--ar 4:7", "--ar 7:4", "--ar 2:1", "--ar 1:2", "--ar 3:1", "--ar 1:3", "--ar 9:16"],
    "CHAOS": ["", "--c 0", "--c 5", "--c 10", "--c 20", "--c 25", "--c 35", "--c 40", "--c 50", "--c 60", "--c 75", "--c 90", "--c 95", "--c 100"],
    "STYLIZE": ["", "--s 0", "--s 10", "--s 50", "--s 100", "--s 200", "--s 300", "--s 500", "--s 700", "--s 800", "--s 900", "--s 950", "--s 990", "--s 1000"],
    "TILE": ["--tile", ""],
    "WEIRD": ["--weird " + str(i) for i in [0, 10, 25, 50, 75, 100, 150, 250, 350, 500, 750, 1000, 1250, 1500, 2000, 2500, 3000]]
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")
        self.categories = utils.load_categories("categories.json")
        self.create_widgets()
        self.arrange_widgets()
        self.statusBar().showMessage('Ready')

    def create_combobox(self, options, default=None):
        combobox = QComboBox()
        combobox.addItems(options)
        if default:
            combobox.setCurrentIndex(options.index(default))
        return combobox

    def create_widgets(self):
        self.file_label = QLabel("Number of Files:")
        self.file_selector = self.create_combobox(OPTIONS["NUM"])
        self.category_selectors = {category: (self.create_combobox(OPTIONS["NUM"]), QCheckBox("Range?")) for category in self.categories.keys()}
        self.aspect_ratio_selector = self.create_combobox(OPTIONS["ASPECT_RATIO"], "--ar 16:9")
        self.chaos_selector = self.create_combobox(OPTIONS["CHAOS"], "--c 0")
        self.stylize_selector = self.create_combobox(OPTIONS["STYLIZE"], "--s 100")
        self.tile_selector = self.create_combobox(OPTIONS["TILE"], "")
        self.weird_selector = self.create_combobox(OPTIONS["WEIRD"], "--weird 0")
        self.start_button = QPushButton("Generate Files")
        self.start_button.setStyleSheet("QPushButton { background-color: #2ecc71; font-weight: bold; color: white; } QPushButton:hover { background-color: #27ae60; }")
        self.start_button.setIcon(QIcon('start_icon.png'))
        self.start_button.clicked.connect(self.start_process)
        self.result_box = QTextEdit()
        self.progress_bar = QProgressBar(self)

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
        layout.addWidget(QLabel("Weird:"), row, 0)
        layout.addWidget(self.weird_selector, row, 1)
        row += 1
        layout.addWidget(self.start_button, row, 0, 1, 2)
        layout.addWidget(self.result_box, row+1, 0, 1, 2)
        layout.addWidget(self.progress_bar, row+2, 0, 1, 2)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_process(self):
        num_files = int(self.file_selector.currentText())
        category_counts = {category: (int(selector.currentText()), checkbox.isChecked()) for category, (selector, checkbox) in self.category_selectors.items()}
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        aspect_ratio = self.aspect_ratio_selector.currentText()
        chaos = self.chaos_selector.currentText()
        stylize = self.stylize_selector.currentText()
        tile = self.tile_selector.currentText()
        weird = self.weird_selector.currentText()
        utils.select_items(num_files, category_counts, self.categories, output_dir, self.progress_bar, aspect_ratio, chaos, stylize, tile, weird)
        self.statusBar().showMessage('Files generated successfully')

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
