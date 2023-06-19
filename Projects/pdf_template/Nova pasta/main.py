# CB: 1.0 - Import necessary libraries
from elements import create_header, create_footer, create_heading, create_subheading, create_body_text, create_bullet_points, create_image, create_table
from styles import create_styles
from pdf_creator import create_pdf
import logging

# CB: 2.0 - Set up logging
logging.basicConfig(filename='pdf_template.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# CB: 3.0 - Define function to test the template
def test_template():
    # CB: 3.1 - Create styles
    styles = create_styles()

    # CB: 3.2 - Create report
    report = [
        {
            "header": create_header("Header Text", styles),
            "footer": create_footer("Footer Text", styles),
            "heading": create_heading("Heading Text", styles),
            "subheading": create_subheading("Subheading Text", styles),
            "body_text": create_body_text("Body Text", styles),
            "bullet_points": create_bullet_points(["Bullet 1", "Bullet 2", "Bullet 3"], styles),
            "image": create_image("image_path"),
            "table": create_table([["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]])
        }
    ]

    # CB: 3.3 - Create PDF
    create_pdf(report, styles)

# CB: 4.0 - Main entry point
if __name__ == "__main__":
    test_template()
