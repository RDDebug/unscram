"""
Provides image manipulation functions for pixelating and dithering images.

This module contains functions to apply pixelation and Floyd-Steinberg
dithering effects to images using the Pillow library. It can be imported
into other Python scripts to use its functions directly:
  - pixelate_image(image, pixel_size)
  - dither_image(image, palette_size=16)
  - pixelate_and_dither_image(input_path, output_path, pixel_size, palette_size=16)

Alternatively, this script can be run directly from the command line
(e.g., `python image_utils.py`). When run as a script, it will interactively
prompt the user for the input image path, output image path, pixel size,
and palette size, and then process the image accordingly.
"""
import math
import random

from PIL import Image
import sys  # Added for sys.exit()

current_pix = 50
target_pix = 50
current_pal = 2
target_pal = 2


def pixelate_image(image, pixel_size):
    """Pixelates a Pillow Image object.

  Args:
    image: A Pillow Image object.
    pixel_size: The size of the pixels in the pixelated image.

  Returns:
    A Pillow Image object representing the pixelated image.
  """
    original_width, original_height = image.size

    # Calculate new dimensions, ensuring they are at least 1
    new_width = max(1, original_width // pixel_size)
    new_height = max(1, original_height // pixel_size)

    # Resize down
    # downscaled_image = image.resize((new_width, new_height), Image.Resampling.BILINEAR)
    downscaled_image = image.resize((new_width, new_height), Image.Resampling.HAMMING)

    # Resize up
    # pixelated_image = downscaled_image.resize((original_width, original_height), Image.Resampling.NEAREST)
    pixelated_image = downscaled_image.resize((original_width, original_height), Image.Resampling.BILINEAR)

    return pixelated_image


def dither_image(image, palette_size=16):
    """Applies Floyd-Steinberg dithering to a Pillow Image object.

  Args:
    image: A Pillow Image object.
    palette_size: The number of colors for quantization. Defaults to 16.

  Returns:
    A Pillow Image object representing the dithered image.
  """
    # Method 2 in quantize typically corresponds to Floyd-Steinberg dithering.
    dithered_image = image.quantize(colors=palette_size, method=2)
    return dithered_image


def pixelate_and_dither_image(input_path, output_path, pixel_size, palette_size=16):
    """Opens an image, pixelates it, dithers it, and saves the result.

  Args:
    input_path: Path to the input image file.
    output_path: Path to save the processed image file.
    pixel_size: The size of the pixels for pixelation.
    palette_size: The number of colors for dithering quantization. Defaults to 16.
  
  Side effects:
    - Prints error messages to stdout if file operations fail.
    - Saves the processed image to output_path if successful.
  """
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
        return
    except IOError:
        print(f"Error: Could not open or read input image at '{input_path}'")
        return
    except Exception as e:
        print(f"An unexpected error occurred while opening the image: {e}")
        return

    # Process the image
    pixelated_img = pixelate_image(img, pixel_size)
    dithered_pixelated_img = dither_image(pixelated_img, palette_size)

    try:
        dithered_pixelated_img.save(output_path)
        print(f"Successfully processed and saved image to '{output_path}'")
    except IOError:
        print(f"Error: Could not save image to '{output_path}'")
    except Exception as e:
        print(f"An unexpected error occurred while saving the image: {e}")


def gen_animation(sol, steps, incorrect):
    global current_pal, current_pix, target_pal, target_pix
    gen_values(sol[0], sol[1], sol[2], incorrect)
    pix_steps = range_steps(current_pix, target_pix, steps)
    pal_steps = range_steps(current_pal, target_pal, steps)
    img = Image.open("images/GPS3.png")

    for step in range(0, steps):
        pixelated = pixelate_image(img, pix_steps[step])
        dithered = dither_image(pixelated, pal_steps[step])
        current_pix = pix_steps[step]
        current_pal = pal_steps[step]
        yield dithered


def range_steps(a, b, steps):
    if steps <= 0:
        raise ValueError("Number of steps must be positive")

    step_size = (b - a) / steps
    return [int(a + i * step_size) for i in range(steps + 1)]


def gen_values(a, b, c, errors):
    global current_pal, current_pix, target_pal, target_pix
    if errors == 0:
        target_pix = 1
        target_pal = 16
    elif errors == 1:
        target_pix = random.randint(9, 22)
        target_pal = random.randint(11, 16)
    elif errors == 2:
        target_pix = random.randint(22, 36)
        target_pal = random.randint(6, 11)
    elif errors == 3:
        target_pix = random.randint(36, 50)
        target_pal = random.randint(3, 6)


if __name__ == '__main__':
    # input_path_str = input("Enter the path to the input image: ")
    # output_path_str = input("Enter the path to save the output image: ")
    input_path_str = "C:\\Users\\jsaus\\Documents\\Python_Projects\\unscram\\unscram\\images\\GPS3.png"
    output_path_str = "C:\\Users\\jsaus\\Documents\\Python_Projects\\unscram\\unscram\\images\\GPS3"
    # pixel_size_str = input("Enter the pixel size (e.g., 8): ")
    # palette_size_str = input("Enter the palette size (number of colors, e.g., 16, press Enter for default 16): ")
    a = int(input("a: "))
    b = int(input("b: "))
    c = int(input("c: "))

    gen_values(a, b, c)

    # # Validate pixel_size
    # try:
    #     pixel_size_int = int(pixel_size_str)
    #     if pixel_size_int <= 0:
    #         print("Error: Pixel size must be a positive integer.")
    #         sys.exit(1)
    # except ValueError:
    #     print("Error: Pixel size must be a number.")
    #     sys.exit(1)
    #
    # # Validate palette_size
    # if not palette_size_str:  # Check if the string is empty
    #     palette_size_int = 16  # Default value
    # else:
    #     try:
    #         palette_size_int = int(palette_size_str)
    #         if palette_size_int <= 0:
    #             print("Error: Palette size must be a positive integer.")
    #             sys.exit(1)
    #     except ValueError:
    #         print("Error: Palette size must be a number.")
    #         sys.exit(1)

    # Call the main processing function with validated inputs
    pix_steps = range_steps(current_pix, target_pix, 10)
    pal_steps = range_steps(current_pal, target_pal, 10)
    for step in range(0, 10):
        pixelate_and_dither_image(input_path_str, "{}_{}_{}.png".format(output_path_str, pix_steps[step], pal_steps[step]), pix_steps[step], pal_steps[step])
    # pixelate_and_dither_image(input_path_str, output_path_str, pixel_size_int, palette_size_int)
