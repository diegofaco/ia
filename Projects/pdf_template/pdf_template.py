# CB: 1.0 - Import necessary libraries
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, PageBreak, TableStyle, ListFlowable, Preformatted
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import datetime
import logging
import os

# CB: 2.0 - Set up logging
logging.basicConfig(filename='pdf_template.log', level=logging.INFO)

# CB: 3.0 - Define the Report class
class Report:
    def __init__(self, style_config=None, orientation='portrait'):
        self.styles = getSampleStyleSheet()
        self.style_config = style_config if style_config else {}
        self.elements = []
        self.headings = []
        if orientation == 'landscape':
            self.doc = SimpleDocTemplate("report.pdf", pagesize=landscape(A4))
        else:
            self.doc = SimpleDocTemplate("report.pdf", pagesize=A4)
        self.template = PageTemplate(id='main', frames=[Frame(0, 0, self.doc.width, self.doc.height, id='main_frame')], onPage=self.add_page_decorations)
        self.doc.addPageTemplates(self.template)
        self.styles.add(ParagraphStyle(name='Footer', fontSize=10, leading=12))
        self.styles.add(ParagraphStyle(name='CustomBullet', fontSize=10, leading=12, leftIndent=20, firstLineIndent=-20, spaceAfter=5))

    def add_page_decorations(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(inch, inch, f"Page {doc.page}")
        canvas.restoreState()

    # CB: 3.1 - Define functions for creating each element
    def create_element(self, element_type, content):
        try:
            if element_type == "header":
                return Paragraph(content, self.styles['Heading1'])
            elif element_type == "footer":
                return Paragraph(content, self.styles['Footer'])
            elif element_type == "heading":
                self.headings.append((content, len(self.elements)))
                return Paragraph(content, self.styles['Heading2'])
            elif element_type == "subheading":
                return Paragraph(content, self.styles['Heading3'])
            elif element_type == "body_text":
                return Paragraph(content, self.styles['BodyText'])
            elif element_type == "bullet_points":
                return [Paragraph(bullet, self.styles['CustomBullet']) for bullet in content]
            elif element_type == "image":
                if not os.path.exists(content):
                    raise FileNotFoundError(f"Image file not found: {content}")
                return Image(content, width=200)
            elif element_type == "table":
                return self.create_table(content)
            elif element_type == "list":
                return ListFlowable(content, bulletType='bullet')
            elif element_type == "code":
                return Preformatted(content, self.styles['Code'])
            else:
                logging.error(f"Unknown element type: {element_type}")
                return None
        except Exception as e:
            logging.error(f"Error creating {element_type}: {e}")
            return None
        
    def create_table(self, data):
        try:
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),

                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            return table
        except Exception as e:
            logging.error(f"Error creating table: {e}")
            return None
    
    # CB: 3.2 - Define function for creating the table of contents page
    def create_toc_page(self):
        data = [["Table of Contents"]]
        for heading, position in self.headings:
            data.append([heading, str(position + 1)])
        table = Table(data, colWidths=[400, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        return table

    # CB: 3.3 - Define function for building the report
    def build(self):
        try:
            logging.info("Building report...")
            toc_page = self.create_toc_page()
            self.elements.insert(0, toc_page)
            self.doc.build(self.elements)
            logging.info("Report built successfully.")
        except Exception as e:
            logging.error(f"Error building report: {e}")

# CB: 4.0 - Define a function to test the template
def test_template(style_config):
    try:
        r = Report(style_config)
        elements = [
            r.create_element("header", "This is a header"),
            r.create_element("footer", "This is a footer"),
            r.create_element("heading", "This is a heading"),
            r.create_element("subheading", "This is a subheading"),
            r.create_element("body_text", "This is some body text"),
            r.create_element("bullet_points", ["Bullet point 1", "Bullet point 2", "Bullet point 3"]),
            r.create_element("image", "path_to_image.jpg"),
            r.create_element("table", [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]]),
            r.create_element("list", ["List item 1", "List item 2", "List item 3"]),
            r.create_element("code", "print('Hello, world!')")
        ]
        r.elements = [e for e in elements if e is not None]
        r.build()
    except Exception as e:
        logging.error(f"Error testing template: {e}")

# CB: 5.0 - Define the style configuration
style_config = {
    "header": {"fontSize": 14, "leading": 16},
    "footer": {"fontSize": 12, "leading": 14},
    "heading": {"fontSize": 12, "leading": 14},
    "subheading": {"fontSize": 10, "leading": 12},
    "body_text": {"fontSize": 10, "leading": 12},
    "bullet_points": {"fontSize": 10, "leading": 12},
    "image": {"width": 200},
    "table": {"fontSize": 10, "leading": 12},
    "list": {"fontSize": 10, "leading": 12},
    "code": {"fontSize": 10, "leading": 12}
}

# CB: 6.0 - Test the template
test_template(style_config)
