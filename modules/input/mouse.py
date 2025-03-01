import sys
import time

if sys.platform.startswith("win"):
    import ctypes
    import ctypes.wintypes

    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    MOUSEEVENTF_WHEEL = 0x0800
    MOUSEEVENTF_ABSOLUTE = 0x8000

    user32 = ctypes.windll.user32

    def move_mouse(x, y):
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        x = int(x * 65535 / screen_width)
        y = int(y * 65535 / screen_height)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)

    def left_click(x, y):
        move_mouse(x, y)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def right_click(x, y):
        move_mouse(x, y)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def double_click(x, y):
        left_click(x, y)
        time.sleep(0.1)
        left_click(x, y)

    def scroll(amount):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, amount, 0)
elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
    from Xlib import display, X
    from Xlib.ext import xtest

    d = display.Display()
    s = d.screen()
    root = s.root

    def move_mouse(x, y):
        root.warp_pointer(x, y)
        d.sync()

    def left_click(x, y):
        move_mouse(x, y)
        xtest.fake_input(d, X.ButtonPress, 1)
        xtest.fake_input(d, X.ButtonRelease, 1)
        d.sync()

    def right_click(x, y):
        move_mouse(x, y)
        xtest.fake_input(d, X.ButtonPress, 3)
        xtest.fake_input(d, X.ButtonRelease, 3)
        d.sync()

    def double_click(x, y):
        left_click(x, y)
        time.sleep(0.1)
        left_click(x, y)

    def scroll(amount):
        button = 4 if amount > 0 else 5
        for _ in range(abs(amount)):
            xtest.fake_input(d, X.ButtonPress, button)
            xtest.fake_input(d, X.ButtonRelease, button)
        d.sync()

else:
    raise SystemError("Unsupported OS")


if __name__ == "__main__":
    time.sleep(2) 
    print("Moving mouse to (500, 500)")
    move_mouse(500, 500)

    print("Scrolling up")
    scroll(5)
