'''Package API
'''

from .ladder import URL, API, urlpathjoin, flatten, iterflatten

from .__meta__ import (
    __title__,
    __summary__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)

__all__ = ['URL', 'API', 'urlpathjoin', 'flatten', 'iterflatten']
