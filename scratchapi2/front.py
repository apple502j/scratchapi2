"""
Front Page APIs.
Contains:
class FrontPage
- news()
- featured_projects()
- new_projects()
- most_remixed()
- most_loved()
- featured_studios()
- sds()
- curator()
"""
from warnings import warn
import requests
from .user import Project, User
from .gclass import GenericData

class FrontPage(object):
    """ A class to handle front page """
    def __init__(self):
        """ See FrontPage module """
        pass

    def __repr__(self):
        """ Always return <ScratchAPI2 FrontPage> """
        return "<ScratchAPI2 FrontPage>"

    __str__ = __repr__

    @staticmethod
    def news(limit=3, offset=0):
        """ Get Scratch News """
        result = requests.get("https://api.scratch.mit.edu/news?limit={0}&offset={1}".format(limit, offset)).json()
        return_values = []
        for item in result:
            return_values.append(GenericData(
                repr_value="<GenericData::News {0}>".format(item["id"]),
                newsid=item["id"],
                timestamp=item["stamp"],
                title=item["headline"],
                url=item["url"],
                image=item["image"],
                description=item["copy"]
                )
                                )
        return return_values

    @staticmethod
    def featured_projects():
        """ Get Featured Projects """
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["community_featured_projects"]
        projects = []
        for item in result:
            projects.append(Project(item["id"], getinfo=False))
        return projects

    @staticmethod
    def new_projects():
        """ Get New Projects """
        warn("The recent projects row was removed. This API won't continue supporting in the future.", PendingDeprecationWarning)
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["community_newest_projects"]
        projects = []
        for item in result:
            projects.append(Project(item["id"], getinfo=False))
        return projects

    @staticmethod
    def most_remixed():
        """ Get Most Remixed Projects """
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["community_most_remixed_projects"]
        projects = []
        for item in result:
            projects.append(Project(item["id"], getinfo=False))
        return projects

    @staticmethod
    def most_loved():
        """ Get Most Loved Projects """
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["community_most_loved_projects"]
        projects = []
        for item in result:
            projects.append(Project(item["id"], getinfo=False))
        return projects

    @staticmethod
    def curator():
        """ Get Curator's Selected Projects """
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["curator_top_projects"]
        projects = []
        for item in result:
            projects.append(GenericData(project=Project(item["id"], getinfo=False), curator=User(item["curator_name"], getinfo=False)))
        return projects

    @staticmethod
    def sds():
        """ Get SDS Projects """
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["scratch_design_studio"]
        projects = []
        for item in result:
            projects.append(GenericData(project=Project(item["id"], getinfo=False), studio=GenericData(studio_id=item["gallery_id"], title=item["gallery_title"])))
        return projects

    @staticmethod
    def featured_studios():
        """ Get Featured Studios """
        result = requests.get("https://api.scratch.mit.edu/proxy/featured").json()["community_featured_studios"]
        studios = []
        for item in result:
            studios.append(GenericData(studio_id=item["id"], title=item["title"], image=item["thumbnail_url"]))
        return studios
