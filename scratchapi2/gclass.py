"""Contains the GenericData class."""

class GenericData(object):
    """Base class for other data objects created on the fly."""

    _repr_str = None

    def __init__(self, **kwargs):
        """Initialize object by updating __dict__ with kwargs."""
        self.__dict__.update(kwargs)

    def __repr__(self):
        if self._repr_str:
            return self._repr_str.format(**self.__dict__)
        return '<GenericData>'

    __str__ = __repr__
