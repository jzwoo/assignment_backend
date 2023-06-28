from pymongo import MongoClient

# add connection line
client = MongoClient('mongodb://localhost:27017/')
db = client['userDB']
