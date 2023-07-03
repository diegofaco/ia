# CB: 3.1 - Import necessary libraries
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# CB: 3.2 - Define PDFGenerator class
class PDFGenerator:
    def __init__(self, input_file, output_file, header_image):
        self.input_file = input_file
        self.output_file = output_file
        self.header_image = header_image
        self.doc = SimpleDocTemplate(self.output_file, pagesize=A4)
        self.styles = getSampleStyleSheet()

    # CB: 3.3 - Method to read file
    def read_file(self):
        with open(self.input_file, 'r', encoding='utf-8-sig') as file:
            return file.readlines()

    # CB: 3.4 - Method to interpret formatting
    def interpret_formatting(self, line):
        return line[0], line[1:].strip()

    # CB: 3.5 - Method to apply formatting
    def apply_formatting(self, instruction, text):
        if instruction == '2':  # Heading 1
            return Paragraph(text, self.styles['Heading1'])
        elif instruction == '3':  # Heading 2
            return Paragraph(text, self.styles['Heading2'])
        elif instruction == '4':  # Heading 3
            return Paragraph(text, self.styles['Heading3'])
        elif instruction == '5':  # Body Text
            return Paragraph(text, self.styles['BodyText'])
        elif instruction == '6':  # Numbered List
            return Paragraph('<seq id="numbered">. ' + text, self.styles['BodyText'])
        elif instruction == '7':  # Bullet Point List
            return Paragraph('• ' + text, self.styles['Bullet'])
        elif instruction == '8':  # Blank Line
            return Spacer(1, 12)  # 12 points of space
        else:
            print(f"Unknown formatting instruction: {instruction}")
            return None

    # CB: 3.6 - Method to generate PDF
    def generate_pdf(self):
        lines = self.read_file()
        elements = []
        for line in lines:
            instruction, text = self.interpret_formatting(line)
            element = self.apply_formatting(instruction, text)
            if element:
                elements.append(element)
        self.doc.build(elements)

# CB: 3.7 - Test PDFGenerator
pdf_generator = PDFGenerator('data.txt', 'output.pdf', 'header.jpg')
pdf_generator.generate_pdf()
