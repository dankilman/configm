import copy
import os

import yaml
from path import path

from configm import git


class Config(object):

    def __init__(self, config, config_path=None):
        self.config_path = config_path
        self.config = copy.deepcopy(config)
        self.normalize()

    def configm(self):
        self.clone()
        self.symlink()
        for repo in self.repos.values():
            repo_config = repo['target'] / '.configm'
            if repo_config.exists():
                config = load(repo_config)
                config.configm()

    def clone(self):
        for repo in self.repos.values():
            git.clone(repo['source'], repo['target'])

    def symlink(self):
        for symlink in self.symlinks.values():
            if symlink['target'].exists():
                continue
            os.symlink(symlink['source'], symlink['target'])

    def normalize(self):
        if 'repos' not in self.config:
            self.config['repos'] = {}
        if 'symlinks' not in self.config:
            self.config['symlinks'] = {}
        for repo in self.repos.values():
            repo['target'] = path(repo['target']).expanduser().abspath()
        for source in self.symlinks.keys():
            full_source = path(source).expanduser()
            if not full_source.exists():
                full_source = self.config_path.dirname() / full_source
            else:
                full_source = full_source.abspath()
            target = self.symlinks[source]
            self.symlinks[source] = {
                'source': full_source,
                'target': path(target).expanduser().abspath()
            }

    @property
    def repos(self):
        return self.config['repos']

    @property
    def symlinks(self):
        return self.config['symlinks']


def load(config):
    config_path = None
    if os.path.exists(os.path.expanduser(config)):
        config_path = path(config).expanduser().abspath()
        config = config_path.text()
    return Config(yaml.safe_load(config), config_path)
