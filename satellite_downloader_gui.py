import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Satellite Downloader")

# --- Global variables for widgets ---
label = None
button = None
binary_label = None
failure_label = None

# --- Functions for button actions ---
def start_download_process():
    """Clears initial widgets, shows binary string, schedules failure message."""
    global label, button, binary_label, root
    if label:
        label.pack_forget()
    if button:
        button.pack_forget()

    # Generate random binary string
    binary_string = ''.join(random.choice('01') for _ in range(50))

    # Create and display binary label
    binary_label = tk.Label(root, text=binary_string, wraplength=280) # Wrap text if needed
    binary_label.pack(pady=10)

    # Schedule the failure message
    root.after(3000, show_failure_message)

def show_failure_message():
    """Clears binary label and shows failure message."""
    global binary_label, failure_label, root
    if binary_label:
        binary_label.pack_forget()

    # Create and display failure label
    failure_label = tk.Label(root, text="Download Failed")
    failure_label.pack(pady=10)


# --- Initialize GUI elements ---
# Create initial label widget
label = tk.Label(root, text="Download Satellite database")
label.pack(pady=10)

# Create initial button widget
button = tk.Button(root, text="Begin", command=start_download_process) # Assign command
button.pack(pady=5)

# Note: We are not calling root.mainloop() here as per the instructions.
# The mainloop will be started in the main application script.

# Optional: Set a default window size (can be adjusted later)
root.geometry("300x150")

# Start the Tkinter event loop
root.mainloop()
