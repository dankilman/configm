from configm import config


def main():
    conf = config.load('.configm')
    conf.configm()


if __name__ == '__main__':
    main()
