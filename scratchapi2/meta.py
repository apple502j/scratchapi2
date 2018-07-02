#pylint: disable=trailing-whitespace
"""
Scratch API Meta

It contains some functions that are not categorized.
Contains:
* API Information
* Search
* Statistics
* Scratch Information

NOTE: This feature is implemented in Misc:
* Translate

Anything put on Front Page is implemented in FrontPage.
"""
#pylint: enable=trailing-whitespace

try:
    from urllib.parse import quote as urlencode
except ImportError:
    from urllib import quote as urlencode
import re
import requests
from .gclass import GenericData
from .user import Project

class Meta(object):
    """ Meta - Generic things """

    def __repr__(self):
        """ Always return <ScratchAPI2 Meta> """
        return "<ScratchAPI2 Meta>"

    __str__ = __repr__

    @staticmethod
    def apiinfo():
        """ Get information. """
        return GenericData(**requests.get("https://api.scratch.mit.edu/").json())

    @staticmethod
    def health():
        """ Get Health Information """
        health_info = requests.get("https://api.scratch.mit.edu/").json()
        return GenericData(**{
            'version' : health_info['version'],
            'uptime' : health_info['uptime'],
            'loads' : health_info['load'],
            'sql_ssl' : health_info['sql']['ssl'],
            'sql_min' : health_info['sql']['min'],
            'sql_max' : health_info['sql']['max'],
            'cache_connected' : health_info['cache']['connected'],
            'cache_ready' : health_info['cache']['ready']
            }
                          )
    @staticmethod
    def allprojects():
        """ Count all shared projects """
        project_num = requests.get("https://api.scratch.mit.edu/projects/count/all").json()
        return project_num["count"]

    @staticmethod
    def searchprojects(key=None, limit=10):
        """ Search Projects. """
        if key is None:
            result_url = "https://api.scratch.mit.edu/search/projects?limit={LIMIT}"
        else:
            result_url = "https://api.scratch.mit.edu/search/projects?q={KEY}&limit={LIMIT}"
        result_url = result_url.format(KEY=urlencode(key), LIMIT=limit)
        results = requests.get(result_url).json()
        projects = []
        for result in results:
            projects.append(Project(result["id"]))
        return projects

    def popularprojects(self, limit=10):
        """ Return popular projects """
        return self.searchprojects(key=None, limit=limit)

    @staticmethod
    def searchstudios(key=None, limit=10):
        """ Search Studios. """
        if key is None:
            raise ValueError("Missing key.")
        result_url = "https://api.scratch.mit.edu/search/studios?q={KEY}&limit={LIMIT}"
        result_url = result_url.format(KEY=urlencode(key), LIMIT=limit)
        results = requests.get(result_url).json()
        studios = []
        for result in results:
            studios.append(GenericData(
                owner=result["owner"],
                studio_id=result["id"],
                title=result["title"],
                description=result["description"],
                image=result["image"],
                created_at=result["history"]["created"],
                last_modified=result["history"]["modified"],
                followers=result["stats"]["followers"]
                )
                          )
        return studios

    @staticmethod
    def username_available(name=None):
        """ Check if a username is available """
        result_url = "https://scratch.mit.edu/accounts/check_username/" + name
        result = requests.get(result_url).json()
        return result[0]["msg"]

    @staticmethod
    def offline_ver():
        """ Get Version of Scratch 2 Offline Editor """
        result_url = "https://scratch.mit.edu/scratchr2/static/sa/version.xml"
        raw_xml = requests.get(result_url).text
        match = re.search(r"<versionNumber>[0-9\.]{1,8}</versionNumber>", raw_xml)
        val = re.sub(r"[^0-9\.]", "", raw_xml[match.start():match.end()])
        return val
