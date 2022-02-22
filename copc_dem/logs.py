
import logging
import sys

logger = logging.getLogger("copc_dem")
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

def setLevel(log_level):
    handler.setLevel(log_level)
    logger.setLevel(log_level)

