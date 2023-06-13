# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
import sys

# CB: 2.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")

        # CB: 2.1 - Create widgets
        self.file_selector = QComboBox()
        self.file_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.item_selector = QComboBox()
        self.item_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)  # Connect button click to start_process function

        self.result_box = QTextEdit()

        # CB: 2.2 - Arrange widgets in a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_selector)
        layout.addWidget(self.item_selector)
        layout.addWidget(self.start_button)
        layout.addWidget(self.result_box)

        # CB: 2.3 - Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 2.4 - Define start_process function
    def start_process(self):
        num_files = self.file_selector.currentText()
        num_items = self.item_selector.currentText()
        print(f"Number of files: {num_files}, Number of items: {num_items}")

# CB: 3.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 4.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())