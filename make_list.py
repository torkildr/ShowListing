#!/usr/bin/env python

import os

from Archive import Archive

if __name__ == "__main__" :
    a = Archive()

    for dirname, dirnames, filenames in os.walk('/home/shared/done'):
        for subdirname in dirnames:
            a.add(subdirname)

        #a.add(line)

    for (show, episodes) in a.data.items():
        print show
        for episode in episodes:
            print "  " + str(episode)

