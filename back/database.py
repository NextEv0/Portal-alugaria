from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Carlos_Esteves:mario_elgrably123@cadmus.smz7lcv.mongodb.net/?retryWrites=true&w=majority&appName=Cadmus"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    db = client['Arsenium']
    User = db['User']
    Room = db['Room']
    Schedules = db['Schedules']
except Exception as e:
    print(e)
