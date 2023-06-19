# CB: 1.0 - Import necessary libraries
from elements import create_header, create_footer, create_heading, create_subheading, create_body_text, create_bullet_points, create_image, create_table
from styles import create_styles
from pdf_creator import create_pdf
from data import get_test_report_data
import logging

# CB: 2.0 - Set up logging
logging.basicConfig(filename='pdf_template.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# CB: 3.0 - Define function to test the template
def test_template():
    # CB: 3.1 - Create styles
    styles = create_styles()

    # CB: 3.2 - Get report data
    report_data = get_test_report_data()

    # CB: 3.3 - Create report
    report = [
        {
            "header": create_header(report_data["header"], styles),
            "footer": create_footer(report_data["footer"], styles),
            "heading": create_heading(report_data["heading"], styles),
            "subheading": create_subheading(report_data["subheading"], styles),
            "body_text": create_body_text(report_data["body_text"], styles),
            "bullet_points": create_bullet_points(report_data["bullet_points"], styles),
            "image": create_image(report_data["image"]),
            "table": create_table(report_data["table"])
        }
    ]

    # CB: 3.4 - Create PDF
    create_pdf(report, styles)

# CB: 4.0 - Main entry
