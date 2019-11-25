from .__version__ import __version__
from .core.session import Session
from .core.wrapper import BrowserWrapper
from .core.exceptions import LogInError, NotConnectedError


def init_session():
    return Session(BrowserWrapper())