# pylint: skip-file
'''Python 2/3 compatibility
'''

import sys


PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qs
    text_type = str
else:  # pragma: no cover
    from urllib import urlencode
    from urlparse import urlsplit, urlunsplit, parse_qs
    text_type = unicode
