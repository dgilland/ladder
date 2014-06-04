
from unittest import TestCase

from ladder import URLPath


class TestURLPath(TestCase):

    def test_empty_url(self):
        self.assertEqual(str(URLPath()), '')

    def test_single_slash_url(self):
        self.assertEqual(str(URLPath('/')), '/')

    def test_initialized_url(self):
        self.assertEqual(
            str(URLPath('http://github.com')),
            'http://github.com')

    def test_chaining(self):
        self.assertEqual(
            str(URLPath().foo.bar(1, 'one').baz(a='a').qux),
            'foo/bar/1/one/baz/qux?a=a')

    def test_params(self):
        url = URLPath(params={'a': '2'})('/foo?a=1&b=2').bar(c=3)('?a=0')
        urlsplit = str(url).split('?')

        self.assertEqual(len(urlsplit), 2)

        params = urlsplit[1].split('&')

        self.assertEqual(urlsplit[0], '/foo/bar/')
        self.assertEqual(set(params), set(['a=0', 'a=1', 'a=2', 'b=2', 'c=3']))

    def test_multiple_params(self):
        url = URLPath('/')(a=1)(a=2)(a=3)
        params = str(url).split('?')[1].split('&')
        self.assertEqual(set(params), set(['a=1', 'a=2', 'a=3']))

    def test_multiple_params_list(self):
        url = URLPath('/')(a=[1, 2, 3])
        params = str(url).split('?')[1].split('&')
        self.assertEqual(set(params), set(['a=1', 'a=2', 'a=3']))

    def test_instance_regeneration(self):
        url = URLPath('/foo')
        original = str(url)
        url(a=1)
        self.assertEqual(str(url), original)

    def test_leading_slash(self):
        self.assertEqual(str(URLPath()('/foo').bar), '/foo/bar')

    def test_append_slash(self):
        self.assertEqual(str(URLPath().foo), 'foo')
        self.assertEqual(str(URLPath(append_slash=True).foo), 'foo/')

    def test_port(self):
        self.assertEqual(
            str(URLPath('http://github.com:8000').foo.bar),
            'http://github.com:8000/foo/bar')

    def test_add_operator_with_url(self):
        url = URLPath('start/of/path') + URLPath('end/of/path')
        self.assertTrue(isinstance(url, URLPath))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

    def test_div_operator_with_url(self):
        url = URLPath('start/of/path') / URLPath('end/of/path')
        self.assertTrue(isinstance(url, URLPath))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

    def test_add_operator_with_string(self):
        url = URLPath('start/of/path') + 'end/of/path'
        self.assertTrue(isinstance(url, URLPath))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

        url = 'start/of/path' + URLPath('end/of/path')
        self.assertTrue(isinstance(url, URLPath))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

    def test_div_operator_with_string(self):
        url = URLPath('start/of/path') / 'end/of/path'
        self.assertTrue(isinstance(url, URLPath))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

        url = 'start/of/path' / URLPath('end/of/path')
        self.assertTrue(isinstance(url, URLPath))
        self.assertEqual(str(url), 'start/of/path/end/of/path')
