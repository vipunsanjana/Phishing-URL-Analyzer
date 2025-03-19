
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from app.services.google_chat.send_message import send_error_message
from app.utils import constants, image_context
from app.utils import html_context
from app.services.firebase_service.firebase import upload_image_and_get_url
from app.services.openai_service.openai import generate_response

async def take_screenshot(page, retries=3):
    """
    Takes a screenshot of the page and returns it as a buffer.
    
    Args:
        page (playwright.async_api.Page): The Playwright page instance.
        retries (int): Number of retries in case of failure.
    
    Returns:
        bytes: The screenshot image as a buffer.
    """
    for attempt in range(retries):
        try:
            screenshot_buffer = await page.screenshot(timeout=60000)
            return screenshot_buffer
        except Exception as e:
            if attempt == retries - 1:
                raise Exception(f"Failed to take screenshot after {retries} attempts: {str(e)}")
            constants.LOGGER.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")

async def scrape_website(url):
    """
    Takes a screenshot of the page and returns it as a buffer.
    
    Args:
        page (playwright.async_api.Page): The Playwright page instance.
        retries (int): Number of retries in case of failure.
    
    Returns:
        bytes: The screenshot image as a buffer.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, slow_mo=500)
        context = await browser.new_context(user_agent="SOC-AI Testing Agent", viewport={"width": 1280, "height": 720})
        page = await context.new_page()

        try:
            response = await page.goto(url, wait_until="domcontentloaded")
            status_code = response.status
            if status_code < 200 or status_code >= 400:
                send_error_message("Status Code Error this URL: ", url)
                constants.LOGGER.error(f"Failed to load the page. Status code: {status_code}")
                raise Exception(f"Failed to load the page. Status code: {status_code}")

            await page.wait_for_load_state("networkidle", timeout=60000)
            await page.wait_for_function("document.readyState === 'complete'")

            # Extract content
            html_content = await page.content()
            html_content, text_content = html_context.extract_content(html_content=html_content)
            if not text_content.strip():
                raise Exception("No text content found on the page.")

            # Take a screenshot
            screenshot_buffer = await take_screenshot(page)
            await page.wait_for_timeout(2000)
            resized_screenshot_buffer = process_image(screenshot_buffer)

            # Generate GPT response
            gpt_output = generate_response(url, html_content, text_content)
            if not gpt_output:
                raise Exception("GPT response is empty.")

            if gpt_output.get("Phishing"):
                return gpt_output

            # Upload image
            image_url = await upload_image(resized_screenshot_buffer, constants.screenshot_path)

            return {
                "gpt_response": gpt_output,
                "downloadable_screenshot_path": image_url,
            }

        except PlaywrightTimeoutError as e:
            send_error_message("Timeout Error this URL: ", url)
            constants.LOGGER.error(f"Timeout error: {str(e)}")
            raise Exception(f"Timeout error: {str(e)}")

        except Exception as e:
            constants.LOGGER.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")

        finally:
            await browser.close()  
            
def process_image(screenshot_buffer):
    """
    Resizes the screenshot image to optimize it for further processing.

    Args:
        screenshot_path (str): The path to the screenshot image that needs to be resized.
    """
    try:
        resized_image_buffer = image_context.resize_image(screenshot_buffer)
        return resized_image_buffer
    except Exception as e:
        constants.LOGGER.error(f"Failed to resize image: {str(e)}")
        raise Exception(f"Failed to resize image: {str(e)}")

async def upload_image(screenshot_buffer, destination_blob_name):
    """
    Uploads the given image to Firebase storage and retrieves the URL.

    Args:
        destination_blob_name (str): The destination path for the image in Firebase storage.

    Returns:
        str: The URL of the uploaded image in Firebase storage.
    """
    try:
        constants.LOGGER.info("Uploading image to Firebase")
        image_url = await upload_image_and_get_url(screenshot_buffer, destination_blob_name)
        return image_url
    
    except Exception as e:
        constants.LOGGER.error(f"Error during image upload: {str(e)}")
        raise Exception(f"Error during image upload: {str(e)}")


