from .__version__ import __version__
from .core.session import Session
from .core.exceptions import LogInError, NotConnectedError

def default_session():
    return Session()