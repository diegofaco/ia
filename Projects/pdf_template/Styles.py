# CB: 1.0 - Import necessary libraries
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# CB: 2.0 - Define function for creating styles
def create_styles(style_config=None):
    styles = getSampleStyleSheet()

    # CB: 1.1.1 - Check if style configuration is provided
    if style_config is None:
        # Default styles
        styles.add(ParagraphStyle(name='Header', parent=styles['Normal'], fontSize=16, textColor=colors.gray, alignment=1))
        styles.add(ParagraphStyle(name='Footer', parent=styles['Normal'], fontSize=10, textColor=colors.gray))
        styles.add(ParagraphStyle(name='Heading1', parent=styles['Normal'], fontSize=14, textColor=colors.black, spaceAfter=12))
        styles.add(ParagraphStyle(name='Heading2', parent=styles['Normal'], fontSize=12, textColor=colors.black, spaceBefore=12, spaceAfter=6))
        styles.add(ParagraphStyle(name='BodyText', parent=styles['Normal'], fontSize=10, textColor=colors.black))
        styles.add(ParagraphStyle(name='Bullet', parent=styles['BodyText'], firstLineIndent=0, spaceBefore=20))
    else:
        # User-provided styles
        for style_name, attributes in style_config.items():
            styles.add(ParagraphStyle(name=style_name, parent=styles['Normal'], **attributes))

    return styles
