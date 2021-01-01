from decouple import config
from pymongo import MongoClient

def connectDB():
  username = config('DBUSERNAME')
  password = config('DBPASSWORD')
  dbname = config('DBNAME')
  uri = f"mongodb+srv://{username}:{password}@cluster0.alocm.mongodb.net/{dbname}?retryWrites=true&w=majority"
  client = MongoClient(uri)
  db = client[dbname]
  return db


def readData():
  db = connectDB()
  collection = db['questions']
  return list(collection.find({}))