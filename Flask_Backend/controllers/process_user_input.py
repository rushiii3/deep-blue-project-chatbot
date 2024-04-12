import spacy
import joblib
import sys
sys.path.append("../models")
sys.path.append("../common")
import predict_category_tfidf 
import labels_and_their_numeric_code_dict
from transformers import pipeline,set_seed
import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel


#print(predict_category_tfidf.labels_and_their_numeric_code_dict)



'''
Here we anaylze the user input and determine the category to which the user query belongs to
The categories are the headings in the extracted pdf contents
intents are :- balance sheets, profit loss statements and cash flow statements, choose other pdf, by default the current pdf is chosen
'''

'''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    FUNCTIONS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''



def get_categories():
    categories=["Business","Risk Factors","Unresolved Staff Comments","Properties","Legal Proceedings","Mine Safety Disclosures","Market For Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities","Selected Financial Data","Management’s Discussion and Analysis of Financial Condition and Results of Operations","Quantitative and Qualitative Disclosures About Market Risk","Changes in and Disagreements with Accountants on Accounting and Financial Disclosure","Controls and Procedures","Other Information","Disclosure Regarding Foreign Jurisdictions that Prevent Inspections","Directors, Executive Officers and Corporate Governance","Executive Compensation","Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters","Certain Relationships and Related Transactions, and Director Independence","Principal Accountant Fees and Services","Exhibits and Financial Statement Schedules","Form 10-K Summary","Signatures"]
    #print(len(categories))
    return categories


#1.
def determine_category(user_query):
    #get_categories()
    #preprocess the text
    list_predict=[]
    #preprocessed_sentence=preprocess_user_query(user_query.strip())
    print(user_query)
    list_predict.append(user_query)

    #feed it to the model and determine the category
    pipeline=joblib.load('../models/tfidf_category_model.pkl')
    predicted_label_code = pipeline.predict(list_predict)
    #print(predicted_label_code[0])

    predict_category=determine_string_predicted_category(int(predicted_label_code[0]))
    if predict_category!=None:
        [main_heading,subheading]=predict_category
        print(f"text belongs to subheading:{subheading} inside the main heading :{main_heading} \n")
        return predict_category
    else:
        print("sorry couldnt determine the category for it")

    #print()

    #extract the text from the 

#2. preprocess the text
def preprocess_user_query(user_query):
    #tokenize it    
    spacy_text= spacy_large_model(user_query)

    preprocessed_tokens=[]

    #remove the stop words
    for token in spacy_text:
        if not token.is_punct and not token.is_stop:
            #lowercase the user query
            #get the lemmas in the user query


            #lemma_of_the_token=token.lemma_
            preprocessed_tokens.append(token.lemma_.lower())
    
    string_representation_of_preprocessed_text= ' '.join(preprocessed_tokens)
    print(string_representation_of_preprocessed_text)
    return string_representation_of_preprocessed_text


def determine_string_predicted_category(predicted_numerical_category):
    for heading_and_subheading, label_code in labels_and_their_numeric_code_dict.labels_and_label_codes_dict.items():
        array= heading_and_subheading.split("__")
        heading=array[0]
        subheading=array[1]

        if predicted_numerical_category==label_code:
            return [heading,subheading]
       
    return None


def generate_response(user_query):
    generator = pipeline('text-generation', model='gpt2-large',max_new_tokens=2000)
    set_seed(48)
    response=generator(user_query,num_return_sequences=1)
    #print(response["generated_text"])
    return response["generated_text"]

def summarize(text,tokenizer,model, maxSummarylength=500):
    # Encode the text and summarize
    inputs = tokenizer.encode(text,
                              return_tensors="pt",
                              max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=maxSummarylength,
                                 min_length=int(maxSummarylength/5),
                                 length_penalty=10.0,
                                 num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print(summary)
    return summary


def get_pdf_text(predicted_main_heading,predicted_subheading):
    if predicted_subheading==None and predicted_main_heading==None:
        return "no text found in pdf for the entered query"
        #extract_entire_text_in_main_heading(main_heading)
    else:
        
        # Open the JSON file
        with open('../../PDFExtraction/pdfs_extracted_file_output/output.json', 'r') as f:
            # Load the JSON data into a dictionary
            data = json.load(f)

        # Now, 'data' contains the content of the JSON file as a dictionary
        #print(data)
        text_from_which_query_needs_to_be_answered=""

        for heading,subheadings_text_array in data.items():
            for subheading_dict in subheadings_text_array:
                subheading=list(subheading_dict.keys())[0]
                if heading.strip()== predicted_main_heading and subheading.strip()==predicted_subheading:
                    text_from_which_query_needs_to_be_answered+=subheading_dict[subheading]
                elif subheading=="all_text" or subheading=="before_first_subheading":
                    text_from_which_query_needs_to_be_answered+=subheading_dict[subheading]
        if len(text_from_which_query_needs_to_be_answered)>0:
            return text_from_which_query_needs_to_be_answered
        else:
            return "no text found in pdf for the entered query"

def split_text_into_pieces(text,tokenizer,
                           max_tokens=900,
                           overlapPercent=10):
    # Tokenize the text
    tokens = tokenizer.tokenize(text)

    # Calculate the overlap in tokens
    overlap_tokens = int(max_tokens * overlapPercent / 100)

    # Split the tokens into chunks of size
    # max_tokens with overlap
    pieces = [tokens[i:i + max_tokens]
              for i in range(0, len(tokens),
                             max_tokens - overlap_tokens)]

    # Convert the token pieces back into text
    text_pieces = [tokenizer.decode(
        tokenizer.convert_tokens_to_ids(piece),
        skip_special_tokens=True) for piece in pieces]

    return text_pieces


def recursive_summarize(text, tokenizer,model,max_length=200, recursionLevel=0):
    recursionLevel=recursionLevel+1
    print("######### Recursion level: ",
          recursionLevel,"\n\n######### ")
    tokens = tokenizer.tokenize(text)
    expectedCountOfChunks = len(tokens)/max_length
    max_length=int(len(tokens)/expectedCountOfChunks)+2

    print(f"Max length is:{max_length}")
    print(f" expected count of chunks is:{expectedCountOfChunks}")

    # Break the text into pieces of max_length
    pieces = split_text_into_pieces(text,tokenizer, max_tokens=max_length)

    print("Number of pieces: ", len(pieces))
    # Summarize each piece
    summaries=[]
    k=0
    for k in range(0, len(pieces)):
        piece=pieces[k]
        print("****************************************************")
        print("Piece:",(k+1)," out of ", len(pieces), "pieces")
        print(piece, "\n")
        summary =summarize(piece, tokenizer,model,maxSummarylength=max_length+1)
        print("SUMNMARY: ", summary)
        summaries.append(summary)
        print("****************************************************")

    concatenated_summary = ' '.join(summaries)

    tokens = tokenizer.tokenize(concatenated_summary)

    if len(tokens) > max_length:
        # If the concatenated_summary is too long, repeat the process
        print("############# GOING RECURSIVE ##############")
        return recursive_summarize(concatenated_summary,
                                   max_length=max_length,
                                   recursionLevel=recursionLevel)
    else:
      # Concatenate the summaries and summarize again
        final_summary=concatenated_summary
        if len(pieces)>1:
            final_summary = summarize(concatenated_summary,
                                  maxSummarylength=max_length)
        return final_summary
                    

'''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    ACTUAL IMPLEMENTATION
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''


