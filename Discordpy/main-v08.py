# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout
from random import choice, shuffle
import sys
import os
import json
import logging

# CB: 1.1 - Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# CB: 2.0 - Define utility functions
def load_categories(file):
    # CB: 2.1 - Load categories from JSON file
    try:
        with open(file, 'r') as f:
            categories = json.load(f)
        return categories
    except FileNotFoundError:
        logging.error(f"File not found: {file}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from file: {file}. Error: {e}")
        return {}

def generate_parameters(num_items):
    # CB: 2.2 - Function to generate parameters with specified odds
    parameters = [1, 2, 3, 4] * (num_items // 4) + [1, 2, 3, 4][:num_items % 4]
    shuffle(parameters)
    parameters[0] = 1  # Ensure at least one ::1
    if num_items > 4:
        parameters[-1] = 5  # Ensure at least one ::5
    shuffle(parameters)
    return parameters

# CB: 2.3 - Define item selection and file writing function
def select_items(num_files, category_counts, categories):
    os.makedirs("output", exist_ok=True)
    for i in range(num_files):
        try:
            with open(f"output/Prompt_{i+1:02d}.txt", "w") as file:
                file.write("/imagine\n")
                for category, count in category_counts.items():
                    if count > 0:  # Only generate items if count is greater than 0
                        parameters = generate_parameters(count)
                        for _ in range(count):
                            item = choice(categories[category])
                            parameter = parameters[_]
                            file.write(f"{item} ::{parameter}\n")
                file.write("--v 5.1\n")
        except Exception as e:
            logging.error(f"Failed to write file: {e}")

# CB: 3.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")
        self.categories = load_categories("categories.json")
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
        self.file_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10
        self.category_selectors = {}
        for category in self.categories.keys():
            self.category_selectors[category] = QComboBox()
            self.category_selectors[category].addItems([str(i) for i in range(0, 11)])  # Add options 0-10
        self.start_button = QPushButton("Generate Files")
        self.start_button.setStyleSheet("QPushButton{ background-color: #2ecc71; font-weight: bold; color: white; } QPushButton:hover { background-color: #27ae60; }")
        self.start_button.clicked.connect(self.start_process)  # Connect button click to start_process function
        self.result_box = QTextEdit()

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
        # CB: 3.6 - Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 3.7 - Define start_process function
    def start_process(self):
        num_files = int(self.file_selector.currentText())
        category_counts = {category: int(selector.currentText()) for category, selector in self.category_selectors.items()}
        select_items(num_files, category_counts, self.categories)
        self.statusBar().showMessage('Files generated successfully')

# CB: 4.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 5.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())
