# CB: 1.0 - Import necessary libraries
from pdf_creator import create_pdf
from elements import create_header, create_footer, create_heading, create_subheading, create_body_text, create_bullet_points, create_image, create_table
from styles import create_styles
import os
import pytest

# CB: 2.0 - Define tests for create_pdf function
def test_create_pdf():
    styles = create_styles()
    report = [
        {
            "header": create_header("Test Header", styles),
            "footer": create_footer("Test Footer", styles),
            "heading": create_heading("Test Heading", styles),
            "subheading": create_subheading("Test Subheading", styles),
            "body_text": create_body_text("Test Body Text", styles),
            "bullet_points": create_bullet_points(["Test Bullet 1", "Test Bullet 2"], styles),
            "image": None,
            "table": create_table([["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]])
        }
    ]
    create_pdf(report, styles)
    assert os.path.exists("report.pdf")

    with pytest.raises(Exception):
        create_pdf(None, styles)
