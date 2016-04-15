# -*- coding: utf-8 -*-

from .context import src
from src import helpers
import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_fetch_data(self):
        data = helpers.request_new_data()
        assert len(data) > 1



if __name__ == '__main__':
    unittest.main()