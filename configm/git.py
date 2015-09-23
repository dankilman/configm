import sys

import sh


def bake(command):
    return command.bake(_out=lambda line: sys.stdout.write(line),
                        _err=lambda line: sys.stderr.write(line))


git = bake(sh.git)


def clone(source, target):
    if target.exists():
        return
    git.clone(source, target).wait()
