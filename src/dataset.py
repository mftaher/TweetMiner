import sys
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Area51"
__date__ ="$Apr 6, 2011 6:19:30 PM$"

from mongodb import MongoDB
try:
    from dateutil.parser import parse
except:
    print "Error: Requires dateutil to parse date in tweets. try - easy_install dateutil"
    sys.exit()
#from pygeocoder import Geocoder
from datetime import datetime
import utils
import os

class DataSet():
    def __init__(self, conf):
        self.db_engine = conf.database.engine
        self.db = conf.database.db
        self.collection = conf.database.collection
        
        self.counter = 0
        self.location = ""
        self.geo = conf.geo.geo
        self.writefile = conf.output.write
        self.geowrite = conf.geo.write
        self.userwrite = conf.user.write
        self.tweetwrite = conf.tweet.write
        self.wordswrite = conf.words.write

        if self.geo:
            self.geoEngine = conf.geo.engine
            if self.geoEngine == "google":
                self.googleLimit = conf.geo.limit
                
        self.usetime = conf.output.filenamewithdate
        self.outdir = conf.output.directory

        if self.outdir:
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
                
        self.tweetfilename = conf.tweet.filename
        self.geofilename = conf.geo.filename
        self.userfilename = conf.user.filename
        self.wordsfilename = conf.words.filename
        
        if self.usetime:
            time = datetime.now()
            time = time.strftime("%Y-%m-%d")
            self.outdir += "%s/" % (time)

            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
                 
        self.tweetfields = conf.tweet.fields.split(",")
        self.userfields = conf.user.fields.split(",")
        
        self.format = conf.output.format

        self.out_tweets_file = "%s%s.%s" % (self.outdir,self.tweetfilename,self.format)
        self.out_geo_file = "%s%s.%s" % (self.outdir,self.geofilename,self.format)
        self.out_user_file = "%s%s.%s" % (self.outdir,self.userfilename,self.format)
        self.out_words_file = "%s%s.%s" % (self.outdir,self.wordsfilename,self.format)

        self.store = conf.database.store
        if self.store:
            try:
                if self.db_engine == "mongo":
                    self.mongo = MongoDB(self.db,self.collection)
                else:
                    print "Currently only MongoDB supported for storing tweets. \nContact ftaher@gmail.com for additional support"
                    print "==================================================\n"
                    self.mongo = MongoDB(self.db,self.collection)
            except:
                print "Couldn't find database driver. Storing option disabled"
                print "==================================================\n"
                self.store = False
                pass
                
    def output_tweet(self,tweet):
        if self.writefile:
            self.output_tweets_in_file(tweet)
            
        if self.store:
            self.output_db(tweet)
         
    def output_tweets_in_file(self,result):
        keywords=""
        points = ""
        words = True
        uid = result['user']['id']
        if self.geo:
            if self.geowrite:
                if not type(result["geo"]).__name__  == 'NoneType':
                    lat=0.00
                    long=0.00

                    while len(result["geo"]["coordinates"]) != 0:
                        if len(result["geo"]["coordinates"]) == 2:
                            lat = str(result["geo"]["coordinates"].pop(0))
                        else:
                            long = str(result["geo"]["coordinates"].pop(0))
                    points = "%s %s" % (lat,long)
        
        if self.userwrite:
            user = ""
            if self.userfields:
                i = 0
                ttl = len(self.userfields)
                for field in self.userfields:
                    if field == 'screenname' or field== 'name':
                        user += "\"%s\"" % result["user"][field].encode("UTF-8")
                    elif field== 'description' or field == 'time_zone':
                        user += "\"%s\"" % utils.clean(result["user"][field].encode("ASCII","ignore"))
                    elif field =='created_at':
                        created = result["user"][field].encode("UTF-8")
                        date = parse(created)
                        created = date.strftime("%Y-%m-%d %H:%M:%S")
                        user += "\"%s\"" % created
                    elif not field == 'id':
                        if result["user"][field] != "":
                            user += "%s" % result["user"][field]
                        else:
                            user += "0" 
                    if i < ttl:
                        user += ","
                    i += 1

        if self.tweetwrite:
            tweet = ""
            if self.tweetfields:
                i = 0
                ttl = len(self.tweetfields)
                for field in self.tweetfields:
                    if field == 'source':
                        source = utils.parse_alink(result[field])
                        tweet += "\"%s\"" % source.encode("UTF-8")
                    elif field == 'created_at':
                        created = result[field].encode("UTF-8")
                        date = parse(created)
                        created = date.strftime("%Y-%m-%d %H:%M:%S")
                        tweet += "\"%s\"" % created
                    elif field == 'tokens':
                        list(result[field]).sort()
                        for token in result[field]:
                            keywords += token.lower()+" "
                        keywords = keywords.rstrip().encode("UTF-8")
                        if keywords == "":
                            words = False
                        tweet += "\"%s\"" % keywords
                    elif field == 'text':
                        text = utils.clean(result[field])
                        tweet += "\"%s\"" % text.encode("UTF-8")
                    elif field == 'retweet_count':
                        tweet += "\"%s\"" % str(result[field]).encode("UTF-8").replace("+","")
                        
                    i += 1
                    if i < ttl:
                        tweet += ","
        
        if points != "":
            if keywords == "":
                field = "tokens"
                list(result[field]).sort()
                for token in result[field]:
                    keywords += token.lower()+" "
                keywords = keywords.rstrip().encode("UTF-8")
            geo_data = "%s,\"%s\",\"%s\"" % (uid,points,keywords)
            self.output_data_file(self.out_geo_file, geo_data)
        
        if user != "":
            user_data = "%s,%s" % (uid,user)
            self.output_data_file(self.out_user_file, user_data)
            
        if tweet != "":
            tweets_data = "%s,%s" % (uid,tweet)
            self.output_data_file(self.out_tweets_file, tweets_data)
            
        if self.wordswrite:
            if words:
                if keywords == "":
                    field = "tokens"
                    list(result[field]).sort()
                    for token in result[field]:
                        keywords += token.lower()+" "
                    keywords = keywords.rstrip().encode("UTF-8")
                words_data = "\"%s\"" % keywords
                self.output_data_file(self.out_words_file,words_data)
             
    def output_data_file(self,filename,data):
        if self.format == 'arff':
            #self.output_arff(filename, data)
            print "arff output currently not supported"
        if self.format == 'txt':
            self.output_txt(filename, data)
            
    def output_arff(self,filename,data):        
        if not os.path.exists(filename):
            header = '''
% Title: TweetStream Dataset
%
% Sources:
%      (a) Creator: M. Fazle Taher
%      (b) Email: ftaher@gmail.com
%
@relation tweet-stream

@attribute tweet string
@attribute source string

@data
'''
            with open(filename,"w") as fp:
                fp.write(header)
                fp.close()

        with open(filename,"ab") as fp:
            fp.writelines("%s\n" % data.strip())
            fp.close()
            
    def output_txt(self,filename,data):
        with open(filename,"a") as fp:
            fp.writelines("%s\n" % (data))
            fp.close()

    def output_db(self,tweet):
        if self.store:
            self.mongo.insert(tweet)

    def get_region_country_from_points(self,latitude,longitude):
        if self.counter < self.google_limit:
            gcoder = Geocoder()
            results = gcoder.reverse_geocode(latitude,longitude)
            region = results.administrative_area_level_1__short_name
            country = results.country
            counter=counter+1
            self.location="%s %s" %(region,country)

    