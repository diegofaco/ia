# CB: 1.0 - Import necessary libraries
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import datetime

# CB: 2.0 - Define functions for creating each element
# CB: 2.1 - Function for creating a header
def create_header(header_text, stylesheet):
    header = Paragraph(header_text, stylesheet['Heading1'])
    return header

# CB: 2.2 - Function for creating a footer
def create_footer(footer_text, stylesheet):
    footer = Paragraph(footer_text, stylesheet['Footer'])
    return footer

# CB: 2.3 - Function for creating a heading
def create_heading(heading_text, stylesheet):
    heading = Paragraph(heading_text, stylesheet['Heading2'])
    return heading

# CB: 2.4 - Function for creating a subheading
def create_subheading(subheading_text, stylesheet):
    subheading = Paragraph(subheading_text, stylesheet['Heading3'])
    return subheading

# CB: 2.5 - Function for creating body text
def create_body_text(body_text, stylesheet):
    body = Paragraph(body_text, stylesheet['BodyText'])
    return body

# CB: 2.6 - Function for creating bullet points
def create_bullet_points(bullet_points, stylesheet):
    bullets = [Paragraph(bullet, stylesheet['CustomBullet']) for bullet in bullet_points]
    return bullets

# CB: 2.7 - Function for creating an image
def create_image(image_path):
    image = Image(image_path, width=200)
    return image

# CB: 2.8 - Function for creating a table
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

# CB: 3.0 - Main function for creating the PDF
def create_pdf(report):
    # CB: 3.1 - Get the current date and time
    now = datetime.datetime.now()

    # CB: 3.2 - Format the date and time as a string
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # CB: 3.3 - Create a unique filename by appending the timestamp to the base filename
    filename = f"report_{timestamp}.pdf"

    # CB: 3.4 - Create the SimpleDocTemplate with the unique filename
    doc = SimpleDocTemplate(filename, pagesize=A4)

    # CB: 3.5 - Create a list to hold the Flowables
    elements = []

    # CB: 3.6 - Get the sample style sheet and add custom styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Footer', parent=styles['Normal'], fontSize=10, textColor=colors.gray))
    styles.add(ParagraphStyle(name='CustomBullet', parent=styles['BodyText'], firstLineIndent=0, spaceBefore=20))

    # CB: 3.7 - Create the elements and add them to the list of elements
    header = create_header(report["header"], styles)
    elements.append(header)

    footer = create_footer(report["footer"], styles)
    elements.append(footer)

    for section in report["sections"]:
        heading = create_heading(section["heading"], styles)
        elements.append(heading)

        subheading = create_subheading(section["subheading"], styles)
        elements.append(subheading)

        body_text = create_body_text(section["body_text"], styles)
        elements.append(body_text)

        bullet_points = create_bullet_points(section["bullet_points"], styles)
        elements.extend(bullet_points)

        image = create_image(section["image"])
        elements.append(image)

        table = create_table(section["table"])
        elements.append(table)

        elements.append(PageBreak())

    # CB: 3.8 - Build the PDF
    doc.build(elements)

# CB: 4.0 - Test function
def test_template():
    # CB: 4.1 - Define a test report
    report = {
        "header": "My Report Header",
        "footer": "Page 1",
        "sections": [
            {
                "heading": "Main Heading",
                "subheading": "Subheading",
                "body_text": "This is some body text.",
                "bullet_points": ["Point 1", "Point 2", "Point 3"],
                "image": "grafico01.jpg",
                "table": [["Header 1", "Header 2"], ["Row 1, Column 1", "Row 1, Column 2"], ["Row 2, Column 1", "Row 2, Column 2"]]
            },
            # Additional sections go here
        ]
    }

    # CB: 4.2 - Call the create_pdf function with the test report
    create_pdf(report)

# CB: 5.0 - Main entry point
if __name__ == "__main__":
    test_template()
