#!/usr/bin/env python

import os
import urllib
import pickle

from ShowListing import *

root_path = "/home/shared/torrent_jukebox/"

htmlHead = "<html>\n<head><title></title><link rel=stylesheet href=\"style.css\" type=\"text/css\" /></head>\n<body>\n<p id=\"title\">%s</p>\n<table>\n"
htmlFoot = "</table>\n</body>\n</html>\n"
htmlData = "<tr class=\"show%d\"><td class=\"text\">%s</td><td class=\"desc\">%s</td></tr>\n"

html_path = root_path + "html/"

def toggle(num):
    if num == 0:
        return 1
    else:
        return 0

if __name__ == "__main__" :
    try:
        df = open(root_path + "data.dat")
        a = pickle.load(df)
        df.close()
        a.unfind()
    except IOError:
        a = Archive()

    for dirname, dirnames, filenames in os.walk('/home/shared/done'):
        for subdirname in dirnames:
            a.add(os.path.join(dirname, subdirname))

    index=open(root_path + "index.html", "w")

    shows = a.data.keys()
    shows.sort()

    index.write(htmlHead % "TV Show listing")

    showColor = 1

    for show in shows:
        episodes = a.data[show].keys()
        episodes.sort()

        ep = a.data[show].values()[0]
        showColor = toggle(showColor)

        if len(episodes) > 1:
            print "%s: %d episodes" % (show, len(episodes))
            index.write(htmlData % (showColor, ep.showLink, "%d episodes" % len(episodes)))
        else:
            print show
            index.write(htmlData % (showColor, ep.showLink, ""))
        
        showIndex = open(html_path + ep.dotName + ".html", "w")
        showIndex.write(htmlHead % show)

        epColor = 1

        for episode in episodes:
            if not a.data[show][episode].found:
                del a.data[show][episode]
            else:
                epColor = toggle(epColor)
                s = a.data[show][episode]
                showIndex.write(htmlData % (epColor, s.link, s.description))

                showJsp   = open(html_path + "jsp/" + ep.dotName + "." + s.episode + ".jsp", "w")
                for url in s.urls:
                    showJsp.write("%s - %s|0|0|%s|" % (s.name, s.episode, url))
                showJsp.close()

        showIndex.write(htmlFoot)
        showIndex.close()

    index.write(htmlFoot)
    index.close()

    df = open(root_path + "data.dat", "w")
    pickle.dump(a, df)
    df.close()

