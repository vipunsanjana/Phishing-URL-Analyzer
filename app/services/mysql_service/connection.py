import mysql.connector
from mysql.connector import Error
from app.utils import constants, config

def create_mysql_connection():
    """
    Establish and return a synchronous connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    Raises:
        Exception: If connection fails.
    """
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
        constants.LOGGER.error(f"Error connecting to MySQL database: {e}")
        raise Exception(f"Error connecting to MySQL database: {e}")
