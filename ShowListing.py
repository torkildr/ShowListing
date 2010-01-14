#!/usr/bin/env python

import re, os
from subprocess import Popen, PIPE

def readableToSeconds(tup):
    return (int(tup[0])*60*60) + (int(tup[1])*60) + int(tup[2])

def secondsToReadable(s):
    return "%02d:%02d:%02d" % ((s / (60*60)), (s / 60) % 60, s % 60)

class walkDir(object):
    def __init__(self, root, exts=None):
        self.root = root
        self.ext = exts

    def __iter__(self):
        for dirpath, dirnames, filename in os.walk(self.root):
            for dirname in dirnames:
                walkDir(dirname)
            for file in filename:
                if self.ext.count(os.path.splitext(file)[-1].lower()):
                    yield os.path.join(dirpath, file)

class Show(object):
    pattern = "(.*?)[ .]?(S?(\d+)(E|x)(\d+)).*"

    def __init__(self, path):
        self.path = path
        
        self.processPath(os.path.basename(path))
        self.processVideoFiles()

    def __repr__(self):
        return "%s (%s) %d" % (self.episode, secondsToReadable(self.time), len(self.files))

    @property
    def name(self):
        if self.match:
            return self.show
        else:
            return self.basename

    @property
    def episode(self):
        if self.match:
            return "S%sE%s" % (self.ses, self.ep)
        else:
            return self.show

    def processPath(self, basename):
        self.basename = basename
        p = re.compile(self.pattern)
        m = p.match(self.basename)
        self.match = m

        if m:
            self.show   = m.group(1).replace(" ", ".").replace("_", ".")
            self.ses    = m.group(3)
            self.ep     = m.group(5)
            self.groups = ", ".join(["(%s)" % x for x in m.groups()])
        else:
            self.show   = self.basename.replace(" ", ".").replace("_", ".")

    def processVideoFiles(self):
        """
        family.guy.s08e10.hdtv.xvid-2hd.avi, 173Mb
        video: 512x384 00:20:54 23.97fps XviD 1Mbps
        audio: 48KHz  00:20:54 Stereo 121Kbps mp3
        """

        p = re.compile("video.*(\d+):(\d+):(\d+)")
        
        self.time = 0
        self.files = []

        for file in walkDir(self.path, [".avi", ".mkv", ".mpg", ".mpeg"]):
            output = Popen(["/usr/bin/avinfo", file], stdout=PIPE).communicate()[0]
            m = p.match(output.split("\n")[1])
            
            if m:
                self.time += readableToSeconds(m.groups())
                self.files.append(file)
    
        
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

# test stuff

test="""/home/shared/done/The.Simpsons.20th.Anniversary.Special.in.3D.On.Ice.REPACK.720p.HDTV.x264-2HD
/home/shared/done/The.Simpsons.S21E01.720p.HDTV.x264-CTU
/home/shared/done/Top_Gear.14x05.720p_HDTV_x264-FoV
/home/shared/done/Top.Gear.S14E06.720p.HDTV.x264-BiA
/home/shared/done/Top Gear.S14E07.720p.HDTV.x264-BiA
/home/shared/done/V.2009.S01E01.720p.HDTV.X264-DIMENSION
/home/shared/done/House.S06E01E02.720p.HDTV.x264-CTU"""

if __name__ == "__main__" :
    a = Archive()

    for line in test.split("\n"):
        a.add(line)


    for (show, episodes) in a.data.items():
        print "%s: %d episode(s)" % (show, len(episodes)) 
        for episode in episodes:
            print "  " + str(episode)

