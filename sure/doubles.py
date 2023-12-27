"""Sure's own Test-Doubles"""
from collections import OrderedDict


class FakeOrderedDict(OrderedDict):
    """ OrderedDict that has the repr of a normal dict

    We must return a string whether in py2 or py3.
    """
    def __str__(self):
        if len(self) == 0:
            return '{}'
        key_values = []
        for key, value in self.items():
            key, value = repr(key), repr(value)
            key_values.append("{0}: {1}".format(key, value))

        res = "{{{0}}}".format(", ".join(key_values))
        return res

    def __repr__(self):
        return self.__str__()
