import pymongo
import os


class Database:
    DATABASE_URI = os.environ['MONGODB_URI']
    client = None
    database_conn = None

    def __init__(self):
        self.getConnection()

    def getConnection(self):
        if not self.database_conn:
            self.database_conn = self.getClient()['telegram']
            self.database_conn.authenticate('heroku_kbd1k1h8', 'l4c60tknrm33v0qj1ncnndb7dg')
        return self.database_conn

    def getClient(self):
        if not self.client:
            self.client = pymongo.MongoClient(self.DATABASE_URI)
        return self.client
