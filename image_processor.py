from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import math

modify_array = None

def unscramble_image_old(a0, a1, a2, image_path):
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        print(f"Image '{image_path}' opened successfully. Mode: {img.mode}, Size: {img.size}")

        sy = img.size[0]
        sx = img.size[1]
        r1 = np.zeros((sx, sy))
        r2 = np.zeros((sx, sy))
        modified_array = np.zeros((sx, sy, 4), dtype=np.uint8)
        for x in range(0, sx):
            for y in range(0, sy):
                radius = math.sqrt(pow(x - round(sx / 2), 2) + pow(y - round(sy / 2), 2))
                r1[x, y] = math.cos(x)
                r2[x, y] = math.cos(
                    x * math.cos(math.radians(a0 + (x * a1))) + y * math.sin(math.radians(a0 + (y * a2))))

        # Convert the image to a NumPy array
        img_array = np.array(img, dtype=np.int16)
        print(f"Image converted to NumPy array. Shape: {img_array.shape}, Dtype: {img_array.dtype}")

        # Ensure array is of a type that can be divided (e.g., float or int)
        # and handle potential alpha channels (e.g., RGBA)
        if img_array.dtype == np.int16:
            # img_array = img_array.view('<f4').reshape((1200, 1920))
            # Perform pixel manipulation: divide each pixel value by 2
            # Integer division is used here
            for x in range(0, sx):
                for y in range(0, sy):

                    # modified_array[x, y, 0] = img_array[x, y] / r2[x, y] / r1[x, y]
                    # modified_array[x, y, 1] = img_array[x, y] / r2[x, y] / r1[x, y]
                    # modified_array[x, y, 2] = img_array[x, y] / r2[x, y] / r1[x, y]
                    # modified_array[x, y, 3] = 255
                    pixel = img_array[x, y, 2]
                    pixel *= 4
                    pixel = (pixel / 1000) + img_array[x, y, 1]
                    pixel *= 4
                    pixel = (pixel / 1000) + img_array[x, y, 0]
                    if img_array[x, y, 3] == 254:
                        pixel *= -1
                    p = pixel / r1[x, y] / r2[x, y]
                    p = p + 128
                    p = p if p <= 255 else 255
                    p = p if p >= 0 else 0
                    modified_array[x, y, 0] = round(p) if p <= 255 else 255
                    modified_array[x, y, 1] = round(p) if p <= 255 else 255
                    modified_array[x, y, 2] = round(p) if p <= 255 else 255
                    modified_array[x, y, 3] = 255

        else:
            # If not uint8, convert to a type that supports division and then back if necessary
            # This is a simplification; robust handling might require type checks and conversions
            print(f"Warning: Image array dtype is {img_array.dtype}. Attempting conversion for division.")
            modified_array = (img_array / 2).astype(img_array.dtype)

        print(f"Pixel values divided by 2. New min/max: {modified_array.min()}/{modified_array.max()}")

        # Convert the modified NumPy array back to a Pillow image
        # The mode might need to be explicitly set if it changed or is ambiguous
        modified_img = Image.fromarray(modified_array, mode=img.mode)
        print("NumPy array converted back to Pillow image.")

        # Display the resulting image using Tkinter
        print("Attempting to display the modified image using Tkinter...")

        # Comment out or remove the saving part if Tkinter is the primary display
        output_path = "un_" + image_path.split('/')[-1]
        modified_img.save(output_path)
        print(f"Modified image saved to '{output_path}'")
        return modified_img, None


    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None, None


