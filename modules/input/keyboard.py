import ctypes
import time


user32 = ctypes.windll.user32

VK_CODES = {
    "A": 0x41, "B": 0x42, "C": 0x43, "D": 0x44, "E": 0x45, "F": 0x46, "G": 0x47, "H": 0x48, "I": 0x49, "J": 0x4A,
    "K": 0x4B, "L": 0x4C, "M": 0x4D, "N": 0x4E, "O": 0x4F, "P": 0x50, "Q": 0x51, "R": 0x52, "S": 0x53, "T": 0x54,
    "U": 0x55, "V": 0x56, "W": 0x57, "X": 0x58, "Y": 0x59, "Z": 0x5A,
    "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34, "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39,
    "ENTER": 0x0D, "ESC": 0x1B, "BACKSPACE": 0x08, "TAB": 0x09, "SPACE": 0x20, "SHIFT": 0x10, "CTRL": 0x11,
    "ALT": 0x12, "CAPSLOCK": 0x14, "NUMLOCK": 0x90, "SCROLLLOCK": 0x91,
    "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73, "F5": 0x74, "F6": 0x75, "F7": 0x76, "F8": 0x77, "F9": 0x78,
    "F10": 0x79, "F11": 0x7A, "F12": 0x7B,
    "LEFT": 0x25, "UP": 0x26, "RIGHT": 0x27, "DOWN": 0x28, "HOME": 0x24, "END": 0x23, "PAGEUP": 0x21, "PAGEDOWN": 0x22,
    "INSERT": 0x2D, "DELETE": 0x2E, "PRINTSCREEN": 0x2C, "WIN": 0x5B
}

def key_down(key):
    """Press down a key"""
    vk_code = VK_CODES.get(key.upper())
    if vk_code:
        user32.keybd_event(vk_code, 0, 0, 0)

def key_up(key):
    """Release a key"""
    vk_code = VK_CODES.get(key.upper())
    if vk_code:
        user32.keybd_event(vk_code, 0, 2, 0)

def press_key(key):
    """Press and release a key"""
    key_down(key)
    key_up(key)

def press_key_combination(keys_list:list):
    """Press and release a key"""
    for key in keys_list:
        key_down(key)
    for key in keys_list:
        key_up(key)

def type_string(string):
    """Type out a full string, one key at a time"""
    for char in string:
        if char.upper() in VK_CODES:
            press_key(char.upper())
        elif char == " ":
            press_key("SPACE")
        time.sleep(0.05)


if __name__ == "__main__":
    time.sleep(2)
    key_combination = ["WIN" ]
    press_key_combination(key_combination)
