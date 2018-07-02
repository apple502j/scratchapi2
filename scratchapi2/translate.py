"""
Translate - Contains things related to automatic translation.
class Translate
- translate_status()
- languages()
- translate()
"""
import requests

class Translate(object):
    """Represents the Translate API."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Enforce this class as a singleton."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, api_url="https://translate-service.scratch.mit.edu/"):
        """Initialize the object with the API URL."""
        self.api_url = api_url

    def __repr__(self):
        """Represent the Translate API"""
        return "<Translate>"
    
    __str__ = __repr__

    def _request(self, path, *opts, api_url=None):
        return requests.get(
            (api_url or self.api_url)
            + path.format(*opts)
        ).json()

    def translate_status(self):
        """Check the status of the API."""
        try:
            req = self._request("")
            return req["ok"]
        except:
            return False

    def languages(self, locale="en"):
        """Return available langauges."""
        return self._request('supported?language={}', locale)

    def translate(self, locale="ja", text="Hello"):
        """Translate text."""
        return self._request('translate?language={0}&text={1}',
                             locale, text)['result']