def unscramble_image(corrections, image_path):
    global modify_array
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        print(f"Image '{image_path}' opened successfully. Mode: {img.mode}, Size: {img.size}")

        sy = img.size[0]
        sx = img.size[1]
        r1 = np.zeros((sx, sy))
        r2 = np.zeros((sx, sy))

        a0 = corrections[0]
        a1 = corrections[1]
        a2 = corrections[2]

        for x in range(0, sx):
            for y in range(0, sy):
                radius = math.sqrt(pow(x - round(sx / 2), 2) + pow(y - round(sy / 2), 2))
                r1[x, y] = math.cos(x)
                r2[x, y] = math.cos(
                    x * math.cos(math.radians(a0 + (x * a1))) + y * math.sin(math.radians(a0 + (y * a2))))

        # Convert the image to a NumPy array
        img_array = np.array(img, dtype=np.int16)
        print(f"Image converted to NumPy array. Shape: {img_array.shape}, Dtype: {img_array.dtype}")

        # Ensure array is of a type that can be divided (e.g., float or int)
        # and handle potential alpha channels (e.g., RGBA)
        if img_array.dtype == np.int16:
            # img_array = img_array.view('<f4').reshape((1200, 1920))
            # Perform pixel manipulation: divide each pixel value by 2
            # Integer division is used here
            for x in range(0, sx):
                for y in range(0, sy):

                    # modified_array[x, y, 0] = img_array[x, y] / r2[x, y] / r1[x, y]
                    # modified_array[x, y, 1] = img_array[x, y] / r2[x, y] / r1[x, y]
                    # modified_array[x, y, 2] = img_array[x, y] / r2[x, y] / r1[x, y]
                    # modified_array[x, y, 3] = 255
                    pixel = img_array[x, y, 2]
                    pixel *= 4
                    pixel = (pixel / 1000) + img_array[x, y, 1]
                    pixel *= 4
                    pixel = (pixel / 1000) + img_array[x, y, 0]
                    if img_array[x, y, 3] == 254:
                        pixel *= -1
                    p = pixel / r1[x, y] / r2[x, y]
                    p = p + 128
                    p = p if p <= 255 else 255
                    p = p if p >= 0 else 0
                    modify_array[x, y, 0] = round(p) if p <= 255 else 255
                    modify_array[x, y, 1] = round(p) if p <= 255 else 255
                    modify_array[x, y, 2] = round(p) if p <= 255 else 255
                    modify_array[x, y, 3] = 255
                # if x % 20 == 0:
                    # print("processing: {}".format(x))

        else:
            # If not uint8, convert to a type that supports division and then back if necessary
            # This is a simplification; robust handling might require type checks and conversions
            print(f"Warning: Image array dtype is {img_array.dtype}. Attempting conversion for division.")
            modify_array = (img_array / 2).astype(img_array.dtype)

        print(f"Pixel values divided by 2. New min/max: {modify_array.min()}/{modify_array.max()}")

        # Convert the modified NumPy array back to a Pillow image
        # The mode might need to be explicitly set if it changed or is ambiguous
        modified_img = Image.fromarray(modify_array, mode=img.mode)
        print("NumPy array converted back to Pillow image.")

        # Display the resulting image using Tkinter
        print("Attempting to display the modified image using Tkinter...")

        # Comment out or remove the saving part if Tkinter is the primary display
        output_path = "un_" + image_path.split('/')[-1]
        modified_img.save(output_path)
        print(f"Modified image saved to '{output_path}'")
        # return modified_img, True

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        # return None, None


def scramble_image(image_path):

    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        print(f"Image '{image_path}' opened successfully. Mode: {img.mode}, Size: {img.size}")

        sy = img.size[0]
        sx = img.size[1]
        a = [8, 1993, 4]
        r1 = np.zeros((sx, sy))
        r2 = np.zeros((sx, sy))
        # modified_array = np.zeros((sx, sy), '<f4')
        modified_array = np.zeros((sx, sy, 4), dtype='uint8')
        for x in range(0, sx):
            for y in range(0, sy):
                radius = math.sqrt(pow(x-round(sx/2), 2) + pow(y-round(sy/2), 2))
                r1[x, y] = math.cos(x)
                r2[x, y] = math.cos(x * math.cos(math.radians(a[0] + (x*a[1]))) + y*math.sin(math.radians(a[0]+(y*a[2]))))

        # Convert the image to a NumPy array
        img_array = np.array(img, dtype=np.int16)
        print(f"Image converted to NumPy array. Shape: {img_array.shape}, Dtype: {img_array.dtype}")

        # Ensure array is of a type that can be divided (e.g., float or int)
        # and handle potential alpha channels (e.g., RGBA)
        if img_array.dtype == np.int16:
            # Perform pixel manipulation: divide each pixel value by 2
            # Integer division is used here
            for x in range(0, sx):
                for y in range(0, sy):
                    # modified_array[x, y, 0] = modified_array[x, y, 0] * r1[x, y] * r2[x, y]
                    # modified_array[x, y, 1] = modified_array[x, y, 1] * r1[x, y] * r2[x, y]
                    # # modified_array[x, y, 2] = modified_array[x, y, 2] * r1[x, y] * r2[x, y]

                    p = img_array[x, y, 0] - 128
                    pixel = p * r1[x, y] * r2[x, y]
                    if pixel < 0:
                        pixel *= -1
                        modified_array[x, y, 3] = 254
                    else:
                        modified_array[x, y, 3] = 255
                    modified_array[x, y, 0] = pixel
                    pixel = (pixel - math.trunc(pixel)) * 1000
                    pixel /= 4
                    modified_array[x, y, 1] = pixel
                    pixel = (pixel - math.trunc(pixel)) * 1000
                    pixel /= 4
                    modified_array[x, y, 2] = pixel

                    # pixel = img_array[x, y, 0] if img_array[x, y, 0] > 0 else 1
                    # modified_array[x, y] = pixel * r1[x, y] * r2[x, y]

        else:
            # If not uint8, convert to a type that supports division and then back if necessary
            # This is a simplification; robust handling might require type checks and conversions
            print(f"Warning: Image array dtype is {img_array.dtype}. Attempting conversion for division.")
            modified_array = (img_array / 2).astype(img_array.dtype)

        print(f"Pixel values divided by 2. New min/max: {modified_array.min()}/{modified_array.max()}")

        # Convert the modified NumPy array back to a Pillow image
        # The mode might need to be explicitly set if it changed or is ambiguous
        # modified_array = modified_array.astype(np.uint8)
        #array_8 = modified_array.view(dtype='uint8')
        #array_8 = array_8.reshape((1200, 1920, 4))
        #modified_img = Image.fromarray(array_8, mode=img.mode)
        modified_img = Image.fromarray(modified_array, mode=img.mode)
        print("NumPy array converted back to Pillow image.")

        # Display the resulting image using Tkinter
        print("Attempting to display the modified image using Tkinter...")

        # Comment out or remove the saving part if Tkinter is the primary display
        output_path = "scrambled_" + image_path.split('/')[-1]
        modified_img.save(output_path)
        print(f"Modified image saved to '{output_path}'")
        return output_path, None


    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None, None


