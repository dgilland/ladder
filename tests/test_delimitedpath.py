
from unittest import TestCase

from ladder import DelimitedPath


PeriodPath = DelimitedPath(delimiter='.')


class TestDelimitedPath(TestCase):
    def test_empty_path(self):
        self.assertEqual(str(DelimitedPath()), '')

    def test_single_slash_path(self):
        self.assertEqual(str(DelimitedPath('.')), '.')

    def test_initialized_path(self):
        self.assertEqual(str(DelimitedPath('.home.ladder')), '.home.ladder')

    def test_chaining(self):
        self.assertEqual(
            str(DelimitedPath(delimiter='.').foo.bar(1, 'one').baz().qux),
            'foo.bar.1.one.baz.qux')

    def test_instance_regeneration(self):
        path = DelimitedPath('.foo')
        original = str(path)
        path()
        self.assertEqual(str(path), original)

    def test_add_operator_with_path(self):
        path = PeriodPath('start.of.path') + PeriodPath('end.of.path')
        self.assertTrue(isinstance(path, DelimitedPath))
        self.assertEqual(str(path), 'start.of.path.end.of.path')

    def test_div_operator_with_path(self):
        path = PeriodPath('start.of.path') / PeriodPath('end.of.path')
        self.assertTrue(isinstance(path, DelimitedPath))
        self.assertEqual(str(path), 'start.of.path.end.of.path')

    def test_add_operator_with_string(self):
        path = PeriodPath('start.of.path') + 'end.of.path'
        self.assertTrue(isinstance(path, DelimitedPath))
        self.assertEqual(str(path), 'start.of.path.end.of.path')

        path = 'start.of.path' + PeriodPath('end.of.path')
        self.assertTrue(isinstance(path, DelimitedPath))
        self.assertEqual(str(path), 'start.of.path.end.of.path')

    def test_div_operator_with_string(self):
        path = PeriodPath('start.of.path') / 'end.of.path'
        self.assertTrue(isinstance(path, DelimitedPath))
        self.assertEqual(str(path), 'start.of.path.end.of.path')

        path = 'start.of.path' / PeriodPath('end.of.path')
        self.assertTrue(isinstance(path, DelimitedPath))
        self.assertEqual(str(path), 'start.of.path.end.of.path')
