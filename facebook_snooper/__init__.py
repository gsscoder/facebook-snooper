from .__version__ import __version__
from .core.session import Session
from .core.session import FacebookSession


def default_session():
    return FacebookSession()