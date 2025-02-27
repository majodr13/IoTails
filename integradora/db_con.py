import pymongo

url ="mongodb+srv://atlas-sample-dataset-load-67c0b913156f7b4bb247b483:IoTails1234@iot.gcez4.mongodb.net/"

client = pymongo.MongoClient(url)
db= client["IoTails"]