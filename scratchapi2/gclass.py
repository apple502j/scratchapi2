""" GClass is a functional class library. """

class GenericData(object):
    """ Very generic, very useful. Thanks to kenny2github! (dev) use repr_value to set repr. """
    def __init__(self, repr_value="<GenericData>", **kwargs):
        """ Very generic, very useful. Thanks to kenny2github! """
        self._repr_value = repr_value
        self.__dict__.update(kwargs)

    def __repr__(self):
        """ Just return """
        return self._repr_value
    __str__ = __repr__
