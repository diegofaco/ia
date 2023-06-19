# CB: 1.0 - Define function to get test report data
def get_test_report_data():
    report = [
        {
            "header": "Header Text",
            "footer": "Footer Text",
            "heading": "Heading Text",
            "subheading": "Subheading Text",
            "body_text": "Body Text",
            "bullet_points": ["Bullet 1", "Bullet 2", "Bullet 3"],
            "image": "image_path",
            "table": [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]]
        }
    ]
    return report