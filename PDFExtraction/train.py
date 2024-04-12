import numpy as np

import json
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
import os
import sys
current_directory = os.getcwd()

parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory+'/')


print(current_directory)
from  utils.nltk_utlis import tokenize,stem,bag_of_words

with open("intents.json","r") as f:
    intents = json.load(f)
tags = []
pattern_all_words = []
xy = []
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        pattern_all_words.extend(w)
        xy.append((w,tag))
ignore_words = [',','.',':','!','?']
pattern_all_words = [stem(w) for w in pattern_all_words if w not in ignore_words]
pattern_all_words = sorted(set(pattern_all_words))
tag = sorted(set(tags))
x_train = []
y_train = []
for (pattern_sentence,tag) in xy:
    bag = bag_of_words(pattern_sentence,pattern_all_words)
    print(bag)
    x_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

class ChatDataset(Dataset):
    def __init__(self):
        self.nsamples = len(x_train)
        self.xdata = x_train
        self.ydata = y_train
    def __getitem__(self, index):
        return self.xdata[index],self.ydata[index]
    def __len__(self):
        return self.nsamples

x_train = np.array(x_train)
y_train = np.array(y_train)
dataset = ChatDataset()
batch_size = 8
num_epoches = 1000
learning_rate = 0.01
input_size = len(x_train[0])
hidden_size = 8
output_size = len(tags)
train_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size,hidden_size,output_size).to(device)
print(model)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)
for epoch in range(num_epoches):
    for (words,labels) in train_loader:
        words = words.to(device)
        print(words)
        labels = labels.to(dtype=torch.long).to(device)
        outputs = model(words)
        loss = criterion(outputs,labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if((epoch+1) % 100 == 0):
        print(f'Epoch [{epoch+1}/{num_epoches}], Loss :{loss.item():.4f}')

data = {
    "model_state" : model.state_dict(),
    "input_size" : input_size,
    "hidden_size" : hidden_size,
    "output_size" : output_size,
    "pattern_all_words" : pattern_all_words,
    "tags" : tags 
}
FILE = "data.pth"
torch.save(data,FILE)
print(f'tarning complete. File saved to{FILE}')