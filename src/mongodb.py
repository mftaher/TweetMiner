# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Area51"
__date__ ="$Feb 22, 2011 3:31:38 AM$"

try:
    from pymongo.connection import Connection
    from pymongo.errors import PyMongoError
    from bson import json_util
except:
    print "Error: Requires pymongo for database support. try - easy_install pymongo"


fileencoding = "iso-8859-1"

class MongoDB():
    def __init__(self,db,collection):
        self.conn = Connection()
        self.db = self.conn[db]
        self.collection = self.db[collection]

    def find(self,where={},select={}):
        try:
            return self.collection.find(where,select)
        except PyMongoError, e:
            print e
    def save(self,what = {}):
        try:
            return self.collection.save(what)
        except PyMongoError, e:
            print e
            
    def find_one(self,where={},select={}):
        try:
            return self.collection.find_one(where,select)
        except PyMongoError, e:
            print e
    def insert(self,content):
        try:
            self.collection.insert(content)
        except PyMongoError, e:
            print e
        
    def update_all(self,modifier,where={},upsert=False,mani=False,safe=True,multi=True):
        try:
            self.collection.update(where,modifier,upsert,mani,safe,multi)
        except PyMongoError, e:
            pass
            print e

    def update(self,modifier,where={}):
        try:
            self.collection.update(where,modifier)
        except PyMongoError, e:
            print e
            pass

    def remove(self,where={},safe=True):
        try:
            if self.collection.remove(where,safe):
                return True
            else:
                return False
        except PyMongoError, e:
            pass
            print e

    def e_index(self,what):
        try:
            self.collection.ensure_index(what)
        except PyMongoError, e:
            print e

    def json_hook(self, doc):
        try:
            return json_util.object_hook(doc)
        except PyMongoError, e:
            print e

    def mongo_js(self):
        return self.db.system_js

    
    def list_js(self):
        return self.db.system_js.list()