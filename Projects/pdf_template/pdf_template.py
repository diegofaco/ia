# CB: 1.0 - Import necessary libraries
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, ListFlowable, ListItem, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY
import datetime
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF


# CB: 2.0 - Define common elements
def create_header(c, text):
    # CB: 2.1.1 - Set the font and size for the header
    c.setFont("Helvetica-Bold", 24)

    # CB: 2.1.2 - Set the color for the header (in RGB)
    c.setFillColorRGB(0, 0, 0) # Black color

    # CB: 2.1.3 - Set the x-coordinate for the text
    text_x = 30  # 50 units from the left edge of the page

    # CB: 2.1.4 - Draw the header
    c.drawString(text_x, 750, text)

def create_footer(c, text):
    # CB: 2.2.1 - Set the font and size for the footer
    c.setFont("Helvetica", 10)

    # CB: 2.2.2 - Set the color for the footer (in RGB)
    c.setFillColorRGB(0, 0, 0) # Black color

    # CB: 2.2.3 - Set the x-coordinate for the text
    text_x = 50  # 50 units from the left edge of the page

    # CB: 2.2.4 - Draw the footer
    c.drawString(text_x, 30, text)

def add_page_number(c, page_number):
    # CB: 2.3.1 - Set the font and size for the page number
    c.setFont("Helvetica", 8)

    # CB: 2.3.2 - Set the color for the page number (in RGB)
    c.setFillColorRGB(0, 0, 0) # Black color

    # CB: 2.3.3 - Calculate the width of the page number
    page_number_width = c.stringWidth(str(page_number), "Helvetica", 8)

    # CB: 2.3.4 - Calculate the x-coordinate for the page number
    page_number_x = A4[0] - 50 - page_number_width  # 50 units from the right edge of the page

    # CB: 2.3.5 - Draw the page number
    c.drawString(page_number_x, 30, str(page_number))
    
def add_body_text(c, text, y):
    # CB: 2.4.1 - Set the font and size for the body text
    c.setFont("Helvetica", 12)

    # CB: 2.4.2 - Set the color for the body text (in RGB)
    c.setFillColorRGB(0, 0, 0) # Black color

    # CB: 2.4.3 - Calculate the height of the text
    text_height = 12  # This is a rough estimate, you might need to adjust it

    # CB: 2.4.4 - Check if the text will fit on the page
    if y - text_height < 50:  # Leave a 50 unit margin at the bottom
        # The text won't fit on the page, start a new page
        c.showPage()
        y = 750  # Reset the y-coordinate to the top of the page

    # CB: 2.4.5 - Draw the text
    c.drawString(50, y, text)

    # CB: 2.4.6 - Return the new y-coordinate
    return y - text_height

def get_stylesheet():
    # CB: 3.1 - Get the sample stylesheet
    stylesheet = getSampleStyleSheet()

    # CB: 3.2 - Customize the default (Normal) style
    stylesheet["Normal"].fontName = "Helvetica"
    stylesheet["Normal"].fontSize = 24
    stylesheet["Normal"].leading = 18
    stylesheet["Normal"].alignment = TA_JUSTIFY  # Add this line

    # CB: 3.3 - Add custom styles
    stylesheet.add(ParagraphStyle(name="Header", parent=stylesheet["Normal"], fontSize=24, leading=28, spaceAfter=12))
    stylesheet.add(ParagraphStyle(name="Footer", parent=stylesheet["Normal"], fontSize=10, leading=12, spaceBefore=12))

    return stylesheet

# CB: 3.4 - Define text formatting
def format_heading(c, text):
    # Set the font and size for the heading
    c.setFont("Helvetica-Bold", 14)
    
    # Set the color for the heading (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the heading
    # The numbers 30 and 680 here represent the x and y coordinates of where we want to place the heading.
    # You can adjust these numbers to move the heading around on the page.
    c.drawString(30, 680, text)

def format_subheading(c, text):
    # Set the font and size for the subheading
    c.setFont("Helvetica-Bold", 12)
    
    # Set the color for the subheading (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the subheading
    # The numbers 30 and 660 here represent the x and y coordinates of where we want to place the subheading.
    # You can adjust these numbers to move the subheading around on the page.
    c.drawString(30, 660, text)

def format_body_text(c, text):
    # Set the font and size for the body text
    c.setFont("Helvetica", 10)
    
    # Set the color for the body text (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the body text
    # The numbers 30 and 700 here represent the x and y coordinates of where we want to place the body text.
    # You can adjust these numbers to move the body text around on the page.
    c.drawString(30, 700, text)

