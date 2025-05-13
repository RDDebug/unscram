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
from PIL import Image
import sys # Added for sys.exit()

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
  downscaled_image = image.resize((new_width, new_height), Image.Resampling.BILINEAR)

  # Resize up
  pixelated_image = downscaled_image.resize((original_width, original_height), Image.Resampling.NEAREST)

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

if __name__ == '__main__':
  input_path_str = input("Enter the path to the input image: ")
  output_path_str = input("Enter the path to save the output image: ")
  pixel_size_str = input("Enter the pixel size (e.g., 8): ")
  palette_size_str = input("Enter the palette size (number of colors, e.g., 16, press Enter for default 16): ")

  # Validate pixel_size
  try:
    pixel_size_int = int(pixel_size_str)
    if pixel_size_int <= 0:
      print("Error: Pixel size must be a positive integer.")
      sys.exit(1)
  except ValueError:
    print("Error: Pixel size must be a number.")
    sys.exit(1)

  # Validate palette_size
  if not palette_size_str: # Check if the string is empty
    palette_size_int = 16 # Default value
  else:
    try:
      palette_size_int = int(palette_size_str)
      if palette_size_int <= 0:
        print("Error: Palette size must be a positive integer.")
        sys.exit(1)
    except ValueError:
      print("Error: Palette size must be a number.")
      sys.exit(1)

  # Call the main processing function with validated inputs
  pixelate_and_dither_image(input_path_str, output_path_str, pixel_size_int, palette_size_int)
