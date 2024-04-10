import sys
import os
current_directory = os.getcwd()

parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory+'/')
from utils.nltk_utlis import tokenize
def get_response(msg) :
    sentence = tokenize(msg) 
    print(sentence)
    return sentence


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    resp = get_response("hey hello how are youu")
    print(resp)