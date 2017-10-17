import re

from .data import (FormattedName,
                   Name,
                   Birthday,
                   Email,
                   Phone,
                   Address,
                   Organization,
                   Role,
                   Note,
                   Url,
                   Uid)
from .vcard import vCard
from .errors import K_TEL_TIP


class Builder:
    card = None

    def __init__(self):
        self.card = vCard()

    def FN(self, val):
        if val:
            self.card.fn = FormattedName('FN:%s' % val)

    def N(self, val):
        if val:
            self.card.n = Name('N:%s' % ';'.join(val))

    def TEL(self, val, types):
        if val:
            data = 'TEL;TYPE=%s:%s' % (types, val)
            try:
                self.card.phone.add(Phone(data))
            except ValueError:
                self.card.note.add(Note(K_TEL_TIP % data.rstrip()))

    def EMAIL(self, val, types):
        if val:
            types = types.replace('*', '') if types else types
            types = ';TYPE=' + types.lower() if types else ''
            self.card.email.add(Email('EMAIL%s:%s' % (types, val)))

    def ADR(self, val, types):
        test = list(filter((lambda x: x), val))
        if 1 < len(test):
            fixedVal = [re.sub(r'\r*\n+', ' ', x) for x in val]
            # fixedVal = [x.replace('\r\n',' ') for x in val]
            types = ';TYPE=' + types.lower() if types else ''
            self.card.adr.add(Address('ADR%s:%s' % (types,
                                                    ';'.join(fixedVal))))

    def NOTE(self, val):
        if val:
            self.card.note = Note('NOTE:%s' % val)

    def BDAY(self, val):
        if val and '0/0/00' != val:
            self.card.birthday = Birthday('BDAY:%s' % val)

    def ORG(self, val):
        if val:
            self.card.org = Organization('ORG:%s' % val)

    def ROLE(self, val):
        if val:
            self.card.role = Role('ROLE:%s' % val)

    def UID(self, val):
        if val:
            self.card.uid = Uid('UID:%s' % val)

    def URL(self, val):
        if val:
            self.card.url.add(Url('URL:%s' % val))


class Builder2(Builder):
    def N(self,
          family='',
          given='',
          additional='',
          prefix='',
          suffix=''):
        val = (family, given, additional, prefix, suffix)
        if val:
            self.card.n = Name('N:%s' % ';'.join(val))
