import sys

import sh


def bake(command):
    return command.bake(_out=lambda line: sys.stdout.write(line),
                        _err=lambda line: sys.stderr.write(line))


git = bake(sh.git)


def clone(source, target, logger):
    if target.exists():
        with target:
            try:
                remote = sh.git.config('remote.origin.url').stdout.strip()
                if remote == source:
                    logger.info('Not cloning {0} as it already exists in {1}'
                                .format(source, target))
                else:
                    logger.warn('Not cloning {0} as it already exists in {1}. '
                                'Note that the current remote.origin is {2}'
                                .format(source, target, remote))
            except sh.ErrorReturnCode:
                logger.warn('Not cloning {0} as it already exists in {1}. '
                            'Note that current target does not point to a '
                            'valid git repository'.format(source, target))
    else:
        git.clone(source, target).wait()
