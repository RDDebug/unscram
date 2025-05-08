from PIL import Image, ImageTk
import numpy as np
import tkinter as tk

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

        # Display the resulting image using Tkinter
        print("Attempting to display the modified image using Tkinter...")
        
        # Comment out or remove the saving part if Tkinter is the primary display
        # output_path = "modified_" + image_path.split('/')[-1]
        # modified_img.save(output_path)
        # print(f"Modified image saved to '{output_path}'")

        try:
            root = tk.Tk()
            root.title(f"Processed Image: {image_path}")
            
            # Convert the Pillow Image to a PhotoImage
            tk_image = ImageTk.PhotoImage(modified_img)
            
            # Create a Label to display the image
            image_label = tk.Label(root, image=tk_image)
            image_label.pack()
            
            # Keep a reference to the image to prevent garbage collection
            image_label.image = tk_image 
            
            print("Starting Tkinter main loop...")
            root.mainloop()
            print("Tkinter main loop finished.")
            
            # Mainloop is blocking, so this return happens after window is closed.
            # The concept of 'output_path' is less relevant if we are displaying directly.
            return modified_img, None 

        except tk.TclError as e:
            print(f"Tkinter error: {e}. This might happen if there's no display environment (e.g., running in a headless server).")
            print("Falling back to saving the image.")
            output_path = "modified_" + image_path.split('/')[-1]
            modified_img.save(output_path)
            print(f"Modified image saved to '{output_path}'")
            return modified_img, output_path
        except Exception as e_tk:
            print(f"An unexpected error occurred during Tkinter display: {e_tk}")
            print("Falling back to saving the image.")
            output_path = "modified_" + image_path.split('/')[-1]
            modified_img.save(output_path)
            print(f"Modified image saved to '{output_path}'")
            return modified_img, output_path

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None, None
    except ImportError as e_imp:
        # Check if it's Tkinter specific import error if possible
        if 'ImageTk' in str(e_imp) or 'tkinter' in str(e_imp):
            print(f"Error: Tkinter or ImageTk is not available. Cannot display image. {e_imp}")
        else:
            print(f"Error: Pillow (PIL) or NumPy library is not installed. {e_imp}")
        print("Please ensure Pillow, NumPy, and Tkinter are installed to process and display images.")
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
        # The function will now block until the Tkinter window is closed.
        # save_path will be None if Tkinter display succeeds.
        processed_image, display_info = process_image(dummy_image_path)
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
