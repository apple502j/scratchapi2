"""
Scratch API library scratchapi2
Under GPL version 3 or any later version.
See LICENSE

Scratch is a project of the Lifelong Kindergarten Group at the MIT Media Lab

Requires the requests library.

This is made from these classes:
* Misc - Generic things, Statistics, Search, Health
* Project - Information about projects
* User - Information about Scratch user, Followers, Messages, Favorites
* FrontPage - Information about the front page
* Translate - Translator
* ScratchAPIError - Error
* GenericData - help yourself.
* StatisticsType - Use along with Misc.statistics()
* Studio - Information about a studio
* Classroom - Information about a classroom
* Maintenance - an exception which is raised when Scratch is in Maintenance Mode.
"""

from .user import User, Project, Classroom, Studio
from .translate import Translate
from .front import FrontPage
from .misc import Misc, StatisticsType
from .excs import ScratchAPIError, Maintenance
from .gclass import GenericData

__version__ = '1.5'

__all__ = [
    'Translate',
    'Project',
    'User',
    'Classroom',
    'Studio',
    'FrontPage',
    'Misc',
    'ScratchAPIError',
    'GenericData',
    'StatisticsType',
    'Maintenance'
]
