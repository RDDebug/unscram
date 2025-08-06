import csv
import os.path
import time
import tkinter as tk
import random
from tkinter import font, simpledialog, messagebox
import threading

import numpy as np

import image_processor
from PIL import Image, ImageTk

# --- Global variables for widgets ---
import image_utils
from images.ascii_art import *

root = None
image_controls = None
label = None
end_label = None
time_label = None
start_time = 0
cur_time = 0
delta_time = 0
game_complete = False
button = None
tx_button = None
back_button = None
validate_button = None
attempt_label = None
binary_label = None
failure_label = None
image_label = None
binary_string = ''
download_string = ''
count = 0
attempt = 1
wait_list = []
array_size = len(art_0)
downloading = False
complete = False
solved = False
processing = False
image_thread = None
corrections = [16, 1994, 3]
corrections_truth = [8, 1993, 4]
correction_labels = [None, None, None]
correction_inputs = [None, None, None]
correction_vars = [None, None, None]
team_name_var = None
team_name_input = None
unmatched_ct = 0
image_steps = 20
image_gen = None
scores = []


def gui_init(new_root):
    global root, button, image_label, correction_vars, correction_labels, correction_inputs, validate_button, \
        image_controls, team_name_var, team_name_input

    root = new_root
    button = tk.Button(text="Begin Scenario", command=start_session, font=font.Font(size=100), state=tk.DISABLED)
    button.place(relx=0.5, rely=0.5, anchor=tk.N)

    team_name_var = tk.StringVar()
    team_name_var.set("Team Name")
    team_name_input = tk.Entry(root, textvariable=team_name_var, font=font.Font(size=100), width=15)
    team_name_input.bind("<KeyRelease>", check_game_start)
    team_name_input.place(relx=0.5, rely=0.5, anchor=tk.S)

    # Note: We are not calling root.mainloop() here as per the instructions.
    # The mainloop will be started in the main application script.
    root.attributes('-fullscreen', True)
    # Optional: Set a default window size (can be adjusted later)
    # root.geometry("300x150")

    image_label = tk.Label(root)

    image_processor.modify_array = np.zeros((1080, 1920, 4), dtype=np.uint8)
    image_processor.modify_array[:, :, 3] = 255  # Alpha channel (fully opaque)

    image_controls = tk.Frame(root)
    vcmd = root.register(valid_input)
    correction_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
    correction_labels = [tk.Label(image_controls, text=s, width=10, justify="center") for s in
                         ["Tropo", "Iono", "Clock"]]
    correction_inputs = [
        tk.Entry(image_controls, textvariable=correction_vars[i], validate="key", validatecommand=(vcmd, "%P"),
                 width=10) for i in range(0, 3)]
    validate_button = tk.Button(image_controls, text="Apply Corrections", command=update_image, font=font.Font(size=10),
                                width=30)
    for i in range(0, 3):
        correction_labels[i].grid(row=0, column=i)
        correction_inputs[i].grid(row=1, column=i)
    validate_button.grid(row=3, column=0, columnspan=3)

    # global end_label, tx_button, label, button, back_button, image_label
    # # --- Initialize GUI elements ---
    # # Create initial label widget
    # # label = tk.Label(root, text="Download Satellite database", font=font.Font(size=60))
    # # label.pack(pady=10)
    # # end_label = tk.Label(root, text="Download Satellite database", font=font.Font(size=60))
    # # label.pack(pady=10)
    #
    # # Create initial button widget
    # tx_button = tk.Button(root, text="Transmit Location to Range Control", command=tx_location, font=font.Font(size=30))  # Assign command
    # tx_button.pack(pady=5)
    # button = tk.Button(root, text="Download Satellite database", command=download_database, font=font.Font(size=30))  # Assign command
    # button.pack(pady=5)
    # back_button = tk.Button(root, text="Back", command=return_to_start)


def check_game_start(event=None):
    global button
    text = team_name_input.get()
    if len(text) > 3 and text not in "Team Name":
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)


def get_time():
    global start_time, delta_time
    end_time = time.time()
    delta_time = end_time - start_time

    minutes, seconds = divmod(int(delta_time), 60)
    hours, minutes = divmod(minutes, 60)

    color = "black"
    if delta_time > 2700:
        color = "red" if int(delta_time) % 2 else "black"
        # print(difference % 2)
    if delta_time > 3600:
        color = "red"
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), color


def update_time():
    global time_label, cur_time
    if not game_complete:
        cur_time, c = get_time()
        time_label.config(text=cur_time, fg=c)

        root.after(1000, update_time)


