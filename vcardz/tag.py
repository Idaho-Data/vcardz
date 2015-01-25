import re


class tag:
    _prop = None
    _attr = None

    def __init__(self, data):
        try:
            tag = re.split(r'(?<!\\):', data)[0]
            attrs = tag.split(';')
            self._prop = attrs.pop(0)
            frags = self.prop.split('.')
            if 1 < len(frags):
                self.prop = frags[1]
                self.prop = self.prop.upper()

            if None != attrs:
                self._attr = {}
                for token in attrs:
                    (type, val) = token.split('=')
                    key = type.upper()
                    try:
                        self._attr[key] = self._attr[type.upper()] | \
                            set([x.lower() for x in val.split(',')])
                    except:
                        self._attr[key] = set([x.lower()
                                               for x in val.split(',')])

        except IndexError:
            return

    def __getitem__(self, key):
        try:
            return self._attr[key.upper()]
        except:
            return []

    def __str__(self):
        if None == self._prop:
            return ""
        else:
            return self._prop

    def __repr__(self):
        if None == self._prop:
            return ""
        else:
            if None == self.attr:
                return self._prop
            else:
                temp = ""
                for key in self._attr:
                    if 0 == len(self._attr[key]):
                        continue
                        temp += ";%s=%s" % (key, ','.join(self._attr[key]))
                        return self._prop + temp
