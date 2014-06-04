"""Generic interface for path generation.
"""

from .utils import require_override


class Ladder(object):
    """Base class used to provide common methods for creating a path or
    path-like generator.

    This class should NOT be used directly and should instead only be used
    as a super class.
    """

    # Define our state attributes which correspond to the argument names of
    # the __init__() function. These attributes (minus the leading and trailing
    # "__") will be passed to subsequent generative calls.
    __attrs__ = ['__pathway__']

    # You are required to override this method. Parameters defined in __attrs__
    # will be passed to this function via **argument unpacking in __call__().
    # WARNING: Inside this function, the class instance attributes in __attrs__
    # should be assigned. If they are not, then a recursion error will result
    # during the generative call.
    @require_override
    def __init__(self, pathway=None, **params):  # pragma: no cover
        pass

    def __str__(self):
        return self.__getpathway__()

    def __repr__(self):   # pragma: no cover
        return '<{0} path="{1}">'.format(
            self.__class__.__name__, self.__getpathway__())

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
        removed. This is used to propagate init args to next class generation.
        """
        state = dict((attr.replace('__', ''), getattr(self, attr, None))
                     for attr in self.__attrs__)

        return state

    def __getattr__(self, path):
        """Treat attribute access as path concatenation."""
        return self(path)

    def __getpathway__(self):
        """Return current object as string."""
        return self.__pathway__

    @require_override
    def __preparestate__(self, *paths, **params):  # pragma: no cover
        """Given paths and params prepare arguments for call to
        class(**state).

        Generally, you will want to call self.__getstate__() and mutate the
        data in some way to get to the "next" class instance.
        """
        pass

    def __call__(self, *paths, **params):
        """Generate a new class instance from our self."""
        state = self.__preparestate__(*paths, **params)
        return self.__class__(**state)
