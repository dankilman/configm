import sh


def bake(command, logger):
    return command.bake(_out=lambda line: logger.info(line.strip()),
                        _err=lambda line: logger.warn(line.strip()))


def clone(source, target, logger):
    if target.exists():
        with target:
            try:
                remote = sh.git.config('remote.origin.url').stdout.strip()
                if remote == source:
                    logger.info('Not cloning {} as it already exists in {}'
                                .format(source, target))
                else:
                    logger.warn('Not cloning {} as it already exists in {}. '
                                'Note that the current remote.origin is {}'
                                .format(source, target, remote))
            except sh.ErrorReturnCode:
                logger.warn('Not cloning {} as it already exists in {}. '
                            'Note that current target does not point to a '
                            'valid git repository'.format(source, target))
    else:
        git = bake(sh.git, logger)
        git.clone(source, target).wait()
