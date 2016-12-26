"""
Module just to print out current version.
That's all.
"""

VERSION = (1, 1, 0)


def get_version():
    """
    Returns version
    """
    return ".".join(map(str, VERSION))
