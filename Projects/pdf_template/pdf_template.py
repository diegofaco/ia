# CB: 1.0 - Import necessary libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

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
        format_body_text(c, report["body_text"][i])
        
        # Format the bullet points
        format_bullet_points(c, report["bullet_points"][i], 640)  # Start the bullet points at y-coordinate 640
        
        # Add an image
        add_image(c, report["images"][i], 30, 400)  # Replace with the path to your image file
        
        # Add a table
        add_table(c, report["tables"][i], 30, 200)
        
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
        "body_text": ["This is some body text.", "This is some more body text."],
        "bullet_points": [["Point 1", "Point 2", "Point 3"], ["Another Point 1", "Another Point 2"]],
        "images": ["C:\github\ia\Projects\pdf_template\grafico01.jpg", "C:\github\ia\Projects\pdf_template\grafico01.jpg"],
        "tables": [[["Header 1", "Header 2"], ["Row 1, Column 1", "Row 1, Column 2"], ["Row 2, Column 1", "Row 2, Column 2"]], None],
        "page_numbers": [1, 2]
    }
    create_pdf(report)


if __name__ == "__main__":
    test_template()
