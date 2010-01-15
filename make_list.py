#!/usr/bin/env python

import os
import pickle

from ShowListing import *

if __name__ == "__main__" :
    try:
        df = open("data.dat")
        a = pickle.load(df)
        df.close()

        a.unfind()
    except IOError:
        a = Archive()

    for dirname, dirnames, filenames in os.walk('/home/shared/done'):
        for subdirname in dirnames:
            a.add(os.path.join(dirname, subdirname))

    index=open("index.html", "w")

    shows = a.data.keys()
    shows.sort()

    for show in shows:
        episodes = a.data[show].keys()
        episodes.sort()

        if len(episodes) > 1:
            print "%s: %d episodes" % (show, len(episodes))
            index.write("%s: %d episodes\n" % (show, len(episodes)))
        else:
            index.write(show + "\n")
        
        showIndex = open("html/" + a.data[show].values()[0].dotName + ".html", "w")

        for episode in episodes:
            showIndex.write("  " + str(a.data[show][episode]) + "\n")

        showIndex.close()

    index.close()

    df = open("data.dat", "w")
    pickle.dump(a, df)
    df.close()
