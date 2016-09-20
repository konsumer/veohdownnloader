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
import threading
from time import sleep
import os
import wx


import trace


class KThread(threading.Thread):
	"""A subclass of threading.Thread, with a kill() method."""
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False
	
	def start(self):
		"""Start the thread."""
		self.__run_backup = self.run
		self.run = self.__run # Force the Thread to install our trace.
		threading.Thread.start(self)
	
	def __run(self):
		"""Hacked run function, which installs the trace."""
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup
	
	def globaltrace(self, frame, why, arg):
		if why == 'call':
			return self.localtrace
		else:
			return None
	
	def localtrace(self, frame, why, arg):
		if self.killed:
			if why == 'line':
				raise SystemExit()
		return self.localtrace
	
	def kill(self):
		self.killed = True


# Thread class that executes veoh processing
class WorkerThread(KThread):
	"""Worker Thread Class."""
	def __init__(self, video, saveDir='~/Desktop'):
		"""Init Worker Thread Class."""
		KThread.__init__(self)
		self.veoh = VeohMovie(url=video, saveDir=saveDir)
		self.completed_total=-1
		self.start()

	def run(self):
		"""Run Worker Thread."""
		self.veoh.update_info()
		self.info = self.veoh.info
		self.outfilename = self.veoh.outfilename
		self.completed_total=0
		while self.veoh.get_next_piece():
			self.completed_total=self.veoh.completed_total
		
		# over 100 to stop
		self.completed_total=200



# simple percent-dialog downloader
def wx_main(video):
	app = wx.PySimpleApp()
	
	# you could put a DirDialog in here to ask where to save...
	
	# this does the actual work of downloading
	worker = WorkerThread(video)

	# there could be something smarter in here to get a more accurate time
	# estimate - range is existing to 100, not 0 to 100
	
	dlg = wx.ProgressDialog("Veoh Download",
		                    "Getting info...",
		                    maximum = 100,
		                    style = wx.PD_CAN_ABORT | wx.RESIZE_BORDER |
		                      wx.PD_APP_MODAL |
		                      wx.PD_ELAPSED_TIME |
		                      wx.PD_ESTIMATED_TIME |
		                      wx.PD_REMAINING_TIME)

	while worker.completed_total <= 100:
		if worker.completed_total > 0:
			(keepGoing, skip) = dlg.Update(worker.completed_total, "Downloading %s" % os.path.basename(worker.outfilename))
		else:
			(keepGoing, skip) = dlg.Update(0.0)
		
		if not keepGoing:
			break
		sleep(0.2)
	
	worker.kill()
	sys.exit(0)
    
    # all info has been downloaded at this point, so you could do a check
    # for existing file ( and even filesize) here
    
    
    


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print """\nUsage: %s URL
        URL can be any veoh video page like
        http://www.veoh.com/videos/v6525744grmT6Jhz?jalsdkj=234&blah=asd
        or veoh://downloadVideo?permalinkId=v6525744grmT6Jhz&command=49347A0A-C783-4e92-ADCE-ED7C93207E58
        it also supports permalink id's, so you can just use v6525744grmT6Jhz
    """ % (sys.argv[0])
        sys.exit()
    wx_main(sys.argv[1])

