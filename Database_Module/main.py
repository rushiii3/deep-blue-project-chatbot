from bson import ObjectId
import pymongo

myclient = pymongo.MongoClient('mongodb+srv://hrushiop:oq16yL7AoXMn1c3x@cluster0.h4boskd.mongodb.net/')
mydb = myclient['test']
mycol = mydb["files"]


def insert_extract_db(extract,id):
    myquery = { "_id": ObjectId(id) }
    newvalues = { "$set": { "extracted_data": extract } }

    try:
        # Attempt to find the document
        y = mycol.find_one(myquery)
        
        if y is None:
            print("Document not found.")
        else:
            # Update the document
            x = mycol.update_one(myquery, newvalues)
            print(x.modified_count, "documents updated.")

    except pymongo.errors.PyMongoError as e:
        # Handle any exceptions that occur during MongoDB operations
        print("An error occurred:", e)

