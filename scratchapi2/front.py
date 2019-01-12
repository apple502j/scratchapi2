"""
Front Page APIs.
Contains:
class FrontPage (ALWAYS use like FrontPage())
- news()
- featured_projects()
- new_projects()
- most_remixed()
- most_loved()
- featured_studios()
- sds()
- curator()
"""
from .user import Project, User, Studio
from .gclass import GenericData
from .api import APISingleton

GETINFO = False

class FrontPage(APISingleton):
    """The Front Page of the Scratch website."""

    def news(self, limit=3, offset=0):
        """Get Scratch news."""
        result = self._request('news?limit={0}&offset={1}', limit, offset)
        class News(GenericData):
            """Represents a news item."""
            _repr_str = '<News {newsid}>'
            newsid = None
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

    def new_projects(self): # pylint: disable=no-self-use
        """Removed. Get new Projects."""
        # pylint: enable=no-self-use
        raise Exception("This function has been removed and is no longer available.")

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
                curator=User(item["curator_name"], getinfo=GETINFO),
                _repr_str='<Curated Project>'
            )

    def sds_projects(self):
        """Get SDS Projects."""
        result = self._request('proxy/featured')["scratch_design_studio"]
        for item in result:
            yield GenericData(
                project=Project(item["id"], getinfo=GETINFO),
                studio=Studio(item["gallery_id"], getinfo=GETINFO),
                _repr_str='<SDS Project>'
            )

    def featured_studios(self):
        """Get featured Studios."""
        result = self._request('proxy/featured')["community_featured_studios"]
        for item in result:
            yield Studio(item["id"], getinfo=GETINFO)
