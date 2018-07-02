"""
Misc - Contains things that are not generic.
class Misc
- translate_status()
- languages()
- translate()
"""
import requests

class Misc(object):
    """ Misc - contains things that are not generic. """
    def __repr__(self):
        """ Always returns <ScratchAPI2 Misc> """
        return "<ScratchAPI2 Misc>"
    __str__ = __repr__

    @staticmethod
    def translate_status():
        """ Check the status of the API """
        try:
            req = requests.get("https://translate-service.scratch.mit.edu/").json()
            return req["ok"]
        except:
            return "false"

    @staticmethod
    def languages(locale="en"):
        """ Return available langauges. """
        req = requests.get("https://translate-service.scratch.mit.edu/supported?language=" + locale).json()
        return req

    @staticmethod
    def translate(locale="ja", text="Hello"):
        """ Translate API """
        req = requests.get("https://translate-service.scratch.mit.edu/translate?language={0}&text={1}".format(locale, text)).json()
        return req["result"]
