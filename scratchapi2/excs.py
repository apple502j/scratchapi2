""" Scratch API Error """

class ScratchAPIError(Exception):
    """ Scratch API Error (Generic) """
    pass

class RemovedFeatureError(NotImplementedError):
    """This feature has been removed."""
    pass
