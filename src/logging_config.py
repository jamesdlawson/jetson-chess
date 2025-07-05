import logging
import os
import sys
from datetime import datetime
from textual.widgets import RichLog


def setup_logging():
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}-log.txt"
    if os.path.exists(log_file):
        with open(log_file, "a") as f:
            f.write(f"\n--- NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        if os.path.getsize(log_file) > 10 * 1024 * 1024:  # 10MB
            with open(log_file, "r") as f:
                lines = f.readlines()
            with open(log_file, "w") as f:
                f.writelines(lines[-10000:])  # Keep last 10000 lines
    return log_file


class RichLogHandler(logging.Handler):
    def __init__(self, rich_log: RichLog):
        super().__init__()
        self.rich_log = rich_log

    def emit(self, record):
        self.rich_log.write(self.format(record))


class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


def configure_logging(log_widget: RichLog):
    log_file = setup_logging()
    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    handler = RichLogHandler(log_widget)
    handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
    logging.getLogger().addHandler(handler)

    sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)
    sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)
