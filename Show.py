#!/usr/bin/env python

import re

test="""The.Simpsons.20th.Anniversary.Special.in.3D.On.Ice.REPACK.720p.HDTV.x264-2HD
The.Simpsons.S21E01.720p.HDTV.x264-CTU
Top_Gear.14x05.720p_HDTV_x264-FoV
Top.Gear.S14E06.720p.HDTV.x264-BiA
Top Gear.S14E07.720p.HDTV.x264-BiA
V.2009.S01E01.720p.HDTV.X264-DIMENSION
House.S06E01E02.720p.HDTV.x264-CTU"""

class Show(object):
    pattern = "(.*?)[ .]?(S?(\d+)(E|x)(\d+)).*"

    @property
    def name(self):
        if self.match:
            return self.show
        else:
            return self.path

    @property
    def episode(self):
        return "S%sE%s" % (self.ses, self.ep)

    def processPath(self, path):
        self.path = path
        p = re.compile(self.pattern)
        m = p.match(self.path)
        self.match = m

        if m:
            self.show   = m.group(1).replace(" ", ".").replace("_", ".")
            self.ses    = m.group(3)
            self.ep     = m.group(5)
            self.groups = ", ".join(["(%s)" % x for x in m.groups()])
        
    def __init__(self, path):
        self.processPath(path)

    def __repr__(self):
        if (self.match):
            return self.episode
        else:
            return self.path

if __name__ == "__main__" :
    for line in test.split("\n"):
        s=Show(line)
        print s

