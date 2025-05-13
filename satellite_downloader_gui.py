import time
import tkinter as tk
import random
from tkinter import font, simpledialog, messagebox
import threading

import numpy as np

import image_processor
from PIL import Image, ImageTk

# --- Global variables for widgets ---
root = None
label = None
end_label = None
time_label = None
start_time = 0
button = None
tx_button = None
back_button = None
attempt_label = None
binary_label = None
failure_label = None
image_label = None
binary_string = ''
count = 0
attempt = 1
wait_list = []
array_size = 100
downloading = False
complete = False
solved = False
processing = False
image_thread = None
corrections = [16, 1994, 3]
corrections_truth = [8, 1993, 4]


def gui_init(new_root):
    global root, button, image_label

    root = new_root
    button = tk.Button(text="Begin", command=start_session, font=font.Font(size=60))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                           # Note: We are not calling root.mainloop() here as per the instructions.
    # The mainloop will be started in the main application script.
    root.attributes('-fullscreen', True)
    # Optional: Set a default window size (can be adjusted later)
    # root.geometry("300x150")

    image_label = tk.Label(root)

    image_processor.modify_array = np.zeros((1200, 1920, 4), dtype=np.uint8)
    image_processor.modify_array[:, :, 3] = 255  # Alpha channel (fully opaque)

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


