# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Area51"
__date__ ="$Apr 19, 2011 4:46:43 PM$"
from mongodb import MongoDB
from config import Configuration
from textprocess import TextProcess
from dataset import DataSet
import time

class TweetDB():
    def __init__(self):
        conf = Configuration()
        self.ptext = TextProcess(conf)
        self.ds = DataSet(conf)
        self.mongo = MongoDB(self.ds.db,self.ds.collection)
        self.tweet=""
        self.tokens = ""
        self.i = 0
        self.enable_translation = self.ptext.translation
        self.translation_store = self.ptext.translation_store

    def get_tweet_from_db(self):
        where = {
                    "text":{"$exists":"true"},
                    "geo.coordinates":{"$exists":"true"}
                }
        select = {"text":1,"source":1,"geo":1, "user":1,"retweet_count":1,"created_at":1}
        results = self.mongo.find(where,select)
        return results

    def process_tweets(self):
        tweets = self.get_tweet_from_db()
        for rawTweet in tweets:
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


    def get_tweet_count(self):
        return self.i
    
def main():
    t = TweetDB()
    t.process_tweets()

start = time.time()
main()
print "Elapsed Time: %.2fsecs" % (time.time() - start)