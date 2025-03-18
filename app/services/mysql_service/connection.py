import aiomysql
from app.utils import constants, config

async def create_mysql_connection():
    """
    Establish and return an asynchronous connection to the MySQL database.

    Returns:
        aiomysql.Connection: Database connection object.
    Raises:
        DatabaseConnectionError: If connection fails.
    """
    try:
        connection = await aiomysql.connect(
            host=config.MYSQL_DB_HOST,
            user=config.MYSQL_DB_USER,
            password=config.MYSQL_DB_PASSWORD,
            db=config.MYSQL_DB_NAME,
            port=config.MYSQL_DB_PORT,
        )
        if connection:
            constants.LOGGER.info("Connected to MySQL database")
            return connection
    except Exception as e:
        constants.LOGGER.error(f"Error connecting to MySQL database: {e}")
        raise Exception(f"Error connecting to MySQL database: {e}")
