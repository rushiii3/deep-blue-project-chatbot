from flask import Flask, jsonify, request
from flask_cors import CORS

# import sys
# import os

# # Get current working directory
# current_directory = os.getcwd() 
# # Get parent directory
# parent_directory = os.path.dirname(current_directory)
# # Append parent directory to sys.path to access modules from the parent directory
# sys.path.append(parent_directory+'/')


# get_response is accessed from the chat folder
from main.chat import get_response
from PDFExtraction.extract_pdf import extract_pdf_from_url
from Database_Module.main import insert_extract_db
app = Flask(__name__)
CORS(app)

# Define a sample route for your API
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

# API route for extraction
@app.route('/api/extraction',methods=['POST'])
def extract_pdf():
    url = request.get_json().get("url")
    id = request.get_json().get("id")
    extract = extract_pdf_from_url(url)
    insert_extract_db(extract,id)
    message = {"message": "Your url reached!!","url":url}
    return jsonify(message)


# API route for prediction
@app.route('/api/predict',methods=['POST'])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)
