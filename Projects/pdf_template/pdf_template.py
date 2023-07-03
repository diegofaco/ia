# CB: 1.1 - Import necessary libraries
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tableofcontents import SimpleIndex
from reportlab.platypus.flowables import DocAssign, DocExec, DocPara, DocIf, DocWhile

# CB: 2.1 - Define PDFGenerator class
class PDFGenerator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.styles = getSampleStyleSheet()
        self.elements = []
        self.current_letter = 'a'
        self.previous_instruction = None

    # CB: 3.1 - Method to apply formatting
    def apply_formatting(self, instruction, text):
        if instruction == '1':  # Cover
            return Paragraph(text, self.styles['Title'])
        elif instruction == '2':  # Heading 1
            return Paragraph(text, self.styles['Heading1'], bulletText='1')
        elif instruction == '3':  # Heading 2
            return Paragraph(text, self.styles['Heading2'], bulletText='2')
        elif instruction == '4':  # Heading 3
            return Paragraph(text, self.styles['Heading3'], bulletText='3')
        elif instruction == '5':  # Body Text
            return Paragraph(text, self.styles['BodyText'])
        elif instruction == '6':  # Numbered List
            if self.previous_instruction != '6':
                self.current_letter = 'a'  # Reset the current letter whenever we start a new list
            element = Paragraph(f'({self.current_letter}) {text}', self.styles['BodyText'])
            self.current_letter = chr(ord(self.current_letter) + 1)  # Move to the next letter
            return element
        elif instruction == '7':  # Bullet Point List
            return Paragraph(f'• {text}', self.styles['BodyText'])
        elif instruction == '8':  # Blank Line
            return Spacer(1, 12)
        elif instruction == 'P':  # Page Break
            return PageBreak()
        else:
            print(f"Unknown formatting instruction: {instruction}")
            return None  # Ignore lines with unknown formatting instructions
        finally:
            self.previous_instruction = instruction

    # CB: 4.1 - Method to generate PDF
    def generate_pdf(self):
        with open(self.input_file, 'r') as file:
            for line in file:
                instruction = line[0]
                text = line[1:].strip()
                element = self.apply_formatting(instruction, text)
                if element is not None:
                    self.elements.append(element)
        doc = SimpleDocTemplate(self.output_file, pagesize=A4, rightMargin=2.85*cm, leftMargin=3.2*cm, topMargin=3.3*cm, bottomMargin=2*cm)
        doc.multiBuild(self.elements, canvasmaker=NumberedCanvas)

# CB: 5.1 - Define NumberedCanvas class
class NumberedCanvas(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self._
