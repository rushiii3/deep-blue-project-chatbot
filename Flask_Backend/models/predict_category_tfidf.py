
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import numpy as np
from pprint import pprint
from sklearn.metrics import classification_report
import spacy
spacy_large_model=spacy.load("en_core_web_lg")
from sklearn.model_selection import StratifiedShuffleSplit



'''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    FUNCTIONS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''

labels_and_their_numeric_code_dict={}

#
def training_phase():
    datasets=load_and_split_dataset()
    #print(type(datasets))
    #print(datasets)
    
    train_tfidf_model(datasets)
    testing_phase(datasets)
    write_labels_to_file_for_future_use(labels_and_their_numeric_code_dict)

#
def load_and_split_dataset():
    df= pd.read_csv("../../Datasets/category_prediction_dataset.csv")
    df["heading_and_subheading"]=0

    #we need to encode the heading and subheading as an integer because the model wants it in an integer form
    #hence we are going to use two indexes, one for main heading and one for subheadings withing the headings

    unique_main_headings=df["main_heading"].unique()
    # Extract subheadings for each main heading
    subheadings_dict = {}
    for main_heading in unique_main_headings:
        subheadings = df.loc[df['main_heading'] == main_heading, 'subheading'].unique()
        subheadings_dict[main_heading] = subheadings

    print(subheadings_dict)

    #labels_and_their_numeric_code_dict={}

    label_code=0
    for main_heading_index, (main_heading,subheadings_array) in enumerate(subheadings_dict.items()):
       
        for subheading_index,subheading in enumerate(subheadings_array):
            
            label=main_heading.strip()+"__"+subheading.strip()
            #label_code=int(str(main_heading_index)+str(subheading_index))
            labels_and_their_numeric_code_dict[label]=label_code
            label_code+=1
            
    pprint(labels_and_their_numeric_code_dict)

    for index, row in df.iterrows():
        main_heading=row["main_heading"]
        subheading=row["subheading"]
        label=main_heading.strip()+"__"+subheading.strip()

        for new_label in list(labels_and_their_numeric_code_dict.keys()):
            if new_label==label:
                #print(new_label, label)
                #print(labels_and_their_numeric_code_dict[new_label])
                #row["heading_and_subheading"]=labels_and_their_numeric_code_dict[new_label]
                df.at[index,"heading_and_subheading"]=labels_and_their_numeric_code_dict[new_label]
    #print(df.head(10))
    

    #print(df.head(10))
    #df['heading_and_subheading'] = df['main_heading'].astype(str) + '_' + df['subheading'].astype(str)
    
    # Drop the original target columns from the DataFrame
    #df.drop(columns=['main_heading','subheading'], inplace=True)

   
    for index,row in df.iterrows():
        query=row["user_query"]
        processed_query=preprocess_each_query(str(query))
        df.at[index,"user_query"]=processed_query


    processed_x=df["user_query"]
    #print(processed_x.head(10))

    y = df['heading_and_subheading']
    
    
    # Assuming your data is in X (features) and y (labels) format
    sss = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)

    # Split the data into train and test sets
    for train_index, test_index in sss.split(processed_x, y):
        #print(train_index, test_index)
        x_train, x_test = processed_x[train_index], processed_x[test_index]
        y_train, y_test = y[train_index], y[test_index]

    # Split the dataset into training and test sets
    #x_train, x_test, y_train, y_test = train_test_split(processed_x, y, test_size=0.25, random_state=48)
    #print(x_train.head(10))

    return [x_train,x_test,y_train,y_test]

#
def train_tfidf_model(datasets):
    x_train=datasets[0]
    y_train=datasets[2]

    #print(x_train.shape)
    #print(y_train.shape)
    #pprint(x_train)

    # Initialize TF-IDF vectorizer and logistic regression classifier
    tfidf_vectorizer = TfidfVectorizer()  # You can adjust max_features as needed
    #classifier = LogisticRegression()
    #classifier=MultinomialNB()
    classifier=RandomForestClassifier(n_estimators=100)
    #classifier=SVC(kernel='linear')

    # Create a pipeline
    pipeline = Pipeline([('tfidf', tfidf_vectorizer), ('clf', classifier)])

    # Train the model
    pipeline.fit(x_train, y_train)
    # Save the trained model
    joblib.dump(pipeline, '../models/tfidf_category_model.pkl')

#
def testing_phase(datasets):
    x_test=datasets[1]
    y_test=datasets[3]

    #pprint(x_test)

    # Create a pipeline
    pipeline = joblib.load('../models/tfidf_category_model.pkl')

    # Train the model
    pipeline.fit(x_test, y_test)
    # Step 4: Predictions
    y_pred = pipeline.predict(x_test)

    #Step 5: Evaluation
    print(classification_report(y_test, y_pred))

#2. preprocess the text
def preprocess_each_query(query):
    #tokenize it    
    spacy_text= spacy_large_model(query)

    preprocessed_tokens=[]

    #remove the stop words
    for token in spacy_text:
        if not token.is_punct and not token.is_stop:
            #lowercase the user query
            #get the lemmas in the user query
            #lemma_of_the_token=token.lemma_
            preprocessed_tokens.append(token.lemma_.lower())
    
    string_representation_of_preprocessed_text= ' '.join(preprocessed_tokens)
    #print(string_representation_of_preprocessed_text)
    return string_representation_of_preprocessed_text

def write_labels_to_file_for_future_use(labels_and_their_numeric_code_dict):
    f=open("../common/labels_and_their_numeric_code_dict.py","w")
    f.write("labels_and_label_codes_dict="+str(labels_and_their_numeric_code_dict))
    f.close()

'''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    ACTUAL IMPLEMENTATION
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''

#training_phase()
