import mysql.connector
from mysql.connector import Error
from app.utils import constants, config
import time

def create_mysql_connection(retries=5, delay=5):
    """
    Establish and return a synchronous connection to the MySQL database with retries.

    Args:
        retries (int): Number of retry attempts before failing.
        delay (int): Delay (in seconds) between retries.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    
    Raises:
        Exception: If connection fails after all retries.
    """
    attempt = 0
    while attempt < retries:
        try:
            connection = mysql.connector.connect(
                host=config.MYSQL_DB_HOST,
                user=config.MYSQL_DB_USER,
                password=config.MYSQL_DB_PASSWORD,
                database=config.MYSQL_DB_NAME,
                port=int(config.MYSQL_DB_PORT),
            )
            if connection.is_connected():
                constants.LOGGER.info("Connected to MySQL database")
                return connection  
        except Error as e:
            constants.LOGGER.error(f"❌ Connection attempt {attempt+1} failed: {e}")
            attempt += 1
            time.sleep(delay)  

    raise Exception("Failed to connect to MySQL after multiple attempts")
