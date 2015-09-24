import sys

import sh


def bake(command):
    return command.bake(_out=lambda line: sys.stdout.write(line),
                        _err=lambda line: sys.stderr.write(line))


git = bake(sh.git)


def clone(source, target, logger):
    if target.exists():
        logger.info('Not cloning {0} as it already exists in {1}'
                    .format(source, target))
    else:
        git.clone(source, target).wait()
