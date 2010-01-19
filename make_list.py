#!/usr/bin/env python

import os
import pickle

from ShowListing import *

root_path = "/home/shared/torrent_jukebox/"

htmlHead = "<html>\n<head><title></title><link rel=stylesheet href=\"style.css\" type=\"text/css\" /></head>\n<body>\n"
htmlFoot = "</body>\n</html>\n"
htmlData = "<div class=\"show\"><div class=\"link%d\">%s</div><div class=\"desc\">%s</div></div>\n"

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

    index.write(htmlHead)

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
        showIndex.write(htmlHead)

        epColor = 1

        for episode in episodes:
            if not a.data[show][episode].found:
                del a.data[show][episode]
            else:
                epColor = toggle(epColor)
                s = a.data[show][episode]
                showIndex.write(htmlData % (epColor, s.link, s.duration))

                showJsp   = open(html_path + ep.dotName + "." + s.episode + ".jsp", "w")
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

