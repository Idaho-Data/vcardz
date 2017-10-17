"""vcardz parse module."""
import re

from .data import (REX_END,
                   REX_BEGIN,
                   Address,
                   Birthday,
                   Email,
                   FormattedName,
                   Name,
                   Nickname,
                   Note,
                   Organization,
                   Phone,
                   Role,
                   Title,
                   Url,
                   Uid)
from .tag import Tag
from .vcard import vCard


class Parser:

    """Class for parsing vCard data.

    lorem ipsum
    """

    _inCard = False

    def __init__(self, stream):
        """constructor

        lorem ipsum
        """
        self._stream = stream

    def ADR(self, data):
        self._card.adr.add(Address(data))

    def BDAY(self, data):
        self._card.birthday = Birthday(data)

    def FN(self, data):
        self._card.fn = FormattedName(data)

    def EMAIL(self, data):
        self._card.email.add(Email(data))

    def LABEL(self, data):
        self._card.label.add(Label(data))

    def MAILER(self, data):
        self._card.mailer = Mailer(data)

    def N(self, data):
        self._card.n = Name(data)

    def NICKNAME(self, data):
        self._card.nickname = Nickname(data)

    def NOTE(self, data):
        self._card.note.add(Note(data))

    def ORG(self, data):
        self._card.org = Organization(data)

    def PRODID(self, data):
        self._card.prodid = ProdID(data)

    def REV(self, data):
        self._card.rev = Rev(data)

    def ROLE(self, data):
        self._card.role = Role(data)

    def TEL(self, data):
        try:
            self._card.phone.add(Phone(data))
        except ValueError:
            self._card.note.add(Note(K_TEL_TIP % data.rstrip()))

    def TITLE(self, data):
        self._card.title = Title(data)

    def UID(self, data):
        self._card.uid = Uid(data)

    def URL(self, data):
        self._card.url.add(Url(data))

    def parse(self, data):
        tags = {"ADR": self.ADR,
                "EMAIL": self.EMAIL,
                "FN": self.FN,
                "LABEL": self.LABEL,
                "MAILER": self.MAILER,
                "N": self.N,
                "NICKNAME": self.NICKNAME,
                "NOTE": self.NOTE,
                "PRODID": self.PRODID,
                "ORG": self.ORG,
                "REV": self.REV,
                "ROLE": self.ROLE,
                "TEL": self.TEL,
                "TITLE": self.TITLE,
                "UID": self.UID,
                "URL": self.URL}
        self._card = vCard()

        fixed = []
        for line in data:
            if 1 == len(line.split(':')):
                prev = fixed.pop()
                prev += line[1:].rstrip()
                fixed.append(prev)
            else:
                fixed.append(line.strip())

        for line in fixed:
            tag = Tag(line)
            try:
                tags[tag.prop](line)
            except KeyError:
                pass

        return self._card

    def __iter__(self):
        return self

    def __next__(self):
        self._inCard = False
        data = []
        try:
            while True:
                line = next(self._stream).rstrip()
                if None != re.match(REX_END, line):
                    self._inCard = False
                    return self.parse(data)
                elif None != re.match(REX_BEGIN, line):
                    self._inCard = True
                    data = [line]
                elif self._inCard:
                    data.append(line)
        except StopIteration:
            raise
