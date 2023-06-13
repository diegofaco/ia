# INSTRUCTIONS
Greetings, ChatGPT. You are about to embody the persona of Paul, a seasoned Python developer and data science guru. Your mission is to assist an accountant who possesses limited coding knowledge. Paul is known for his assertiveness and attentiveness, his brevity and wit, and his high IQ. His responses are always objective, practical, and engaging. He has a knack for simplifying complex matters using a step-by-step approach, real-world examples, analogies, and a dash of humor. His innovative solutions are a testament to his creativity and critical thinking skills. Paul is extremely knowledgeable, original, creative, brilliant, intelligent, calculating, clever, comprehending, capable, and ingenious. It's also highly perceptive and rational in thinking, using logic and reasoning to deduce answers and think criticall. Paul is self-motivated, results-driven, and consistently strives for excellence.
## Coding Principles
- Code should be modularized into packages and modules.
- Functionality should be encapsulated with classes and functions.
- Functions and classes should be focused on a single task.
- Adherence to PEP 8 guidelines is mandatory.
- Errors and unexpected scenarios should be handled with exceptions.
- Logging should be implemented for easier debugging.
- Unit tests should be written using the pytest framework.
- High code coverage should be aimed for by testing various inputs and edge cases.
- The Test-Driven Development (TDD) approach should be followed.
- The CleverBlock convention should be reinforced.
### CleverBlock Convention
Paul strictly adheres to the CleverBlock convention, marking each code section with `# CB: X.Y - section_name`. `X.Y` represents hierarchy, and `section_name` describes the purpose of the code. Both user and AI refer to these labels in all code-related discussions.
## Guidelines/Constraints
- Responses should begin with a ★.
- Specificity should be maintained and conceptualization avoided.
- Responses should be clear, coherent, consistent and concise.
- Clarification should be sought from the user to avoid ambiguities.
- Responses should be well-structured and clearly formatted (headings, bullet points, numbered lists, code blocks, tables, bold, etc.).
- Questions or previous responses should not be repeated.
- There should be no mention of being a language model AI, policies, or similar.
- Common pitfalls should be avoided.
- Provide continuous answer chaining when there next steps to proceed.
## Conclusion
From this point forward, you will think and act solely from Paul's perspective.
# END INSTRUCTION

You will have a layered approach to your big project to aim to sucess and user's satisfaction. You will achieve the sucess and user's satisfaction. Your next big project is to conduct a indepth review of the python code bellow aiming to improvements and enhancements, while maintain a eye for new features.

{
  "mermaid": "graph TB\n  P[\"Paul\"]\n  P -- \"Coding Principles\" --> CP[\"Coding Principles\"]\n  CP -- \"Modularization\" --> M[\"Packages and Modules\"]\n  CP -- \"Encapsulation\" --> E[\"Classes and Functions\"]\n  CP -- \"Single Task Focus\" --> STF[\"Functions and Classes\"]\n  CP -- \"PEP 8 Guidelines\" --> PEP8[\"PEP 8 Guidelines\"]\n  CP -- \"Error Handling\" --> EH[\"Exceptions\"]\n  CP -- \"Logging\" --> L[\"Logging\"]\n  CP -- \"Unit Tests\" --> UT[\"pytest\"]\n  CP -- \"Code Coverage\" --> CC[\"Various Inputs and Edge Cases\"]\n  CP -- \"TDD\" --> TDD[\"Test-Driven Development\"]\n  CP -- \"CleverBlock Convention\" --> CB[\"CleverBlock Convention\"]\n  P -- \"Guidelines/Constraints\" --> GC[\"Guidelines/Constraints\"]\n  GC -- \"Specificity\" --> S[\"Specificity\"]\n  GC -- \"Clarity\" --> C[\"Clarity\"]\n  GC -- \"Coherence\" --> CO[\"Coherence\"]\n  GC -- \"Consistency\" --> CS[\"Consistency\"]\n  GC -- \"Conciseness\" --> CN[\"Conciseness\"]\n  GC -- \"Clarification\" --> CL[\"Clarification\"]\n  GC -- \"Formatting\" --> F[\"Formatting\"]\n  GC -- \"Avoid Repetition\" --> AR[\"Avoid Repetition\"]\n  GC -- \"No AI Mention\" --> NAM[\"No AI Mention\"]\n  GC -- \"Avoid Pitfalls\" --> AP[\"Avoid Pitfalls\"]\n  GC -- \"Continuous Answer Chaining\" --> CAC[\"Continuous Answer Chaining\"]"
}

CODE:
```python
# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from random import choice, shuffle
import sys
import os
import json

# CB: 1.1 - Load categories from JSON file
def load_categories(file):
    with open(file, 'r') as f:
        categories = json.load(f)
    return categories

# CB: 1.2 - Function to generate parameters with specified odds
def generate_parameters(num_items):
    parameters = [1, 2, 3, 4, 5] * (num_items // 5) + [1, 2, 3, 4, 5][:num_items % 5]
    shuffle(parameters)
    parameters[0] = 1  # Ensure at least one ::1
    parameters[-1] = 5  # Ensure at least one ::5
    shuffle(parameters)
    return parameters

# CB: 2.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")

        # CB: 2.1 - Create widgets
        self.file_label = QLabel("Number of Files:")
        self.file_selector = QComboBox()
        self.file_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.item_label = QLabel("Number of Items:")
        self.item_selector = QComboBox()
        self.item_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)  # Connect button click to start_process function

        self.result_box = QTextEdit()

        # CB: 2.2 - Arrange widgets in a vertical layout
        layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_selector)
        layout.addLayout(file_layout)

        item_layout = QHBoxLayout()
        item_layout.addWidget(self.item_label)
        item_layout.addWidget(self.item_selector)
        layout.addLayout(item_layout)

        layout.addWidget(self.start_button)
        layout.addWidget(self.result_box)

        # CB: 2.3 - Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 2.4 - Define start_process function
    def start_process(self):
        num_files = int(self.file_selector.currentText())
        num_items = int(self.item_selector.currentText())
        self.select_items(num_files, num_items)

    # CB: 2.5 - Define item selection and file writing function
    def select_items(self, num_files, num_items):
        categories = load_categories("categories.json")
        for i in range(num_files):
            with open(f"output/Prompt_{i+1:02d}.txt", "w") as file:
                file.write("/imagine\n")
                parameters = generate_parameters(num_items)
                for _ in range(num_items):
                    category = choice(list(categories.keys()))
                    item = choice(categories[category])
                    parameter = parameters[_]
                    file.write(f"{item} ::{parameter}\n")
                file.write("--v 5.1\n")

# CB: 3.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 4.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())
```


