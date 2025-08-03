import pyautogui
import time
import random
import string

print("Realistic keep-awake script started. Press Ctrl+C to stop.")

def random_typing():
    # Type 1–3 random letters
    length = random.randint(1, 3)
    text = ''.join(random.choices(string.ascii_letters, k=length))
    pyautogui.typewrite(text)
    for _ in range(len(text)):
        pyautogui.press('backspace')

def random_mouse_move():
    # Get screen si
    screenWidth, screenHeight = pyautogui.size()
    # Move to random nearby po
    x = random.randint(0, screenWidth)
    y = random.randint(0, screenHeight)
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))

try:
    while True:
        # Randomly decide what
        action = random.choice(['move', 'type', 'both'])
        if action == 'move':
            random_mouse_move()
        elif action == 'type':
            random_typing()
        else:
            random_mouse_move()
            time.sleep(0.5)
            random_typing()

        # Wait 10–30 seconds
        time.sleep(random.uniform(10, 30))

except KeyboardInterrupt:
    print("\nStopped by user.")