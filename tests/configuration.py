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
        result = env_loader(
            defaults={
                "test": "$CHOR_test",
                "test_2": "$CHOR_test_2",
                "test_3": "Static value"
            }
        )
        assert result['test'] == 'test value'
        assert result['test_2'] == 'test value2'
        assert result['test_3'] == 'Static value'

