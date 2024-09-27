import logging

class CustomFormatter(logging.Formatter):

    grey : str = "\x1b[38;20m"
    yellow : str = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format : str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)" # type: ignore

    FORMATS = {
        logging.DEBUG: grey + format + reset, # type: ignore
        logging.INFO: grey + format + reset, # type: ignore
        logging.WARNING: yellow + format + reset, # type: ignore
        logging.ERROR: red + format + reset, # type: ignore
        logging.CRITICAL: bold_red + format + reset # type: ignore
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatters = logging.Formatter(log_fmt)
        return formatters.format(record)



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)

logging.basicConfig(filename='simple_rest_api/app/logs/app.log',filemode='w',encoding='utf-8' ,format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)")

console_logger.setFormatter(CustomFormatter())

logger.addHandler(console_logger)