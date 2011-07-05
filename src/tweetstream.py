#! /usr/bin/python
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Fazle Taher"
__date__ ="$Apr 18, 2011 7:23:13 PM$"

from getpass import getpass
from config import Configuration
from Queue import Queue
from processtweets import ProcessTweets
import simplejson as json
import pycurl
import time
import sys


class TweetStream():
    def __init__(self,conf,q):
        self.user = conf.stream.user
        if self.user =="":
            print "Edit username and password in stream.ini file"
            print "==================================================\n"
            self.user = raw_input("Username: ")
        self.passwd = conf.stream.password
        if self.passwd == "":
            self.passwd = getpass("Password: ")
        self.url = conf.stream.url
        self.delimited = conf.stream.delimited
        self.trackwords = conf.track.words
        self.follow = conf.follow.users
        self.locations = conf.location.geo
        self.verbose = int(conf.curl.verbose)
        self.timeout = int(conf.curl.timeout)
        self.keepalive = conf.curl.keep_alive
        self.buffer = ""
        self.tweets = q
        
    def on_receive(self,data):
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            try:
                content = json.loads(self.buffer)
                self.buffer = ""
            except Exception, e:
                print e
                content={}
                self.buffer = ""
                pass
            if content:
                self.tweets.put(content)

    def start(self):
        headers = ["User-Agent: R&D Cooker", "Keep-Alive: " + str(self.keepalive), "Connection: Keep-Alive"]

        params = ""

        if self.trackwords != "":
            params += "track=%s&" % self.trackwords
        if self.follow !="":
            params +="follow=%s&" % self.follow
        if self.locations != "":
            params +="locations=%s" % self.locations

        if params != "":
            params += "delimited=%s" % self.delimited
        else:
            print "============================================================="
            print """You need to specify at least a parameter in stream.ini file:
                    \nword to track or user to follow or location bounding box"""
            print "============================================================="
            sys.exit()
            
        conn = pycurl.Curl()
        conn.setopt(pycurl.POST,1)
        conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        conn.setopt(pycurl.USERPWD, "%s:%s" % (self.user, self.passwd))
        conn.setopt(pycurl.URL, self.url)
        conn.setopt(pycurl.VERBOSE, self.verbose)
        conn.setopt(pycurl.HTTPHEADER, headers)
        conn.setopt(pycurl.POSTFIELDS,params)
        conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
        conn.setopt(pycurl.CONNECTTIMEOUT, self.timeout)

        try:
            conn.perform()
        except pycurl.error, e:
            print e
            pass
        except KeyboardInterrupt:
            print "BYE!!"

start = time.time()

def main():
    tweets = Queue()
    conf = Configuration('stream.ini')
    
    pT = ProcessTweets(conf,tweets)
    pT.setDaemon(True)
    pT.start()
    
    stream = TweetStream(conf,tweets)
    stream.start()

    tweets.join()

main()
print "Elapsed Time: %.2fsecs" % (time.time() - start)
