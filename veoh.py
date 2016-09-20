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

import httplib
import libxml2
import urllib, urllib2
import os
import cPickle as pickle
import re


"""
The basic process is this:

get info/piece hashes (both cached)
loop:
    get peers - not used yet
    download piece  - from old central veoh file server, eventually will be UDP peers
    update completed list

"""

class VeohError(Exception):
    pass

class VeohMovie:
    """ Encapsulates veoh networking, info, and downloading functions for one video file """
    
    # developer debugging, dumps xml files that are being parsed
    debug = True
        
    veoh_client_info={'clientGUID':'', 'version': '3.0.0'}
    headers = {"Content-type": "application/xml", "User-agent": "veoh-3.0 service (MacOS; Safari; darwin)"}
    peers = []
    saveDir = ''
    logFile = ''
    pieceDir = ''
    outfilename = ''
    vid=''
    pieces = []
    completed = []
    info = []
    completed_total=0
    decrament = 0
    
    def __init__(self, url=None, vid=None, saveDir='~/Desktop', logFile=None, delLog=True):
    	"""
    	constructor.
    	
    	url is the url of the video - you must set 1 of these.
    	vid is the video id - you must set 1 of these.
    	
    	saveDir is the output dir for the movie, defaults to Desktop
    	logFile is the filename of the log file, which stores info about what has been downloaded
    	delLog determines whether or not the log is deleted when the download is complete
    	"""
        if vid is None:
            if url is None:
                raise VeohError('You must set either vid or url.')
            vid = self.get_vid(url)
        self.vid = vid
        
        # TODO: some dirname trickery here to put log in sensible place
        if logFile is None:
            logFile = '%s.pieces' % (self.vid)
               
        self.saveDir = os.path.expanduser(saveDir)
        self.logFile = os.path.expanduser("~/.veoh_downloader/" + logFile)
        
        # mkdir if it doesn't exist
        try:
            os.makedirs(os.path.dirname(self.logFile))
        except OSError:
            pass
        try:
            os.makedirs(self.saveDir)
        except OSError:
            pass       
    
    def update_info(self):
    	# open piece-list, or get it, if it doesn't exist, and save it for next time
        try:
            f = open(self.logFile, 'rb')
            self.pieces, self.completed, self.info = pickle.load(f)
            f.close()
        except:
            # haven't downloaded info, get it now, and save
            
            self.info = self.get_info(self.vid)
            self.pieces = self.get_pieces()
            self.completed = []
            [self.completed.append(False) for piece in self.pieces]
            self.save_progress()
        
        self.outfilename = "%s/%s%s" % (self.saveDir, self.info['title'], self.info['extension'])
        
        size = int(self.info['size'])
        self.decrament =(size / len(self.completed)) * (100.0/size)
        
        # if out file doesn't exist, then log should not exist
        if not os.path.exists(self.outfilename):
        	os.remove(self.logFile)
            
    def get_peers(self):
        """ This is not used yet - for when veoh stops letting people use their cache/get.jsp, and this will have to work with UDP P2P """
        xml = self.get_url('http://pt.veoh.com/tracker/getPeers.jsp?fileHash=%s&minVersion=5&maxCount=20&myNat=symmetric' % self.info['filehash'])
        # save pieces file to be analyzed
        if self.debug:
            f=open('peers.xml','wb')
            f.write(xml)
            f.close()
        doc = libxml2.parseDoc(xml)
        
        peersXp = doc.xpathEval('/response/peer/@externalAddress')
        addresses = []
        for i in peersXp:
            addresses.append(i.getContent().strip())
        
        peersXp = doc.xpathEval('/response/peer/@percentComplete')
        complete = []
        for i in peersXp:
            complete.append(i.getContent().strip())
        
        peers = [(addresses[i].split(':'),complete[i])for i in range(len(addresses))]
        return peers
    
    
    def get_next_piece(self):
        """ Download next pending piece, append it to download file """   
        # search for first uncompleted
        for i in range(len(self.pieces)):
            if not self.completed[i]:
                piece = self.get_url('%s/cache/get.jsp?fileHash=%s&pieceHash=%s' % (self.info['urlroot'], self.info['filehash'], self.pieces[i]))
                
                """
                # get UDP peers and download a packet from one
                newpeers = self.get_peers()
                if len(newpeers) > 0:
                    self.peers = newpeers
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer = self.peers[random.randrange(len(self.peers))]
                s.connect(peer[0])
                # do UDP here...
                s.close()
                """
                
                if (piece):
                    f = open(self.outfilename, 'ab')
                    f.write(piece)
                    f.close()
                    self.completed[i] = True
                    self.completed_total=i * self.decrament
                    self.save_progress()
                else:
                    print 'failed to get piece: %s' % self.pieces[i]
                    self.completed[i] = False
                
                # keep downloading
                return True
        
        # no more pieces
        return False
         
    
    def save_progress(self):
        """ Store cached internal representation of info - peers, video info, and completed packets"""
        f = open(self.logFile, 'wb')
        pickle.dump((self.pieces, self.completed, self.info),f)
        f.close()
        
    
    def get_pieces(self):
        """ Return a list of pieces for current video file """
        xml = self.get_url(self.info['piecehashfile'])
        doc = libxml2.parseDoc(xml)
        piecesXp = doc.xpathEval('/file/piece/@id')
        pieces = []
        for i in piecesXp:
            hash = i.getContent().strip()
            pieces.append(hash)
        
        # save pieces file to be analyzed
        if self.debug:
            f=open('pieces.xml','wb')
            f.write(xml)
            f.close()
        return pieces
    
            
    def get_url(self, url, data=''):
        """ Wrapper for downloading/posting data, return response text """
        req = urllib2.Request(url)
        for i in self.headers:
            req.add_header(i,self.headers[i])
        
        if self.debug:
        	print 'getting: ' + url + "\n" + data
        
        content_length = len(data)
        if content_length > 0:
            req.add_header('Content-Length', content_length)
            req.add_data(data)
        
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print url
            print 'Error code: %s' % e.code
            return False
        return f.read()
    
    
    def get_info(self, vid):
        """ Return top-level info about video file """
        info={'vid':vid}
        xml = self.get_url('http://www.veoh.com/service/getMediaInfo.xml?%s' % urllib.urlencode(self.veoh_client_info), '<MediaIdList><MediaId permalinkId="%s"/></MediaIdList>' % info['vid'])
        doc = libxml2.parseDoc(xml)
        for i in ('FileHash', 'Size', 'Title', 'Extension', 'Duration', 'PieceHashFile','UrlRoot'):
            result = doc.xpathEval('/Response/QueueEntry/Video/%s' % i)
            info[i.lower()] = result[0].get_content().strip()
        
        # save info file to be analyzed
        if self.debug:
            f=open('info.xml','wb')
            f.write(xml)
            f.close()
        return info   
        
        
    def get_vid(self, url):
        """ Return vid for a URL of any supported type """
        re_permalink = re.compile('permalinkId=(v[a-zA-Z0-9]+)')
        matches = re_permalink.findall(url)
        if (len(matches) > 0):
            return matches[0]
        else:
            re_vidlink = re.compile('videos/(v[a-zA-Z0-9]+)')
            matches = re_vidlink.findall(url) 
            return matches[0]
    
    
        
        
