import keyboard
from PIL import ImageGrab 
from datetime import datetime

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot1.png")
    screenshot.close()
 
keyboard.add_hotkey("ctrl+shift+a", take_screenshot)
keyboard.wait("esc")
