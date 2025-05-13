import tkinter as tk
import random
import satellite_downloader_gui

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


def kill_program(event):
    if event.keysym.lower() == 'j' and event.state & 0x4:
        root.quit()


if __name__ == '__main__':
    satellite_downloader_gui.gui_init(root)

    root.bind("<Control-KeyPress>", kill_program)

    # Start the Tkinter event loop
    root.mainloop()
