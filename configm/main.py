import logging
import sys

from configm import config


def _setup_logging():
    for h in logging.root.handlers:
        logging.root.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.INFO)


def main():
    _setup_logging()
    config_path = '.configm' if len(sys.argv) == 1 else sys.argv[1]
    conf = config.load(config_path)
    conf.configm()


if __name__ == '__main__':
    main()
