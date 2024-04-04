import fitz
import re
import spacy
import os
nlp=spacy.load("en_core_web_sm")

''' 
######################################################################################################################################################################
                                                                                    PREPROCESSING FUNCTIONS
######################################################################################################################################################################

'''


#1.get the table of contents page number  
def get_table_of_contents_page_number(doc):
    
    print(f"total pages :{doc.page_count}")
    toc_page_num_array=[]#represents the table of contents(TOC) page number
    
    for i in range (0,doc.page_count):
        current_page= doc.load_page(i)
        
        extracted_text=current_page.get_text()
        #print(f"current page number:{i}")
        #print(extracted_text)
    
        regex_table_of_content=r'(table\s+of\s+contents)|(contents)|(in\s+this\s+)/gi'

        #There might be multiple table of contents as well in the pdf, so consider all of them to create one single dictionary
        if re.findall(regex_table_of_content,extracted_text.lower()):
            print(f"table of contents on page {i}")
            toc_page_num_array.append(i)
    return toc_page_num_array


    
#2. Get the Dictonary with the headings of the Table Of Contents
def get_toc_dict_for_pdf(toc_page_num_array,doc):

    #a list of created toc dictionaries after all the preprocessing for multiple TOCs in a single pdf
    toc_dictionaries_array=[]

    for each_page_number in toc_page_num_array:
        
        toc_page_text= doc.load_page(each_page_number).get_text()
        #print(toc_page_text)
        
        # a dict to hold the headings and their page number
        dict_headings_for_current_pdf={}
    
        regex_for_presence_of_digits=r'(\d+)'
    
        preprocessed_text_1=preprocess_step_1(toc_page_text)
        preprocessed_text_array_2= preprocess_step_2(preprocessed_text_1,regex_for_presence_of_digits) 
        preprocessed_text_array_3= preprocess_step_3(preprocessed_text_array_2,regex_for_presence_of_digits)
        toc_order=encode_the_pattern_and_determine_the_toc_order(preprocessed_text_array_3)
    
        if(toc_order!=None):
            (toc_pattern,actual_order_array)=toc_order
            dict_headings_for_current_pdf=create_the_toc_dictionary(actual_order_array,preprocessed_text_array_3,toc_pattern)
    
            #add the dictonary to all dictonaries list
            toc_dictionaries_array.append(dict_headings_for_current_pdf)

    
    if(len(toc_dictionaries_array)>0):
        return toc_dictionaries_array
    else:
        return None
        '''
        regex_for_heading_and_its_page_num=r'^([^\.]+)([^a-zA-Z\d]+)([\d\s]+)$'
        checking_regex= re.match(regex_for_heading_and_its_page_num, toc_page_text)
        print(type(checking_regex))
        
        if checking_regex:
            print(f"heading and its page number is present")
        
        else:
            print(f"no headings present")
        '''

#1. 
def preprocess_step_1(toc_page_text):
    '''In this step the following preprocessing is performed:-
    1. The dots from the headings
    2. The phrases "table of contents, index, page, contents, etc" are removed

    Then the cleaned text is returned
    '''
    
     #split the table of contents page by new line character
    lines_array= toc_page_text.split('\n')
    
    ###################################################################################################
    #clean the contents. like removing the dots from the table of contents,etc.
    #remove the dots from the table of contents sentences eg:heading.................46
    cleaned_table_of_contents=[]
    
    for sentence in lines_array:
        #split each sentence to give words in each sentence
        if sentence.strip().lower() not in ["table of contents","page","index","contents"]:
            inner_split_arr= sentence.split()
            cleaned_sentence_arr=[]
            for word in inner_split_arr:
                if word.strip() !="." and word !=" ":
                    cleaned_sentence_arr.append(word.strip())
        
            print(cleaned_sentence_arr)
            joined_cleaned_sentence= ' '.join(cleaned_sentence_arr)
            if len(cleaned_sentence_arr)>0:
                cleaned_table_of_contents.append(joined_cleaned_sentence)
    
    print()
    #print(cleaned_table_of_contents)  
    return cleaned_table_of_contents
    ###################################################################################################


