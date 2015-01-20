import csv
import io
import jellyfish
import re
import sys
import uuid

import lib.kontexa.vcard as vcard
import lib.pst as pst

# from lib.kontexa.vcard import scrub, vCard, Parser, Url, fscrub
from .utils import *
from .builder import *

"""
PST parsing
"""

class OutlookPST():
  pst_parser = None
  pst_contacts = None

  DISPLAY_NAME = 0x3001
  SURNAME = 0x3a11
  GIVEN_NAME = 0x3a06
  MIDDLE_NAME = 0x3a44
  PREFIX = 0x3a45
  SUFFIX = 0x3a05
  
  BIZ_PHONE = 0x3a08
  BIZ_PHONE2 = 0x3a1b
  BIZ_FAX = 0x3a24
  CALLBACK = 0x3a02
  CAR_PHONE = 0x3a1e
  COMPANY_MAIN_PHONE = 0x3a57
  HOME_FAX = 0x3a25
  HOME_PHONE = 0x3a09
  HOME_PHONE2 = 0x3a2f
  ISDN = 0x3a2d
  MOBILE_PHONE = 0x3a1c
  OTHER_FAX = 0x3a23
  OTHER_PHONE = 0x3a1f
  PAGER = 0x3a21
  PRIMARY_PHONE = 0x3a1a

  EMAIL1_ADR = 0x8083
  EMAIL1_TYPE = 0x8082
  EMAIL2_ADR = 0x8093
  EMAIL2_TYPE = 0x8092
  EMAIL3_ADR = 0x80a3
  EMAIL3_TYPE = 0x80a2
  
  BIZ_PO_BOX = 0x3a2b
  BIZ_STREET = 0x8045
  BIZ_CITY = 0x8046
  BIZ_STATE = 0x8047
  BIZ_ZIP = 0x8048
  BIZ_COUNTRY = 0x8049

  HOME_PO_BOX = 0x3a5e
  HOME_STREET = 0x3a5d
  HOME_CITY = 0x3a59
  HOME_STATE = 0x3a5c
  HOME_ZIP = 0x3a5b
  HOME_COUNTRY = 0x3a5a

  OTHER_PO_BOX = 0x3a64
  OTHER_STREET = 0x3a63
  OTHER_CITY = 0x3a5f
  OTHER_STATE = 0x3a62
  OTHER_ZIP = 0x3a61
  OTHER_COUNTRY = 0x3a60

  URL_VAL = 0x3a51
  
  USER_FIELD = 0x804f
  BIRTHDAY = 0x3a42
  COMPANY = 0x3a16
  TITLE = 0x3a17
  

  def __init__(self, pstFile):
    self.pst_parser = pst.py_pst(pstFile)
    self.pst_contacts = iter(self.pst_parser.get_contacts())

  def __iter__(self):
    return self

  def next(self):
    contact = next(self.pst_contacts)
    # self.card = vcard.vCard()
    builder = Builder()
    
    builder.FN(contact.get_val(self.DISPLAY_NAME))
    builder.N([contact.get_val(self.SURNAME),
               contact.get_val(self.GIVEN_NAME),
               contact.get_val(self.MIDDLE_NAME),
               contact.get_val(self.PREFIX),
               contact.get_val(self.SUFFIX)])

    builder.TEL(contact.get_val(self.BIZ_PHONE), 'work')
    builder.TEL(contact.get_val(self.BIZ_PHONE2), 'work')
    builder.TEL(contact.get_val(self.BIZ_FAX), 'work,fax')
    builder.TEL(contact.get_val(self.CALLBACK), 'callback')
    builder.TEL(contact.get_val(self.CAR_PHONE), 'mobile')
    builder.TEL(contact.get_val(self.COMPANY_MAIN_PHONE), 'work')
    builder.TEL(contact.get_val(self.HOME_FAX), 'home,fax')
    builder.TEL(contact.get_val(self.HOME_PHONE), 'home')
    builder.TEL(contact.get_val(self.HOME_PHONE2), 'home')
    builder.TEL(contact.get_val(self.ISDN), '')
    builder.TEL(contact.get_val(self.MOBILE_PHONE), 'mobile')
    builder.TEL(contact.get_val(self.OTHER_FAX), 'fax')
    builder.TEL(contact.get_val(self.OTHER_PHONE), '')
    builder.TEL(contact.get_val(self.PAGER), 'pager')
    builder.TEL(contact.get_val(self.PRIMARY_PHONE), 'pref')


    builder.EMAIL(contact.get_prop(self.EMAIL1_ADR), contact.get_prop(self.EMAIL1_TYPE))
    builder.EMAIL(contact.get_prop(self.EMAIL2_ADR), contact.get_prop(self.EMAIL2_TYPE))
    builder.EMAIL(contact.get_prop(self.EMAIL3_ADR), contact.get_prop(self.EMAIL3_TYPE))

    builder.ADR([contact.get_val(self.BIZ_PO_BOX),
              '',
              contact.get_prop(self.BIZ_STREET),
              contact.get_prop(self.BIZ_CITY),
              contact.get_prop(self.BIZ_STATE),
              contact.get_prop(self.BIZ_ZIP),
              contact.get_prop(self.BIZ_COUNTRY)],
             'work')

    builder.ADR([contact.get_val(self.HOME_PO_BOX),
              '',
              contact.get_val(self.HOME_STREET),
              contact.get_val(self.HOME_CITY),
              contact.get_val(self.HOME_STATE),
              contact.get_val(self.HOME_ZIP),
              contact.get_val(self.HOME_COUNTRY)],
             'home')

    builder.ADR([contact.get_val(self.OTHER_PO_BOX),
              '',
              contact.get_val(self.OTHER_STREET),
              contact.get_val(self.OTHER_CITY),
              contact.get_val(self.OTHER_STATE),
              contact.get_val(self.OTHER_ZIP),
              contact.get_val(self.OTHER_COUNTRY)],
             '')

    builder.URL(contact.get_val(self.URL_VAL))
    builder.NOTE(contact.get_prop(self.USER_FIELD))
    builder.BDAY(contact.get_val(self.BIRTHDAY))
    builder.ORG(contact.get_val(self.COMPANY))
    builder.ROLE(contact.get_val(self.TITLE))

    return str(builder.card)
    
           
    
