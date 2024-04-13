import sys
import os
import random
import json
import torch

current_directory = os.getcwd()

parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory+'/')


print(current_directory)
from utils.nltk_utlis import tokenize, bag_of_words
from PDFExtraction.model import NeuralNet
def get_response(msg) :
    sentence = tokenize(msg) 
    print(sentence)
    return sentence


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')




with open('../PDFExtraction/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "../PDFExtraction/data.pth"
data = torch.load(FILE)




input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
pattern_all_words = data["pattern_all_words"]
tags = data['tags']
model_state = data["model_state"]


model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "DiGiCOR Chatbot" 



def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, pattern_all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
 
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.85:      #Increasing specifisity to reduce incorrect classifications
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return f"I'm sorry, but I cannot understand your query. "




if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