def get_time():
    global start_time
    end_time = time.time()
    difference = end_time - start_time

    minutes, seconds = divmod(int(difference), 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def update_time():
    global time_label
    time_label.config(text=get_time())
    root.after(1000, update_time)


def start_session():
    global start_time, time_label, end_label, tx_button, label, button, back_button, image_label
    start_time = time.time()

    time_label = tk.Label(root, text="", font=font.Font(size=25))
    time_label.place(anchor="se", relx=0.98, rely=0.98)
    update_time()

    tx_button = tk.Button(root, text="Transmit Location to Range Control", command=tx_location, font=font.Font(size=40))  # Assign command
    tx_button.place(relx=0.5, rely=0.4, anchor="s")
    button.config(text="Download Satellite database", command=download_database, font=font.Font(size=40))  # Assign command
    button.place(relx=0.5, rely=0.6, anchor="n")
    # button.place_forget()
    # button.pack(pady=5)
    back_button = tk.Button(root, text="Back", command=return_to_start)


# def start_main_page
#     binary_label = tk.Label(root, text=binary_string, width=1000, wraplength=1000, anchor="w", justify="left"


def return_to_start():
    global image_label, label, back_button, binary_label, attempt_label, attempt, downloading
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
    tx_button.place(relx=0.5, rely=0.4, anchor="s")
    button.place(relx=0.5, rely=0.6, anchor="n")
    downloading = False
    attempt = 0


def tx_location():
    input1 = simpledialog.askstring("Connected to Range Control", "Enter your position")

    if input1 == "abc":
        messagebox.showinfo("Success", "Location successfully logged. Live arms test is being diverted from your location.")
    elif input1 is not None:
        messagebox.showwarning("error", "Invalid Location")
    print(input1)


def build_wait_list(max_wait):
    global array_size
    waits = [0] * array_size
    for i, v in enumerate(waits):
        waits[i] = random.choice([100, 300, 500, 1000])
    ratio = (max_wait * 1000) / sum(waits)
    adj_waits = [int(num * ratio) for num in waits]
    return adj_waits


def update_label():
    global binary_label, count, binary_string, wait_list, array_size
    # Update the label's text with new content
    binary_string += random.choice('01')
    binary_label.config(text=binary_string)
    if downloading:
        if count < array_size:
            root.after(wait_list[count], update_label)
            count += 1
        elif attempt < 3:
            show_failure_message()
        else:
            show_success_message()


def first_download():
    global binary_label, root, binary_string, attempt_label, downloading

    binary_string = ''
    attempt_label = tk.Label(root, text="Attempt #{}".format(attempt))
    binary_label = tk.Label(root, text=binary_string, width=1000, wraplength=1000, anchor="w", justify="left")  # Wrap text if needed
    attempt_label.pack(pady=10)
    binary_label.pack(pady=10)

    downloading = True


    start_download_process()


# --- Functions for button actions ---
def start_download_process():
    """Clears initial widgets, shows binary string, schedules failure message."""
    global binary_string, wait_list, attempt_label

    binary_string = ''
    attempt_label.config(text="Attempt #{}".format(attempt))
    wait_list = build_wait_list(1)
    update_label()


def show_failure_message():
    """Clears binary label and shows failure message."""
    global binary_label, attempt, count, root, binary_string
    attempt += 1
    count = 0
    binary_label.config(text=binary_string + "\n\nDownload Failed. Reaquiring signal... Standby...")
    root.after(2000, start_download_process)


def show_success_message():
    """Clears binary label and shows failure message."""
    global binary_label, binary_string
    binary_label.config(text=binary_string + "\n\nPossible success. Data being prepare. Standby")
    root.after(1000, prepare_image)


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


def prepare_image():
    global attempt_label, binary_label, image_label, complete
    attempt_label.pack_forget()
    binary_label.pack_forget()
    image_label.pack()
    image_label.lower()
    root.after(1000, build_image)


def update_image():
    global processing, image_thread, image_label, complete
    banlk_img = Image.fromarray(image_processor.modify_array, 'RGBA')
    tk_image = ImageTk.PhotoImage(banlk_img)
    image_label.config(image=tk_image)
    image_label.image = tk_image
    if image_thread is None or image_thread.is_alive():
        root.after(10, update_image)
    else:
        image_thread.join()
        image_thread = None
        complete = True
        processing = False
        root.after(500, check_corrections)


def check_corrections():
    global corrections, corrections_truth
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
        root.after(0, build_image)



def get_corrections():

    return input1, input2, input3


def build_image_old():
    global complete, processing
    dummy_image_path = "scrambled_dummy_test_image_no_a.png"
    processing = True

    image_processor.modify_array = np.zeros((1200, 1920, 4), dtype=np.uint8)
    # img_data[:, :, 0] = 0  # Red channel
    # img_data[:, :, 1] = 0  # Green channel
    # img_data[:, :, 2] = 0  # Blue channel
    image_processor.modify_array[:, :, 3] = 255  # Alpha channel (fully opaque)
    update_image()
    banlk_img = Image.fromarray(image_processor.modify_array, 'RGBA')
    try:
        # # Convert the Pillow Image to a PhotoImage
        # tk_image = ImageTk.PhotoImage(banlk_img)
        # # Create a Label to display the image
        # image_label.config(image=tk_image)
        # image_label.image = tk_image
        # # Keep a reference to the image to prevent garbage collection
        # image_label.lower()
        # print("sleeping: 1")
        # time.sleep(1)

        image_thread = threading.Thread(target=image_processor.unscramble_image, args=(0, 0, 0, dummy_image_path))
        image_thread.start()

        while image_thread.is_alive():

            print("sleeping: 2")
            update_image()
            time.sleep(1)

        image_thread.join()
        # gen = image_processor.unscramble_image(0, 0, 0, dummy_image_path)
        #
        # while processing:
        #     modified_img, processing = next(gen)
        #     print("beep")
        #     tk_image = ImageTk.PhotoImage(modified_img)
        #     image_label.config(image=tk_image)
        #     image_label.image = tk_image

        # for modified_img, processing in gen:
        #     # modified_img, processing = image_processor.unscramble_image(0, 0, 0, dummy_image_path)
        #     print("beep")
        #     image_label.config(image=modified_img)

        complete = True
        processing = False

        # values = get_corrections()
        # if values[0] is not None and values[1] is not None and values[2] is not None:
        #     print("Input 1:", values[0])
        #     print("Input 2:", values[1])
        #     print("Input 3:", values[2])
        # else:
        #     print("User cancelled or did not enter all inputs.")

        # Mainloop is blocking, so this return happens after window is closed.
        # The concept of 'output_path' is less relevant if we are displaying directly.
    except tk.TclError as e:
        print(
            f"Tkinter error: {e}. This might happen if there's no display environment (e.g., running in a headless server).")
        print("Falling back to saving the image.")
    except Exception as e_tk:
        print(f"An unexpected error occurred during Tkinter display: {e_tk}")
        print("Falling back to saving the image.")


def build_image():
    global complete, processing, image_thread
    dummy_image_path = "scrambled_dummy_test_image_no_a.png"
    processing = True

    update_image()
    # banlk_img = Image.fromarray(image_processor.modify_array, 'RGBA')

    image_thread = threading.Thread(target=image_processor.unscramble_image, args=(corrections, dummy_image_path))
    image_thread.start()


def load_image():
    image_label.pack()
    image_label.lower()
