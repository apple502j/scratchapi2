"""Contains the APIClass and APISingleton base classes."""
import requests

class APIClass(object):
    """Base class for classes that access the API."""

    def __init__(self, api_url="https://api.scratch.mit.edu/"):
        """Initialize the object with the API URL."""
        self.api_url = api_url

    def __repr__(self):
        """Represent the object."""
        return "<{}>".format(type(self).__name__)

    __str__ = __repr__

    def _request(self, path, *opts, api_url=None):
        """Internal method to request data from the API."""
        return requests.get(
            (api_url or self.api_url)
            + path.format(*opts)
        ).json()

class APISingleton(APIClass):
    """Base class for singleton classes that access the API."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Enforce this class as a singleton."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
