import sys
import logging


import colors


_log_level_color = {
    'W': 'yellow',
    'E': 'red',
    'I': 'green'
}


class Handler(logging.Handler):

    def __init__(self, out, indicator, nesting):
        logging.Handler.__init__(self)
        self.out = out
        self.indicator = indicator
        self.nesting = nesting
        self.setLevel(logging.DEBUG)

    def flush(self):
        self.out.flush()

    def emit(self, record):
        level = record.levelname[0].upper()
        space = ' ' * self.nesting
        context = '{}:{}'.format(
            self.indicator,
            colors.color(level, fg=_log_level_color.get(level, 15)))
        self.out.write('[{}] {}{}\n'
                       .format(context, space, record.msg))


def setup_logger(logger_name, indicator, nesting):
    logger = logging.getLogger(logger_name)
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(Handler(sys.stdout, indicator, nesting))
    logger.setLevel(logging.INFO)
    return logger
