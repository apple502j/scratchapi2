"""Scratch API errors"""

class ScratchAPIError(Exception):
    """Generic Scratch API error."""

class Maintenance(ScratchAPIError):
    """Error when maintenance mode."""
