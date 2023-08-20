import logging


class Logger:
    def __init__(self, log_file="conversion_log.log"):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
        )

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def warning(message):
        logging.warning(message)