def format_bullet_points(c, points, x, y, width, style):
    # Set the font, size, and color for the bullet points
    c.setFont(style.fontName, style.fontSize)
    c.setFillColor(style.textColor)
    
    # Calculate the height of a line of text
    line_height = style.leading
    
    # Loop over the bullet points
    for i, point in enumerate(points):
        # Calculate the y-coordinate for this bullet point
        y_point = y - i * line_height
        
        # Draw the bullet point
        c.drawString(x, y_point, "•")
        
        # Draw the text
        c.drawString(x + 20, y_point, point)  # Start the text 20 units to the right of the bullet point

def format_paragraph(c, text, x, y, width, style):
    # Create a Paragraph object
    p = Paragraph(text, style)
    
    # Add the paragraph to the canvas
    p.wrap(width, y)
    p.drawOn(c, x, y)

def format_table(c, data, x, y, style):
    # Check if data is None or not a list of lists
    if data is None or not all(isinstance(row, list) for row in data):
        return
    
    # Create a Table object
    t = Table(data)
    
    # Apply the style to the table
    t.setStyle(style)
    
    # Add the table to the canvas
    t.wrapOn(c, x, y)
    t.drawOn(c, x, y)

def format_image(c, path, x, y, width):
    # Create an ImageReader object
    img = ImageReader(path)
    
    # Get the size of the image
    img_width, img_height = img.getSize()
    
    # Calculate the height of the image when it's scaled to the specified width
    height = width * img_height / img_width
    
    # Add the image to the canvas
    c.drawImage(path, x, y-height, width, height)

def format_page_number(c, page_number, x, y, style):
    # Set the font, size, and color for the page number
    c.setFont(style.fontName, style.fontSize)
    c.setFillColor(style.textColor)
    
    # Draw the page number
    c.drawCentredString(x, y, str(page_number))
    
def add_table(c, data, x, y):
    # Check if data is None
    if data is None:
        return
    
    # Create the table
    table = Table(data)
    
    # Add the table
    table.wrapOn(c, x, y)
    table.drawOn(c, x, y)
    
# CB: 4.10 - Main function
def create_pdf(report):
    # CB: 4.1 - Get the current date and time
    now = datetime.datetime.now()

    # CB: 4.2 - Format the date and time as a string
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # CB: 4.3 - Create a unique filename by appending the timestamp to the base filename
    filename = f"report_{timestamp}.pdf"

    # CB: 4.4 - Create the canvas with the unique filename
    c = canvas.Canvas(filename, pagesize=A4)
    
    # Loop over the data in the report
    for i in range(len(report["headings"])):
        # Create the header
        create_header(c, report["header"])
        
        # Create the footer
        create_footer(c, report["footer"])
        
        # Add the page number
        add_page_number(c, report["page_numbers"][i])
        
        # Format the heading
        format_heading(c, report["headings"][i])
        
        # Format the subheading
        format_subheading(c, report["subheadings"][i])
        
        # Format the body text
        style = ParagraphStyle('BodyText', parent=getSampleStyleSheet()['BodyText'], fontName='Helvetica', fontSize=10, textColor=colors.black)
        format_paragraph(c, report["body_text"][i], 30, 700, 500, style)
        
        # Format the bullet points
        style = ParagraphStyle('BulletPoints', parent=getSampleStyleSheet()['BodyText'], fontName='Courier', fontSize=10, textColor=colors.black, leftIndent=20, leading=12)
        format_bullet_points(c, report["bullet_points"][i], 30, 640, 500, style) # Start the bullet points at y-coordinate 640
        
        # Add an image
        format_image(c, report["images"][i], 30, 600, 200) # Start the image at y-coordinate 600 and scale it to a width of 200
        
        # Add a table
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
        
        # Start a new page
        c.showPage()
    
    c.save()

# CB: 5.10 - Test the template
def test_template():
    report = {
        "header": "My Report Header",
        "footer": "Page 1",
        "headings": ["Main Heading", "Another Heading"],
        "subheadings": ["Subheading", "Another Subheading"],
        "body_text": ["This is some more body text that can be elaborated upon to provide additional information and context. As we delve further into the topic, it becomes apparent that there are various aspects to consider and explore. By expanding upon this body text, we can delve into the intricacies, nuances, and related subject matter, shedding light on the matter at hand.", "This is some more body text."],
        "bullet_points": [["Point 1", "Point 2", "Point 3"], ["Another Point 1", "Another Point 2"]],
        "images": ["C:\github\ia\Projects\pdf_template\grafico01.jpg", "C:\github\ia\Projects\pdf_template\grafico02.jpg"],
        "tables": [[["Header 1", "Header 2"], ["Row 1, Column 1", "Row 1, Column 2"], ["Row 2, Column 1", "Row 2, Column 2"]], None],
        "page_numbers": [1, 2]
    }
    create_pdf(report)


if __name__ == "__main__":
    test_template()