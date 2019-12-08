from .__version__ import __version__
from .core.session import Session
from .core.wrapper import BrowserWrapper
from .core.exceptions import LogInError, NotConnectedError
from .core._parser import InfoTypes, ResultTypes


def init_session():
    return Session(BrowserWrapper())