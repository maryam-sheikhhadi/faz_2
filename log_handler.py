import logging

logger = logging.getLogger(__name__)
assert logger.level == logging.NOTSET
assert logger.getEffectiveLevel() == logging.WARNING
logger.setLevel(logging.INFO)
# create handler and set level
file_handler = logging.FileHandler('project.log')
file_handler.setLevel(logging.INFO)
# create formatter and add it to handler
file_format = logging.Formatter('%(asctime)s ::%(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(message)s')
file_handler.setFormatter(file_format)
# add handler to the logger
logger.addHandler(file_handler)
