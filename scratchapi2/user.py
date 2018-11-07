"""
Scratch API User

Anything returned from API does not contain any attributes.
Use info() to set/get it.

Contains classes:
* Project
* User
* Classroom
"""

import warnings
import requests
from .excs import ScratchAPIError
from .gclass import GenericData

#pylint: disable=too-many-instance-attributes,too-many-function-args

def _request(path, *opts, api_url="https://api.scratch.mit.edu/"):
    result = requests.get(api_url + path.format(*opts)).json()
    if 'code' in result:
        raise ScratchAPIError(result['code'] + ': ' + result['message'])
    return result

def _streaming_request(fileobj, path, *opts,
                       api_url="https://projects.scratch.mit.edu/"):
    """Make a large request (usually a project's JSON). This must provide
    a file object ``fileobj`` to copy the request into.
    """
    req = requests.get(api_url + path.format(*opts), stream=True)
    for block in req.iter_content(1024):
        fileobj.write(block)

class Studio(GenericData):
    """Represents a studio."""
    _repr_str = '<Studio {studio_id}>'
    studio_id = None

class Project(object):
    """Represents a Scratch Project."""

    projectid = None

    def __init__(self, projectid, getinfo=True):
        """Initialize a Project."""
        self.projectid = int(projectid)
        if getinfo:
            self.info()

    def __repr__(self):
        """Represent a Project."""
        return "<Project {0}>".format(self.projectid)

    __str__ = __repr__

    def __eq__(self, other):
        """If the project IDs are equal, the projects are considered equal."""
        return self.projectid == other.projectid

    def info(self):
        """Get information about a project. It sets its dict and returns it."""
        req = _request('projects/{0}', self.projectid)
        self.title = req["title"]
        self.description = req["description"]
        self.instructions = req["instructions"]
        #this does getinfo because info is only called with getinfo=True anyway
        self.author = User(req["author"]["username"], getinfo=True)
        self.image = req["image"]
        self.created = req["history"]["created"]
        self.modified = req["history"]["modified"]
        self.shared = req["history"]["shared"]
        self.views = req["stats"]["views"]
        self.loves = req["stats"]["loves"]
        self.favorites = req["stats"]["favorites"]
        self.comments = req["stats"]["comments"]
        #renamed to avoid conflict with "remix" method
        self.remix_count = req["stats"]["remixes"]
        self.parent = (
            Project(req["remix"]["parent"], getinfo=True)
            if req['remix']['parent']
            else None
        )
        self.root = (
            Project(req["remix"]["root"], getinfo=False)
            if req['remix']['root']
            else None
        )

        # Just for convenience
        self.notes = self.description
        self.credits = self.description
        # links
        self.url = "https://scratch.mit.edu/projects/{}".format(
            self.projectid
        )
        self.remixes_url = self.url + "/remixes"
        self.remixtree_url = self.url + "/remixtree"
        self.studios_url = self.url + "/studios"
        self.see_inside_url = self.url + "#editor"
        self.fullscreen_url = self.url + "#fullscreen"
        self.embed_url = "https://scratch.mit.edu/projects/embed/{}".format(
            self.projectid
        )
        self.embed_html = """<iframe
    allowtransparency="true"
    width="485"
    height="402"
    src="{0}?autostart=false"
    frameborder="0"
    allowfullscreen
></iframe>""".format(self.embed_url)
        self.beta_url = "https://beta.scratch.mit.edu/#{}".format(
            self.projectid
        )
        return self.__dict__.copy()

    @property
    def preview_url(self):
        """
        This is kept for a historical reason. You had better use
        Project.beta_url instead.
        """
        warnings.warn("Use of Project.preview_url will "
                      "be deprecated. Please use Project."
                      "beta_url.", PendingDeprecationWarning)
        return self.beta_url

    def remixes(self, limit=3, offset=0):
        """Yield all remixes of this Project."""
        req = _request("projects/{0}/remixes?limit={1}&offset={2}",
                       self.projectid, limit, offset)
        for remix in req:
            yield Project(remix['id'], getinfo=False)

    def studios(self, limit=3, offset=0):
        """Yield all studios this Project belongs to."""
        req = _request('projects/{0}/studios?limit={1}&offset={2}',
                       self.projectid, limit, offset)
        for studio in req:
            yield Studio(
                owner=studio["owner"],
                studio_id=studio["id"],
                title=studio["title"],
                description=studio["description"],
                image=studio["image"],
                created_at=studio["history"]["created"],
                last_modified=studio["history"]["modified"],
                followers=studio["stats"]["followers"]
            )

    def save_json(self, filename_or_obj):
        """Save a project's JSON to a file."""
        if isinstance(filename_or_obj, str):
            filename_or_obj = open(filename_or_obj, 'wb')
        with filename_or_obj:
            _streaming_request(filename_or_obj,
                               '{}',
                               self.projectid)

