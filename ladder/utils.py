"""General utility functions.
"""

import os
from functools import wraps

from ._compat import (
    text_type
)


def require_override(func):
    """Decorator which raises NotImplementedError when method called."""
    # pylint: disable=missing-docstring,unused-argument
    @wraps(func)
    def decorated(*args, **kargs):
        raise NotImplementedError('Method must be overridden.')
    return decorated


def ospathjoin(*paths):
    """Join OS path into a single path."""
    paths = [text_type(path) for path in flatten(paths) if path]
    return os.path.join(*paths) if paths else ''


def delimitedpathjoin(delimiter, *paths):
    """Join delimited path using specified delimiter.

    >>> assert delimitedpathjoin('.', '') == ''
    >>> assert delimitedpathjoin('.', '.') == '.'
    >>> assert delimitedpathjoin('.', ['', '.a']) == '.a'
    >>> assert delimitedpathjoin('.', ['a', '.']) == 'a.'
    >>> assert delimitedpathjoin('.', ['', '.a', '', '', 'b']) == '.a.b'
    >>> ret = '.a.b.c.d.e.'
    >>> assert delimitedpathjoin('.', ['.a.', 'b.', '.c', 'd', 'e.']) == ret
    >>> assert delimitedpathjoin('.', ['a', 'b', 'c']) == 'a.b.c'
    >>> ret = 'a.b.c.d.e.f'
    >>> assert delimitedpathjoin('.', ['a.b', '.c.d.', '.e.f']) == ret
    >>> ret = '.a.b.c.1.'
    >>> assert delimitedpathjoin('.', '.', 'a', 'b', 'c', 1, '.') == ret
    >>> assert delimitedpathjoin('.', []) == ''
    """
    paths = [text_type(path) for path in flatten(paths) if path]

    if len(paths) == 1:
        # Special case where there's no need to join anything.
        # Doing this because if path==[delimiter], then an extra slash would be added
        # if the else clause ran instead.
        path = paths[0]
    else:
        leading = delimiter if paths and paths[0].startswith(delimiter) else ''
        trailing = delimiter if paths and paths[-1].endswith(delimiter) else ''
        path = ''.join([leading,
                        delimiter.join([p.strip(delimiter)
                                        for p in paths if p.strip(delimiter)]),
                        trailing])

    return path


def urlpathjoin(*paths):
    """Join URL paths into single URL while maintaining leading and trailing
    slashes if present on first and last elements respectively.
    """
    return delimitedpathjoin('/', *paths)


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
