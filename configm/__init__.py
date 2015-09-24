import sys
import logging


import colors


_log_level_color = {
    'W': 'yellow',
    'E': 'red',
    'I': 'green'
}


class Handler(logging.Handler):

    def __init__(self, out, indicator):
        logging.Handler.__init__(self)
        self.out = out
        self.indicator = indicator
        self.setLevel(logging.DEBUG)

    def flush(self):
        self.out.flush()

    def emit(self, record):
        level = record.levelname[0].upper()
        context = '{0}:{1}'.format(
            self.indicator,
            colors.color(level, fg=_log_level_color.get(level, 15)))
        self.out.write('[{0}] {1}\n'
                       .format(context, record.msg))


def setup_logger(logger_name, indicator):
    logger = logging.getLogger(logger_name)
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(Handler(sys.stdout, indicator))
    logger.setLevel(logging.INFO)
    return logger
