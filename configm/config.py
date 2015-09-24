import copy
import os

import yaml
from path import path

import configm
from configm import git


class Config(object):

    counter = 0

    def __init__(self, config, config_path=None):
        Config.counter += 1
        indicator = Config.counter
        self.logger = configm.setup_logger('configm_{0}'.format(indicator),
                                           indicator)
        self.config_path = config_path
        self.config = copy.deepcopy(config)
        self.normalize()

    def configm(self):
        self.logger.info('Processing {0}'.format(self.config_path))
        self.clone()
        self.symlink()
        for repo in self.repos.values():
            repo_config = repo['target'] / '.configm'
            if repo_config.exists():
                config = load(repo_config)
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
                        self.logger.info('Skipping symlink creation at {0} as '
                                         'it already exists'
                                         .format(symlink['target']))
                    else:
                        self.logger.info('Skipping symlink creation at {0}. '
                                         'It currently links to {1} instead '
                                         'of {2}'
                                         .format(symlink['target'],
                                                 actual_target,
                                                 symlink['source']))
                else:
                    self.logger.warn('Skipping symlink creation at {0}. '
                                     'It is not a link'
                                     .format(symlink['target']))
            else:
                self.logger.info('Creating symlink from {0} to {1}'
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


def load(config):
    if not os.path.exists(os.path.expanduser(config)):
        raise IOError('Missing configuration: {0}'.format(config))
    config_path = path(config).expanduser().abspath()
    config = config_path.text()
    return Config(yaml.safe_load(config), config_path)
