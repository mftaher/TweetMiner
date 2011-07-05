# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Fazle Taher"
__date__ ="$Mar 9, 2011 4:45:18 PM$"

gntlk = True
from googlelanguage import *
try:
    from nltk.corpus import words
except:
    print "Error: Requires NLTK corpus from - http://www.nltk.org for translation to work"
    gnltk = False
    pass
import utils

class TextProcess():
    def __init__(self,conf):
        self.translation = conf.translation.translate
        self.translation_store = conf.translation.store
        self.translate_threshold = conf.translation.threshold
        self.translate_failed = False
        self.translate_status = False
        self.text = ""
        self.source = ""
        self.tokens= []
        self.tweet_id = ""
        if self.translation:
            self.english_vocab = set(w.lower() for w in words.words())
        self.stopfile = conf.stopwords.filename
        self.stopset = set(open(self.stopfile, 'r').read().split())

    """ Process Stream Tweets """
    def process_text(self):
        text = utils.clean(self.get_tweet_text())
        self.set_tweet_text(text)
        self.set_tweet_source(utils.parse_alink(self.get_tweet_source()))
        if self.translation:
            self.detect_language_or_translate()
        self.filter_text()
        
    def set_tweet_id(self,id):
        self.tweet_id = id

    def get_tweet_id(self):
        return self.tweet_id

    def set_tweet_text(self,text):
        self.text = text

    def get_tweet_text(self):
        return self.text

    def set_tweet_source(self,source):
        self.source = source

    def get_tweet_source(self):
        return self.source
    
    def set_tweet_tokens(self,tokens):
        self.tokens = tokens

    def get_tweet_tokens(self):
        return self.tokens

    def set_translate_status(self,translate=False):
        self.set_translate_failed()
        self.translate_status = translate
        
    def get_translate_status(self):
        return self.translate_status

    def set_translate_failed(self,translate=False):
        self.translate_failed = translate

    def get_translate_failed(self):
        return self.translate_failed
       
    """ Language detection and translation using google translation API """
    def detect_language_or_translate(self):
        text = self.get_tweet_text()
        text_vocab = set(w.lower() for w in text if w.isalpha())
        unusual = text_vocab.difference(self.english_vocab)
        self.set_translate_status(False)

        if len(unusual) > self.translate_threshold:
            self.set_translate_status(True)
            if self.translation:
                self.get_translated_text(text)

    def get_translated_text(self,text):
        text = text.encode('UTF-8')
        translated = lang_translate(text, dest_lang="en")
        if translated['responseStatus'] == 200:
            text = "(%s): %s" % (translated['detectedSourceLanguage'],translated['translatedText'])
            self.set_tweet_text(text)
        else:
            self.set_translate_failed(True)
    
    """ Tokenize text then filter text with stopwords and apply Porter stemming """
    def filter_text(self):
        text = self.get_tweet_text()
        text = set(utils.tokenise(text))
        filteredText = list(self.remove_stopwords(text))
        keywords = utils.stem_words(filteredText)
        self.set_tweet_tokens(keywords)
    
    def remove_stopwords(self,list):
        """ Remove common words which have no search value """
        #return [word for word in list if word not in self.stopwords ]
        return set(list.difference(self.stopset))
    

    
