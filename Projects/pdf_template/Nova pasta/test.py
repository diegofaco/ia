from styles import create_styles
from elements import create_image
from reportlab.platypus import TableStyle

# Test create_styles
styles = create_styles()
print(f"Styles: {styles}")

# Test create_image
try:
    create_image("non_existent_file.jpg")
except Exception as e:
    print(f"Caught an exception: {e}")

# Test TableStyle
print(f"TableStyle: {TableStyle}")