#2. 
def preprocess_step_2(preprocessed_text_1,regex_for_presence_of_digits):
    '''
    The following preprocessing is performed
    We are trying to find out the sentences which are the table of contents and separate them from any other text present.This is required due to the issue caused by the Abbott pdf.Refer "pdfs" directory to see the pdf

    Steps are:-
    1.check whether there is a digit in the sentence
    2. if yes then consider the sentence
    3. if no then check whether the last sentence contains a digit 
    4. if yes then consider it
    5. if no , then check whether the next sentence contains the digit, if yes then consider it
    '''

    #list store the preprocessed text 
    preprocessed_text_array=[]
    
    

    #iterate over the preprocessed text from step 1
    for index,sentence in enumerate(preprocessed_text_1):
        #if there is a digit in the sentence then consider it
        if re.findall(regex_for_presence_of_digits,sentence):
            preprocessed_text_array.append(sentence)

        #if there is no digit but the previous sentence contains a digit then consider it
        elif re.findall(regex_for_presence_of_digits,preprocessed_text_1[index-1]):
            #print(index)
            #print(f" index is {index} ,current sentence:{sentence} sentence at previous index: {cleaned_table_of_contents[index-1]}")
            preprocessed_text_array.append(sentence)

        #if the next sentence contains a digit then consider it
        elif index < len(preprocessed_text_1)-1:
            if re.findall(regex_for_presence_of_digits,preprocessed_text_1[index+1]):
                preprocessed_text_array.append(sentence)
       
    print()
    print()
    #print(cleaned_split_array)
    return preprocessed_text_array

    
#3.
def preprocess_step_3(preprocessed_text_2,regex_for_presence_of_digits):
    '''
    Here, after getting the sentences that are part of table of contents, we preprocess them in the following ways
    1. For sentences that contain a digit,split them using the digit. This is done to identify whether the digit in the sentence is the page number or is part of the heading
    After splitting them using the digit, these sentences will be analyzed further to determine whether the digit is the page number or not.
    2. Remove any empty strings that are present in them
    '''

    
    preprocessed_text_array=[]
    final_preprocessed_text_array=[]
    
    #1. iterate over 'cleaned_split_array' elements and split the sentences that contain digits to find the pattern
    for index,sentence in enumerate(preprocessed_text_2):
        if re.findall(regex_for_presence_of_digits,sentence):
            split_sentence= re.split(r'^(\s*\d+)|(\d+\s*)$',sentence) #need to test this regex
            #print(split_sentence)
            preprocessed_text_array.extend(split_sentence)
        else:
            preprocessed_text_array.append(sentence)
    print()
    #print(new_cleaned_split_array)

    
    #2. remove any empty strings
    for sentence in preprocessed_text_array:
        if sentence!="" and sentence!=" " and sentence!=None and sentence!=".":
            final_preprocessed_text_array.append(sentence)
    print()
    return final_preprocessed_text_array


#4.
def encode_the_pattern_and_determine_the_toc_order(preprocessed_text_array_3):
    '''
    Here the aim is to find the order in which the heading and the page number are arranged. 
    Possible orders can be :1. Heading......24(page number) or 24....Heading
    Hence to determine this, we encode the string and the digits
    Encoding :-  0=> digit,1=> string
    Then we remove the duplicates by replacing similar consecutive elements with a single value ie. [1,1,1,1,0 ]=>[1,0] (all 1s are replaced with a single one)
    Then to determine the Order, we consider the last two elements in the list.This is considered to be the represent order accurately. This is based on my observation and may not be accurate for all pdfs, but it works for the currently considered pdf.
    
    '''
    #.find the pattern. 0 => digit,1=> word
    toc_pattern=[]
    for sentence in preprocessed_text_array_3:
        if sentence.strip().isdigit():
            toc_pattern.append(0)
        else:
            toc_pattern.append(1)
    print(toc_pattern)
    
    
    cleaned_toc_pattern=[]
    for index, element in enumerate(toc_pattern):
        if index==0:
            cleaned_toc_pattern.append(element)
        elif toc_pattern[index-1]!=element:
            cleaned_toc_pattern.append(element)
    print(cleaned_toc_pattern)
    
    
    #check the ending element in the cleaned toc pattern. This signifies whether the ending element is string or digit and assumption is that it is correct ie. if its a digit here it means that it is a page number in the pdf as well
    #the last pair of elements is the actual order

    if len(cleaned_toc_pattern)>=2:
        actual_order_array=[cleaned_toc_pattern[-2], cleaned_toc_pattern[-1]]
        print(actual_order_array)
        return (toc_pattern,actual_order_array)
    else:
        return None


