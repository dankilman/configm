import unittest

from configm.tests import resource
from configm import config


class Tests(unittest.TestCase):

    def test(self):
        conf = config.load(resource.get('test.yaml'))
        conf.configm()
