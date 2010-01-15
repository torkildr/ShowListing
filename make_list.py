#!/usr/bin/env python

import os
import pickle

from ShowListing import *

if __name__ == "__main__" :
    try:
        df=open("data.dat")
        a = pickle.load(df)
        df.close()
    except IOException:
        a = Archive()

    for dirname, dirnames, filenames in os.walk('/home/shared/done'):
        for subdirname in dirnames:
            a.add(os.path.join(dirname, subdirname))

    index=open("index.html", "w")

    shows = a.data.keys()
    shows.sort()

    for show in shows:
        episodes = a.data[show] 

        if len(episodes) > 1:
            print "%s: %d episodes" % (show, len(episodes))
            index.write("%s: %d episodes\n" % (show, len(episodes)))
        else:
            index.write(show + "\n")
        
        showIndex = open("html/" + episodes[0].dotName + ".html", "w")

        for episode in episodes:
            showIndex.write("  " + str(episode) + "\n")

        showIndex.close()

    index.close()

