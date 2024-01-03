import unittest
import os

from chordataweb.configuration import env_loader, dynamic_key_loader

"""
Automated tests for the configuration module
"""


class TestConfiguration(unittest.TestCase):
    def test_environment_variable(self):
        os.environ['CHOR_test'] = "test value"
        os.environ['CHOR_test_2'] = "test value2"
        result = env_loader(['test', 'test_2'])
        assert result['test'] == 'test value'
        assert result['test_2'] == 'test value2'

    def test_custom_keys_loader(self):
        os.environ['CHOR_test'] = "test value"
        os.environ['CHOR_test_2'] = "test value2"
        os.environ['CHOR_custom_keys'] = "test:test_2"
        result = env_loader([])
        assert result['test'] == 'test value'
        assert result['test_2'] == 'test value2'
