'''Easy URL generation via object notation.
'''

from functools import partial

from ._compat import (
    text_type,
    urlencode,
    urlsplit,
    urlunsplit,
    parse_qs
)


class URL(object):
    '''Generate URLs using object notation.'''

    __attrs__ = ['__url__', '__params__', '__append_slash__']

    def __init__(self, url='', params=None, append_slash=False):
        if params is None:
            params = {}

        self.__url__ = urlpathjoin(url)
        self.__params__ = params
        self.__append_slash__ = append_slash

    def __str__(self):
        return self.__geturl__()

    def __repr__(self):   # pragma: no cover
        return '<{0} url={1}>'.format(self.__class__.__name__, self.__geturl__())

    def __add__(self, other):
        return self(other)
    __div__ = __add__
    __truediv__ = __add__

    def __radd__(self, other):
        return self.__class__(other)(self)
    __rdiv__ = __radd__
    __rtruediv__ = __radd__

    def __getstate__(self):
        '''Return self.__attrs__ resolved onto self with leading/trailing `__` removed.
        This is used to propagate init args to next URL generation.
        '''
        state = dict((attr.replace('__', ''), getattr(self, attr, None)) for attr in self.__attrs__)

        # Only shallow copy `params` since we just want to ensure updating `params`
        # doesn't modify previous generations. Could use deepcopy but want to avoid
        # the overhead.
        state['params'] = state['params'].copy()

        return state

    def __geturl__(self):
        '''Return current URL as string. Combines query string parameters found in
        string URL with any named parameters created during `__call__`.'''
        scheme, netloc, path, query, fragment = self.__urlsplit__

        if self.__append_slash__ and not path.endswith('/'):
            path = path + '/'

        query = dict(parse_qs(query))
        query.update(self.__params__)
        query = urlencode(query)

        return urlunsplit((scheme, netloc, path, query, fragment))

    @property
    def __urlsplit__(self):
        '''Return urlsplit() of current URL.'''
        return urlsplit(self.__url__)

    def __getattr__(self, path):
        '''Treat attribute access as path concatenation.'''
        return self(path)

    def __call__(self, *paths, **params):
        '''Generate a new URL while extending the `url` with `path` and query `params`.'''
        state = self.__getstate__()

        state['url'] = urlpathjoin(state['url'], *paths)
        state['params'].update(params)

        # Use `__class__` to spawn new generation in case we are a subclass.
        return self.__class__(**state)


class API(URL):
    '''Add URL generation to an HTTP request client. Requires that the `client` support
    HTTP verbs as lowercase methods. An example client would be the one from Requests package.

    Since the HTTP verbs are class methods, if
    '''
    __attrs__ = ['__client__', '__url__', '__params__', '__append_slash__', '__uppercase_methods__']
    __http_methods__ = ['head', 'options', 'get', 'post', 'put', 'patch', 'delete']

    def __init__(self, client, url='', params=None, append_slash=False, uppercase_methods=True):
        super(API, self).__init__(url, params, append_slash)
        self.__client__ = client
        self.__uppercase_methods__ = uppercase_methods

        # Dynamically set client proxy methods accessed during the getattr call.
        self.__methods__ = [
            method.upper() if self.__uppercase_methods__ else method for method in self.__http_methods__
        ]

    def __getattr__(self, attr):
        if attr in self.__methods__:
            # Proxy call to client method with url bound to first argument.
            return partial(getattr(self.__client__, attr.lower()), self.__geturl__())
        else:
            return super(API, self).__getattr__(attr)


def urlpathjoin(*paths):
    '''Join URL paths into single URL while maintaining leading and trailing slashes
    if present on first and last elements respectively.

    >>> assert urlpathjoin(['/a/', 'b/', '/c', 'd', 'e/']) == '/a/b/c/d/e/'
    >>> assert urlpathjoin(['a', 'b', 'c']) == 'a/b/c'
    >>> assert urlpathjoin('/', 'a', 'b', 'c', 1, '/') == '/a/b/c/1/'
    >>> assert urlpathjoin([]) == ''
    '''
    paths = [text_type(path) for path in flatten(paths)]
    leading = '/' if paths and paths[0].startswith('/') else ''
    trailing = '/' if paths and paths[-1].endswith('/') else ''
    url = leading + '/'.join([p.strip('/') for p in paths if p.strip('/')]) + trailing
    return url


def iterflatten(items):
    '''Return iterator which flattens list/tuple of lists/tuples
    >>> assert list(iterflatten([1, [2,3], [4, [5, [6]], 7], 8])) == [1,2,3,4,5,6,7,8]
    '''
    for item in items:
        if isinstance(item, (list, tuple)):
            for itm in flatten(item):
                yield itm
        else:
            yield item


def flatten(items):
    '''Return flattened list of a list/tuple of lists/tuples
    >>> assert flatten([1, [2,3], [4, [5, [6]], 7], 8]) == [1,2,3,4,5,6,7,8]
    '''
    return list(iterflatten(items))
