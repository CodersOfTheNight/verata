import yaml


class Config(object):

    """
    Class which handles config related stuff
    """

    def __init__(self, f):
        with open(f, "r") as f:
            self._data = yaml.load(f)
