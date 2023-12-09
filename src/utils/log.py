import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# set log directory
log_dir = Path("logs")
try:
    log_dir.mkdir()
except FileExistsError:
    ...

# set log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(filename)s:%(module)s:%(name)s:%(lineno)d] %(message)s"
)

# create TimedRotatingFileHandler
file_handler = TimedRotatingFileHandler(
    filename=log_dir / "log.log",
    when="midnight",  # rotate every midnight
    backupCount=3,  # define number of log files, set 0 to save infinity log files
    encoding="utf-8",
)
file_handler.setFormatter(formatter)

# create StreamHandler
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

# create Logger instance
logger = logging.getLogger("logger")

# add log handler to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
