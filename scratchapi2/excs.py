""" Scratch API Error """

class ScratchAPIError(Exception):
    """ Scratch API Error (Generic) """
    pass

class RemovedFeatureError(NotImplementedError):
    """ Error for removed features. """
    def __init__(self):
        super().__init__()
        print("This feature has been removed.")
