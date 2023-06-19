# CB: 1.0 - Import necessary libraries
from styles import create_styles

# CB: 2.0 - Define tests for create_styles function
def test_create_styles():
    styles = create_styles()
    assert len(styles) == 6

    style_config = {"CustomStyle": {"fontSize": 20, "textColor": colors.red}}
    styles = create_styles(style_config)
    assert len(styles) == 7
    assert styles["CustomStyle"].fontSize == 20
    assert styles["CustomStyle"].textColor == colors.red
