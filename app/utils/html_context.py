
import hashlib
from dataclasses import dataclass
from typing import List, Tuple
from bs4 import BeautifulSoup
from app.utils import constants

@dataclass
class ProcessedHTMLContent:
    """
    A base model class to represent processed HTML content.
    """
    html_content: str
    text_content: str
    hash_value: str
    a_tags: List[BeautifulSoup]  
    script_tags: List[str]       

def process_html_content(html_content: str) -> ProcessedHTMLContent:
    """
    Processes the given HTML content by extracting text, computing hash, and filtering <a> and <script> tags.
    
    Args:
        html_content (str): The raw HTML content to be processed.
    
    Returns:
        ProcessedHTMLContent: An instance of the ProcessedHTMLContent model containing the processed data.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract clean text
        text_content = soup.get_text(separator=' ', strip=True)

        # Generate MD5 hash of HTML tags
        all_tags = soup.find_all(True)
        tags = "".join(tag.name for tag in all_tags)
        hash_value = hashlib.md5(tags.encode()).hexdigest()

        # Filter <a> and <script> tags
        a_tags = soup.find_all('a')
        script_tags_filtered = []
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string:
                script_tags_filtered.append(script.string.strip())
            elif script.get('src'):
                script_tags_filtered.append(script.get('src'))

        # Return an instance of the ProcessedHTMLContent model
        return ProcessedHTMLContent(
            html_content=html_content,
            text_content=text_content,
            hash_value=hash_value,
            a_tags=a_tags,
            script_tags=script_tags_filtered
        )

    except Exception as e:
        constants.LOGGER.error(f"Error processing HTML content: {str(e)}")
        raise Exception(f"Error processing HTML content: {str(e)}")

@dataclass
class FilteredTags:
    """
    A base model class to represent filtered <a> and <script> tags.
    """
    a_tags: List[BeautifulSoup]  
    script_tags: List[str]       

def process_tags(html_content: str) -> FilteredTags:
    """
    Extracts <a> and <script> tags from the given HTML content.
    
    Args:
        html_content (str): The raw HTML content.
    
    Returns:
        FilteredTags: An instance of the FilteredTags model containing the filtered tags.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        a_tags = soup.find_all('a')
        script_tags_filtered = []
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string:
                script_tags_filtered.append(script.string.strip())
            elif script.get('src'):
                script_tags_filtered.append(script.get('src'))

        # Return an instance of the FilteredTags model
        return FilteredTags(
            a_tags=a_tags,
            script_tags=script_tags_filtered
        )

    except Exception as e:
        constants.LOGGER.error(f"Error processing HTML content: {str(e)}")
        raise Exception(f"Error processing HTML content: {str(e)}")

def extract_content(html_content: str) -> Tuple[str, str]:
    """
    Extracts plain text content from the given HTML content.
    
    Args:
        html_content (str): The raw HTML content.
    
    Returns:
        Tuple[str, str]: A tuple containing the original HTML and extracted text content.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        return html_content, text_content

    except Exception as e:
        constants.LOGGER.error(f"Error extracting content: {str(e)}")
        raise Exception(f"Error extracting content: {str(e)}")
