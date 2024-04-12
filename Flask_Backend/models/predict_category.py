'''from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np
from pprint import pprint
'''

'''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    FUNCTIONS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''

'''
class CustomDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels
        #print(self.features)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        #print("the input to tokenizer is")
        #print(str(self.features.values[idx]))

        input_ids = tokenizer.encode_plus(str(self.features.values[idx]), add_special_tokens=True)
        attention_mask = [1] * len(input_ids)
        label = self.labels.iloc[idx]
        return {
            'input_ids': torch.tensor(input_ids),
            'attention_mask': torch.tensor(attention_mask),
            'labels': torch.tensor(label)
        }
'''
'''
class CustomDataset(Dataset):
    def __init__(self, features, labels, max_seq_length=128):  # Set max_seq_length to desired maximum sequence length
        self.features = features
        self.labels = labels
        self.tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        self.max_seq_length = max_seq_length

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        input_text = str(self.features.values[idx])
        tokens = self.tokenizer.encode_plus(input_text, add_special_tokens=True, max_length=self.max_seq_length, truncation=True, padding='max_length', return_tensors='pt')
        input_ids = tokens['input_ids'].squeeze(0)  # Remove batch dimension
        attention_mask = tokens['attention_mask'].squeeze(0) # Remove batch dimension
        label = self.labels.iloc[idx]

        to_return={
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': torch.tensor(label)
            }

        #print(f"\nwhen get item is called in the class\n")
        #print(to_return)
        return to_return


def training_phase():
    num_epochs=1
    datasets=load_and_split_dataset()
    fine_tune_finbert_model(datasets,num_epochs)

    #testing_phase(datasets)


def load_and_split_dataset():
    df= pd.read_csv("../../Datasets/sample_dataset.csv")
    df["heading_and_subheading"]=0

    #we need to encode the heading and subheading as an integer because the model wants it in an integer form
    #hence we are going to use two indexes, one for main heading and one for subheadings withing the headings

    unique_main_headings=df["main_heading"].unique()
    # Extract subheadings for each main heading
    subheadings_dict = {}
    for main_heading in unique_main_headings:
        subheadings = df.loc[df['main_heading'] == main_heading, 'subheading'].unique()
        subheadings_dict[main_heading] = subheadings

    #print(subheadings_dict)

    labels_and_their_numeric_code_dict={}

    label_code=0
    for main_heading_index, (main_heading,subheadings_array) in enumerate(subheadings_dict.items()):
        #print(main_heading_index)
        for subheading_index,subheading in enumerate(subheadings_array):
            label=main_heading.strip()+"_"+subheading.strip()
            #label_code=int(str(main_heading_index)+str(subheading_index))
            labels_and_their_numeric_code_dict[label]=label_code
            label_code+=1
    pprint(labels_and_their_numeric_code_dict)

    for index, row in df.iterrows():
        main_heading=row["main_heading"]
        subheading=row["subheading"]
        label=main_heading.strip()+"_"+subheading.strip()

        for new_label in list(labels_and_their_numeric_code_dict.keys()):
            if new_label==label:
                #print(new_label, label)
                #print(labels_and_their_numeric_code_dict[new_label])
                #row["heading_and_subheading"]=labels_and_their_numeric_code_dict[new_label]
                df.at[index,"heading_and_subheading"]=labels_and_their_numeric_code_dict[new_label]
    print(df.head(10))
    

    #print(df.head(10))
    #df['heading_and_subheading'] = df['main_heading'].astype(str) + '_' + df['subheading'].astype(str)
    
    # Drop the original target columns from the DataFrame
    df.drop(columns=['main_heading','subheading'], inplace=True)

   
    x= df.drop(columns=['heading_and_subheading'])
    y = df['heading_and_subheading']

    # Split the dataset into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=48)
    #print(x_train.head(10))

    return [x_train,x_test,y_train,y_test]

#3.
def fine_tune_finbert_model(datasets,num_epochs):

    x_train=datasets[0]
    y_train=datasets[2]

    pytorch_training_set=CustomDataset(x_train,y_train)
    #y_pytorch_train=CustomDataset(y_train)

    #print(len(x_train))
    train_loader=DataLoader(pytorch_training_set,batch_size=64,shuffle=True)
    optimizer = torch.optim.AdamW(finbert.parameters(), lr=0.0001)
    criterion = torch.nn.CrossEntropyLoss()

    #put finbert in training mode
    finbert.train()

    print("HERE")

    #print(train_loader)

    #epoch means one complete round of going through the entire dataset, It updates it weights accoringly
    for epoch in range(num_epochs):
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch['input_ids']
            attention_mask = batch['attention_mask']
            labels = batch['labels']
            print(labels)
            outputs = finbert(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
    



def testing_phase(datasets):

    true_labels=[]
    predicted_labels=[]
    #put finbert in evaluation mode
    finbert.eval()

    x_test=datasets[1]
    y_test=datasets[3]

    pytorch_test_set=CustomDataset(x_test,y_test)
    #y_pytorch_test=CustomDataset(y_test)

    test_loader=DataLoader(pytorch_test_set,shuffle=True,batch_size=32)

    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids']
            attention_mask = batch['attention_mask']
            labels = batch['labels']
            outputs = finbert(input_ids=input_ids, attention_mask=attention_mask)
            predictions = torch.argmax(outputs.logits, dim=1)

            # Append true labels and predicted labels to the lists
            true_labels.extend(labels.cpu().numpy())
            predicted_labels.extend(predictions.cpu().numpy())

    # Convert lists to numpy arrays
    true_labels = np.array(true_labels)
    predicted_labels = np.array(predicted_labels)
    print(true_labels)
    print(predicted_labels)

    # Compute evaluation metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='macro')  # 'macro' averaging for multi-class tasks
    recall = recall_score(true_labels, predicted_labels, average='macro')
    f1 = f1_score(true_labels, predicted_labels, average='macro')

    # Print the evaluation metrics
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)

'''
'''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    ACTUAL IMPLEMENTATION
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''

'''
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

training_phase()
#testing_phase()
'''
