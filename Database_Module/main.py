import pymongo

myclient = pymongo.MongoClient('mongodb+srv://hrushiop:oq16yL7AoXMn1c3x@cluster0.h4boskd.mongodb.net/')
mydb = myclient['test']
mycol = mydb["extracted_data"]
mydict = { "name": "John", "address": "Highway 37" }
x = mycol.insert_one(mydict)

print(x)
