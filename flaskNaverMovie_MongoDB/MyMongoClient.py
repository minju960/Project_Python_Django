from pymongo import MongoClient

class MyMongoClient:
    def __init__(self):
        self.connect_string = 'mongodb+srv://minju:2483@minju-cluster.tdqyh.mongodb.net/naver_movie_db?retryWrites=true&w=majority'
        self.client = MongoClient(self.connect_string)
        self.db = self.client['naver_movie_db']
        self.collection = self.db['naver_movie_collection']