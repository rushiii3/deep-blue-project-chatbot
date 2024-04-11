from flask import Flask, jsonify, request
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
# from PDFExtraction.extract_pdf import get_pdf_from_url
app = Flask(__name__)


# Define a sample route for your API
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

# API route for extraction
@app.route('/api/extraction',methods=['POST'])
def extract_pdf():
    print("yeee")
    url = request.get_json().get("url")
    get_pdf_from_url(url)
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
