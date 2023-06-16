# CB: 1.0 - Import necessary libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, TableOfContents

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
    
def add_headings(c, headings, toc):
    for heading in headings:
        # Add the heading to the PDF
        c.setFont("Helvetica-Bold", 14)
        c.drawString(10, 800, heading["text"])

        # Add an entry to the table of contents
        toc.addEntry(1, heading["text"], c.getPageNumber())
    
def add_subheadings(c, subheadings, toc):
    for subheading in subheadings:
        # Add the subheading to the PDF
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20, 780, subheading["text"])
        
        # Add an entry to the table of contents
        toc.addEntry(2, subheading["text"], c.getPageNumber())
        
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

def format_bullet_points(c, points, start_position):
    # Set the font and size for the bullet points
    c.setFont("Helvetica", 10)
    
    # Set the color for the bullet points (in RGB)
    c.setFillColorRGB(0, 0, 0)  # Black color
    
    # Draw the bullet points
    # The start_position parameter is the y-coordinate where we want to start the bullet points.
    y = start_position
    for point in points:
        c.drawString(30, y, f"• {point}")
        y -= 14  # Move down the page for the next bullet point

def add_image(c, image_path, x, y, width=200, height=200):
    # Add the image
    c.drawImage(image_path, x, y, width, height)

def add_table(c, data, x, y):
    # Check if data is None
    if data is None:
        return
    
    # Create the table
    table = Table(data)
    
    # Create a table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Set the background color of the first row to grey
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Set the text color of the first row to white

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all text to center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Use bold for the first row
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Set the font size for all cells to 12

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Add extra space below the text of the first row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Set the background color of all other rows to beige
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Add a grid around all cells
    ])
    
    # Apply the table style
    table.setStyle(style)
    
    # Add the table
    table.wrapOn(c, x, y)
    table.drawOn(c, x, y)
    
# CB: 4.10 - Main function
def create_pdf(report):
    # Create the PDF
    c = canvas.Canvas("report.pdf")
    
    # Create a SimpleDocTemplate
    doc = SimpleDocTemplate(c)
    
    # Create a TableOfContents object
    toc = TableOfContents()
    
    # Add the TableOfContents to the document
    doc.add(toc)
    
    # Add the rest of the content
    add_header(c, report["header"])
    add_footer(c, report["footer"])
    add_headings(c, report["headings"])
    add_subheadings(c, report["subheadings"])
    add_body_text(c, report["body_text"])
    add_bullet_points(c, report["bullet_points"])
    add_images(c, report["images"])
    add_tables(c, report["tables"])
    
    # Save the PDF
    c.save()

# CB: 5.11 - Test the template
def test_template():
    report = {
        "header": "My Report",
        "footer": "Page %d",
        "headings": [
            {"text": "Introduction"},
            {"text": "Main Section"},
            {"text": "Conclusion"}
        ],
        "subheadings": [
            {"text": "Subheading 1"},
            {"text": "Subheading 2"},
            {"text": "Subheading 3"}
        ],
        "body_text": [
            {"text": "This is some body text."},
            {"text": "This is some more body text."},
            {"text": "This is even more body text."}
        ],
        "bullet_points": [
            {"text": "Bullet point 1"},
            {"text": "Bullet point 2"},
            {"text": "Bullet point 3"}
        ],
        "images": [
            {"path": "grafico01.jpg"},
            {"path": "grafico01.jpg"},
            {"path": "grafico01.jpg"}
        ],
        "tables": [
            {"data": [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]]},
            {"data": [["Cell 5", "Cell 6"], ["Cell 7", "Cell 8"]]},
            {"data": [["Cell 9", "Cell 10"], ["Cell 11", "Cell 12"]]}
        ]
    }

    create_pdf(report)

if __name__ == "__main__":
    test_template()
    toc.generate(c)
