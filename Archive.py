#!/usr/bin/env python

test="""The.Simpsons.20th.Anniversary.Special.in.3D.On.Ice.REPACK.720p.HDTV.x264-2HD
The.Simpsons.S21E01.720p.HDTV.x264-CTU
Top_Gear.14x05.720p_HDTV_x264-FoV
Top.Gear.S14E06.720p.HDTV.x264-BiA
Top Gear.S14E07.720p.HDTV.x264-BiA
V.2009.S01E01.720p.HDTV.X264-DIMENSION
House.S06E01E02.720p.HDTV.x264-CTU"""

from Show import Show

class Archive(object):
    def __init__(self):
        self.data = {}

    def add(self, path):
        s=Show(path)
        if self.data.has_key(s.name):
            self.data[s.name].append(s)
        else:
            self.data[s.name] = []
            self.data[s.name].append(s)
        pass

if __name__ == "__main__" :
    a = Archive()

    for line in test.split("\n"):
        a.add(line)


    for (show, episodes) in a.data.items():
        print show
        for episode in episodes:
            print "  " + str(episode)

