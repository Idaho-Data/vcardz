"""
:platform: Unix, Windows
:synopsis: Python class for entity data (i.e. people, organizations)
modeled on `RFC 6350 <https://tools.ietf.org/html/rfc6350>`

.. moduleauthor: Josh Watts <josh.watts@idahodata.io>
"""

from email.utils import parseaddr
import jellyfish
import json
import re
import sys
from six.moves.urllib.parse import urlparse  # noqa

from nameparser import HumanName
from .bag import Bag
from .data import (REX_EMAIL,
                   Address,
                   Email,
                   Label,
                   Name,
                   Phone,
                   Uid,
                   Url)
from .utils import xstr
from .log import get_logger

# FN / required => formatted name
# * semantics of X.520 Common Name attribute

# N / required => name
# * delimiter => semi-colon
# * family name; given name; additional names; honorific prefixes;
# honorific suffixes
# * X.520 individual name attribute

# NICKNAME => nickname
# * delimiter => comma

# PHOTO => profile picture
# * PHOTO;VALUE=uri:http://foo.com/johnqpublic.jpg
# * PHOTO;ENCODING=b;TYPE=JPEG:base64 encoded binary data

# BDAY => birthday
# * BDAY:1953-10-15T23:10:00Z

#
# delivery addressing
#

# ADR => delivery address
# * delimiter => semi-colon
# * box #; extended address; street address; city (locality);
#   region (state); postal code; country name
# * TYPEs
# - dom - domestic
# - intl - international
# - postal - postal
# - parcel - parcel delivery service
# - home - residence
# - work - work
# - pref - preferred
# - TYPE=dom;TYPE=postal or TYPE=dom,postal
# * X.520 geographical and postal attributes

# LABEL => formatted address
# * follows rules of ADR
# * multi-line - escape command and newline

# TEL => telephone #
# * X.500 telephone number attribute
# * TYPEs
# - home - residence
# - msg - voice mail
# - work - work
# - pref - preferred e.g. TYPE=home,pref
# - voice - voice telephone
# - fax - fax
# - cell - mobile
# - video - video conferencing
# - pager - pager
# - bbs - bbs dial-in
# - modem
# * default TYPE => voice

# EMAIL => email address
# * TYPEs
# - internet - internet type e.g. SMTP
# - x400 - X.400 adressing type
# - pref - preferred
# - default => internet

# MAILER => name of software
# * based on MIME type X-Mailer

#
# geographical types
#

# TZ => time zone
# * UTC offset

# GEO => lat & lon
# * delimiter => semi-colon
# * lat;lon
# * decimal = degrees + minutes/60 + seconds/3600

#
# organization
#

# TITLE => position title
# X.520 Title attribute

# ROLE => occupation
# X.520 Business Category

# LOGO => logo of organization
# * see PHOTO

# AGENT => person who acts on behalf of person e.g. secretary
# * AGENT;VALUE=uri:CID:jqpublic.lkjlkjsdfds.xyzMail@hots3.com
# * AGENT:BEGIN:VCARD ... END:VCARD

# ORG => orgnizational name & units
# * delimiter => semi-colon
# * X.520 Organization Name attribute
# * ORG:ABC\, Inc.;North American Division;Marketing

#
# explanatory
#

# CATEGORIES => categories
# * delimiter => comma

# NOTE => comment
# * X.520 Description attribute

# PRODID => identifier for product that created the vCard
# * use Formal Public Identifiers in ISO 9070
# * PRODID:-//ONLINE DIRECTORY//NONSGML Version 1//EN

# REV => revision information
# * single date-time value

# SORT-STRING => family name to be used for national-language-specific
# sorting of FN and N

# SOUND => audio clip for pronunciation
# * TYPE - IANA registered audo format
# * SOUND;TYPE=BASIC=VALUE=uri:....
# * SOUND;TYPE=BASIC;ENCODING=b:base-64 value

# UID => vCard's guid

# URL => uri

# VERSION / required => vCard specification
# * MUST be 3.0

#
# security
#

# CLASS => access control intent
# * e.g. PUBLIC or PRIVATE or CONFIDENTIAL or ...

# KEY => public key or authentication certificate
# * TYPE - key or authentication format


