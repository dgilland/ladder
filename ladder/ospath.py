"""OS path generation.
"""

from .ladder import Ladder
from .utils import ospathjoin


class OSPath(Ladder):
    """Generate os.path strings using Ladder interface."""

    __attrs__ = ['__pathway__']

    def __init__(self, pathway=None):
        self.__pathway__ = ospathjoin(pathway)

    def __preparestate__(self, *paths, **params):
        """Join paths using os.path."""
        state = self.__getstate__()
        state['pathway'] = ospathjoin(state['pathway'], *paths)

        return state
