import logging


logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG) # All messages will be processed, but the output will depend on the handler's level.

#create Handlers

console_handler = logging.StreamHandler() # This handler will output log messages to the console (stdout).
console_handler.setLevel(logging.WARNING) # This handler will only process WARNING, ERROR, and CRITICAL messages.

logger.addHandler(console_handler)

file_handler = logging.FileHandler("debug_output.log",mode='w') # This handler will write log messages to a file named "debug_output.log".
file_handler.setLevel(logging.DEBUG) # This handler will process all messages, including DEBUG and INFO.

logger.addHandler(file_handler)

logger.debug("This goes ONLY to the file.")
logger.info("This also goes ONLY to the file.")
logger.warning("This goes to the console AND the file.")
logger.error("This goes to the console AND the file.")