def start_session():
    global start_time, time_label, end_label, tx_button, label, button, back_button, image_label, team_name_input
    start_time = time.time()

    time_label = tk.Label(root, text="", font=font.Font(size=25))
    time_label.place(anchor="se", relx=0.98, rely=0.98)
    update_time()

    team_name_input.place_forget()

    tx_button = tk.Button(root, text="Transmit Location to Range Control", command=tx_location,
                          font=font.Font(size=40))  # Assign command
    tx_button.place(relx=0.5, rely=0.4, anchor="s")
    button.config(text="Download Satellite database", command=download_database,
                  font=font.Font(size=40))  # Assign command
    button.place(relx=0.5, rely=0.6, anchor="n")
    # button.place_forget()
    # button.pack(pady=5)
    back_button = tk.Button(root, text="Back", command=return_to_start)


# def start_main_page
#     binary_label = tk.Label(root, text=binary_string, width=1000, wraplength=1000, anchor="w", justify="left"


def return_to_start():
    global image_label, label, back_button, binary_label, attempt_label, attempt, downloading, image_controls
    if image_label:
        image_label.pack_forget()
    if label:
        label.pack_forget()
    if back_button:
        back_button.place_forget()
    if binary_label:
        binary_label.pack_forget()
    if attempt_label:
        attempt_label.pack_forget()
    if image_controls:
        image_controls.place_forget()
    tx_button.place(relx=0.5, rely=0.4, anchor="s")
    button.place(relx=0.5, rely=0.6, anchor="n")
    downloading = False
    attempt = 1


def tx_location():
    global game_complete, tx_button, button, time_label, delta_time
    input1 = simpledialog.askstring("Connected to Range Control", "Enter your position")

    if input1 == "15TVG46125312":
        game_complete = True
        tx_button.place_forget()
        button.place_forget()
        time_label.config(font=font.Font(size=200))
        time_label.place(anchor="center", relx=0.5, rely=0.5)
        add_score()
        if delta_time < 3600:
            messagebox.showinfo("Success",
                                "Location successfully logged.\nLive arms test is being diverted from your location.\n"
                                "Congratulations!")
        elif delta_time < 4200:
            messagebox.showinfo("Near Success",
                                "Location successfully logged.\nUnfortunately, live arms test as already begun.\n"
                                "We are sorry...")
        else:
            messagebox.showinfo("~Success",
                                "Location successfully logged.\nThank you for participating.")
    elif input1 == "WE GIVE UP":
        game_complete = True
        tx_button.place_forget()
        button.place_forget()
        time_label.config(font=font.Font(size=200))
        time_label.place(anchor="center", relx=0.5, rely=0.5)
        add_score()
        # messagebox.showinfo("Success", "Location successfully logged. Live arms test is being diverted from your location.")
    elif input1 is not None:
        messagebox.showwarning("error", "Invalid Location Format.")
    print(input1)


def build_wait_list(max_wait):
    global array_size
    array_size = len(download_string) - download_string.count(" ") - download_string.count("\n")
    waits = [0] * array_size
    for i, v in enumerate(waits):
        waits[i] = random.choice([1, 30, 500, 1000, 8000, 20000])
    ratio = (max_wait * 1000) / sum(waits)
    adj_waits = [int(num * ratio) for num in waits]
    return adj_waits


def update_label():
    global binary_label, count, binary_string, wait_list, array_size

    if not hasattr(update_label, "wait_counter"):
        update_label.wait_counter = 0
    update_label.wait_counter += wait_list[count]

    ran_index = 0
    while binary_string[ran_index] == download_string[ran_index]:
        ran_index = random.randint(0, len(download_string)-1)
    binary_string = binary_string[:ran_index] + download_string[ran_index] + binary_string[ran_index + 1:]

    if update_label.wait_counter >= 100:
        binary_label.config(text=binary_string)
        update_label.wait_counter = 0
    # Update the label's text with new content
    # binary_string += random.choice('01')
    # binary_label.config(text=binary_string)
    if downloading:
        count += 1
        if count < array_size:
            root.after(wait_list[count], update_label)
            # print(array_size-count)
        elif attempt < 3:
            show_failure_message()
        else:
            show_success_message()


def first_download():
    global binary_label, root, binary_string, attempt_label, downloading

    # binary_string = ''
    binary_string = art_0
    attempt_label = tk.Label(root, text="Attempt #{}".format(attempt))
    binary_label = tk.Label(root, text=binary_string, width=1000, wraplength=5000, anchor="w", justify="left", font=font.Font(family="Courier", size=10))  # Wrap text if needed
    attempt_label.pack(pady=10)
    binary_label.pack(pady=10)

    downloading = True

    start_download_process()


