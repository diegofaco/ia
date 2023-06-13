# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QFileDialog, QProgressBar, QToolTip
from PyQt5.QtGui import QFont  # Add this line
from random import choice, shuffle
import sys
import os
import json
import logging
from datetime import datetime
import utils  # Import the new utils module

# CB: 1.1 - Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# CB: 3.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")
        self.categories = utils.load_categories("categories.json")  # Use the function from the utils module
        # CB: 3.1 - Create widgets
        self.create_widgets()
        # CB: 3.2 - Arrange widgets in a grid layout
        self.arrange_widgets()
        # CB: 3.3 - Add a status bar
        self.statusBar().showMessage('Ready')

    # CB: 3.4 - Create widgets
    def create_widgets(self):
        QToolTip.setFont(QFont('SansSerif', 10))  # Set the font for tooltips
        self.file_label = QLabel("Number of Files:")
        self.file_label.setToolTip('Select the number of files to generate.')  # Add a tooltip
        self.file_selector = QComboBox()
        self.file_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10
        self.file_selector.setToolTip('Select the number of files to generate.')  # Add a tooltip
        self.category_selectors = {}
        for category in self.categories.keys():
            self.category_selectors[category] = QComboBox()
            self.category_selectors[category].addItems([str(i) for i in range(0, 11)])  # Add options 0-10
            self.category_selectors[category].setToolTip(f'Select the number of {category} items to generate.')  # Add a tooltip
        self.start_button = QPushButton("Generate Files")
        self.start_button.setStyleSheet("QPushButton { background-color: #2ecc71; font-weight: bold; color: white; } QPushButton:hover { background-color: #27ae60; }")
        self.start_button.clicked.connect(self.start_process)  # Connect button click to start_process function
        self.start_button.setToolTip('Click to start the file generation process.')  # Add a tooltip
        self.result_box = QTextEdit()
        self.result_box.setToolTip('The results of the file generation process will be displayed here.')  # Add a tooltip
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setToolTip('Shows the progress of the file generation process.')  # Add a tooltip

    # CB: 3.5 - Arrange widgets in a grid layout
    def arrange_widgets(self):
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.file_label, 0, 0)
        layout.addWidget(self.file_selector, 0, 1)
        row = 1
        for category, selector in self.category_selectors.items():
            layout.addWidget(QLabel(f"{category} Items:"), row, 0)
            layout.addWidget(selector, row, 1)
            row += 1
        layout.addWidget(self.start_button, row, 0, 1, 2)
        layout.addWidget(self.result_box, row+1, 0, 1, 2)
        layout.addWidget(self.progress_bar, row+2, 0, 1, 2)  # Add the progress bar to the layout
        # CB: 3.6 - Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 3.7 - Define start_process function
    def start_process(self):
        num_files = int(self.file_selector.currentText())
        category_counts = {category: int(selector.currentText()) for category, selector in self.category_selectors.items()}
        output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')  # Let the user select the output directory
        utils.select_items(num_files, category_counts, self.categories, output_dir, self.progress_bar)  # Pass the output directory and progress bar to the function
        self.statusBar().showMessage('Files generated successfully')

# CB: 4.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 5.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())
