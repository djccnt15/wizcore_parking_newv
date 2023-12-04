import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# set directory
log_dir = Path("logs")
try:
    log_dir.mkdir()
except FileExistsError:
    ...
LOG_FILENAME = log_dir / "main.log"

# set log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(filename)s:%(module)s:%(name)s:%(lineno)d] %(message)s"
)

# create TimedRotatingFileHandler and setting it
file_handler = TimedRotatingFileHandler(
    filename=LOG_FILENAME, when="midnight", interval=1, encoding="utf-8"
)  # rotate every midnight
file_handler.suffix = "%Y%m%d.log"
file_handler.setFormatter(formatter)

# create Logger instance
logger = logging.getLogger("main_logger")

# add file handler
logger.addHandler(file_handler)
