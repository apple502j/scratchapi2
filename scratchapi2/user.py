#pylint: disable=trailing-whitespace
"""
Scratch API User

Anything returned from API does not contain any attributes.
Use info() to set/get it.

"""
#pylint: enable=trailing-whitespace

import requests
from .excs import ScratchAPIError
from .gclass import GenericData

class Project(object):
    """ For Scratch Project """
    def __init__(self, projectid, getinfo=True):
        """ Set up Project. """
        self.projectid = str(projectid)
        if getinfo:
            self.info()

    def __repr__(self):
        """ Return string <Project (id)> """
        return "<Project {0}>".format(self.projectid)

    __str__ = __repr__

    def __eq__(self, other):
        """ Equal means that project IDs are equal """
        return self.projectid == other.projectid

    def info(self):
        """ Get information about a project. It sets its dict and returns it. """
        try:
            req = requests.get("https://api.scratch.mit.edu/projects/{0}".format(self.projectid)).json()
        except:
            raise ScratchAPIError
        if "code" in req.keys():
            raise ScratchAPIError
        self.title = req["title"]
        self.description = req["description"]
        self.instructions = req["instructions"]
        self.author = User(req["author"]["username"], getinfo=False)
        self.image = req["image"]
        self.created = req["history"]["created"]
        self.modified = req["history"]["modified"]
        self.shared = req["history"]["shared"]
        self.views = req["stats"]["views"]
        self.loves = req["stats"]["loves"]
        self.favorites = req["stats"]["favorites"]
        self.comments = req["stats"]["comments"]
        self.remix_number = req["stats"]["remixes"]
        self.parent = Project(req["remix"]["parent"], getinfo=False)
        self.root = Project(req["remix"]["root"], getinfo=False)

        # Just for convenience
        self.notes = self.description
        self.credits = self.description
        # links
        self.url = "https://scratch.mit.edu/projects/" + self.projectid
        self.url_remixes = self.url + "/remixes"
        self.url_remixtree = self.url + "/remixtree"
        self.url_studios = self.url + "/studios"
        self.url_inside = self.url + "#editor"
        self.url_fullscreen = self.url + "#fullscreen"
        self.url_embed = "https://scratch.mit.edu/projects/embed/" + self.projectid
        self.embed_tag = '<iframe allowtransparency="true" width="485" height="402" src="{0}?autostart=false" frameborder="0" allowfullscreen></iframe>'.format(self.url_embed)
        self.url_scratch3 = "https://preview.scratch.mit.edu/#" + self.projectid
        return self.__dict__

    def remixes(self, limit=3, offset=0):
        """ List all remixes, limit and offset available. """
        try:
            req = requests.get("https://api.scratch.mit.edu/projects/{0}/remixes?limit={1}&offset={2}".format(self.projectid, limit, offset)).json()
        except:
            raise ScratchAPIError
        projects = []
        for remix in req:
            projects.append(Project(remix.id, getinfo=False))
        return projects

    def studios(self, limit=3, offset=0):
        """ List all studios it belongs to. limit and offset available. """
        try:
            req = requests.get("https://api.scratch.mit.edu/projects/{0}/studios?limit={1}&offset={2}".format(self.projectid, limit, offset)).json()
        except:
            raise ScratchAPIError
        list_studios = []
        for studio in req:
            list_studios.append(GenericData(
                owner=studio["owner"],
                studio_id=studio["id"],
                title=studio["title"],
                description=studio["description"],
                image=studio["image"],
                created_at=studio["history"]["created"],
                last_modified=studio["history"]["modified"],
                followers=studio["stats"]["followers"]
                ))
        return list_studios

class User(object):
    """ Scratch User Class """
    def __init__(self, username, getinfo=True):
        """ Set up user. requires one argument (username) at least """
        self.username = username
        if getinfo:
            self.info()

    def __str__(self):
        """ Return string <User (username)> """
        return "<User {0}>".format(self.username)

    __repr__ = __str__

    def __eq__(self, other):
        """ Equal means that usernames are equal """
        return self.username == other.username

    def info(self):
        """ Get an information about an user. It sets its dict and returns it. """
        try:
            req = requests.get("https://api.scratch.mit.edu/users/{0}".format(self.username)).json()
        except:
            raise ScratchAPIError
        if "code" in req.keys():
            raise ScratchAPIError
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
        return self.__dict__

    def following(self, limit=100, offset=0):
        """ Return whom the user follows. limit and offset available. """
        try:
            req = requests.get("https://api.scratch.mit.edu/users/{0}/following?limit={1}&offset={2}".format(self.username, limit, offset)).json()
        except:
            raise ScratchAPIError
        following_users = []
        for user in req:
            following_users.append(User(user["username"], getinfo=False))
        return following_users

    def followers(self, limit=100, offset=0):
        """ Return whom the user is followed by. limit and offset available. """
        try:
            req = requests.get("https://api.scratch.mit.edu/users/{0}/followers?limit={1}&offset={2}".format(self.username, limit, offset)).json()
        except:
            raise ScratchAPIError
        followers = []
        for user in req:
            followers.append(User(user["username"], getinfo=False))
        return followers

    def unread_messages(self):
        """ Return the number of unread messages """
        try:
            req = requests.get("https://api.scratch.mit.edu/users/{0}/messages/count".format(self.username)).json()
        except:
            raise ScratchAPIError
        return req["count"]

    def projects(self, limit=10, offset=0):
        """ Return the user's projects. limit and offset available. """
        try:
            req = requests.get("https://api.scratch.mit.edu/users/{0}/projects?limit={1}&offset={2}".format(self.username, limit, offset)).json()
        except:
            raise ScratchAPIError
        projects = []
        for project in req:
            projects.append(Project(project["id"], getinfo=False))
        return projects

    def favorites(self, limit=10, offset=0):
        """ Return the user's favorite projects. limit and offset available. """
        try:
            req = requests.get("https://api.scratch.mit.edu/users/{0}/favorites?limit={1}&offset={2}".format(self.username, limit, offset)).json()
        except:
            raise ScratchAPIError
        projects = []
        for project in req:
            projects.append(Project(project["id"], getinfo=False))
        return projects

class Classroom(object):
    """ Scratch Classroom Class (not typo!) """
    def __init__(self, classid, getinfo=True):
        """ Set up user. requires one argument (class id) at least """
        self.classid = str(classid)
        if getinfo:
            self.info()

    def __str__(self):
        """ Return string <Class (classid)> """
        return "<Class {0}>".format(self.classid)

    __repr__ = __str__

    def __eq__(self, other):
        """ Equal means that class IDs are equal """
        return self.classid == other.classid

    def info(self):
        """ Get an information about a classroom. It sets its dict and returns it. """
        try:
            req = requests.get("https://api.scratch.mit.edu/classrooms/{0}".format(self.classid)).json()
        except:
            raise ScratchAPIError
        self.title = req["title"]
        self.start = req["date_start"]
        self.end = req["date_end"]
        self.images = req["images"]
        self.status = req["status"]
        self.description = req["description"]
        self.educator = User(req["educator"]["username"], getinfo=False)

        # Just for convenience
        self.about_class = self.status
        self.bio = self.description
        self.what_were_working_on = self.description
        self.what_working_on = self.description
        self.teacher = self.educator
        return self.__dict__
