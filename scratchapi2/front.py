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

GETINFO = False

class FrontPage(object):
    """The Front Page of the Scratch website."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Enforce this class as a singleton."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, api_url="https://api.scratch.mit.edu/"):
        """Initialize the object with the API URL."""
        self.api_url = api_url

    def __repr__(self):
        """Represent the FrontPage."""
        return "<FrontPage>"

    __str__ = __repr__

    def _request(self, path, *opts, api_url=None):
        """Internal method to request data from the API."""
        return requests.get(
            (api_url or self.api_url)
            + path.format(*opts)
        ).json()

    def news(self, limit=3, offset=0):
        """Get Scratch news."""
        result = self._request('news?limit={0}&offset={1}', limit, offset)
        News = type('News', (GenericData, object), {
            '_repr_str': '<News {newsid}>',
            'newsid': None,
        })
        for item in result:
            yield News(
                newsid=item["id"],
                timestamp=item["stamp"],
                title=item["headline"],
                url=item["url"],
                image=item["image"],
                description=item["copy"]
            )

    def featured_projects(self):
        """Get featured Projects."""
        result = self._request('proxy/featured')["community_featured_projects"]
        for item in result:
            yield Project(item["id"], getinfo=GETINFO)

    def new_projects(self):
        """Get new Projects."""
        warn("The recent projects row was removed. "
             "This API endpoint may disappear in the future.",
             PendingDeprecationWarning)
        result = self._request('proxy/featured')["community_newest_projects"]
        for item in result:
            yield Project(item["id"], getinfo=GETINFO)

    def most_remixed_projects(self):
        """Get most remixed Projects."""
        result = self._request('proxy/featured')["community_most_remixed_projects"]
        for item in result:
            yield Project(item["id"], getinfo=GETINFO)

    def most_loved_projects(self):
        """Get most loved Projects."""
        result = self._request('proxy/featured')["community_most_loved_projects"]
        for item in result:
            yield Project(item["id"], getinfo=GETINFO)

    def curated_projects(self):
        """Get the currently curated Projects and the current curator."""
        result = self._request('proxy/featured')["curator_top_projects"]
        for item in result:
            yield GenericData(
               project=Project(item["id"], getinfo=GETINFO),
               curator=User(item["curator_name"], getinfo=GETINFO)
            )

    def sds_projects(self):
        """Get SDS Projects."""
        result = self._request('proxy/featured')["scratch_design_studio"]
        Studio = type('Studio', (GenericData, object), {
            '_repr_str': '<Studio {studio_id}>',
            'studio_id': None,
        })
        for item in result:
            yield GenericData(
                project=Project(item["id"], getinfo=GETINFO),
                studio=Studio(
                    studio_id=item["gallery_id"],
                    title=item["gallery_title"]
                )
            )

    def featured_studios(self):
        """Get featured Studios."""
        result = self._request('proxy/featured')["community_featured_studios"]
        Studio = type('Studio', (GenericData, object), {
            '_repr_str': '<Studio {studio_id}>',
            'studio_id': None,
        })
        for item in result:
            yield Studio(
                studio_id=item["id"],
                title=item["title"],
                image=item["thumbnail_url"]
            )
