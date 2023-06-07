import pyautogui
import time
import keyboard
import random

# For each number from 1 to 99
for i in range(1, 100):
    # Generate the file path
    file_path = r"c:\dados\discordpy\Prompt_{:03d}.txt".format(i)

    # Open the file and read the content
    with open(file_path, 'r') as file:
        content = file.read()

    # Give some time to manually select the Discord window and the text input field
    time.sleep(random.randint(1, 10))

    # Type the content and press enter
    pyautogui.write(content)
    pyautogui.press('enter')
    pyautogui.press('enter')

    # Wait a random amount of time between 1 and 10 seconds before the next message
    time.sleep(random.randint(1, 10))
