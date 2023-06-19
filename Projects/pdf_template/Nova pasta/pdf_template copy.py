# CB: 1.0 - Import necessary libraries
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader

# CB: 2.0 - Define common elements
def create_element(c, text, x, y, font, size, color):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text)

def create_header(c, text, x=30, y=750):
    create_element(c, text, x, y, "Helvetica-Bold", 24, (0, 0, 0))

def create_footer(c, text, x=30, y=30):
    create_element(c, text, x, y, "Helvetica", 10, (0, 0, 0))

def add_page_number(c, page_number, x=550, y=30):
    create_element(c, str(page_number), x, y, "Helvetica", 8, (0, 0, 0))

# CB: 3.0 - Define text formatting
def format_heading(c, text, x=30, y=680):
    create_element(c, text, x, y, "Helvetica-Bold", 14, (0, 0, 0))

def format_subheading(c, text, x=30, y=660):
    create_element(c, text, x, y, "Helvetica-Bold", 12, (0, 0, 0))

def format_body_text(c, text, x=30, y=700):
    style = ParagraphStyle('BodyText', parent=getSampleStyleSheet()['BodyText'], fontName='Helvetica', fontSize=10, textColor=colors.black)
    p = Paragraph(text, style)
    p.wrapOn(c, 500, y)
    p.drawOn(c, x, y)

def format_bullet_points(c, points, x, y, width, style):
    line_height = style.leading
    for i, point in enumerate(points):
        y_point = y - i * line_height
        create_element(c, "•", x, y_point, style.fontName, style.fontSize, style.textColor)
        create_element(c, point, x + 20, y_point, style.fontName, style.fontSize, style.textColor)

def format_table(c, data, x, y, style):
    if data is None or not all(isinstance(row, list) for row in data):
        return
    t = Table(data)
    t.setStyle(style)
    t.wrapOn(c, x, y)
    t.drawOn(c, x, y)

def format_image(c, path, x, y, width):
    img = ImageReader(path)
    img_width, img_height = img.getSize()
    height = width * img_height / img_width
    c.drawImage(path, x, y-height, width, height)

# CB: 4.0 - Main function
def create_pdf(report):
    c = canvas.Canvas("report.pdf", pagesize=A4)
    for i in range(len(report["headings"])):
        create_header(c, report["header"])
        create_footer(c, report["footer"])
        add_page_number(c, report["page_numbers"][i])
        format_heading(c, report["headings"][i])
        format_subheading(c, report["subheadings"][i])
        format_body_text(c, report["body_text"][i])
        style = ParagraphStyle('BulletPoints', parent=getSampleStyleSheet()['BodyText'], fontName='Courier', fontSize=10, textColor=colors.black, leftIndent=20, leading=12)
        format_bullet_points(c, report["bullet_points"][i], 30, 640, 500, style)
        format_image(c, report["images"][i], 30, 600, 200)
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
        format_table(c, report["tables"][i], 30, 200, style)
        c.showPage()
    c.save()

# CB: 5.0 - Test the template
def test_template():
    report = {
        "header": "My Report Header",
        "footer": "Page 1",
        "headings": ["Main Heading", "Another Heading"],
        "subheadings": ["Subheading", "Another Subheading"],
        "body_text": ["This is some more body text that can be elaborated upon to provide additional information and context. As we delve further into the topic, it becomes apparent that there are various aspects to consider and explore. By expanding upon this body text, we can delve into the intricacies, nuances, and related subject matter, shedding light on the matter at hand.", "This is some more body text."],
        "bullet_points": [["Point 1", "Point 2", "Point 3"], ["Another Point 1", "Another Point 2"]],
        "images": ["C:\\github\\ia\\Projects\\pdf_template\\grafico01.jpg", "C:\\github\\ia\\Projects\\pdf_template\\grafico02.jpg"],
        "tables": [[["Header 1", "Header 2"], ["Row 1, Column 1", "Row 1, Column 2"], ["Row 2, Column 1", "Row 2, Column 2"]], None],
        "page_numbers": [1, 2]
    }
    create_pdf(report)

if __name__ == "__main__":
    test_template()
