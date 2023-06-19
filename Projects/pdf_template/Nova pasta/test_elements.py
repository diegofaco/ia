# CB: 1.0 - Import necessary libraries
from reportlab.platypus.tables import TableStyle  # Add this line
from elements import create_header, create_footer, create_heading, create_subheading, create_body_text, create_bullet_points, create_image, create_table
from styles import create_styles
import pytest

print(TableStyle)

# CB: 2.0 - Define tests for each function
def test_create_header():
    styles = create_styles()
    header = create_header("Test Header", styles)
    assert header.text == "Test Header"

def test_create_footer():
    styles = create_styles()
    footer = create_footer("Test Footer", styles)
    assert footer.text == "Test Footer"

def test_create_heading():
    styles = create_styles()
    heading = create_heading("Test Heading", styles)
    assert heading.text == "Test Heading"

def test_create_subheading():
    styles = create_styles()
    subheading = create_subheading("Test Subheading", styles)
    assert subheading.text == "Test Subheading"

def test_create_body_text():
    styles = create_styles()
    body_text = create_body_text("Test Body Text", styles)
    assert body_text.text == "Test Body Text"

def test_create_bullet_points():
    styles = create_styles()
    bullet_points = create_bullet_points(["Test Bullet 1", "Test Bullet 2"], styles)
    assert len(bullet_points) == 2
    assert bullet_points[0].text == "Test Bullet 1"
    assert bullet_points[1].text == "Test Bullet 2"

def test_create_image():
    with pytest.raises(Exception):
        create_image("non_existent_image_path")

def test_create_table():
    table_data = [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]]
    table = create_table(table_data)
    assert len(table.data) == 2
    assert table.data[0] == ["Cell 1", "Cell 2"]
    assert table.data[1] == ["Cell 3", "Cell 4"]
