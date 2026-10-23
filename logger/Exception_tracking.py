import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find(data):
    try:
        ans = data//2
        return ans 
        logger.info("Successfully found the answer.")
    except Exception as e:
        logger.exception("failed to process the data due to a type ,smatch")



find("string")