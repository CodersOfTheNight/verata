import yaml


class Config(object):

    """
    Class which handles config related stuff
    """

    def __init__(self, f):
        with open(f, "r") as f:
            self._data = yaml.load(f)

        print(self._data)

    def __repr__(self):
        return "{0}: {1}".format(self.name, self.desc)

    @property
    def name(self):
        return self._data["name"]

    @property
    def desc(self):
        return self._data["description"]
