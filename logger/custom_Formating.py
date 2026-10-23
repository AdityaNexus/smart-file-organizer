import logging
# Format : [Timestamp] - [Logger Name] - [Log Level] - [Message]
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level = logging.INFO,
    format = log_format,
    datefmt = "%Y-%m-%d %H:%M:%S"
)


logging.info("Server started successfully.")
logging.warning("User attempted invalid login.")