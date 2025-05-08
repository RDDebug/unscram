from PIL import Image
import numpy as np

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
            modified_array = img_array // 2
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

        # Display the resulting image
        # In a script environment without a GUI, 'showing' an image might mean saving it
        # or just returning the object for further processing.
        # For now, let's try to show it, though it might not work in all environments.
        # If img.show() doesn't work or is not appropriate, this can be changed to saving the image.
        print("Attempting to display/save the modified image...")
        
        # Let's save it instead of displaying, as display might not work
        output_path = "modified_" + image_path.split('/')[-1]
        modified_img.save(output_path)
        print(f"Modified image saved to '{output_path}'")
        
        return modified_img, output_path

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None, None
    except ImportError:
        print("Error: Pillow (PIL) or NumPy library is not installed.")
        print("Please ensure Pillow and NumPy are installed to process images.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == '__main__':
    # Create a dummy PNG image for testing if one doesn't exist.
    # This part requires Pillow and NumPy to create the dummy image.
    # So, if they are not installed, this test setup will also fail.
    try:
        from PIL import Image, ImageDraw
        import numpy as np
        
        dummy_image_path = "dummy_test_image.png"

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
        processed_image, save_path = process_image(dummy_image_path)
        if processed_image:
            print(f"Image processing apparently successful. Modified image saved to {save_path}")
            # In a real scenario, you might want to verify the content of 'save_path'
        else:
            print("Image processing failed.")

    except ImportError:
        print("Cannot run main test block: Pillow or NumPy not available to create/process dummy image.")
    except Exception as e:
        print(f"Error in main test block: {e}")
