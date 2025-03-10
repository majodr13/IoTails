import pymongo

client = pymongo.MongoClient("mongodb+srv://IoTails:IoTails1234@iot.gcez4.mongodb.net/")
db = client["IoTails"]
pets_collection = db["pets"]  # Ensure this is defined 