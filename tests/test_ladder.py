
from unittest import TestCase

from ladder import Ladder


class TestLadder(TestCase):
    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, Ladder)
