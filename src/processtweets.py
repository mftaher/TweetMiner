# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Fazle Taher"
__date__ ="$Feb 18, 2011 1:42:15 AM$"

from threading import Thread
from textprocess import TextProcess
from keycleaner import KeyCleaner
from dataset import DataSet

class ProcessTweets(Thread):
    def __init__(self,conf,q):
        self.ptext = TextProcess(conf)
        self.ds = DataSet(conf)
        self.cleaner = KeyCleaner()
        self.enable_translation = self.ptext.translation
        self.translation_store = self.ptext.translation_store
        self.tweets = q         # Tweets queue
        self.tweet = ""
        self.tokens = ""
        self.i = 0
        Thread.__init__(self)
        
    def run(self):
        while True:
            rawTweet = self.tweets.get()
            if "text" in rawTweet:
                tokens = {}
                self.ptext.set_tweet_text(rawTweet['text'])
                self.ptext.set_tweet_source(rawTweet['source'])
                self.ptext.process_text()
                rawTweet['source'] = self.ptext.get_tweet_source()
                rawTweet['text'] = self.ptext.get_tweet_text()
                self.tokens = self.ptext.get_tweet_tokens()
                tokens['tokens'] = self.tokens
                rawTweet.update(tokens)
                self.tweet = self.cleaner.unset_tweet_keys(rawTweet)

                if not self.ptext.get_translate_status():
                    self.ds.output_tweet(self.tweet)
                    self.i +=  1
                else:
                    if self.translation_store:
                        if self.enable_translation:
                            if not self.ptext.get_translate_failed():
                                self.ds.output_tweet(self.tweet)
                                self.i +=  1
                        else:
                            self.ds.output_tweet(self.tweet)
                            self.i +=  1

                self.tweets.task_done()

    def get_tweet_count(self):
        return self.i