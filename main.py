import re
import keyboard
import time
import string
import pyautogui
import cv2

def validate(word):
    for i in sample:
        if word.count(i) > sample.count(i) or len(word) < 4:
            return False
    return True

fake_letter = ''
stop = ''

def fake(event):
    global stop
    global fake_letter
    keyboard.press('backspace')
    if event.name == 'enter':
        stop = 'stop'
    if event.name in string.ascii_lowercase:
        fake_letter = event.name

while True:
    with open(file="words.txt") as f:
        text = f.read()

    sample = input("Enter:  ")
    comb = (f'[{sample}]?') * len(sample)

    matches = re.findall(fr"\n({comb})\n", text)
    final_matches = list(filter(validate, matches))
    print(final_matches)
    storage = list(tuple([x for x in final_matches]))

    keyboard.on_press(fake)

    location = pyautogui.locateCenterOnScreen("dark.png", confidence=0.8)

    if not location:
        location = pyautogui.locateCenterOnScreen("light.png", confidence=0.8)

    if location:
        x, y = location
        pyautogui.click(x, y)

    t = 1
    for match in final_matches:
        if stop != '':
            stop = ''
            break
        if fake_letter == '':
            time.sleep(t)
            storage.remove(match)
            keyboard.write(match)
            keyboard.press('enter')
        else:
            changed_matches = [x for x in storage if fake_letter not in x]
            for changed_match in changed_matches:
                time.sleep(t)
                keyboard.write(changed_match)
                keyboard.press('enter')
                t = 2
            fake_letter = ''
            break
        t = 2
    keyboard.unhook_all()
