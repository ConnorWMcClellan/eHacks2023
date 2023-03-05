import pymongo
from pymongo import MongoClient
import datetime

try:
    conn = MongoClient()
    cluster = MongoClient('mongodb+srv://UmbranDrake:eHacks23FlyinLions@atscluster.cez6evd.mongodb.net/?retryWrites=true&w=majority')
    print("Successful connection!")
except:
    print("Oh no, connection failed!")

db = cluster["ats"]
collection = db["records"]

lName = ""
fName = ""

d = datetime.datetime.utcnow()

#Inserts a record
db.records.insert_one({"lastName":lName,"firstName":fName, "date": d})

#Prints all of "records" collection
results = collection.find({})
for iter in results:
    print(iter)