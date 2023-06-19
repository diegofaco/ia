# CB: 1.0 - Import necessary libraries
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import datetime

# CB: 2.0 - Define functions for creating each element
def create_header(header_text, stylesheet):
    header = Paragraph(header_text, stylesheet['Heading1'])
    return header

def create_footer(footer_text, stylesheet):
    footer = Paragraph(footer_text, stylesheet['Footer'])
    return footer

def create_heading(heading_text, stylesheet):
    heading = Paragraph(heading_text, stylesheet['Heading2'])
    return heading

def create_subheading(subheading_text, stylesheet):
    subheading = Paragraph(subheading_text, stylesheet['Heading3'])
    return subheading

def create_body_text(body_text, stylesheet):
    body = Paragraph(body_text, stylesheet['BodyText'])
    return body

def create_bullet_points(bullet_points, stylesheet):
    bullets = [Paragraph(bullet, stylesheet['CustomBullet']) for bullet in bullet_points]
    return bullets

def create_image(image_path):
    image = Image(image_path, width=200)
    return image

def create_table(table_data):
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

# CB: 3.0 - Define the function to create the PDF
def create_pdf(report, style_config=None):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"report_{timestamp}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # CB: 1.1.1 - Check if style configuration is provided
    if style_config is None:
        # Default styles
        styles.add(ParagraphStyle(name='Header', parent=styles['Normal'], fontSize=16, textColor=colors.gray, alignment=1))
        styles.add(ParagraphStyle(name='Footer', parent=styles['Normal'], fontSize=10, textColor=colors.gray))
        styles.add(ParagraphStyle(name='Heading1', parent=styles['Normal'], fontSize=14, textColor=colors.black, spaceAfter=12))
        styles.add(ParagraphStyle(name='Heading2', parent=styles['Normal'], fontSize=12, textColor=colors.black, spaceBefore=12, spaceAfter=6))
        styles.add(ParagraphStyle(name='BodyText', parent=styles['Normal'], fontSize=10, textColor=colors.black))
        styles.add(ParagraphStyle(name='Bullet', parent=styles['BodyText'], firstLineIndent=0, spaceBefore=20))
    else:
        # User-provided styles
        for style_name, attributes in style_config.items():
            styles.add(ParagraphStyle(name=style_name, parent=styles['Normal'], **attributes))
            
    for section in report:
        header = create_header(section["header"], styles)
        footer = create_footer(section["footer"], styles)
        heading = create_heading(section["heading"], styles)
        subheading = create_subheading(section["subheading"], styles)
        body_text = create_body_text(section["body_text"], styles)
        bullet_points = create_bullet_points(section["bullet_points"], styles)
        table = create_table(section["table"], styles)
        image = create_image(section["image"], styles)
        page_number = create_page_number(section["page_number"], styles)
        elements.extend([header, footer, heading, subheading, body_text, bullet_points, table, image, page_number])

    style_config = {
        'Header': {'fontSize': 20, 'textColor': colors.darkgray, 'alignment': 1},
        'Footer': {'fontSize': 12, 'textColor': colors.darkgray},
        'Heading1': {'fontSize': 16, 'textColor': colors.black, 'spaceAfter': 12},
        'Heading2': {'fontSize': 14, 'textColor': colors.black, 'spaceBefore': 12, 'spaceAfter': 6},
        'BodyText': {'fontSize': 12, 'textColor': colors.black},
        'Bullet': {'parent': 'BodyText', 'firstLineIndent': 0, 'spaceBefore': 20}
    }

    test_template(style_config=style_config)

# CB: 4.0 - Test the template
def test_template(style_config=None):
    report = [
        {
            "header": "My Report Header",
            "footer": "Page 1",
            "heading": "Main Heading",
            "subheading": "Subheading",
            "body_text": "This is some more body text that can be elaborated upon to provide additional information and context. As we delve further into the topic, it becomes apparent that there are various aspects to consider and explore. By expanding upon this body text, we can delve into the intricacies, nuances, and related subject matter, shedding light on the matter at hand.",
            "bullet_points": ["Point 1", "Point 2", "Point 3"],
            "table": [["Header 1", "Header 2"], ["Row 1, Column 1", "Row 1, Column 2"], ["Row 2, Column 1", "Row 2, Column 2"]],
            "image": "Grafico01.jpg"
        }
    ]
    create_pdf(report, style_config)

# CB: 6.0 - Main entry point
if __name__ == "__main__":
    test_template()
