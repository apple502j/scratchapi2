"""
Scratch API modules with auth.
For example, you can use scratchapi2.Auth(username, password).User(username)
instead of scratchapi2.User(username)
"""

import requests
from .api import APIClass as __APIClass
from .user import User as __User, Project as __Project

#loginname = None

class APIClass(__APIClass):
    """Base class for auth."""
    def __init__(self, api_url="https://api.scratch.mit.edu/"):
        """Initialize this API with auth."""
        super().__init__(api_url)
        self._session = requests.session()

    def _request(self, path, *opts, api_url=None, method="get", params={}, headers={}, no_json=False):
        """Internal method to request data from the API."""
        def p(a):
            print(a)
            return a
        req = getattr(self._session, method, self._session.get)(
            p((api_url or self.api_url)
            + path.format(*opts)),
            data=params,
            headers=headers
        )
        print(req, req.headers)
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
        self.login(username, password)

    def login(self, username, password):
        req = self._request("csrf_token",
                            api_url="https://scratch.mit.edu/",
                            no_json=True)
        self._session.headers["X-CSRFToken"] = self._session.cookies["scratchcsrftoken"]
        self._session.headers["X-Requested-With"] = 'XMLHttpRequest'
        self._session.headers["Origin"] = 'https://scratch.mit.edu'
        self._session.cookies["permissions"] = '{}'
        print(self._session.headers)
        print(self._session.cookies)
        req2 = self._request("login",
                             api_url="https://scratch.mit.edu/",
                             method="post",
                             params={
                                 "username": username,
                                 "password": password,
                                 "useMessages": True
                             },
                             no_json=True)
        print(req2)
        print(self._session.headers)
        print(self._session.cookies)
        req3 = self._request("session/",
                             api_url="https://scratch.mit.edu/",
                             method="get")
        self._session.headers["X-Token"] = req3['user']['token']
