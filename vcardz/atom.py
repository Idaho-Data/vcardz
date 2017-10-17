import re

from .tag import Tag

"""
vCard field with a single string value
"""


class Atom:
    tag = None
    value = None

    def __init__(self, data):
        try:
            t = ':'.join(re.split(r'(?<!\\):', data)[1:])
            self.value = t.replace(r'\,', ',')\
                          .replace(r'\;', ';')\
                          .replace(r'\:', ':')
            self.tag = Tag(data)
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
        if self.value and self.tag:
            return "%s:%s" % (repr(self.tag), self.escape())
        elif self.tag:
            return repr(self.tag) + ":"
        else:
            return ""
