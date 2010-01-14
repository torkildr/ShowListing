#!/usr/bin/env python

import os

from ShowListing import *

if __name__ == "__main__" :
    a = Archive()

    for dirname, dirnames, filenames in os.walk('/home/shared/done'):
        for subdirname in dirnames:
            a.add(os.path.join(dirname, subdirname))

    for (show, episodes) in a.data.items():
        if len(episodes) > 1:
            print "%s: %d episodes" % (show, len(episodes))
        else:
            print show
        
        for episode in episodes:
            print "  " + str(episode)

