from database import db, User, Room, Schedules
from bson import ObjectId
import pprint
import pandas as pd

user_df = pd.DataFrame(list(User.find()))
user_df['user_id'] = user_df['_id']
user_df = user_df.drop(['_id','role','register','account'], axis=1)

room_df = pd.DataFrame(list(Room.find()))
room_df['room_id'] = room_df['_id']
room_df = room_df.drop(['_id','floor', 'description'], axis=1)


schedules_df = pd.DataFrame(list(Schedules.find()))
query = schedules_df.merge( room_df, on='room_id')
query = query.merge(user_df, on='user_id', how='left')

query = query.drop([ '_id', 'room_id'], axis=1)

print(query.head(20))
