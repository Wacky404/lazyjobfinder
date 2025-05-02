from src.utils.logger import logger, setup_logging
from prometheus_client import start_http_server
from src.Models.dbsetup import db_setup

setup_logging()
db_setup()
start_http_server(8000)
print("Finished!")
