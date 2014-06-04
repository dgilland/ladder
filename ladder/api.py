"""API client wrapper.
"""

from functools import partial

from .urlpath import URLPath


class API(URLPath):
    """Add URL generation to an HTTP request client. Requires that the `client`
    support HTTP verbs as lowercase methods. An example client would be the one
    from Requests package.
    """
    __attrs__ = [
        '__client__',
        '__pathway__',
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

    def __init__(self, client, pathway='', params=None,
                 append_slash=False, upper_methods=True):
        super(API, self).__init__(pathway, params, append_slash)
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
                           self.__getpathway__())
        else:
            return super(API, self).__getattr__(attr)
