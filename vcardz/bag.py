from .tag import Tag


class Bag:
    """Bag class.

    Holds tokenized values such as ADDR.
    """
    tag = None
    value = None
    _tokens = None

    def __init__(self, data):
        try:
            self.tag = Tag(data)
            tokens = [x.lower() for x in data.split(':')[1].split(';')]
            self._tokens = set(filter((lambda x: x if '' != x else None),
                                      tokens))
            self.value = data.split(':')[1].split(';')
        except IndexError:
            return

    @property
    def tokens(self):
        if None == self._tokens:
            return set()
        else:
            return self._tokens

    @tokens.setter
    def tokens(self, val):
        self._tokens = val

    def __len__(self):
        count = 0
        if not self.value:
            return 0

        for temp in self.value:
            if temp:
                count = count + 1
        return count

    def __str__(self):
        if None == self.value:
            return ""
        else:
            return ';'.join(self.value)

    def __repr__(self):
        if self.value and self.tag:
            return "%s:%s" % (repr(self.tag),
                              ';'.join(self.value))
        elif self.tag:
            return repr(self.tag) + ":"
        else:
            return ""
