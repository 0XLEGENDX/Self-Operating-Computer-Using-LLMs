
from PIL import ImageGrab 

screenshot_save = ""

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("temp.png")
    global screenshot_save
    screenshot_save = screenshot
    return screenshot

def fetch_screenshot():
    return screenshot_save

