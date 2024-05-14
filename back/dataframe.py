from database import db, User, Room, Schedules
from bson import ObjectId
import pprint
import pandas as pd

id = ObjectId("6641076e5cc70f1f94e2e53f")
reservas = Schedules.find({'room_id': id})

df = pd.DataFrame(list(reservas))

pipeline = [
    {
        '$lookup': {
            'from': 'User',
            'localField': 'room_id',
            'foreignField': '_id',
            'as': 'user_info'
        }
    },
    {
        '$lookup': {
            'from': 'Room',
            'localField': 'room_id',
            'foreignField': '_id',
            'as': 'room_info'
        }
    },
    {
        '$project': {
            'user_info.account': 0,
            'room_info': 0
        }
    }
]

result = db['Schedules'].aggregate(pipeline)

df = pd.DataFrame(list(result))

print(df.head())
