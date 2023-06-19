# CB: 1.0 - Import necessary libraries
from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
import datetime
import logging

# CB: 2.0 - Set up logging
logging.basicConfig(filename='pdf_template.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# CB: 3.0 - Define function for creating PDF
def create_pdf(report, styles, filename_prefix="report"):
    try:
        logging.info('Creating PDF')
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        for section in report:
            header = create_header(section["header"], styles)
            footer = create_footer(section["footer"], styles)
            heading = create_heading(section["heading"], styles)
            subheading = create_subheading(section["subheading"], styles)
            body_text = create_body_text(section["body_text"], styles)
            bullet_points = create_bullet_points(section["bullet_points"], styles)
            table = create_table(section["table"])
            image = create_image(section["image"])

            elements.extend([header, Spacer(1, 20), heading, Spacer(1, 10), subheading, Spacer(1, 10), body_text, Spacer(1, 10)] + bullet_points + [Spacer(1, 10), table, Spacer(1, 10), image, PageBreak()])

        doc.build(elements)
    except Exception as e:
        logging.error(f'Error creating PDF: {e}')
