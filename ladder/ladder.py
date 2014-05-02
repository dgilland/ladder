"""Easy URL generation via object notation.
"""

from functools import partial

from ._compat import (
    text_type,
    iteritems,
    urlencode,
    urlsplit,
    urlunsplit,
    parse_qsl
)


class URLSplitParts(object):
    """Convert return from urlsplit into an updatable named attribute object.
    """
    def __init__(self, scheme, netloc, path, query, fragment):
        self.scheme = scheme
        self.netloc = netloc
        self.path = path
        self.query = query
        self.fragment = fragment

    def __iter__(self):
        return iter([
            self.scheme,
            self.netloc,
            self.path,
            self.query,
            self.fragment
        ])


class URL(object):
    """Generate URLs using object notation."""

    __attrs__ = ['__url__', '__params__', '__append_slash__']

    def __init__(self, url=None, params=None, append_slash=False):
        self.__url__ = urlpathjoin(url)
        self.__append_slash__ = append_slash
        self.__params__ = []

        self.__setparams__(params)

    def __str__(self):
        return self.__geturl__()

    def __repr__(self):   # pragma: no cover
        return '<{0} url={1}>'.format(
            self.__class__.__name__, self.__geturl__())

    def __add__(self, other):
        return self(other)
    __div__ = __add__
    __truediv__ = __add__

    def __radd__(self, other):
        return self.__class__(other)(self)
    __rdiv__ = __radd__
    __rtruediv__ = __radd__

    def __getstate__(self):
        """Return self.__attrs__ resolved onto self with leading/trailing `__`
        removed. This is used to propagate init args to next URL generation.
        """
        state = dict((attr.replace('__', ''), getattr(self, attr, None))
                     for attr in self.__attrs__)

        return state

    def __geturl__(self):
        """Return current URL as string. Combines query string parameters found
        in string URL with any named parameters created during `__call__`."""
        urlparts = self.__urlparts__

        if self.__append_slash__ and not urlparts.path.endswith('/'):
            urlparts.path = urlparts.path + '/'

        urlparts.query = urlencode(self.__params__)

        return urlunsplit(urlparts)

    def __setparams__(self, params):
        """Extract any query string parameters from URL and merge with
        `params`.
        """
        urlparts = self.__urlparts__
        if urlparts.query:
            # move url query to params and remove it from url string
            self.__params__ += parse_qsl(urlparts.query)
            urlparts.query = None
            self.__url__ = urlunsplit(urlparts)

        if params:
            if isinstance(params, dict):
                params = list(iteritems(params))
            self.__params__ += params

    @property
    def __urlsplit__(self):
        """Return urlsplit() of current URL."""
        return urlsplit(self.__url__)

    @property
    def __urlparts__(self):
        """Return urlsplit as URLSplitParts object."""
        return URLSplitParts(*self.__urlsplit__)

    def __getattr__(self, path):
        """Treat attribute access as path concatenation."""
        return self(path)

    def __call__(self, *paths, **params):
        """Generate a new URL while extending the `url` with `path` and query
        `params`.
        """
        state = self.__getstate__()

        state['url'] = urlpathjoin(state['url'], *paths)
        state['params'] += list(iteritems(params))

        # Use `__class__` to spawn new generation in case we are a subclass.
        return self.__class__(**state)


class API(URL):
    """Add URL generation to an HTTP request client. Requires that the `client`
    support HTTP verbs as lowercase methods. An example client would be the one
    from Requests package.
    """
    __attrs__ = [
        '__client__',
        '__url__',
        '__params__',
        '__append_slash__',
        '__upper_methods__'
    ]

    __http_methods__ = [
        'head',
        'options',
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ]

    def __init__(self, client, url='', params=None,
                 append_slash=False, upper_methods=True):
        super(API, self).__init__(url, params, append_slash)
        self.__client__ = client
        self.__upper_methods__ = upper_methods

        # Dynamically set client proxy methods accessed during the getattr
        # call.
        self.__methods__ = [
            method.upper() if self.__upper_methods__ else method
            for method in self.__http_methods__
        ]

    def __getattr__(self, attr):
        if attr in self.__methods__:
            # Proxy call to client method with url bound to first argument.
            return partial(getattr(self.__client__, attr.lower()),
                           self.__geturl__())
        else:
            return super(API, self).__getattr__(attr)


def urlpathjoin(*paths):
    """Join URL paths into single URL while maintaining leading and trailing
    slashes if present on first and last elements respectively.

    >>> assert urlpathjoin('') == ''
    >>> assert urlpathjoin(['', '/a']) == '/a'
    >>> assert urlpathjoin(['a', '/']) == 'a/'
    >>> assert urlpathjoin(['', '/a', '', '', 'b']) == '/a/b'
    >>> assert urlpathjoin(['/a/', 'b/', '/c', 'd', 'e/']) == '/a/b/c/d/e/'
    >>> assert urlpathjoin(['a', 'b', 'c']) == 'a/b/c'
    >>> assert urlpathjoin(['a/b', '/c/d/', '/e/f']) == 'a/b/c/d/e/f'
    >>> assert urlpathjoin('/', 'a', 'b', 'c', 1, '/') == '/a/b/c/1/'
    >>> assert urlpathjoin([]) == ''
    """
    paths = [text_type(path) for path in flatten(paths) if path]
    leading = '/' if paths and paths[0].startswith('/') else ''
    trailing = '/' if paths and paths[-1].endswith('/') else ''
    url = (leading +
           '/'.join([p.strip('/') for p in paths if p.strip('/')]) +
           trailing)
    return url


def iterflatten(items):
    """Return iterator which flattens list/tuple of lists/tuples
    >>> to_flatten = [1, [2,3], [4, [5, [6]], 7], 8]
    >>> assert list(iterflatten(to_flatten)) == [1,2,3,4,5,6,7,8]
    """
    for item in items:
        if isinstance(item, (list, tuple)):
            for itm in flatten(item):
                yield itm
        else:
            yield item


def flatten(items):
    """Return flattened list of a list/tuple of lists/tuples
    >>> assert flatten([1, [2,3], [4, [5, [6]], 7], 8]) == [1,2,3,4,5,6,7,8]
    """
    return list(iterflatten(items))
