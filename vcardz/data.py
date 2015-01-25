#
# Kontexa vCard data structure and processing
#

from email.utils import parseaddr
import re
from six.moves.urllib.parse import urlparse

from .atom import Atom
from .bag import Bag
from .utils import new_id

REX_BEGIN = "^BEGIN:VCARD"
REX_END = "END:VCARD$"
REX_PHONE_NUMBERS = "\+?1? *\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})(?:[,x ]*)([0-9]*)"  # noqa
REX_EMAIL = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"  # noqa


class FormattedName(Atom):
    pass


class Name(Bag):
    pass


class Nickname(Atom):
    pass


class Photo(Atom):
    pass


class Birthday(Atom):
    pass


class Email(Atom):
    user = ""
    domain = ""

    def __init__(self, data):
        Atom.__init__(self, data)
        try:
            self.value = self.value.lower()
            # temp = re.match(Parser.REX_EMAIL, self.value)
            # if not temp:
            #   self.tag = None
            #   self.value = None
            #   return

            self.value = parseaddr(self.value)[1].lower()
            frags = self.value.split('@')
            self.user = frags[0]
            self.domain = frags[1]
        except IndexError:
            pass


class Phone(Atom):
    def __init__(self, data):
        temp = re.sub('[^0-9]', '', data)
        if not temp:
            raise ValueError
        Atom.__init__(self, data)
        match = re.match(REX_PHONE_NUMBERS, self.value)
        if None != match:
            phone = match.group(1) + "-" + \
                match.group(2) + "-" + \
                match.group(3)

            if "" != match.group(4):
                phone += " x" + match.group(4)
            self.value = phone


class Address(Bag):
    pass


class Label(Bag):
    pass


class Organization(Atom):
    pass


class Role(Atom):
    def __init__(self, data):
        Atom.__init__(self, data)
        if "- - -" == self.value:
            self.tag = None
            self.value = None


class Title(Atom):
    pass


class Categories(Bag):
    pass


class Note(Atom):
    pass


class ProdID(Atom):
    pass


class Rev(Atom):
    pass


class SortString(Atom):
    pass


class Url(Atom):
    def __init__(self, data):
        Atom.__init__(self, data)
        o = urlparse(self.value)
        if '' == o.scheme:
            self.value = 'http://' + self.value
        self.value = self.value.replace('http\://', '')


class Mailer(Atom):
    pass

class Uid(Atom):
    @staticmethod
    def create():
        return Uid("UID:kontexa;%s" % new_id())
