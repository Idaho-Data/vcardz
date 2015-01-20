import csv
from functools import reduce
import json
import re
import sys
import uuid

class Tag:
  prop = None
  attr = None

  def __init__(self,data):
    try:
      tag = re.split(r'(?<!\\):', data)[0]
      attrs = tag.split(';')
      self.prop = attrs.pop(0)
      frags = self.prop.split('.')
      if 1 < len(frags):
        self.prop = frags[1]
      self.prop = self.prop.upper()

      if None != attrs:
        self.attr = {}
        for token in attrs:
          (type, val) = token.split('=')
          try:
            self.attr[type.upper()] = self.attr[type.upper()] | set([x.lower() for x in val.split(',')])
          except:
            self.attr[type.upper()] = set([x.lower() for x in val.split(',')])
        
    except IndexError:
      return

  def __getitem__(self, key):
    try:
      return self.attr[key.upper()]
    except:
      return []


  def __str__(self):
    if None == self.prop:
      return ""
    else:
      return self.prop

  def __repr__(self):
    if None == self.prop:
      return ""
    else:
      if None == self.attr:
        return self.prop
      else:
        temp = ""
        for key in self.attr:
          if 0 == len(self.attr[key]):
            continue
          temp += ";%s=%s" % (key, ','.join(self.attr[key]))
        return self.prop + temp
