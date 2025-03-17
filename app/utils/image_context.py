import io
from PIL import Image
from app.utils import constants

def resize_image(screenshot_buffer):
    """
    Resize an image by a given percentage and save it to the same file path.

    Args:
        image_url (str): The file path of the image to be resized.
        percentage (int, optional): The percentage by which the image should be resized. Defaults to 40.

    Returns:
        Image: The resized PIL image object.

    Raises:
        Exception: If an error occurs during image resizing.
    """
    try:
         # Open the image from the buffer
        image = Image.open(io.BytesIO(screenshot_buffer))
        
        # Calculate new dimensions (40% of original size)
        width, height = image.size
        new_width = int(width * 0.4)
        new_height = int(height * 0.4)
        
        # Resize the image using ANTIALIAS for high-quality downsampling
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save the resized image to a buffer
        resized_image_buffer = io.BytesIO()
        resized_image.save(resized_image_buffer, format="PNG")
        resized_image_buffer.seek(0)
        
        # Return the resized image as bytes
        return resized_image_buffer.getvalue()
    except Exception as e:
        constants.LOGGER.error(f"Failed to resize image: {str(e)}")
        raise Exception(f"Failed to resize image: {str(e)}")