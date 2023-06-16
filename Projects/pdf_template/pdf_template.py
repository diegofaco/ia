# CB: 1.0 - Import necessary libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, ListFlowable, ListItem
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.utils import ImageReader

# CB: 2.0 - Define common elements
def create_header(c, text):
    # Set the font and size for the header
    c.setFont("Helvetica-Bold", 24)
    
    # Set the color for the header (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the header
    # The numbers 30 and 750 here represent the x and y coordinates of where we want to place the header.
    # You can adjust these numbers to move the header around on the page.
    c.drawString(30, 750, text)

def create_footer(c, text):
    # Set the font and size for the footer
    c.setFont("Helvetica", 10)
    
    # Set the color for the footer (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the footer
    # The numbers 30 and 30 here represent the x and y coordinates of where we want to place the footer.
    # You can adjust these numbers to move the footer around on the page.
    c.drawString(30, 30, text)

def add_page_number(c, page_number):
    # Set the font and size for the page number
    c.setFont("Helvetica", 8)
    
    # Set the color for the page number (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the page number
    # The numbers 550 and 30 here represent the x and y coordinates of where we want to place the page number.
    # You can adjust these numbers to move the page number around on the page.
    c.drawString(550, 30, str(page_number))
    
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
    c = canvas.Canvas("report.pdf", pagesize=letter)
    
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