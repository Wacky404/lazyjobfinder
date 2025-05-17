from src.utils.logger import logger, setup_logging
from prometheus_client import start_http_server, Counter
from src.Models.dbsetup import db_setup
import time

setup_logging()
# setting up the db initally; will be moved; only for first time startup.
db_setup()
# exposes the metrics
start_http_server(4000)

requests = Counter("my_app_requests", "Total number of requests")
while True:
    requests.inc()
    time.sleep(1)
