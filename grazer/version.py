"""
Module just to print out current version.
That's all.
"""

VERSION = (1, 0, 7)


def get_version():
    """
    Returns version
    """
    return ".".join(map(str, VERSION))
