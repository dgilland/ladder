"""URL path generation.
"""

from .ladder import Ladder
from .utils import urlpathjoin
from ._compat import (
    iteritems,
    urlencode,
    urlsplit,
    urlunsplit,
    parse_qsl)


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


class URLPath(Ladder):
    """Generate URLs using Ladder interface."""

    __attrs__ = ['__pathway__', '__params__', '__append_slash__']

    def __init__(self, pathway=None, params=None, append_slash=False):
        self.__pathway__ = urlpathjoin(pathway)
        self.__append_slash__ = append_slash
        self.__params__ = []

        self.__setparams__(params)

    def __getpathway__(self):
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
            self.__pathway__ = urlunsplit(urlparts)

        if params:
            self.__params__ += flatten_params(params)

    @property
    def __urlsplit__(self):
        """Return urlsplit() of current URL."""
        return urlsplit(self.__pathway__)

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

        state['pathway'] = urlpathjoin(state['pathway'], *paths)
        state['params'] = state['params'] + list(iteritems(params))

        # Use `__class__` to spawn new generation in case we are a subclass.
        return self.__class__(**state)

# class StrictURL(URL):
#    def __init__(self, url=None):
#        super(StrictURL, self).__init__(url=url)
#
#    def __getattr__(self, attr):
#        raise AttributeError(attr)
#
#    def __call__(self, *args, **kargs):
#        state = self.__getstate__()
#
#        try:
#            url = state['url'].format(*args, **kargs)
#        except IndexError:
#            raise TypeError(
#                ('{0} must be called with correct format arguments.'
#                 .format(repr(self)))
#            )
#
#        return self.__class__(**state)


def flatten_params(params):
    """Flatten URL params into list of tuples. If any param value is a list or
    tuple, then map each value to the param key.
    >>> params = [('a', 1), ('a', [2, 3])]
    >>> assert flatten_params(params) == [('a', 1), ('a', 2), ('a', 3)]
    >>> params = {'a': [1, 2, 3]}
    >>> assert flatten_params(params) == [('a', 1), ('a', 2), ('a', 3)]
    """
    if isinstance(params, dict):
        params = list(iteritems(params))

    flattened = []
    for param, value in params:
        if isinstance(value, (list, tuple)):
            flattened += zip([param] * len(value), value)
        else:
            flattened.append((param, value))

    return flattened
