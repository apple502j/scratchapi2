"""
Scratch API modules with auth.
For example, you can use scratchapi2.Auth(username, password).User(username)
instead of scratchapi2.User(username)
"""

import requests
from .api import APIClass as __APIClass
from .user import (User as __User, Project as __Project)

#loginname = None

class APIClass(__APIClass):
    """Base class for auth."""
    def __init__(self, api_url="https://api.scratch.mit.edu/"):
        """Initialize this API with auth."""
        super().__init__(api_url)
        self._session = requests.session()

    def _request(self, path, *opts, api_url=None, method="get", params={}, headers={}, no_json=False):
        """Internal method to request data from the API."""
        methods = {
            "get": self._session.get,
            "post": self._session.post
        }
        if not methods.get(method, None):
            raise ValueError("Unknown method: {}".format(method))
        req = methods[method](
            (api_url or self.api_url)
            + path.format(*opts),
            data=params,
            headers=headers
        )
        return req.text if no_json else req.json()

class APISingleton(APIClass):
    """Base class for singleton classes that access the API."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Enforce this class as a singleton."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

class Auth(APIClass):
    """All apis with auth are in this class."""
    def __init__(self, username, password):
        super().__init__()
        self.loginuser = username
        self._headers = {}
        self.login(username, password)

    def login(self, username, password):
        req=self._request("session",
                        api_url="https://scratch.mit.edu/",
                        params={"X-Requested-With":"XMLHttpRequest"},
                        no_json=True)
        self._headers["Cookie"]="scratchcsrftoken={};".format(
            self._session.cookies["scratchcsrftoken"])
        self._headers["X-CSRFToken"]=self._session.cookies["scratchcsrftoken"];
        print(self._headers)
        print(self._session.cookies)
        req2=self._request("login",
                        api_url="https://scratch.mit.edu/",
                        method="post",
                        params={
                            "username": username,
                            "password": password,
                            "csrftoken": self._session.cookies["scratchcsrftoken"],
                            "csrfmiddlewaretoken": self._session.cookies["scratchcsrftoken"]
                        },
                        headers=self._headers,
                        no_json=True)
        print(self._headers)
        print(self._session.cookies)
        #self._headers["Cookie"]+="scratchsessionsid={};".format(
        #    self._session.cookies["scratchsessionsid"])
        self._headers["X-CSRFToken"]=self._session.cookies["scratchcsrftoken"];
