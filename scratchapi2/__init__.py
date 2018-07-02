"""
Scratch API library scratchapi2
Under GPL version 3 or any later version.
See LICENSE

Scratch is a project of the Lifelong Kindergarten Group at the MIT Media Lab

Requires the requests library.

This is made from these classes:
* Meta - Generic things, Statistics, Search, Health
* Project - Information about project
* User - Information about Scratch user, Followers, Messages, Favorites
* FrontPage - Information about the front page
* Misc - Translator
* ScratchAPIError - Error
* RemovedFeatureError - Error for removed features
* GenericData - help yourself.
"""

from .user import User, Project
from .meta import Meta
from .front import FrontPage
from .misc import Misc
from .excs import ScratchAPIError, RemovedFeatureError
from .gclass import GenericData

__version__ = '0.1'

__all__ = [
    'Meta',
    'Project',
    'User',
    'FrontPage',
    'Misc',
    'ScratchAPIError',
    'RemovedFeatureError',
    'GenericData',
]
