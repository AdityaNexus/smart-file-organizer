import logging 

logging.basicConfig(level = logging.WARNING)
#How it works: If you set your logger's level to WARNING, 
# it will only process WARNING, ERROR, and CRITICAL messages.
# DEBUG and INFO messages will be silently discarded.
logging.debug("Developer details: var_x = 42")
logging.info("User successfully logged in")


logging.warning("Disk space is running low")
logging.error("Failed to open the file")
logging.critical("Database connetion lost. System halting")

