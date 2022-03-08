import sys
import logging
from typing import TextIO

import colors


_log_level_color = {
    "W": "yellow",
    "E": "red",
    "I": "green"
}


class Handler(logging.Handler):

    def __init__(self, out: TextIO, indicator: str, nesting: int):
        super().__init__(logging.DEBUG)
        self.out = out
        self.indicator = indicator
        self.nesting = nesting

    def flush(self):
        self.out.flush()

    def emit(self, record: logging.LogRecord):
        level = record.levelname[0].upper()
        space = " " * self.nesting
        colored_level = colors.color(level, fg=_log_level_color.get(level, 15))
        context = f"{self.indicator}:{colored_level}"
        self.out.write(f"[{context}] {space}{record.msg}\n")


def setup_logger(logger_name: str, indicator: str, nesting: int) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(Handler(sys.stdout, indicator, nesting))
    logger.setLevel(logging.INFO)
    return logger
