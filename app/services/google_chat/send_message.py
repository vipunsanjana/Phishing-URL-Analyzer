from app.utils import config, constants
from app.services.google_chat.message_template import generate_report
import requests
from app.utils.constants import VALID_CONTENT_TYPE

def send_webhook_message(payload):

    try:

        # Send the POST request
        headers = {"Content-Type": VALID_CONTENT_TYPE}
        message = generate_report(payload)
        payload_text = {
            "text": message
        }

        response = requests.post(config.WEBHOOK_URL, json=payload_text, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            constants.LOGGER.info("Message sent successfully")
            return {"message": "Message sent successfully"}
        else:
            constants.LOGGER.error(f"Failed to send message, status code: {response.status_code}")
            raise Exception(f"Failed to send message, status code: {response.status_code}")  

    except Exception as e:
        constants.LOGGER.error(f"Failed to send message: {e}")
        raise Exception(f"Failed to send message: {e}")  
    
def send_error_message(url, url_error):
    
    try:

        # Send the POST request
        headers = {"Content-Type": constants.VALID_CONTENT_TYPE}
        message = f"❌ Error analyzing URL: {url}\n\nError is {url_error}"
        payload_text = {
            "text": message
        }

        response = requests.post(config.WEBHOOK_URL, json=payload_text, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            constants.LOGGER.info("Message sent successfully")
            return {"message": "Message sent successfully"}
        else:
            constants.LOGGER.error(f"Failed to send message, status code: {response.status_code}")
            raise Exception(f"Failed to send message, status code: {response.status_code}") 

    except Exception as e:
        constants.LOGGER.error(f"Failed to send message: {e}")
        raise Exception(f"Failed to send message: {e}")  

