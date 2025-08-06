import sys
import tkinter as tk
import ctypes

import satellite_downloader_gui

# Define the constants for SetThreadExecutionState
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

# Create the main window
root = tk.Tk()
root.title("Satellite Downloader")

# --- Global variables for widgets ---
label = None
button = None
attempt_label = None
binary_label = None
failure_label = None
binary_string = ''
count = 0
attempt = 1
wait_list = []
array_size = 100


def prevent_sleep():
    """Prevents the system and display from entering sleep mode."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED)
    print("Screen and system sleep prevented.")


def allow_sleep():
    """Allows the system and display to enter sleep mode again."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS) # Reset to default
    print("Screen and system sleep allowed.")


def kill_program(event):
    if event.keysym.lower() == 'j' and event.state & 0x4:
        allow_sleep()
        root.quit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        wait = int(sys.argv[1])
    else:
        wait = 90
    satellite_downloader_gui.gui_init(root, wait=wait)
    prevent_sleep()
    root.bind("<Control-KeyPress>", kill_program)
    # Ensure sleep is allowed when the application exits
    root.protocol("WM_DELETE_WINDOW", lambda: [allow_sleep(), root.destroy()])

    # Start the Tkinter event loop
    root.mainloop()
