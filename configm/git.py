import logging
import os
from pathlib import Path

import sh


def bake(command: sh.Command, logger: logging.Logger) -> sh.Command:
    return command.bake(
        _out=lambda line: logger.info(line.strip()),
        _err=lambda line: logger.warning(line.strip()),
    )


def clone(source: str, target: Path, logger: logging.Logger):
    if target.exists():
        orig_dir = os.getcwd()
        try:
            os.chdir(target)
            remote = sh.git.config("remote.origin.url").stdout.strip()
            if remote == source:
                logger.info(f"Not cloning {source} as it already exists in {target}")
            else:
                logger.warning(
                    f"Not cloning {source} as it already exists in {target}. "
                    f"Note that the current remote.origin is {remote}"
                )
        except sh.ErrorReturnCode:
            logger.warning(
                f"Not cloning {source} as it already exists in {target}. "
                f"Note that current target does not point to a valid git repository"
            )
        finally:
            os.chdir(orig_dir)
    else:
        git = bake(sh.git, logger)  # noqa
        git.clone(source, str(target)).wait()
