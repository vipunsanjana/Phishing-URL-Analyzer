
from typing import Dict, Any, List, Optional
from app.services.mysql_service.models import PhishingAnalysisResponse
from app.utils import constants

async def execute_query(connection, query: str, values: Optional[tuple] = None, fetch: bool = False) -> Optional[List[tuple]]:
    """
    Execute a SQL query with optional values and fetch result if required.

    Args:
        connection: Active database connection.
        query (str): SQL query string.
        values (tuple, optional): Values to be inserted into the query.
        fetch (bool, optional): Whether to fetch results. Defaults to False.

    Returns:
        List[tuple]: List of results if fetch is True, else None.
    Raises:
        Exception: If there is an error executing the query.
    """
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, values) if values else await cursor.execute(query)
            if fetch:
                result = await cursor.fetchall()
                return result
            await connection.commit()
            constants.LOGGER.info("Query executed successfully.")
    except Exception as e:
        await connection.rollback()
        constants.LOGGER.error(f"Database query error: {e}")
        raise Exception(f"Database query error: {e}")
class PhishingQueries:
    INSERT_PHISHING = """
        INSERT INTO phishing_metadata 
        (url, is_related_to_LK, is_political_content, phishing_score, impersonated_brand, is_phishing, number_of_keyword, keyword_list, page_screenshot_url) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    DELETE_ALL_ANALYSES = "DELETE FROM phishing_url_tracking"
    SELECT_ALL_URLS = "SELECT url FROM phishing_url_tracking"
    SELECT_PHISHING_CASES = "SELECT * FROM phishing_metadata"

async def save_only_phishing(connection, data: Dict[str, Any], url: str):
    """
    Save phishing analysis data into `phishing_metadata` if phishing=True.

    Args:
        connection: Active database connection.
        data (dict): Phishing analysis result.
        url (str): URL being analyzed.
    """
    required_keys = ["gpt_response", "downloadable_screenshot_path"]
    if not all(key in data for key in required_keys):
        constants.LOGGER.error("Missing required keys in data dictionary")
        raise Exception("Missing required keys in data dictionary")

    res = data.get("gpt_response", {})
    phishing_data = PhishingAnalysisResponse(
        is_related_to_LK=res.get("Website related to Sri Lanka", False),
        is_political_content=res.get("Political Content", False),
        phishing_score=res.get("Phishing Score", 0),
        impersonated_brand=res.get("Brands", ""),
        is_phishing=res.get("Phishing", False),
        number_of_keyword=res.get("Keywords Found", 0),
        keyword_list=res.get("Keywords", [])
    )

    values = (
        url,
        phishing_data.is_related_to_LK,
        phishing_data.is_political_content,
        phishing_data.phishing_score,
        phishing_data.impersonated_brand,
        phishing_data.is_phishing,
        phishing_data.number_of_keyword,
        ', '.join(phishing_data.keyword_list),
        data.get("downloadable_screenshot_path")
    )
    
    await execute_query(connection, PhishingQueries.INSERT_PHISHING, values)

async def delete_all_records(connection):
    """
    Delete all records from `all_analyses` and `phishing_cases` tables.
    """
    await execute_query(connection, PhishingQueries.DELETE_ALL_ANALYSES)

async def get_all_urls(connection) -> List[str]:
    """
    Retrieve all URLs from the specified table.

    Returns:
        List[str]: A list of URLs from the database.
    """
    rows = await execute_query(connection, PhishingQueries.SELECT_ALL_URLS, fetch=True)
    urls = [row[0] for row in rows]
    constants.LOGGER.info(f"Fetched {len(urls)} URLs from the database.")
    return urls

async def get_report_from_phishing_sites(connection) -> Dict[str, Any]:
    """
    Generate a report based on data from phishing sites.

    Returns:
        dict: A dictionary containing the analysis report.
    """
    counters = {
        "not_political": 0,
        "political": 0,
        "not_related_to_lk": 0,
        "related_to_lk": 0,
        "not_phishing": 0,
        "phishing": 0,
        "total_sites_scanned": 0
    }

    records = await execute_query(connection, PhishingQueries.SELECT_PHISHING_CASES, fetch=True)

    for record in records:
        counters["total_sites_scanned"] += 1

        political_content = str(record[2]).strip().lower()
        website_related_to_sri_lanka = str(record[1]).strip().lower()
        phishing_status = str(record[5]).strip().lower()

        counters["not_political"] += 1 if political_content != "1" else 0
        counters["political"] += 1 if political_content == "1" else 0
        counters["not_related_to_lk"] += 1 if website_related_to_sri_lanka == "1" else 0
        counters["related_to_lk"] += 1 if website_related_to_sri_lanka != "1" else 0
        counters["not_phishing"] += 1 if phishing_status == "0" else 0
        counters["phishing"] += 1 if phishing_status != "0" else 0

    return counters