# --- Functions for button actions ---
def start_download_process():
    """Clears initial widgets, shows binary string, schedules failure message."""
    global binary_string, wait_list, attempt_label, download_string

    binary_string = art_0
    attempt_label.config(text="Attempt #{}".format(attempt))
    if attempt == 1:
        download_string = art_1
    elif attempt == 2:
        download_string = art_2
    elif attempt == 3:
        download_string = art_3
    wait_list = build_wait_list(30)
    update_label()


def show_failure_message():
    """Clears binary label and shows failure message."""
    global binary_label, attempt, count, root, binary_string
    attempt += 1
    count = 0
    # binary_label.config(text=binary_string + "\n\nDownload Failed. Reaquiring signal... Standby...")
    error_message = "An error occurred in the download process.\n"
    if attempt == 2:
        error_message += "Recalibrating RF..."
    elif attempt == 3:
        error_message += "RF calibration verified\nAdjusting frame offset..."
    messagebox.showerror("Download Error", error_message)
    root.after(2000, start_download_process)


def show_success_message():
    """Clears binary label and shows failure message."""
    global binary_label, binary_string
    # .config(text=binary_string + "\n\nPossible success. Data being prepare. Standby")
    messagebox.showwarning("Download complete!", "Database download successful.\nSignal offsets required for full resolution")
    root.after(500, prepare_image)


def download_database():
    global label, button, root, back_button, complete
    if label:
        label.place_forget()
    if button:
        button.place_forget()
    if tx_button:
        tx_button.place_forget()

    back_button.place(x=50, y=20)
    if complete:
        load_image()
    else:
        first_download()


def valid_input(p):
    return p.isdigit() or p == ""


def prepare_image():
    global attempt_label, binary_label, image_label, complete, image_controls
    attempt_label.pack_forget()
    binary_label.pack_forget()
    image_label.pack()
    image_label.lower()
    image_controls.place(relx=0.01, rely=0.05)
    complete = True
    root.after(1000, update_image)


def update_image():
    global corrections, image_gen, image_steps, unmatched_ct, image_label
    for var in correction_vars:
        if var.get() == "":
            var.set("0")
    corrections = [int(correction.get()) for correction in correction_vars]
    if image_gen is None:
        unmatched_ct = 0
        for i in range(0, 3):
            unmatched_ct += 0 if corrections[i] == corrections_truth[i] else 1
        image_gen = image_utils.gen_animation(corrections, image_steps, unmatched_ct)
    try:
        image = next(image_gen)
        scaler = 0.663 # .78
        image = image.resize((int(1920*scaler), int(1080*scaler)))
        tkimage = ImageTk.PhotoImage(image)
        image_label.config(image=tkimage)
        image_label.image = tkimage
        root.after(50, update_image)
    except StopIteration:
        image_gen = None
        # check_corrections()


# def update_image():
#     global processing, image_thread, image_label, complete
#     banlk_img = Image.fromarray(image_processor.modify_array, 'RGBA')
#     tk_image = ImageTk.PhotoImage(banlk_img)
#     image_label.config(image=tk_image)
#     image_label.image = tk_image
#     if image_thread is None or image_thread.is_alive():
#         root.after(10, update_image)
#     else:
#         image_thread.join()
#         image_thread = None
#         complete = True
#         processing = False
#         root.after(500, check_corrections)


def check_corrections():
    global corrections, corrections_truth, correction_inputs
    corrections = [int(correction.get()) for correction in correction_inputs]
    print(corrections)
    if corrections == corrections_truth:
        messagebox.showinfo("Data Demod Success", "Data Demodulated successfully!")
    else:
        unmatched_ct = 0
        for i in [0, 1, 2]:
            unmatched_ct += 0 if corrections[i] == corrections_truth[i] else 1
        messagebox.showerror("error", "{} decoding errors detected.\nPlease provide corrections".format(unmatched_ct))
        correction_str = ["Tropo Corrections", "Iono Corrections", "Clock Correction"]
        for i, string in enumerate(correction_str):
            try:
                input1 = simpledialog.askstring(string, "Enter value for {}:".format(string))
                corrections[i] = int(input1)
            except Exception as e:
                corrections[i] = 0
        # root.after(0, build_image)


def load_image():
    image_label.pack()
    image_label.lower()
    image_controls.place(relx=0.01, rely=0.05)


def get_scores():
    if not os.path.exists("scores.csv"):
        with open("scores.csv", 'w', newline='') as f:
            pass

    data = []
    with open("scores.csv", 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(tuple(row))
    return data


def save_scores(data):
    with open("scores.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def add_score():
    global team_name_var, cur_time
    scores = get_scores()
    entry = (team_name_var.get(), cur_time)
    scores.append(entry)
    scores.sort(key=lambda x: x[1])
    save_scores(scores)
