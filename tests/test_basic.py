# -*- coding: utf-8 -*-

from .context import src

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def sample(self):
        assert True



if __name__ == '__main__':
    unittest.main()