class vCard:

    """vCard data source based on blah blah blah."""

    def __init__(self):
        """constructor."""
        self.adr = set()
        self.birthday = None
        self.email = set()
        self.fn = None
        self.label = set()
        self.mailer = None
        self.n = Name("")
        self.nickname = None
        self.note = set()
        self.org = None
        self.prodid = None
        self.phone = set()
        self.rev = None
        self.role = None
        self.title = None
        self.sort_name = None
        self.uid = Uid.create()
        self.url = set()

    @staticmethod
    def fmatch(feature, val1, val2):
        """run the fswoosh algorithm."""
        def fn():
            if val1 and val2:
                score = jellyfish.jaro_winkler(val1.lower(), val2.lower())
                return True if .96 < score else False
            else:
                return False

        def n():
            tokens1 = val1.split(';')
            tokens2 = val2.split(';')
            cross = [jellyfish.jaro_winkler(str(x), str(y))
                     for x in tokens1
                     for y in tokens2]
            nTokens = list(filter((lambda x: 1 if x > .95 else 0), cross))
            return True if 1 < len(nTokens) else False

        matches = {'email': (lambda: val1 == val2),
                   'phone': (lambda: val1 == val2),
                   'fn': fn,
                   'n': n}
        return matches[feature]()

    def match(self, other):
        """match."""
        if not other:
            return False

        if self.fn and other.fn:
            name = jellyfish.jaro_winkler(str(self.fn).lower(),
                                       str(other.fn).lower())
            name = True if name > .95 else False
        else:
            name = False

        # score first name
        self_ntokens = list(self.n.tokens)
        other_ntokens = list(other.n.tokens)
        try:
            self_fname = self_ntokens[1]
            other_fname = other_ntokens[1]
            # remove fname from tokens
            self_ntokens.remove(self_fname)
            other_ntokens.remove(other_fname)
            fname_score = jellyfish.jaro_winkler(self_fname, other_fname)
        except IndexError:
            fname_score = 0
        # score the rest of the name tokens
        cross = [jellyfish.jaro_winkler(str(x), str(y))
                 for x in self_ntokens for y in other_ntokens]
        nTokens = list(filter((lambda x: 1 if x > .95 else 0), cross))
        # generate name score
        name_score = (fname_score > .95) and (0 < len(nTokens))

        # cross = [jellyfish.jaro_winkler(str(x), str(y))
        #          for x in self.email for y in other.email]
        cross = [1 if str(x) == str(y) else 0
                 for x in self.email for y in other.email]
        emailHits = list(filter((lambda x: 1 if x > .99 else 0), cross))

        cross = [jellyfish.jaro_winkler(x.user, y.user) for x in self.email
                 for y in other.email]
        emailUserHits = list(filter((lambda x: 1 if x > .95 else 0), cross))

        cross = [str(x) == str(y) and x.tag == y.tag for x in self.phone for y in other.phone]
        phoneHits = list(filter((lambda x: 1 if True == x else 0), cross))

        if name or \
           name_score or \
           0 < len(emailHits) or \
           (1 < len(nTokens) and 0 < len(emailUserHits)) or \
           0 < len(phoneHits):
            return True
        else:
            return False

    def merge(self, other):
        """merge."""
        max = (lambda x, y:  y if x and y and len(str(x)) < len(str(y)) else x)
        result = vCard()

        # if self.fn and other.fn:
        #   if len(str(other.fn)) and len(str(self.fn)):
        #     result.fn = other.fn
        #     result.n = other.n
        # else:
        #   result.fn = self.fn
        #   result.n = self.n
        m1 = re.match(REX_EMAIL, str(self.fn))
        m2 = re.match(REX_EMAIL, str(other.fn))
        if m1 or m2:
            result.fn = other.fn if m1 else self.fn
            result.n = other.n if m1 else self.n
        else:
            result.fn = max(self.fn, other.fn)
            result.n = other.n if result.fn == other.fn else self.n
            result.n.tokens = self.n.tokens | other.n.tokens

        result.email = self.email | other.email
        result.phone = self.phone | other.phone
        result.adr = self.adr | other.adr
        result.label = self.label | other.label
        result.url = self.url | other.url

        result.birthday = max(self.birthday, other.birthday)
        result.nickname = max(self.nickname, other.nickname)
        result.title = max(self.title, other.title)
        result.role = max(self.role, other.role)
        result.org = max(self.org, other.org)
        result.note = self.note | other.note

        result.uid = self.uid

        return result

    @staticmethod
    def escape(val):
        """escape."""
        return val.replace(',', r'\,').replace(';', r'\;').replace(':', r'\:')

    def dedupe(self, docSet, tag, parser):
        """dedupe."""
        try:
            bag = {}
            for doc in docSet:
                key = str(doc)
                if key not in bag:
                    bag[key] = set()
                try:
                    bag[key] = bag[key] | set(doc.tag["TYPE"])
                except KeyError:
                    pass

            result = set()
            for key in bag:
                if issubclass(parser, Bag):
                    data = "%s%s:%s" % (tag,
                                        ';TYPE=' + ','.join(bag[key])
                                        if bag[key] else '',
                                        key)
                else:
                    data = "%s%s:%s" % (tag,
                                        ';TYPE=' + ','.join(bag[key])
                                        if bag[key] else '',
                                        vCard.escape(key))

                result.add(parser(data))
            return result
        except TypeError:
            sys.stderr.write(str(docSet))
            raise

    def cleanName(self):
        """cleanName."""
        pass

    def clean(self):
        """clean."""
        # check for email-only contact
        if (not self.fn or not self.fn.value) \
           and len(self.n) == 0 \
           and not self.org \
           and len(self.adr) == 0 \
           and len(self.phone) == 0:
            return None

        # check for email / fn match
        if 0 < len(self.email):
            test = parseaddr(str(self.fn))[1].lower()
            # cross = [jellyfish.jaro_winkler(x.user.lower(),
            #                                 str(self.fn).lower())
            #          for x in self.email]
            cross = [x.user.lower() == str(self.fn).lower()
                     for x in self.email]
            users = True \
                if 0 < len(list(filter((lambda x: x), cross))) \
                else False

            cross = [jellyfish.jaro_winkler(str(x).lower(), test)
                     for x in self.email]
            emails = True \
                if 0 < len(list(filter((lambda x: True if .94 < x else False), cross))) \
                else False

        try:
            if (users or emails) \
               and len(self.phone) == 0 \
               and len(self.adr) == 0:
                return None
        except UnboundLocalError:
            return self

        hits = [x
                for x in self.email
                if None == re.search(r"reply.", x.domain)]
        self.email = set(hits)
        if 0 == len(self.email) \
           and len(self.phone) == 0 \
           and len(self.adr) == 0:
            return None

        self.adr = self.dedupe(self.adr, "ADR", Address)
        self.email = self.dedupe(self.email, "EMAIL", Email)
        self.label = self.dedupe(self.label, "LABEL", Label)
        self.phone = self.dedupe(self.phone, "TEL", Phone)
        self.url = self.dedupe(self.url, "URL", Url)

        if self.fn and self.n:
            test = ("%s %s" % (xstr(self.n.value[1]),
                               xstr(self.n.value[0]))).lstrip()
            if "" != test:
                testName = HumanName(test)
                testName.capitalize()
                self.fn.value = str(testName)
                #
                # print(testName)
                # print(str(self.fn))
                # print(str(self.fn) == testName)
                # if str(self.fn) != testName:
                #   self.fn.value = str(testName)

        if not str(self.fn):
            if self.org:
                self.fn.value = self.org.value

        return self

    def compact(self):
        """compact."""
        if not self.clean():
            return {}

        data = {}
        for att in self.__dict__:
            val = self.__dict__[att]
            if not val:
                continue
            if set == type(val):
                data[att] = [{"val": x.value,
                              "type": [y
                                       for y
                                       in x.tag["type"]]}
                             for x in val]
            else:
                data[att] = {"val": str(val),
                             "type": [y
                                      for y in val.tag["type"]
                                      if val.tag["type"]]}
        return data

    def features(self):
        """features."""
        data = []
        for attr in ['email', 'fn', 'n', 'phone']:  # ['email','phone','fn','n']:
            val = self.__dict__[attr]
            if not val:
                continue
            if set == type(val):
                temp = [[attr, '{}:{}'.format(','.join(x.tag.types), str(x))] for x in val]
                data.extend(temp)
            else:
                if str(val):
                    temp = str(val)
                    data.append([attr, temp])

        return data

    def to_json(self):
        """to_json."""
        return json.dumps(self.compact())

    def print_json(self):
        """print_json."""
        return json.dumps(self.compact(), indent=4)

    def __str__(self):
        """__str__."""
        card = []
        card.append("BEGIN:VCARD")
        card.append("VERSION:3.0")
        if self.fn:
            card.append(repr(self.fn))
        if self.n:
            card.append(repr(self.n))

        for att in self.__dict__:
            if "n" == att or "fn" == att:
                continue

            val = self.__dict__[att]
            if not val:
                continue
            if set == type(val):
                for x in val:
                    card.append(repr(x))
            else:
                card.append(repr(val))

        card.append("END:VCARD\n")
        return '\n'.join(card)
