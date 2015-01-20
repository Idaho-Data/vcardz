import csv
import io
import jellyfish
import re
from six import StringIO
import sys
import uuid

import kontexa.vcard as vcard
# from lib.kontexa.vcard import scrub, vCard, Parser, Url, fscrub
from .utils import *
from .errors import *


class Builder:
  card = None

  def __init__(self):
    self.card = vcard.vCard()

  def FN(self, val):
    if val:
      self.card.fn = vcard.FormattedName('FN:%s' % val)

  def N(self, val):
    if val:
      self.card.n = vcard.Name('N:%s' % ';'.join(val))

  def TEL(self, val, types):
    if val:
      data = 'TEL;TYPE=%s:%s' % (types, val)
      try:
        self.card.phone.add(vcard.Phone(data))
      except ValueError:
        self.card.note.add(vcard.Note(K_TEL_TIP % data.rstrip()))

  def EMAIL(self, val, types):
    if val:
      types = types.replace("*","") if types else types
      self.card.email.add(vcard.Email('EMAIL%s:%s' % (';TYPE=' + types.lower() if types else "",
                                                       val)))

  def ADR(self, val, types):
    test = list(filter((lambda x: x), val))
    if 1 < len(test):
        fixedVal = [re.sub(r'\r*\n+', ' ', x) for x in val]
        # fixedVal = [x.replace('\r\n',' ') for x in val]
        self.card.adr.add(vcard.Address('ADR%s:%s' % (';TYPE=' + types.lower() if types else "",
                                                      ';'.join(fixedVal))))

  def NOTE(self, val):
    if val:
      self.card.note = vcard.Note('NOTE:%s' % val)

  def BDAY(self, val):
    if val and '0/0/00' != val:
      self.card.birthday = vcard.Birthday('BDAY:%s' % val)

  def ORG(self, val):
    if val:
      self.card.org = vcard.Organization('ORG:%s' % val)

  def ROLE(self, val):
    if val:
      self.card.role = vcard.Role('ROLE:%s' % val)

  def UID(self, val):
      if val:
          self.card.uid = vcard.Uid('UID:%s' % val)

  def URL(self, val):
    if val:
      self.card.url.add(vcard.Url('URL:%s' % val))


class Builder2(Builder):
  def N(self, 
        family='', 
        given='', 
        additional='', 
        prefix='', 
        suffix=''):
    val = (family, given, additional, prefix, suffix)
    if val:
      self.card.n = vcard.Name('N:%s' % ';'.join(val))




  
