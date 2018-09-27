"""
Scratch API Misc

It contains some functions that are not categorized.
Contains:
* API Information
* Search
* Statistics
* Scratch Information

Anything put on Front Page is implemented in FrontPage.
"""

try:
    from urllib.parse import quote as urlencode
except ImportError:
    from urllib import quote as urlencode
import re
import requests
from .gclass import GenericData
from .user import Project, _streaming_request
from .api import APISingleton

class Misc(APISingleton):
    """Misc - Generic things."""

    def info(self):
        """Get meta information."""
        return GenericData(**self._request(""))

    def health(self):
        """Get health information."""
        health_info = self._request("")
        return GenericData(
            version=health_info['version'],
            uptime=health_info['uptime'],
            load=health_info['load'],
            sql=GenericData(
                ssl=health_info['sql']['ssl'],
                min=health_info['sql']['min'],
                max=health_info['sql']['max'],
            ),
            cache=GenericData(
                connected=health_info['cache']['connected'],
                ready=health_info['cache']['ready'],
            ),
        )

    def project_count(self):
        """Count all shared projects."""
        return self._request('projects/count/all')['count']

    def search_projects(self, key=None, limit=10):
        """Search Projects."""
        results = self._request('search/projects?limit={}{}',
                                limit,
                                ('&q={}'.format(urlencode(key))
                                 if key
                                 else ''))
        for result in results:
            yield Project(result["id"])

    def popular_projects(self, limit=10):
        """Return popular projects."""
        return self.search_projects(limit=limit)

    def search_studios(self, key, limit=10):
        """Search Studios."""
        results = self._request('search/studios?limit={}&q={}',
                                limit,
                                key)
        class Studio(GenericData):
            """Represents a studio."""
            _repr_str = '<Studio {studio_id}>'
            studio_id = None
        for result in results:
            yield Studio(
                owner=result["owner"],
                studio_id=result["id"],
                title=result["title"],
                description=result["description"],
                image=result["image"],
                created_at=result["history"]["created"],
                last_modified=result["history"]["modified"],
                followers=result["stats"]["followers"]
            )

    def username_available(self, name):
        """Check if a username is available."""
        result = self._request('accounts/check_username/{}',
                               name,
                               api_url='https://scratch.mit.edu/')
        return result[0]["msg"]

    @staticmethod
    def offline_ver():
        """Get the latest version of the Scratch 2 Offline Editor."""
        result_url = "https://scratch.mit.edu/scratchr2/static/sa/version.xml"
        raw_xml = requests.get(result_url).text
        match = re.search(r"<versionNumber>([0-9\.]{1,8})</versionNumber>",
                          raw_xml)
        val = match.group(1)
        return val

    @staticmethod
    def save_asset(asset_name, filename_or_obj):
        """Save asset to a file. asset_name must be with an extension."""
        if isinstance(filename_or_obj, str):
            filename_or_obj = open(filename_or_obj, 'wb')
        with filename_or_obj:
            _streaming_request(filename_or_obj,
                               'asset/{}/get/',
                               asset_name,
                               api_url="https://cdn.assets.scratch.mit.edu/internalapi/"
                              )
