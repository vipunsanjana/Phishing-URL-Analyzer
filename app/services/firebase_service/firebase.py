import firebase_admin
from firebase_admin import credentials, firestore, storage, initialize_app
from google.api_core.exceptions import GoogleAPIError
from app.utils import constants, config
import asyncio

async def initialize_firebase():
    """
    Initializes the Firebase application asynchronously.
    
    Returns:
        db (Firestore client): The Firestore client instance.
        bucket (Storage bucket): The Firebase storage bucket instance.
    
    Raises:
        Exception: If Firebase initialization fails.
    """
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(config.FIREBASE_CREDENTIALS)
            initialize_app(cred, {'storageBucket': config.BUCKET_NAME})
            constants.LOGGER.info("Firebase initialized successfully.")

        bucket = storage.bucket(config.BUCKET_NAME)
        return bucket
    except Exception as e:
        constants.LOGGER.error(f"Error initializing Firebase: {str(e)}")
        raise Exception(f"Error initializing Firebase: {e}")

async def upload_image_and_get_url(image_buffer, destination_blob_name: str) -> str:
    """
    Asynchronously uploads an image to Firebase Storage and returns the public URL of the uploaded image.
    
    Args:
        image_buffer (bytes): The image content as a byte stream.
        destination_blob_name (str): The destination name (path) for the image in Firebase Storage.
    
    Returns:
        str: The public URL of the uploaded image.
    
    Raises:
        Exception: If there is an error during the upload process.
    """
    try:
        bucket = await initialize_firebase()

        if not bucket:
            constants.LOGGER.error("Failed to retrieve Firebase storage bucket.")
            raise Exception("Failed to retrieve Firebase storage bucket.")

        blob = bucket.blob(destination_blob_name)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, blob.upload_from_string, image_buffer, "image/png")
        await loop.run_in_executor(None, blob.make_public)
        
        return blob.public_url
    except GoogleAPIError as e:
        constants.LOGGER.error(f"Google API Error during image upload: {e}")
        raise Exception(f"Google API Error during upload: {e}")
    except Exception as e:
        constants.LOGGER.error(f"Error during image upload: {e}")
        raise Exception(f"Error during upload: {e}")