spacy_large_model=spacy.load("en_core_web_lg")
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
model = GPT2LMHeadModel.from_pretrained('gpt2-large')

sample_user_queries_list = [
    "What are the revenue sources for PDF Solutions?",
    "Where is PDF Solutions headquartered?",
    "Who are the customers of PDF Solutions?",
    "What benefits do foundry customers derive from PDF Solutions' solutions?",
    "How do equipment manufacturers and factories use PDF Solutions' products?",
    "What is the mission of PDF Solutions?",
    "How does PDF Solutions offer a common platform for a broad group of customers?",
    "What strategic partnership did PDF Solutions enter into in July 2020?",
    "What is the significance of the acquisition of Cimetrix Incorporated by PDF Solutions?",
    "How does PDF Solutions create differentiated data sources?",
    "With whom did PDF Solutions announce a collaboration in December 2021?",
    "What is the brief history of company?",
    "What factors fuel the economic growth of the semiconductor industry?",
    "How does success for every semiconductor company depend on fast product yield ramp?",
    "What technologies or capabilities are highly sought after in the semiconductor industry?",
    "How does PDF Solutions protect its intellectual property?",
    "What is the significance of patent laws to PDF Solutions?",
    "What are some of the trademarks registered by PDF Solutions?",
    "How does PDF Solutions limit access to and distribution of its proprietary information?",
    "What is the significance of the accumulation of a vast library of physical IP by PDF Solutions?"
]



#predict the category
for user_query in sample_user_queries_list:
    predicted_category=determine_category(user_query)
    
    if predicted_category!=None:
        [main_heading,subheading]=predicted_category
    else:
        main_heading=subheading=None

    #go to the category and extract the text
    pdf_text= get_pdf_text(main_heading,subheading)

    #form the answer to the user query
    if pdf_text!="no text found in pdf for the entered query":
        #generated_response=generate_response(user_query+" strictly use the below text to answer the question "+pdf_text)
        #summarize(user_query,pdf_text,tokenizer,model)
        recursive_summarize("question:"+ user_query +" strictly use the below text to answer the question: "+
                              pdf_text, tokenizer,model)
    else:
        generate_response="no text found in pdf for the entered query"
    

    #return the answer
    print(generate_response)



    



