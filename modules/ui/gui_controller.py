import uiautomation as auto
import pywinauto
from pywinauto.application import Application


def click_control(control_name: str):
    """
    Clicks on the control by its name in the specified window.
    """
    # Find the window by title
    window = auto.GetForegroundControl()

    if not window.Exists(5, 1):
        print(f"Window with title '{window.GetWindowText()}' not found.")
        return

    window.SetActive()

    # Traverse all child controls
    for control, depth in auto.WalkControl(window):
        if control.Name == control_name:
            print(f"Clicking on control: {control.Name}")
            control.Click()  # Click the control
            return

    print(f"No control with name '{control_name}' found in the window.")


def set_focus_on_control(control_name: str):
    """
    Sets focus on the control by its name in the specified window.
    """
    # Find the window by title
    window = auto.GetForegroundControl()

    if not window.Exists(5, 1):
        print(f"Window with title '{window.GetWindowText()}' not found.")
        return

    window.SetActive()

    # Traverse all child controls
    for control, depth in auto.WalkControl(window):
        if control.Name == control_name:
            print(f"Setting focus on control: {control.Name}")
            control.SetFocus()  # Focus the control
            return

    print(f"No control with name '{control_name}' found in the window.")

def send_keys_to_control(control_name: str, text: str):
    """
    Sends keys (text) to the control by its name in the specified window.
    """
    # Find the window by title
    window = auto.GetForegroundControl()

    if not window.Exists(5, 1):
        print(f"Window with title '{window.GetWindowText()}' not found.")
        return

    window.SetActive()

    # Traverse all child controls
    for control, depth in auto.WalkControl(window):
        if control.Name == control_name:
            print(f"Sending keys to control: {control.Name}")
            control.SetFocus()  # Ensure the control is focused first
            control.SendKeys(text)  # Send the text
            return

    print(f"No control with name '{control_name}' found in the window.")





def return_active_window_clickables():
    # Get the currently active window
    window = auto.GetForegroundControl()
    if not window:
        print("No active window found.")
        return

    print(f"Scanning window: {window.Name}")

    clickable_items = ""
    
    def find_and_highlight(control):
        global clickable_items
        try:
            if control.ControlType in (
                auto.ControlType.ButtonControl,
                auto.ControlType.HyperlinkControl,
                auto.ControlType.MenuItemControl,
                auto.ControlType.TabItemControl,
                auto.ControlType.ListItemControl,
                auto.ControlType.CheckBoxControl,
                auto.ControlType.EditControl,
            ):
                print(f"Found clickable: {control.Name} ({control.ControlTypeName})")
                clickable_items += f"[Name : {control.Name}\n"
            # Recursively check children

            for child in control.GetChildren():

                find_and_highlight(child)

        except Exception as e:
            pass

    # Start recursion from the root window
    find_and_highlight(window)
    return clickable_items

def get_window_handle_by_title(window_title):
    """
    Returns the window handle of the window with the specified title.
    """
    try:
        # Find the window handle using the window title
        window_handles = pywinauto.findwindows.find_windows(title=window_title)
        if window_handles:
            return window_handles[0]  # Return the first matching window handle
        else:
            print(f"No window found with title: {window_title}")
            return None
    except pywinauto.findwindows.ElementNotFoundError:
        print(f"No window found with title: {window_title}")
        return None

def bring_window_to_front(window_title):
    """
    Brings the specified window to the front by setting keyboard focus to it.
    """

    window_handle = get_window_handle_by_title(window_title)
    try:
        # Connect to the application using the window handle
        app = Application().connect(handle=window_handle)
        
        # Get the top-level window
        window = app.top_window()
        
        # Set keyboard focus to the window, bringing it to the foreground
        window.set_focus()
        print(f"Window with handle {window_handle} brought to the front.")
    except Exception as e:
        print(f"An error occurred: {e}")



def get_all_active_windows():
    """
    Returns a list of all active (open and visible) windows on the system.
    """
    active_windows = []

    # Find all top-level windows that are visible
    try:
        window_handles = pywinauto.findwindows.find_windows(visible_only=True)
        for handle in window_handles:
            window = pywinauto.findwindows.find_element(handle=handle)
            if window.visible:
                if(window.name):
                    active_windows.append(window.name)
    except pywinauto.findwindows.ElementNotFoundError:
        print("No active windows found.")


    return active_windows




# print(return_active_window_clickables())
# send_keys_to_control("Terminal 6, Code Run the command: Toggle Screen Reader Accessibility Mode for an optimized screen reader experience Use Alt+F1 for terminal accessibility help", "Hello World")

# print(get_all_active_windows())
# click_something("Minimize")

# bring_window_to_front("All Control Panel Items")
