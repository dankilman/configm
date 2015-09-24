import sys

from configm import config


def main():
    config_path = '.configm' if len(sys.argv) == 1 else sys.argv[1]
    conf = config.load(config_path)
    conf.configm()


if __name__ == '__main__':
    main()
