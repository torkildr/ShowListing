#!/usr/bin/env python

import re, os
from subprocess import Popen, PIPE

urlBase = "file:///opt/sybhttpd/localhost.drives/NETWORK_SHARE/autotorrent/video/"

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
        self.found = True
        
        self.processPath(os.path.basename(path))
        #self.processVideoFiles()

    def __str__(self):
        return "%s (%s) %d file(s)" % (self.episode, self.duration, len(self.files))

    @property
    def name(self):
        return self.show
    
    @property
    def dotName(self):
        return self.show.replace(" ", ".")

    @property
    def urls(self):
        if len(self.files) <= 0:
            return []
        return [urlBase + "/".join(x.split("/")[4:]) for x in self.files]

    @property
    def link(self):
        return "<a href=\"jsp/%s.jsp\" vod=\"playlist\">%s</a>" % (self.dotName + "." + self.episode, self.episode)

    @property
    def showLink(self):
        return "<a href=\"html/%s.html\">%s</a>" % (self.dotName, self.name)

    @property
    def duration(self):
        return secondsToReadable(self.time)

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
        
        if m:
            self.match = True
        else:
            self.match = False

        if m:
            self.show   = m.group(1).replace(".", " ").replace("_", " ")
            self.ses    = m.group(3)
            self.ep     = m.group(5)
            self.groups = ", ".join(["(%s)" % x for x in m.groups()])
        else:
            self.show   = self.basename.replace(".", " ").replace("_", " ")

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
                print ".",
    
        
class Archive(object):
    def __init__(self):
        self.data = {}

    def add(self, path):
        s=Show(path)

        if self.data.has_key(s.name):
            if self.data[s.name].has_key(s.episode):
                if self.data[s.name][s.episode].time > 0:
                    self.data[s.name][s.episode].found = True
                else:
                    self.data[s.name][s.episode].processVideoFiles()
                return
        else:
            self.data[s.name] = {}
        
        s.processVideoFiles()
        self.data[s.name][s.episode] = s

    def unfind(self):
        for episodes in self.data.values():
            for episode in episodes.values():
                episode.found = False

