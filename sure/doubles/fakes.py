from collections import OrderedDict


class FakeOrderedDict(OrderedDict):
    """Subclass of :py:class:`collections.OrderedDict` which presents has the repr of a regular :py:class:`dict`
    """
    def __str__(self):
        if len(self) == 0:
            return '{}'

        key_values = []
        for key, value in self.items():
            key, value = repr(key), repr(value)
            key_values.append("{0}: {1}".format(key, value))

        res = "{{{}}}".format(", ".join(key_values))
        return res

    def __repr__(self):
        return self.__str__()
