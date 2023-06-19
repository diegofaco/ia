# CB: 1.0 - Import necessary libraries
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import datetime
import logging

# CB: 2.0 - Set up logging
logging.basicConfig(filename='pdf_template.log', level=logging.INFO)

# CB: 3.0 - Define the Report class
class Report:
    def __init__(self, style_config=None):
        self.styles = getSampleStyleSheet()
        self.style_config = style_config if style_config else {}
        self.elements = []

    # CB: 3.1 - Define functions for creating each element
    def create_element(self, element_type, content):
        try:
            if element_type == "header":
                return Paragraph(content, self.styles['Heading1'])
            elif element_type == "footer":
                return Paragraph(content, self.styles['Footer'])
            elif element_type == "heading":
                return Paragraph(content, self.styles['Heading2'])
            elif element_type == "subheading":
                return Paragraph(content, self.styles['Heading3'])
            elif element_type == "body_text":
                return Paragraph(content, self.styles['BodyText'])
            elif element_type == "bullet_points":
                return [Paragraph(bullet, self.styles['CustomBullet']) for bullet in content]
            elif element_type == "image":
                return Image(content, width=200)
            elif element_type == "table":
                return self.create_table(content)
            else:
                logging.error(f"Unknown element type: {element_type}")
                return None
        except Exception as e:
            logging.error(f"Error creating {element_type}: {e}")
            return None

    def create_table(self, table_data):
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table = Table(table_data)
        table.setStyle(style)
        return table

    # CB: 3.2 - Define the function to create the PDF
    def create_pdf(self, report):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        filename = f"report_{timestamp}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)

        # CB: 3.2.1 - Apply style configuration
        for style_name, attributes in self.style_config.items():
            if style_name in self.styles:
                # Update existing style
                self.styles[style_name].__dict__.update(attributes)
            else:
                # Add new style
                self.styles.add(ParagraphStyle(name=style_name, parent=self.styles['Normal'], **attributes))

        # CB: 3.2.2 - Create elements
        for section in report:
            for element_type, content in section.items():
                element = self.create_element(element_type, content)
                if element:
                    self.elements.append(element)
                else:
                    logging.error(f"Failed to create element of type {element_type}")

        # CB: 3.2.3 - Build the PDF
        try:
            doc.build(self.elements)
        except Exception as e:
            logging.error(f"Error building PDF: {e}")

# CB: 4.0 - Test the template
def test_template(style_config=None):
    report = [
        {
            "header": "My Report Header",
            "footer": "Page 1",
            "heading": "Main Heading",
            "subheading": "Subheading",
            "body_text": "This is some more body text that can be elaborated upon to provide additional information and context. As we delve further into the topic, it becomes apparent that there are various aspects to consider and explore.",
            "bullet_points": ["Point 1", "Point 2", "Point 3"],
            "table": [["Header 1", "Header 2"], ["Row 1, Column 1", "Row 1, Column 2"], ["Row 2, Column 1", "Row 2, Column 2"]],
            "image": "Grafico01.jpg"
        }
    ]
    r = Report(style_config)
    r.create_pdf(report)

# CB: 5.0 - Main entry point
if __name__ == "__main__":
    style_config = {
        'Header': {'fontSize': 20, 'textColor': colors.darkgray, 'alignment': 1},
        'Footer': {'fontSize': 12, 'textColor': colors.darkgray},
        'Heading1': {'fontSize': 16, 'textColor': colors.black, 'spaceAfter': 12},
        'Heading2': {'fontSize': 14, 'textColor': colors.black, 'spaceBefore': 12, 'spaceAfter': 6},
        'BodyText': {'fontSize': 12, 'textColor': colors.black},
        'Bullet': {'parent': 'BodyText', 'firstLineIndent': 0, 'spaceBefore': 20}
    }
    test_template(style_config)
