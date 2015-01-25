import re

from .tag import Tag

"""
vCard field with a single string value
"""


class Atom:
    Tag = None
    value = None

    def __init__(self, data):
        try:
            t = ':'.join(re.split(r'(?<!\\):', data)[1:])
            self.value = t.replace(r'\,', ',')\
                          .replace(r'\;', ';')\
                          .replace(r'\:', ':')
            self.Tag = Tag(data)
        except IndexError:
            self.value = None

    def escape(self):
        return self.value\
                   .replace(',', r'\,')\
                   .replace(';', r'\;')\
                   .replace(':', r'\:')

    def __str__(self):
        if None == self.value:
            return ""
        else:
            return self.value

    def __repr__(self):
        if self.value and self.Tag:
            return "%s:%s" % (repr(self.Tag), self.escape())
        elif self.Tag:
            return repr(self.Tag) + ":"
        else:
            return ""