def process_image(image_path):
    """
    Opens a PNG image, divides its pixel values by 2, and displays it.

    Args:
        image_path (str): The path to the PNG image file.
    """
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        print(f"Image '{image_path}' opened successfully. Mode: {img.mode}, Size: {img.size}")

        # Convert the image to a NumPy array
        img_array = np.array(img)
        print(f"Image converted to NumPy array. Shape: {img_array.shape}, Dtype: {img_array.dtype}")

        # Ensure array is of a type that can be divided (e.g., float or int)
        # and handle potential alpha channels (e.g., RGBA)
        if img_array.dtype == np.uint8:
            # Perform pixel manipulation: divide each pixel value by 2
            # Integer division is used here
            modified_array = img_array // 1
        else:
            # If not uint8, convert to a type that supports division and then back if necessary
            # This is a simplification; robust handling might require type checks and conversions
            print(f"Warning: Image array dtype is {img_array.dtype}. Attempting conversion for division.")
            modified_array = (img_array / 2).astype(img_array.dtype)

        print(f"Pixel values divided by 2. New min/max: {modified_array.min()}/{modified_array.max()}")

        # Convert the modified NumPy array back to a Pillow image
        # The mode might need to be explicitly set if it changed or is ambiguous
        modified_img = Image.fromarray(modified_array, mode=img.mode)
        print("NumPy array converted back to Pillow image.")

        # Display the resulting image using Tkinter
        print("Attempting to display the modified image using Tkinter...")
        
        # Comment out or remove the saving part if Tkinter is the primary display
        # output_path = "modified_" + image_path.split('/')[-1]
        # modified_img.save(output_path)
        # print(f"Modified image saved to '{output_path}'")
        return modified_img, None


    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None, None


if __name__ == '__main__':
    # Create a dummy PNG image for testing if one doesn't exist.
    # This part requires Pillow and NumPy to create the dummy image.
    # So, if they are not installed, this test setup will also fail.
    try:
        from PIL import Image, ImageDraw
        import numpy as np
        
        dummy_image_path = "scrambled_dummy_test_image_no_a.png"

        # Check if dummy image already exists
        try:
            with open(dummy_image_path, 'rb') as f:
                print(f"Dummy image '{dummy_image_path}' already exists.")
        except FileNotFoundError:
            print(f"Creating dummy image '{dummy_image_path}' for testing.")
            # Create a small RGBA image (10x10 pixels)
            img_data = np.zeros((10, 10, 4), dtype=np.uint8)
            img_data[:, :, 0] = 255  # Red channel
            img_data[:, :, 1] = 150  # Green channel
            img_data[:, :, 2] = 50   # Blue channel
            img_data[:, :, 3] = 255  # Alpha channel (fully opaque)
            
            dummy_img = Image.fromarray(img_data, 'RGBA')
            dummy_img.save(dummy_image_path)
            print(f"Dummy image '{dummy_image_path}' created and saved.")

        # Test the process_image function
        print(f"\nProcessing image: {dummy_image_path}")
        # The function will now block until the Tkinter window is closed.
        # save_path will be None if Tkinter display succeeds.
        # processed_image, display_info = process_image(dummy_image_path)
        # processed_image, display_info = scramble_image(dummy_image_path)
        # processed_image, display_info = unscramble_image(8, 1993, 4, dummy_image_path)
        processed_image, display_info = unscramble_image(8, 0, 4, dummy_image_path)
        if processed_image:
            if display_info is None: # Assuming None means Tkinter showed and closed
                print(f"Image processing and Tkinter display initiated. Window needs to be closed manually to continue.")
            else: # Assuming display_info contains output_path due to fallback
                print(f"Image processing successful. Tkinter display failed or was skipped, image saved to: {display_info}")
        else:
            print("Image processing failed.")

    except ImportError as e:
        # Catching specific import errors if needed for the main block
        print(f"Cannot run main test block due to Import Error: {e}. Ensure Pillow, NumPy, and Tkinter are available.")
    except Exception as e:
        print(f"Error in main test block: {e}")
