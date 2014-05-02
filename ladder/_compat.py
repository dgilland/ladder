# pylint: skip-file
"""Python 2/3 compatibility
"""

import sys


PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    from urllib.parse import (
        urlencode, urlsplit, urlunsplit, parse_qs, parse_qsl)

    text_type = str

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())
else:  # pragma: no cover
    from urllib import urlencode
    from urlparse import urlsplit, urlunsplit, parse_qs, parse_qsl

    text_type = unicode

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
