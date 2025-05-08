import tkinter as tk
import random
import time

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


def build_wait_list(max_wait):
    global array_size
    waits = [0] * array_size
    for i, v in enumerate(waits):
        waits[i] = random.choice([100, 300, 500, 1000])
    ratio = (max_wait * 1000) / sum(waits)
    adj_waits = [int(num * ratio) for num in waits]
    return adj_waits


def update_label():
    global binary_label, count, binary_string, attempt_label, wait_list, array_size
    # Update the label's text with new content
    binary_string += random.choice('01')
    binary_label.config(text=binary_string)
    if count < array_size:
        root.after(wait_list[count], update_label)
        count += 1
    elif attempt < 3:
        show_failure_message()
    else:
        show_success_message()


def first_download():
    global label, button, binary_label, root, binary_string, attempt_label
    if label:
        label.pack_forget()
    if button:
        button.pack_forget()

    binary_string = ''
    attempt_label = tk.Label(root, text="Attempt #{}".format(attempt))
    binary_label = tk.Label(root, text=binary_string, wraplength=280)  # Wrap text if needed
    attempt_label.pack(pady=10)
    binary_label.pack(pady=10)
    start_download_process()


# --- Functions for button actions ---
def start_download_process():
    """Clears initial widgets, shows binary string, schedules failure message."""
    global label, button, binary_label, root, binary_string, atempt_label, wait_list

    binary_string = ''
    attempt_label.config(text="Attempt #{}".format(attempt))
    wait_list = build_wait_list(10)
    update_label()


def show_failure_message():
    """Clears binary label and shows failure message."""
    global binary_label, failure_label, root, label, attempt, count
    attempt += 1
    count = 0
    binary_label.config(text="Download Failed")
    root.after(5000, start_download_process)


def show_success_message():
    """Clears binary label and shows failure message."""
    global binary_label, failure_label, root, label
    binary_label.config(text="Possible success. Data being prepare. Standby")
    #root.after(5000, start_download_process)



# --- Initialize GUI elements ---
# Create initial label widget
label = tk.Label(root, text="Download Satellite database")
label.pack(pady=10)

# Create initial button widget
button = tk.Button(root, text="Begin", command=first_download) # Assign command
button.pack(pady=5)

# Note: We are not calling root.mainloop() here as per the instructions.
# The mainloop will be started in the main application script.

# Optional: Set a default window size (can be adjusted later)
root.geometry("300x150")

# Start the Tkinter event loop
root.mainloop()
