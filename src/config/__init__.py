from os import getenv
from dotenv import load_dotenv


load_dotenv()
data_path = getenv('DATA_FILE')
driver_cache = getenv('CACHE_DRIVER_PATH')
log_path = getenv('LOG_PATH')