#5. 
def create_the_toc_dictionary(actual_order_array,preprocessed_text_array_3,toc_pattern):

    '''
    Here we create the dictionary that holds the page number and the heading
    '''
    dict_headings={}
    #create the dictionary
    for index,sentence in enumerate(preprocessed_text_array_3):
        if toc_pattern[index]==actual_order_array[0] and toc_pattern[index+1]==actual_order_array[1]:
            dict_headings[preprocessed_text_array_3[index]]=preprocessed_text_array_3[index+1]
    #all_toc_dicts[pdf]=dict_headings
    print(dict_headings)
    return dict_headings


''' 
######################################################################################################################################################################
                                                                                    ACTUAL IMPLEMENTATION
######################################################################################################################################################################

'''
print(os.getcwd())

directory= os.getcwd()+"/pdfs"
all_pdfs=os.listdir(directory)
print(all_pdfs)
all_toc_dicts={}


#Single PDFs testing
doc=fitz.open(os.path.join(directory,all_pdfs[0]))
#doc= fitz.open("../PDFExtraction/pdfs/AnnualReport1.pdf")
#doc= fitz.open("../PDFExtraction/pdfs/abbott_2023_annual_report.pdf")
#for testing, it is a dict of all pdfs and their analyzed table of contents which is in a dict
#doc=fitz.open("../PDFExtraction/pdfs/coca_cola_ar_2023.pdf")
toc_page_num=get_table_of_contents_page_number(doc)
dict_for_current_pdf=get_toc_dict_for_pdf(toc_page_num,doc)

if(dict_for_current_pdf !=None):
    print("DICTIONARY FOR CURRENT PDF IS\n")
    print(dict_for_current_pdf)


'''
#All PDFs testing
for pdf in all_pdfs:
    pdf_file_path=os.path.join(directory, pdf)
    print(pdf)
    doc=fitz.open(pdf_file_path)
    toc_page_num=get_table_of_contents_page_number(doc)
    dict_for_current_pdf=get_toc_dict_for_pdf(toc_page_num,doc)

    if(dict_for_current_pdf !=None):
        #add the dictionary to all dictonary list
        all_toc_dicts[pdf]=dict_for_current_pdf
    

print(all_toc_dicts)
'''


'''
ALL PDFS THAT ARE TESTED AND THEIR ORDER
[0:'AnnualReport1.pdf(working)', 1:'abbott_2023_annual_report.pdf(working)', '2:wipo_pub_rn2021_18e.pdf', 3:'birac_annual_report_2012.pdf', 
4:'nestle_annual_report_2023.pdf', 5:'colgate_annual_report_2023.pdf(working)', 6:'Netflix_annual_report_2023.pdf', 7:'netflix_ar_2022.pdf', 
8:'netflix_ar_2003.pdf', 9:'netflix_ar_2004.pdf', 10:'netflix_ar_2005.pdf', 11:'netflix_ar_2021.pdf', 12:'netflix_ar_2006.pdf', 
13:'netflix_ar_2019.pdf', 14:'meta_ar_2021.pdf', 15:'meta_ar_2020.pdf', 16:'meta_ar_2019.pdf', 17:'meta_ar_2012.pdf', 18:'pfizer_ar_2023.pdf(contains roman numerals for page numbers hence there's an issue', 
19:'tata_group_ar_2024.pdf(wrong pattern detection)', 20:'tata_motors_ar_2022.pdf', 21:'coca_cola_ar_2023.pdf(working)', 22:'apple_ar_2023.pdf(working)']


'''
