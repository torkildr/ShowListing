#!/usr/bin/env python

import os
import urllib
import pickle

from ShowListing import *

root_path = "/home/shared/torrent_jukebox"

htmlHead = "<html>\n<head><title></title><link rel=stylesheet href=\"style.css\" type=\"text/css\" /></head>\n<body>\n<p id=\"title\">%s</p>\n<p>\n<a href=\"%s.html\">%s</a>\n</p>\n<table>\n"
showHead = "<html>\n<head><title></title><link rel=stylesheet href=\"style.css\" type=\"text/css\" /></head>\n<body>\n<p id=\"title\">%s</p>\n<table>\n"
htmlFoot = "</table>\n</body>\n</html>\n"
htmlData = "<tr class=\"show%d\"><td class=\"text\">%s</td><td class=\"desc\">%s</td></tr>\n"

html_path = "%s/html" % (root_path)

def toggle(num):
    if num == 0:
        return 1
    else:
        return 0

if __name__ == "__main__" :
    try:
        df = open("%s/data.dat" % (root_path))
        a = pickle.load(df)
        df.close()
        a.unfind()
    except IOError:
        a = Archive()

    for dirname, dirnames, filenames in os.walk('%s/video' % (root_path)):
        for subdirname in dirnames:
            a.add(os.path.join(dirname, subdirname))

    index=open("%s/index.html" % (root_path), "w")

    shows = a.data.keys()
    shows.sort()

    # we make a different index ordered by mtime later
    latestShows = []

    index.write(htmlHead % ("TV Show listing (alphabetical)", "latest", "Ordered by date"))

    showColor = 1

    # ugly, less portable, and probably unsafe
    # ..very fast though
    os.system("find %s -type f ! -iname \"*.css\" -delete" % html_path)

    for show in shows:
        episodes = a.data[show].keys()
        
        # better this way(tm)
        episodes.sort(reverse=True)

        ep = a.data[show][episodes[0]]
        showColor = toggle(showColor)
       
        latestShows.append((max([x.unixtime for x in a.data[show].values()]), show, ep.episode))

        if len(episodes) > 1:
            index.write(htmlData % (showColor, ep.showLink, "%d episodes" % len(episodes)))
        else:
            index.write(htmlData % (showColor, ep.showLink, ""))
        
        showIndex = open("%s/%s.html" % (html_path, ep.dotName), "w")

        showIndex.write(showHead % show)

        epColor = 1
        infoCount = 0

        for episode in episodes:
            if not a.data[show][episode].found:
                del a.data[show][episode]
            else:
                epColor = toggle(epColor)
                s = a.data[show][episode]
                showIndex.write(htmlData % (epColor, s.link, s.description))

                showJsp   = open("%s/jsp/%s.%s.jsp" % (html_path, ep.dotName, s.episode), "w")
                for url in s.urls:
                    showJsp.write("%s - %s|0|0|%s|" % (s.name, s.episode, url))
                showJsp.close()

                infoCount += 1

        if len(a.data[show]) == 0:
            del a.data[show]
        
        print "%s: %d episodes" % (show, infoCount)

        showIndex.write(htmlFoot)
        showIndex.close()
   
    index.write(htmlFoot)
    index.close()

    df = open("%s/data.dat" % (root_path), "w")
    pickle.dump(a, df)
    df.close()

    # hackish, but write the other index thingy
    
    showColor = 1
    latestShows.sort(reverse=True)

    index=open("%s/latest.html" % (root_path), "w")

    index.write(htmlHead % ("TV Show listing (latest first)", "index", "Ordered by name"))
    
    for (mtime, show, name) in latestShows:
        if not a.data.has_key(show):
            continue

        episodes = a.data[show].keys()
        
        ep = a.data[show].values()[-1]
        showColor = toggle(showColor)
       
        if len(episodes) > 1:
            index.write(htmlData % (showColor, ep.showLink, "%d episodes" % len(episodes)))
        else:
            index.write(htmlData % (showColor, ep.showLink, ""))

    index.write(htmlFoot)
    index.close()

