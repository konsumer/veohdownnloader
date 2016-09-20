
# ======================================================#
# File automagically generated by GUI2Exe version 0.1
# Andrea Gavana, 31 March 2007
# ======================================================#

# Let's start with some default (for me) imports...

from distutils.core import setup
import py2exe
import glob
import os
import zlib
import shutil

shutil.rmtree("build", ignore_errors=True)


class Target(object):
    """ A simple class that holds information on our executable file. """
    def __init__(self, **kw):
        """ Default class constructor. Update as you need. """
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "1.13"
        self.company_name = "Jetboy Studio"
        self.copyright = "2008 David Konsumer"
        self.name = "Veoh Downloader"


# Ok, let's explain why I am doing that.
# Often, data_files, excludes and dll_excludes (but also resources)
# can be very long list of things, and this will clutter too much
# the setup call at the end of this file. So, I put all the big lists
# here and I wrap them using the textwrap module.

data_files = []

includes = []
excludes = ['Tkconstants', 'Tkinter', '_gtkagg', '_tkagg', 'bsddb',
            'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon',
            'pywin.dialogs', 'tcl']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']
icon_resources = []
bitmap_resources = []
other_resources = []


# This is a place where the user custom code may go. You can do almost
# whatever you want, even modify the data_files, includes and friends
# here as long as they have the same variable name that the setup call
# below is expecting.

# No custom code added


# Ok, now we are going to build our target class.
# I chose this building strategy as it works perfectly for me :-D

test_wx = Target(
    # what to build
    script = "veoh_downloader_gui.py",
    icon_resources = icon_resources,
    bitmap_resources = bitmap_resources,
    other_resources = other_resources
    )


# That's serious now: we have all (or almost all) the options py2exe
# supports. I put them all even if some of them are usually defaulted
# and not used. Some of them I didn't even know about.

setup(

    data_files = data_files,

    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },

    zipfile = ,
    windows = [test_wx]
    )


# And we are done. That's a setup script :-D

