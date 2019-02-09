
import unittest

import twarf


class VersionTest(unittest.TestCase):

    def test_version(self):
        self.assertTrue(twarf.__version__)