class User(object):
    """Represents a Scratch user."""

    username = None

    def __init__(self, username, getinfo=True):
        """Initialize a User."""
        self.username = username
        if getinfo:
            self.info()

    def __str__(self):
        """Represent a User."""
        return "<User {0}>".format(self.username)

    __repr__ = __str__

    def __eq__(self, other):
        """If the usernames are equal, the Users are considered equal.
        (Equality is case-insensitive)
        """
        return self.username.lower() == other.username.lower()

    def info(self):
        """Get information about an user. It sets its dict and returns it."""
        req = _request('users/{0}', self.username)
        self.userid = req["id"]
        self.joined = req["history"]["joined"]
        self.images = req["profile"]["images"]
        self.status = req["profile"]["status"]
        self.bio = req["profile"]["bio"]
        self.country = req["profile"]["country"]

        # Just for convenience
        self.joined_at = self.joined
        self.about_me = self.status
        self.what_im_working_on = self.bio
        self.what_working_on = self.bio
        return self.__dict__.copy()

    def following(self, limit=100, offset=0):
        """Yield other Users this User follows."""
        req = _request("users/{0}/following?limit={1}&offset={2}",
                       self.username, limit, offset)
        for user in req:
            yield User(user["username"], getinfo=False)

    def followers(self, limit=100, offset=0):
        """Yield other Users that follow this User."""
        req = requests.get("users/{0}/followers?limit={1}&offset={2}",
                           self.username, limit, offset)
        for user in req:
            yield User(user["username"], getinfo=False)

    def unread_messages(self):
        """Return the number of messages this User has not read."""
        req = _request("users/{0}/messages/count",
                       self.username)
        return req["count"]

    def projects(self, limit=10, offset=0):
        """Yield the user's Projects."""
        req = _request("users/{0}/projects?limit={1}&offset={2}",
                       self.username, limit, offset)
        for project in req:
            yield Project(project["id"], getinfo=False)

    def favorites(self, limit=10, offset=0):
        """Yield the user's favorite Projects."""
        req = _request("users/{0}/favorites?limit={1}&offset={2}",
                       self.username, limit, offset)
        for project in req:
            yield Project(project["id"], getinfo=False)

    def curating(self, limit=10, offset=0):
        """ Yield what studios the user is curating. """
        req = _request("users/{0}/studios/curate?limit={1}&offset={2}",
                       self.username, limit, offset)
        for studio in req:
            yield Studio(
                owner=studio["owner"],
                studio_id=studio["id"],
                title=studio["title"],
                description=studio["description"],
                image=studio["image"],
                created_at=studio["history"]["created"],
                last_modified=studio["history"]["modified"],
                followers=studio["stats"]["followers"]
                )

class Classroom(object):
    """Represents a Scratch Classroom."""

    classid = None

    def __init__(self, classid, getinfo=True):
        """Initialize a Classroom."""
        self.classid = int(classid)
        if getinfo:
            self.info()

    def __str__(self):
        """Represent a Classroom."""
        return "<Class {0}>".format(self.classid)

    __repr__ = __str__

    def __eq__(self, other):
        """If the class IDs are equal, the Classroooms are considered equal."""
        return self.classid == other.classid

    def info(self):
        """Get an information about a classroom. It sets its dict
        and returns it.
        """
        req = _request("https://api.scratch.mit.edu/classrooms/{0}",
                       self.classid)
        self.title = req["title"]
        self.start = req["date_start"]
        self.end = req["date_end"]
        self.images = req["images"]
        self.status = req["status"]
        self.description = req["description"]
        self.educator = User(req["educator"]["username"], getinfo=True)

        # Just for convenience
        self.about_class = self.status
        self.bio = self.description
        self.what_were_working_on = self.description
        self.what_working_on = self.description
        self.teacher = self.educator
        return self.__dict__.copy()
