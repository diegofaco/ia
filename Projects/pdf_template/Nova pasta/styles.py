# CB: 1.0 - Import necessary libraries
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import logging

# CB: 2.0 - Set up logging
logging.basicConfig(filename='pdf_template.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# CB: 3.0 - Define function for creating styles
def create_styles(style_config=None):
    try:
        logging.info('Creating styles')
        styles = getSampleStyleSheet()
        
        # CB: 3.1 - Check if style configuration is provided
        if style_config is None:
            # Default styles
            styles['Heading1'].fontSize = 16
            styles['Heading1'].textColor = colors.gray
            styles['Heading1'].alignment = 1
            styles.add(ParagraphStyle(name='Footer', parent=styles['Normal'], fontSize=10, textColor=colors.gray))
            styles.add(ParagraphStyle(name='CustomBullet', parent=styles['BodyText'], firstLineIndent=0, spaceBefore=20, bulletIndent=0))
            styles['Heading2'].fontSize = 14
            styles['Heading2'].textColor = colors.black
            styles['Heading2'].spaceAfter = 12
            styles['BodyText'].fontSize = 10
            styles['BodyText'].textColor = colors.black
            styles['Bullet'].firstLineIndent = 0
            styles['Bullet'].spaceBefore = 20
            styles['Bullet'].firstLineIndent = 0
            styles['Bullet'].spaceBefore = 20
        else:
            # User-provided styles
            for style_name, attributes in style_config.items():
                if style_name in styles:
                    # Update existing style
                    for attr, value in attributes.items():
                        setattr(styles[style_name], attr, value)
                else:
                    # Add new style
                    styles.add(ParagraphStyle(name=style_name, parent=styles['Normal'], **attributes))

        return styles
    except Exception as e:
        logging.error(f'Error creating styles: {e}')
        print(f'Error creating styles: {e}')  # Add this line
        return None




