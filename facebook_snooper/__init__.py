from .__version__ import __version__
from .core.session import Session


def default_session():
    return Session()