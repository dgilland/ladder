
from unittest import TestCase

from ladder import OSPath


class TestOSPath(TestCase):
    def test_empty_path(self):
        self.assertEqual(str(OSPath()), '')

    def test_single_slash_path(self):
        self.assertEqual(str(OSPath('/')), '/')

    def test_initialized_path(self):
        self.assertEqual(str(OSPath('/home/ladder')), '/home/ladder')

    def test_chaining(self):
        self.assertEqual(
            str(OSPath().foo.bar(1, 'one').baz().qux),
            'foo/bar/1/one/baz/qux')

    def test_instance_regeneration(self):
        path = OSPath('/foo')
        original = str(path)
        path()
        self.assertEqual(str(path), original)

    def test_add_operator_with_path(self):
        path = OSPath('start/of/path') + OSPath('end/of/path')
        self.assertTrue(isinstance(path, OSPath))
        self.assertEqual(str(path), 'start/of/path/end/of/path')

    def test_div_operator_with_path(self):
        path = OSPath('start/of/path') / OSPath('end/of/path')
        self.assertTrue(isinstance(path, OSPath))
        self.assertEqual(str(path), 'start/of/path/end/of/path')

    def test_add_operator_with_string(self):
        path = OSPath('start/of/path') + 'end/of/path'
        self.assertTrue(isinstance(path, OSPath))
        self.assertEqual(str(path), 'start/of/path/end/of/path')

        path = 'start/of/path' + OSPath('end/of/path')
        self.assertTrue(isinstance(path, OSPath))
        self.assertEqual(str(path), 'start/of/path/end/of/path')

    def test_div_operator_with_string(self):
        path = OSPath('start/of/path') / 'end/of/path'
        self.assertTrue(isinstance(path, OSPath))
        self.assertEqual(str(path), 'start/of/path/end/of/path')

        path = 'start/of/path' / OSPath('end/of/path')
        self.assertTrue(isinstance(path, OSPath))
        self.assertEqual(str(path), 'start/of/path/end/of/path')
