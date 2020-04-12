import copy
import os

import yaml
from path import Path as path

from configm import log
from configm import git


class Config:

    counter = 0

    def __init__(self, config, config_path, nesting):
        Config.counter += 1
        indicator = Config.counter
        self.nesting = nesting
        self.logger = log.setup_logger(f'configm_{indicator}',
                                       indicator, nesting)
        self.config_path = config_path
        self.config = copy.deepcopy(config)
        self.normalize()

    def configm(self):
        self.logger.info(f'Processing {self.config_path}')
        self.clone()
        self.symlink()
        for repo in self.repos.values():
            repo_config = repo['target'] / '.configm'
            if repo_config.exists():
                config = load(repo_config, self.nesting+1)
                config.configm()

    def clone(self):
        for repo in self.repos.values():
            git.clone(repo['source'], repo['target'], logger=self.logger)

    def symlink(self):
        for symlink in self.symlinks.values():
            if symlink['target'].exists():
                if symlink['target'].islink():
                    actual_target = symlink['target'].readlink()
                    if not actual_target.isabs():
                        actual_target = symlink[
                            'target'].dirname() / actual_target
                    if actual_target == symlink['source']:
                        self.logger.info('Skipping symlink creation at {} as '
                                         'it already exists'
                                         .format(symlink['target']))
                    else:
                        self.logger.warn('Skipping symlink creation at {}. '
                                         'It currently links to {} instead '
                                         'of {}'
                                         .format(symlink['target'],
                                                 actual_target,
                                                 symlink['source']))
                else:
                    self.logger.warn('Skipping symlink creation at {}. '
                                     'It is not a link'
                                     .format(symlink['target']))
            else:
                self.logger.info('Creating symlink from {} to {}'
                                 .format(symlink['target'], symlink['source']))
                os.symlink(symlink['source'], symlink['target'])

    def normalize(self):
        for key in ['repos', 'symlinks']:
            if key not in self.config:
                self.config[key] = {}
        for repo in self.repos.values():
            repo['target'] = path(repo['target']).expanduser().abspath()
        for source, symlink in self.symlinks.items():
            if isinstance(symlink, basestring):
                symlink = {
                    'target': symlink
                }
            symlink['target'] = path(symlink['target']).expanduser().abspath()
            source_key = source
            source = path(source).expanduser()
            if not source.exists():
                source = self.config_path.dirname() / source
            symlink['source'] = source.abspath()
            self.symlinks[source_key] = symlink

    @property
    def repos(self):
        return self.config['repos']

    @property
    def symlinks(self):
        return self.config['symlinks']


def load(config, nesting=0):
    if not os.path.exists(os.path.expanduser(config)):
        raise OSError(f'Missing configuration: {config}')
    config_path = path(config).expanduser().abspath()
    config = config_path.text()
    return Config(yaml.safe_load(config), config_path, nesting)
