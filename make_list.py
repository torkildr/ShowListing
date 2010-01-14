#!/usr/bin/env python

import os

from ShowListing import *

if __name__ == "__main__" :
    a = Archive()

    for dirname, dirnames, filenames in os.walk('/home/shared/done'):
        for subdirname in dirnames:
            a.add(os.path.join(dirname, subdirname))

    for (show, episodes) in a.data.items():
        print "%s: %d episode(s)" % (show, len(episodes)) 
        for episode in episodes:
            print "  " + str(episode)

