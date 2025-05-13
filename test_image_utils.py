import unittest
import os
from PIL import Image
from unittest.mock import patch

# Assuming image_utils.py is in the same directory or accessible via PYTHONPATH
import image_utils

class TestImageUtils(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        self.test_input_filename = "test_input.png"
        self.test_output_filename = "test_output.png"

        # Create a simple 16x16 image with two colors (half red, half blue)
        img = Image.new('RGB', (16, 16))
        pixels = img.load()
        for i in range(16):
            for j in range(16):
                if j < 8:
                    pixels[i, j] = (255, 0, 0)  # Red
                else:
                    pixels[i, j] = (0, 0, 255)  # Blue
        img.save(self.test_input_filename)
        self.input_image = Image.open(self.test_input_filename)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        if os.path.exists(self.test_input_filename):
            os.remove(self.test_input_filename)
        if os.path.exists(self.test_output_filename):
            os.remove(self.test_output_filename)
        self.input_image.close()

    # --- Tests for pixelate_image ---
    def test_pixelate_returns_image_object(self):
        pixelated_img = image_utils.pixelate_image(self.input_image, 4)
        self.assertIsInstance(pixelated_img, Image.Image)

    def test_pixelate_output_dimensions(self):
        pixelated_img = image_utils.pixelate_image(self.input_image, 4)
        self.assertEqual(pixelated_img.size, self.input_image.size)

    def test_pixelate_effect(self):
        pixel_size = 4
        pixelated_img = image_utils.pixelate_image(self.input_image, pixel_size)
        # Check the color of the top-left pixel block
        block_color = pixelated_img.getpixel((0, 0))
        for i in range(pixel_size):
            for j in range(pixel_size):
                self.assertEqual(pixelated_img.getpixel((i, j)), block_color, 
                                 f"Pixel at ({i},{j}) does not match block color.")

    def test_pixelate_size_one(self):
        # With pixel_size=1, the image should be very similar (though not necessarily identical due to processing)
        pixelated_img = image_utils.pixelate_image(self.input_image, 1)
        # A simple check is to compare a few sample pixels or a histogram if complex.
        # For now, let's check dimensions and that it's not a completely different image.
        self.assertEqual(pixelated_img.size, self.input_image.size)
        # Compare a sample pixel - it should be very close if not identical
        # Note: Bilinear downscale then nearest upscale can alter pixels even at size 1
        # A more robust test might involve image difference metrics, but this is a basic check.
        original_pixel = self.input_image.getpixel((0,0))
        pixelated_pixel = pixelated_img.getpixel((0,0))
        # Allowing for some minor difference due to resampling
        self.assertTrue(
            all(abs(original_pixel[k] - pixelated_pixel[k]) < 10 for k in range(3)),
            "Pixel color changed significantly with pixel_size=1"
        )


    # --- Tests for dither_image ---
    def test_dither_returns_image_object(self):
        dithered_img = image_utils.dither_image(self.input_image, 16)
        self.assertIsInstance(dithered_img, Image.Image)

    def test_dither_output_mode_palettized(self):
        dithered_img = image_utils.dither_image(self.input_image, 16)
        self.assertEqual(dithered_img.mode, 'P', "Image mode should be 'P' (palettized).")

    def test_dither_palette_size(self):
        palette_size_target = 8 # Test with a smaller palette
        dithered_img = image_utils.dither_image(self.input_image, palette_size_target)
        palette = dithered_img.getpalette()
        self.assertIsNotNone(palette)
        # Number of colors in palette. Palette is a flat list [r,g,b,r,g,b,...]
        num_colors = len(palette) // 3
        self.assertLessEqual(num_colors, palette_size_target)
        # Also ensure there are some colors, not an empty palette (unless palette_size_target is 0 or 1)
        if palette_size_target > 0:
            self.assertGreater(num_colors, 0, "Dithered image has no colors in its palette.")


    # --- Tests for pixelate_and_dither_image (Integration) ---
    def test_process_creates_output_file(self):
        image_utils.pixelate_and_dither_image(self.test_input_filename, self.test_output_filename, 4, 16)
        self.assertTrue(os.path.exists(self.test_output_filename))

    @patch('builtins.print') # Mock print to capture stdout/stderr messages
    def test_process_handles_nonexistent_input(self, mock_print):
        non_existent_input = "non_existent_image.png"
        image_utils.pixelate_and_dither_image(non_existent_input, self.test_output_filename, 4, 16)
        
        # Check that an error message was printed (order of calls might vary)
        # Example: "Error: Input file not found at 'non_existent_image.png'"
        # We assert that at least one call to print contains "Error: Input file not found"
        error_message_found = False
        for call_args in mock_print.call_args_list:
            if "Error: Input file not found" in call_args[0][0]:
                error_message_found = True
                break
        self.assertTrue(error_message_found, "Error message for non-existent input not printed.")
        self.assertFalse(os.path.exists(self.test_output_filename), "Output file should not be created on input error.")

    def test_process_output_image_properties(self):
        image_utils.pixelate_and_dither_image(self.test_input_filename, self.test_output_filename, 4, 16)
        self.assertTrue(os.path.exists(self.test_output_filename))
        try:
            processed_img = Image.open(self.test_output_filename)
            self.assertEqual(processed_img.mode, 'P', "Processed image mode should be 'P'.")
            # Check dimensions match original
            self.assertEqual(processed_img.size, self.input_image.size, "Processed image dimensions do not match input.")
        except FileNotFoundError:
            self.fail(f"Output file {self.test_output_filename} was not created.")
        except Exception as e:
            self.fail(f"Error opening or validating processed image: {e}")
        finally:
            if 'processed_img' in locals():
                processed_img.close()

if __name__ == '__main__':
    unittest.main()
