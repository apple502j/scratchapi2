"""
Translate - Contains things related to automatic translation.
class Translate
- translate_status()
- languages()
- translate()
"""
from .api import APISingleton

class Translate(APISingleton):
    """Represents the Translate API."""

    def __init__(self, api_url="https://translate-service.scratch.mit.edu/"):
        """Initialize the object with the API URL."""
        super().__init__(api_url)

    def translate_status(self):
        """Check the status of the API."""
        try:
            req = self._request("")
            return req["ok"]
        except KeyError:
            return False

    def languages(self, locale="en"):
        """Return available langauges."""
        return self._request('supported?language={}', locale)

    def translate(self, locale="ja", text="Hello"):
        """Translate text."""
        return self._request('translate?language={0}&text={1}',
                             locale, text)['result']
