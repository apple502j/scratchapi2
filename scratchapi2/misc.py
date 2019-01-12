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
from datetime import datetime
import requests
from .gclass import GenericData
from .user import Project, Studio, _streaming_request
from .api import APISingleton
from .excs import ScratchAPIError

class StatisticsType:
    """See Misc.statistics() for detail"""
    comment = "comment"
    activity = "activity"
    active_user = "active_user"
    project = "project"
    country = "country"
    age = "age"

    profile = "profile"
    studio = "studio"

    user = "user"

    new = "new"
    remix = "remix"

    types = (
        comment,
        activity,
        active_user,
        project,
        country,
        age
        )

class Misc(APISingleton):
    """Misc - Generic things."""

    def info(self):
        """Get meta information."""
        return GenericData(**self._request(""))

    def health(self):
        """Get health information."""
        health_info = self._request("health")
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
            )
        )

    def project_count(self):
        """Count all shared projects."""
        return self._request('projects/count/all')['count']

    def statistics(self, statistics_type=None, **kwargs): # pylint: disable=inconsistent-return-statements
        """
            Get statistics. This function is complex.
            For those who just wants to get studio/user/comment counts,
            call without any arguments.

            For those who needs monthly data, specify statistics_type,
            by using StatisticsType's properties, like:
            statistics(StatisticsType.age)

            Use the arguments if needed: (strings inside <> are properties of StatisticsType)
            * place (for <comment>: can be chosen from <project>, <studio>, <profile>)
            * kind (for <activity>: can be chosen from <project>, <user>, <comment>
                    for <active_user>: can be chosen from <project>, <comment>
                    for <project>: can be chosen from <new>, <remix>)

            NOTE: values returned from this function is **NOT** a generator.
        """
        # pylint: disable=line-too-long, no-else-return
        if not statistics_type:
            results = self._request('statistics/data/daily/',
                                    api_url='https://scratch.mit.edu/'
                                    )
            return GenericData(projects=results["PROJECT_COUNT"],
                               studios=results["STUDIO_COUNT"],
                               users=results["USER_COUNT"],
                               comments=results["COMMENT_COUNT"],
                               timestamp=datetime.utcfromtimestamp(float(results["_TS"])),
                               _repr_str="DailyStatistics"
                              )
        if statistics_type in StatisticsType.types:
            results = self._request('statistics/data/monthly/',
                                    api_url='https://scratch.mit.edu/'
                                    )
            if statistics_type == StatisticsType.comment:
                comment_keys = (StatisticsType.project,
                                StatisticsType.studio,
                                StatisticsType.profile
                               )
                if kwargs.get("place", None) in comment_keys:
                    smaller_res = results["comment_data"][comment_keys.index(kwargs["place"])]["values"]
                    return_values = []
                    for smallest_res in smaller_res:
                        timestamp = datetime.utcfromtimestamp(smallest_res["x"]/1000)
                        return_values.append(GenericData(timestamp=timestamp,
                                                         value=smallest_res["y"],
                                                         _repr_str="Comments as of  {0}".format(timestamp.isoformat())
                                                        ))
                    return return_values
                else:
                    raise ScratchAPIError("Unknown place: {0}".format(kwargs.get("place", "(not given)")))
            elif statistics_type == StatisticsType.activity:
                activity_keys = (StatisticsType.project,
                                 StatisticsType.user,
                                 StatisticsType.comment
                                )
                if kwargs.get("kind", None) in activity_keys:
                    smaller_res = results["activity_data"][activity_keys.index(kwargs["kind"])]["values"]
                    return_values = []
                    for smallest_res in smaller_res:
                        timestamp = datetime.utcfromtimestamp(smallest_res["x"]/1000)
                        return_values.append(GenericData(timestamp=timestamp,
                                                         value=smallest_res["y"],
                                                         _repr_str="Activity as of  {0}".format(timestamp.isoformat())
                                                        ))
                    return return_values
                else:
                    raise ScratchAPIError("Unknown kind: {0}".format(kwargs.get("kind", "(not given)")))
            elif statistics_type == StatisticsType.active_user:
                activity_keys = (StatisticsType.project,
                                 StatisticsType.comment
                                )
                if kwargs.get("kind", None) in activity_keys:
                    smaller_res = results["active_user_data"][activity_keys.index(kwargs["kind"])]["values"]
                    return_values = []
                    for smallest_res in smaller_res:
                        timestamp = datetime.utcfromtimestamp(smallest_res["x"]/1000)
                        return_values.append(GenericData(timestamp=timestamp,
                                                         value=smallest_res["y"],
                                                         _repr_str="Active Users as of  {0}".format(timestamp.isoformat())
                                                        ))
                    return return_values
                else:
                    raise ScratchAPIError("Unknown kind: {0}".format(kwargs.get("kind", "(not given)")))
            elif statistics_type == StatisticsType.project:
                project_keys = (StatisticsType.new,
                                StatisticsType.remix
                               )
                if kwargs.get("kind", None) in project_keys:
                    smaller_res = results["project_data"][project_keys.index(kwargs["kind"])]["values"]
                    return_values = []
                    for smallest_res in smaller_res:
                        timestamp = datetime.utcfromtimestamp(smallest_res["x"]/1000)
                        return_values.append(GenericData(timestamp=timestamp,
                                                         value=smallest_res["y"],
                                                         _repr_str="Projects as of  {0}".format(timestamp.isoformat())
                                                        ))
                    return return_values
                else:
                    raise ScratchAPIError("Unknown kind: {0}".format(kwargs.get("kind", "(not given)")))
            elif statistics_type == StatisticsType.country:
                return results["country_distribution"]
            elif statistics_type == StatisticsType.age:
                smaller_res = results["age_distribution_data"][0]["values"]
                return_values = []
                for smallest_res in smaller_res:
                    return_values.append(GenericData(age=smallest_res["x"],
                                                     value=smallest_res["y"],
                                                     _repr_str="{0} Years Old Users".format(smallest_res["x"])
                                                    ))
                return return_values
        else:
            raise ScratchAPIError("Unknown statistics type: {0}".format(statistics_type))
    # pylint: enable=line-too-long, no-else-return

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
        for result in results:
            yield Studio(result["id"], getinfo=False)

    def username_available(self, name):
        """Check if a username is available."""
        result = self._request('accounts/check_username/{}',
                               name,
                               api_url='https://scratch.mit.edu/')
        return result[0]["msg"]

    def valid_email(self, email):
        """Check if an email address is valid."""
        result = self._request('accounts/check_email/{}',
                               email,
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
