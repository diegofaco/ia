import pyautogui
import time
import os
import random
import glob
import pyperclip

file_list = glob.glob(r"C:\github\ia\Discordpy\output\*.txt")

random.shuffle(file_list)

for file_path in file_list:

    with open(file_path, 'r') as file:
        content = file.read()

    pyperclip.copy(content)

    time.sleep(random.uniform(1.0, 6.5))
    pyautogui.write('/imagine')
    time.sleep(random.uniform(1.0, 1.5))
    pyautogui.press('tab')
    time.sleep(random.uniform(1.0, 2.5))
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(random.uniform(1.0, 2.5))
    pyautogui.press('enter')
    time.sleep(random.uniform(1.0, 6.5))

    if file_list.index(file_path) % 3 == 0:
        time.sleep(random.uniform(13.0, 27.5))
