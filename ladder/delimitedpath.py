"""Delimited path generation.
"""

from .ladder import Ladder
from .utils import delimitedpathjoin


class DelimitedPath(Ladder):
    """Generate delimited strings using Ladder interface."""

    __attrs__ = ['__pathway__', '__delimiter__']

    def __init__(self, pathway=None, delimiter=''):
        self.__pathway__ = delimitedpathjoin(delimiter, pathway)
        self.__delimiter__ = delimiter

    def __add__(self, other):
        return self(other, delimiter=self.__delimiter__)
    __div__ = __add__
    __truediv__ = __add__

    def __radd__(self, other):
        return self.__class__(other, delimiter=self.__delimiter__)(self)
    __rdiv__ = __radd__
    __rtruediv__ = __radd__

    def __preparestate__(self, *paths, **params):
        """Join paths with our delimiter."""
        state = self.__getstate__()
        state['pathway'] = delimitedpathjoin(state['delimiter'],
                                             state['pathway'],
                                             *paths)

        return state
