"""
Scratch API User

Anything returned from API does not contain any attributes.
Use info() to set/get it.

Contains classes:
* Project
* User
* Classroom
* Comment
"""

import warnings
import requests
from .excs import ScratchAPIError

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
        self.visibility = req["visibility"]
        self.public = req["public"]
        self.comment_open = req["comments_allowed"]
        self.author = User(req["author"]["username"], getinfo=True)
        self.image = req["image"]
        self.created = req["history"]["created"]
        self.modified = req["history"]["modified"]
        self.shared = req["history"]["shared"]
        self.views = req["stats"]["views"]
        self.loves = req["stats"]["loves"]
        self.favorites = req["stats"]["favorites"]
        self.comment_counts = req["stats"]["comments"]
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
        self.studios_url = self.url + "/studios"
        self.see_inside_url = self.url + "/editor"
        self.fullscreen_url = self.url + "/fullscreen"
        self.embed_url = "https://scratch.mit.edu/projects/{}/embed/".format(
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
        return self.__dict__.copy()

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
            yield Studio(studio["id"], getinfo=False)

    def save_json(self, filename_or_obj):
        """Save a project's JSON to a file."""
        if isinstance(filename_or_obj, str):
            filename_or_obj = open(filename_or_obj, 'wb')
        with filename_or_obj:
            _streaming_request(filename_or_obj,
                               '{}',
                               self.projectid)

    def comments(self, limit=10, offset=0):
        """ Get comments. Note that replies are not included here. """
        req = _request('projects/{0}/comments?limit={1}&offset={2}',
                       self.projectid, limit, offset)
        for comment in req:
            yield Comment(
                comment_id=comment["id"],
                sender=comment["author"]["username"],
                path="projects/{0}/comments/".format(self.projectid),
                content=comment["content"],
                parent=None,
                created=comment["datetime_created"],
                last_modified=comment["datetime_modified"],
                visibility=comment["visibility"],
                reply_count=comment["reply_count"]
            )

    def comment(self, comment_id):
        """ Get a specific comment of a project, by using ID.
        limit and offset are not available - because it always returns one. """
        comment = _request('projects/{0}/comments/{1}'.format(self.projectid, comment_id))[0]
        return Comment(
            comment_id=comment_id,
            sender=comment["author"]["username"],
            path="projects/{0}/comments/".format(self.projectid),
            content=comment["content"],
            parent=self.comment(comment["parent_id"]) if comment["parent_id"] else None,
            created=comment["datetime_created"],
            last_modified=comment["datetime_modified"],
            visibility=comment["visibility"],
            reply_count=comment["reply_count"]
        )

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
        self.scratchteam = req["scratchteam"]

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
            yield Studio(studio["id"], getinfo=False)

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

class Comment(object):
    """ A comment. """
    def __init__(self, comment_id, sender, path=None, content=None, parent=None,
                 created=None, last_modified=None, reply_count=0, visibility="visible"):
        """ Initialize a comment. """
        self.comment_id = comment_id
        self.sender = User(sender, getinfo=True)
        self.author = self.sender
        self._path = path
        self.content = content
        self.parent = parent
        self.reply_count = reply_count
        self.created = created
        self.last_modified = last_modified
        self.visibility = visibility

    def __str__(self):
        """ Represent a comment """
        return "<Comment {0}>".format(self.comment_id)

    __repr__ = __str__

    @property
    def is_modified(self):
        """ Check if a comment has been modified. """
        return self.created != self.last_modified

    @property
    def has_reply(self):
        """ Check if a comment has replies. """
        return self.reply_count > 0

    def replies(self, limit=3, offset=0): # pylint: disable=inconsistent-return-statements
        """ Get replies. """
        if not self.has_reply:
            return []
        replies = _request("{0}{1}/replies?limit={2}&offset={3}",
                           self._path,
                           self.comment_id,
                           limit,
                           offset)
        for reply in replies:
            yield Comment(
                comment_id=reply["id"],
                sender=reply["author"]["username"],
                path=self._path,
                content=reply["content"],
                parent=self,
                created=reply["datetime_created"],
                last_modified=reply["datetime_modified"],
                reply_count=0,
                visibility=reply["visibility"]
            )

class Studio(object):
    """Represents a studio. """
    studioid = None
    def __init__(self, studioid, getinfo=True):
        """Initialize studio class."""
        self.studioid = int(studioid)
        if getinfo:
            self.info()

    def __str__(self):
        """Represent a studio."""
        return "<Studio {0}>".format(self.studioid)

    __repr__ = __str__

    def info(self):
        """Get an information about a studio. It sets its dict
        and returns it.
        """
        req = _request("https://api.scratch.mit.edu/studios/{0}",
                       self.studioid)
        self.title = req["title"]
        self.image = req["image"]
        self.description = req["description"]
        self.owner_id = req["owner"]
        self.visibility = req["visibility"]
        self.created = req["history"]["created"]
        self.modified = req["history"]["modified"]
        self.followers = req["stats"]["followers"]
        # Just for convenience
        self.author_id = self.owner_id
        return self.__dict__.copy()

    @property
    def owner(self):
        """Warns the user that this returns User ID."""
        warnings.warn("Warning: this property returns the owner's ID due "
                      "to a bug with API. Don't pass this value to User(), "
                      "because it cannot handle IDs-to-usernames. To dismiss "
                      "this warning, use Studio.owner_id.", UserWarning)
        return self.owner_id

    def projects(self, limit=5, offset=0):
        """Gets list of projects in a studio."""
        req = _request("https://api.scratch.mit.edu/studios/{0}/projects?limit={1}&offset={2}",
                       self.studioid, limit, offset)
        for project in req:
            yield Project(project["id"], getinfo=False)
