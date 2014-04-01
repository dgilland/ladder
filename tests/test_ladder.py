
from unittest import TestCase

from ladder import URL, API


class TestURL(TestCase):

    def test_empty_url(self):
        self.assertEqual(str(URL()), '')

    def test_initialized_url(self):
        self.assertEqual(str(URL('http://github.com')), 'http://github.com')

    def test_chaining(self):
        self.assertEqual(str(URL().foo.bar(1, 'one').baz(a='a').qux), 'foo/bar/1/one/baz/qux?a=a')

    def test_params(self):
        url = URL(params={'a': '2'})('/foo?a=1&b=2').bar(c=3)('?a=0')
        urlsplit = str(url).split('?')

        self.assertEqual(len(urlsplit), 2)

        params = urlsplit[1].split('&')

        self.assertEqual(urlsplit[0], '/foo/bar/')
        self.assertEqual(set(params), set(['a=0', 'a=1', 'a=2', 'b=2', 'c=3']))

    def test_multiple_params(self):
        url = URL('/')(a=1)(a=2)(a=3)
        params = str(url).split('?')[1].split('&')
        self.assertEqual(set(params), set(['a=1', 'a=2', 'a=3']))

    def test_leading_slash(self):
        self.assertEqual(str(URL()('/foo').bar), '/foo/bar')

    def test_append_slash(self):
        self.assertEqual(str(URL().foo), 'foo')
        self.assertEqual(str(URL(append_slash=True).foo), 'foo/')

    def test_port(self):
        self.assertEqual(str(URL('http://github.com:8000').foo.bar), 'http://github.com:8000/foo/bar')

    def test_add_operator_with_url(self):
        url = URL('start/of/path') + URL('end/of/path')
        self.assertTrue(isinstance(url, URL))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

    def test_div_operator_with_url(self):
        url = URL('start/of/path') / URL('end/of/path')
        self.assertTrue(isinstance(url, URL))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

    def test_add_operator_with_string(self):
        url = URL('start/of/path') + 'end/of/path'
        self.assertTrue(isinstance(url, URL))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

        url = 'start/of/path' + URL('end/of/path')
        self.assertTrue(isinstance(url, URL))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

    def test_div_operator_with_string(self):
        url = URL('start/of/path') / 'end/of/path'
        self.assertTrue(isinstance(url, URL))
        self.assertEqual(str(url), 'start/of/path/end/of/path')

        url = 'start/of/path' / URL('end/of/path')
        self.assertTrue(isinstance(url, URL))
        self.assertEqual(str(url), 'start/of/path/end/of/path')


class MockClient(object):
    def head(self, *args, **kargs):
        return ('head', args, kargs)

    def options(self, *args, **kargs):
        return ('options', args, kargs)

    def get(self, *args, **kargs):
        return ('get', args, kargs)

    def post(self, *args, **kargs):
        return ('post', args, kargs)

    def put(self, *args, **kargs):
        return ('put', args, kargs)

    def patch(self, *args, **kargs):
        return ('patch', args, kargs)

    def delete(self, *args, **kargs):
        return ('delete', args, kargs)


class TestAPI(TestCase):
    client = MockClient()

    def setUp(self):
        self.api_lower = API(self.client, 'http://github.com', upper_methods=False)
        self.api_upper = API(self.client, 'http://github.com', upper_methods=True)

    def test_head_method(self):
        expected = ('head', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.head(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.HEAD(a=1)), 'http://github.com/foo/HEAD?a=1')
        self.assertEqual(self.api_upper.foo.HEAD(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.head(a=1)), 'http://github.com/foo/head?a=1')

    def test_options_method(self):
        expected = ('options', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.options(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.OPTIONS(a=1)), 'http://github.com/foo/OPTIONS?a=1')
        self.assertEqual(self.api_upper.foo.OPTIONS(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.options(a=1)), 'http://github.com/foo/options?a=1')

    def test_get_method(self):
        expected = ('get', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.get(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.GET(a=1)), 'http://github.com/foo/GET?a=1')
        self.assertEqual(self.api_upper.foo.GET(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.get(a=1)), 'http://github.com/foo/get?a=1')

    def test_post_method(self):
        expected = ('post', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.post(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.POST(a=1)), 'http://github.com/foo/POST?a=1')
        self.assertEqual(self.api_upper.foo.POST(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.post(a=1)), 'http://github.com/foo/post?a=1')

    def test_put_method(self):
        expected = ('put', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.put(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.PUT(a=1)), 'http://github.com/foo/PUT?a=1')
        self.assertEqual(self.api_upper.foo.PUT(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.put(a=1)), 'http://github.com/foo/put?a=1')

    def test_patch_method(self):
        expected = ('patch', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.patch(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.PATCH(a=1)), 'http://github.com/foo/PATCH?a=1')
        self.assertEqual(self.api_upper.foo.PATCH(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.patch(a=1)), 'http://github.com/foo/patch?a=1')

    def test_delete_method(self):
        expected = ('delete', ('http://github.com/foo',), {'a': 1})
        self.assertEqual(self.api_lower.foo.delete(a=1), expected)
        self.assertEqual(str(self.api_lower.foo.DELETE(a=1)), 'http://github.com/foo/DELETE?a=1')
        self.assertEqual(self.api_upper.foo.DELETE(a=1), expected)
        self.assertEqual(str(self.api_upper.foo.delete(a=1)), 'http://github.com/foo/delete?a=1')
