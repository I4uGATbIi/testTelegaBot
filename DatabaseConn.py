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
        return self.database_conn

    def getClient(self):
        if not self.client:
            self.client = pymongo.MongoClient(self.DATABASE_URI)
        return self.client
