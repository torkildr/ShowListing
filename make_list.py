#!/usr/bin/env python

import os
import pickle

from ShowListing import *

htmlHead = "<html>\n<head><title></title></head>\n<body>\n"
htmlFoot = "</body>\n</html>\n"
htmlData = "<div id=\"show\"><div id=\"link\">%s</div><div id=\"desc\">%s</div></div>\n"

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

    index.write(htmlHead)

    for show in shows:
        episodes = a.data[show].keys()
        episodes.sort()

        ep = a.data[show].values()[0]

        if len(episodes) > 1:
            print "%s: %d episodes" % (show, len(episodes))
            index.write(htmlData % (ep.showLink, "%d episodes" % len(episodes)))
        else:
            print show
            index.write(htmlData % (ep.showLink, ""))
        
        showIndex = open("html/" + ep.dotName + ".html", "w")
        showIndex.write(htmlHead)

        for episode in episodes:
            if not a.data[show][episode].found:
                del a.data[show][episode]
            else:
                s = a.data[show][episode]
                showIndex.write(htmlData % (s.link, s.duration))

        showIndex.write(htmlFoot)
        showIndex.close()

    index.write(htmlFoot)
    index.close()

    df = open("data.dat", "w")
    pickle.dump(a, df)
    df.close()
