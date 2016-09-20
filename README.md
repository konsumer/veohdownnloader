# Defunct

This doesn't work anymore, due to protocol changes on veoh's part. I am keeping it here for historical purposes.

---

I wrote a python veoh downloader for Linux people (and Windows/Mac people who hate the veoh player) to use. It uses wxWindows for the GUI, but you can import and use it with your own interface, if you like.

Make sure to use quotes on the URL, if you run it on the command-line.

## Installing
It has 2 dependencies. wxpython and libxml2.

You can find downloads for your OS here:
wxpython - http://sourceforge.net/project/showfiles.php?group_id=10718&package_id=10559
libxml2 - http://xmlsoft.org/downloads.html

The window installer installs all the dependencies, too, so you only have to install these, if you want to run it as a py file, not an EXE.

### Mac/Linux
on Ubuntu/Debian, use this instead of the packages from above:
```
sudo apt-get install python-wxgtk2.8 python-libxml2
```

If you have a different version of python-wxgtk, it shouldn't be a big deal.

Installs like a standard python package.

Just run
```
python setup.py install
```

After installing it, make sure it runs like this:
```
veoh_downloader_gui.py "http://www.veoh.com/videos/v6525744grmT6Jhz?source=featured&cmpTag=featured2&rank=0"
```


I also included veoh_downloader_cli.py as an example of a very simple command-line version.

### Windows
Use the setup file, and it should take care of everything for you.

### Firefox

If you want it to correctly handle veoh:// links in firefox, for Mac/Linux you will need to set some stuff up.

    * Type about:config into the address bar and press Enter.
    * Right-click -> New -> Boolean -> Name: network.protocol-handler.external.veoh -> Value -> true
    * Right-click -> New -> String -> Name: network.protocol-handler.app.veoh -> Value -> /usr/bin/veoh_downloader_gui.py (Replacing /usr/bin/veoh_downloader_gui.py with the full path to veoh_downloader_gui.py.
    * Ensure network.protocol-handler.expose-all is set to true. 

The windows installer adds a registry handler for `veoh://` links, so that should all be taken care of.

At this point, you should be able to change any veoh video page URL from `http://` to `veoh://` and it will load my script.

[This greasemonkey script](http://userscripts.org/scripts/show/26078) will create a link for you, automatically.

It will make the download link say "Download with VeohDownloader".

