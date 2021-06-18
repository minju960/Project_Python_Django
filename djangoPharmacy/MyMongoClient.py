from pymongo import MongoClient


class MyMongoClient:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://minju:2483@minju-cluster.tdqyh.mongodb.net/pharmacy_db?retryWrites=true&w=majority')
        self.db = self.client['pharmacy_db']
        self.collection = self.db['pharmacy_collection']
