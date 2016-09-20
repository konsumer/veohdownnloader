#!/usr/bin/python
"""
Copyright 2008 David Konsumer <konsumer@jetboystudio.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

from veoh import *
import sys


# very simple loop, just prints percentage as it goes.
# use this as an example of implementing in your own UI
def simple_main(video):
    v = VeohMovie(url=video)
    v.update_info()
    
    # all info has been downloaded at this point, so you could do a check
    # for existing file ( and even filesize) here
    
    while v.get_next_piece():
        print "%.2f%%" % v.completed_total

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print """\nUsage: %s URL
        URL can be any veoh video page like
        http://www.veoh.com/videos/v6525744grmT6Jhz?jalsdkj=234&blah=asd
        or veoh://downloadVideo?permalinkId=v6525744grmT6Jhz&command=49347A0A-C783-4e92-ADCE-ED7C93207E58
        it also supports permalink id's, so you can just use v6525744grmT6Jhz
    """ % (sys.argv[0])
        sys.exit()
    simple_main(sys.argv[1])

