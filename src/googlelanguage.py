#!/usr/bin/env python
#
# Copyright (c) 2009 Jonathan Beilin / Web Ecology Project

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


"""A Python implementation of Google's Language Detect and
Translation APIs

Documentation for the APIs available here:

Transliteration perhaps coming later

Notes: 
- need to handle errors thrown by google - might including following
- need to figure out max string length and give meaningful errors?

"""

import urllib
try:
    import simplejson
except:
    print "Error: Requires simplejson to parse. try - easy_install simplejson"
    pass

DETECT_API_PARAMS = {'v':'1.0', 'q':'','key':'ABQIAAAAe220-ZUFumEDGoDqOURWihRz3HqwGbwfqOn-fJ2FvnTZaw4M3xRzGTOSN0e9x9l0XKBd4mVb01QLvw','userip':'192.168.1.103',}
DETECT_URL = 'http://ajax.googleapis.com/ajax/services/language/detect?'

TRANSLATE_API_PARAMS = {'v':'1.0', 'q':'', 'langpair':'','key':'ABQIAAAAe220-ZUFumEDGoDqOURWihRz3HqwGbwfqOn-fJ2FvnTZaw4M3xRzGTOSN0e9x9l0XKBd4mVb01QLvw','userip':'192.168.1.103',}
TRANSLATE_URL = 'http://ajax.googleapis.com/ajax/services/language/translate?'

TRANSLITERATE_API_PARAMS = {'tlqt' : '1', 'langpair': '', 'text':'', 'tl_app':'1','key':'ABQIAAAAe220-ZUFumEDGoDqOURWihRz3HqwGbwfqOn-fJ2FvnTZaw4M3xRzGTOSN0e9x9l0XKBd4mVb01QLvw','userip':'192.168.1.103',}
TRANSLITERATE_URL = 'http://www.google.com/transliterate/indic?'

detect_params = DETECT_API_PARAMS.copy()
translate_params = TRANSLATE_API_PARAMS.copy()
transliterate_params = TRANSLITERATE_API_PARAMS.copy()

class InputError(Exception):
    """Exception raised for errors given by Google.

    Attributes:
        text -- text for which the error occurred
        status -- status returned by Google signifying error
    """

    def __init__(self, text, status):
        self.text = text
        self.status = status


def lang_detect(text):
    """Takes a block of text and returns language id & confidence from Google's  language detect API server
    Arguments:
      text - string to be language-detected"""
    detect_params['q'] = text

    url = DETECT_URL + urllib.urlencode(detect_params)
    response = simplejson.load(urllib.urlopen(url))    

    data = response['responseData']
    
    return data


def lang_translate(text, source_lang="", dest_lang="en"):
    """Takes a block of text, a source language, and a destination language and returns the translation. Source language is optional
    Arguments:
      text - string to be translated
      source_lang - (optional) source language
      dest_lang - destination language, default en
    """
    translate_params['q'] = text
    translate_params['langpair'] = source_lang + '|' + dest_lang
    url = TRANSLATE_URL + urllib.urlencode(translate_params)
    response = simplejson.load(urllib.urlopen(url))
    data = {}
    if response['responseStatus'] != 200:
        print "google failed translation"
        data['responseStatus'] = response['responseStatus']
        #raise APIError(text, response['responseStatus'])
    else:
        data = response['responseData']
        response['responseData']['responseStatus'] = response['responseStatus']
        
    return data

# NOT DONE
# take a string in English and transliterate it to a specified language (default Hindi)
# Not implemented until the API goes public
# still need to figure out what failures look like. are there failures?
def lang_transliterate(text, language="hi"):
    transliterate_params['text'] = text
    transliterate_params['langpair'] = 'en|' + language
    
    url = TRANSLATE_URL + urllib.urlencode(transliterate_params)
    response = simplejson.load(urllib.urlopen(url))
    
    return reponse