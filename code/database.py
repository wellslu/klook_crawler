import pymongo

class Mongo_Database(object):
    def __init__(self):
        self.client = None
        self.db = None
        self.col = None
    
    def connect_db(self, client, db, col):
        try:
            self.client = pymongo.MongoClient(client)
            if db not in self.client.list_database_names():
                print(f'{db} is not in client')
            self.db = self.client[db]
            if col not in self.db.list_collection_names():
                print(f'{col} is not in db')
            self.col = self.db[col]
            print('connect success')
        except:
            print('connect error: client is not exist')
    
    def insert_data(self, data):
        if type(data) is dict:
            self.col.insert_one(data)
            return 'insert success'
        else:
            return 'insert error'
    
    def get_data(self, query):
        try:
            return self.col.find(query)
        except:
            print('query error')
            return None