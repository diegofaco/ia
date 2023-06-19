# CB: 1.0 - Import necessary libraries
from reportlab.platypus import Paragraph, Image, Table
from reportlab.lib import colors

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
