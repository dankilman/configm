import copy
import os
from typing import Dict, Any, Union

import yaml
from pathlib import Path

from configm import log
from configm import git


class Config:

    counter: int = 0

    def __init__(self, config: Dict[str, Any], config_path: Path, nesting: int):
        self.__class__.counter += 1
        indicator = self.counter
        self.nesting = nesting
        self.logger = log.setup_logger(f"configm_{indicator}", str(indicator), nesting)
        self.config_path = config_path
        self.config = copy.deepcopy(config)
        self.normalize()

    def configm(self):
        self.logger.info(f"Processing {self.config_path}")
        self.clone()
        self.symlink()
        for repo in self.repos.values():
            repo_config = repo["target"] / ".configm"
            if repo_config.exists():
                config = load(repo_config, self.nesting+1)
                config.configm()

    def clone(self):
        for repo in self.repos.values():
            git.clone(repo["source"], repo["target"], logger=self.logger)

    def symlink(self):
        for symlink in self.symlinks.values():
            if symlink["target"].exists():
                if symlink["target"].is_symlink():
                    actual_target = symlink["target"].readlink()
                    if not actual_target.is_absolute():
                        actual_target = symlink["target"].parent / actual_target
                    if actual_target == symlink["source"]:
                        self.logger.info(f"Skipping symlink creation at {symlink['target']} as it already exists")
                    else:
                        self.logger.warning(
                            f"Skipping symlink creation at {symlink['target']}. It currently links to {actual_target} "
                            f"instead of {symlink['source']}"
                        )
                else:
                    self.logger.warning(f"Skipping symlink creation at {symlink['target']}. It is not a link")
            else:
                self.logger.info(f"Creating symlink from {symlink['target']} to {symlink['source']}")
                os.symlink(symlink['source'], symlink['target'])

    def normalize(self):
        for key in ["repos", "symlinks"]:
            if key not in self.config:
                self.config[key] = {}
        for repo in self.config["repos"].values():
            repo["target"] = Path(repo["target"]).expanduser().absolute()
        new_symlinks = {}
        for source, symlinks in self.symlinks.items():
            if not isinstance(symlinks, list):
                symlinks = [symlinks]
            for i, symlink in enumerate(symlinks):
                if isinstance(symlink, str):
                    symlink = {"target": symlink}
                symlink["target"] = Path(symlink["target"]).expanduser().absolute()
                source_key = f"{source}_{i}"
                source = Path(source).expanduser()
                if not source.exists():
                    source = self.config_path.parent / source
                symlink["source"] = source.absolute()
                new_symlinks[source_key] = symlink
        self.symlinks.clear()
        self.symlinks.update(new_symlinks)

    @property
    def repos(self) -> Dict[str, Dict[str, Union[str, Path]]]:
        return self.config["repos"]

    @property
    def symlinks(self) -> Dict[str, Dict[str, Path]]:
        return self.config["symlinks"]


def load(config_path: Path, nesting: int = 0) -> Config:
    if not config_path.expanduser().exists():
        raise ValueError(f"Missing configuration: {config_path}")
    config_path = config_path.absolute()
    config = yaml.safe_load(config_path.read_text())
    return Config(config, config_path, nesting)
