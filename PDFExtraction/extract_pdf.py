import fitz
import re
import spacy
import os
from pprint import pprint 
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


#3. 
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
        
            #print(cleaned_sentence_arr)
            joined_cleaned_sentence= ' '.join(cleaned_sentence_arr)
            if len(cleaned_sentence_arr)>0:
                cleaned_table_of_contents.append(joined_cleaned_sentence)
    
    print()
    #print(cleaned_table_of_contents)  
    return cleaned_table_of_contents
    ###################################################################################################


#4. 
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

    
#5.
def preprocess_step_3(preprocessed_text_2,regex_for_presence_of_digits):
    '''
    Here, after getting the sentences that are part of table of contents, we preprocess them in the following ways
    1. For sentences that contain a digit,split them using the digit. This is done to identify whether the digit in the sentence is the page number or is part of the heading
    After splitting them using the digit, these sentences will be analyzed further to determine whether the digit is the page number or not.
    2. Remove any empty strings that are present in them
    '''

    preprocessed_text_array=[]
    final_preprocessed_text_array=[]
    temp_preprocessed_text_array=[]
    temp_preprocessed_text_array_2=[]
    
    #1. iterate over 'cleaned_split_array' elements and split the sentences that contain digits to find the pattern
    for index,sentence in enumerate(preprocessed_text_2):
        if re.findall(regex_for_presence_of_digits,sentence):
            split_sentence= re.split(r'^(\s*\d+)|(\d+\s*)$',sentence) #need to test this regex
            #print(split_sentence)
            preprocessed_text_array.extend(split_sentence)
        else:
            preprocessed_text_array.append(sentence)

    #print(new_cleaned_split_array)

    
    #2. remove any empty strings
    for sentence in preprocessed_text_array:
        if sentence!="" and sentence!=" " and sentence!=None and sentence!=".":
            final_preprocessed_text_array.append(sentence)
    
    #3. if there are consecutive strings then merge them into one.

    temp_preprocessed_text_array.extend(final_preprocessed_text_array)

    while(check_whether_consecutive_sentences_are_present(temp_preprocessed_text_array)):
        merged_array= merge_consecutive_sentences_into_one(temp_preprocessed_text_array)
        temp_preprocessed_text_array.clear()
        temp_preprocessed_text_array.extend(merged_array)
    final_preprocessed_text_array.clear()
    final_preprocessed_text_array.extend(temp_preprocessed_text_array)

    #4. Extract only the heading and remove all the words like "Part, Item,etc"
    temp_preprocessed_text_array_2=extract_only_valid_words_from_headings(final_preprocessed_text_array)
    final_preprocessed_text_array.clear()
    final_preprocessed_text_array.extend(temp_preprocessed_text_array_2)
    print(f"preprocessed output stage 3 is:{final_preprocessed_text_array}")

    return final_preprocessed_text_array

#6.
def extract_only_valid_words_from_headings(preprocessed_text_array_3):
    final_preprocessed_text_array=[]
    for sentence in preprocessed_text_array_3:
        
        regex_to_remove_unnecessary_words=r'^([\w\s]+[\da-zA-Z]+\.)'

        part_of_sentence_to_remove=re.findall(regex_to_remove_unnecessary_words,sentence)
        split_sentence=re.split(regex_to_remove_unnecessary_words,sentence)

        for part in split_sentence:
            if part!="" and not re.findall(regex_to_remove_unnecessary_words,part):
                final_preprocessed_text_array.append(part.strip())
    return final_preprocessed_text_array
        
        



#6.
def check_whether_consecutive_sentences_are_present(preproccessed_text_array_3):
    value_to_return=False
    for index,sentences in enumerate(preproccessed_text_array_3):
        if index< len(preproccessed_text_array_3)-1:
            if not preproccessed_text_array_3[index].isdigit() and not preproccessed_text_array_3[index+1].isdigit():
                value_to_return=True
                break
            else:
                value_to_return= False
    return value_to_return

#7.
def merge_consecutive_sentences_into_one(preprocessed_text_array_3):
    temp_preprocessed_text_array=[]

    index_to_skip=[]
    for index,sentence in enumerate(preprocessed_text_array_3):
        #check until 2nd last index else index out of range error will be thrown because we are using (index+1)
        if index <len(preprocessed_text_array_3)-1:
            
            #if this index has already been merged
            if index in index_to_skip:
                continue
            #consecutive strings are present
            elif not preprocessed_text_array_3[index].isdigit() and not preprocessed_text_array_3[index+1].isdigit():
                #print(f"consecutive strings are present . string 1 :{final_preprocessed_text_array[index]}, String 2:{final_preprocessed_text_array[index+1]}")
                temp_preprocessed_text_array.append(preprocessed_text_array_3[index]+ " "+ preprocessed_text_array_3[index+1])
                index_to_skip.append(index+1)
            elif not preprocessed_text_array_3[index].isdigit() and not preprocessed_text_array_3[index-1].isdigit():
                previous_string_is=temp_preprocessed_text_array[len(temp_preprocessed_text_array)-1]
                temp_preprocessed_text_array[len(temp_preprocessed_text_array)-1]= previous_string_is + " " +preprocessed_text_array_3[index]
            else:
                temp_preprocessed_text_array.append(sentence)

        #last index
        elif index== len(preprocessed_text_array_3)-1:
            if not preprocessed_text_array_3[index].isdigit() and not preprocessed_text_array_3[index-1].isdigit():
                previous_string_is=temp_preprocessed_text_array[len(temp_preprocessed_text_array)-1]
                temp_preprocessed_text_array[len(temp_preprocessed_text_array)-1]= previous_string_is + " " +preprocessed_text_array_3[index]
            else:
                temp_preprocessed_text_array.append(sentence)

    return temp_preprocessed_text_array


#8.
def encode_the_pattern(preprocessed_text_array_3):
    #.find the pattern. 0 => digit,1=> word
    pattern=[]
    for index, sentence in enumerate(preprocessed_text_array_3):
        if sentence.isdigit():
            pattern.append(0)
        else:
            pattern.append(1)
    return pattern


#9.
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
    '''
    toc_pattern=[]
    for sentence in preprocessed_text_array_3:
        if sentence.strip().isdigit():
            toc_pattern.append(0)
        else:
            toc_pattern.append(1)
    print(f"TOC pattern is :{toc_pattern}")
    
    
    cleaned_toc_pattern=[]
    for index, element in enumerate(toc_pattern):
        if index==0:
            cleaned_toc_pattern.append(element)
        elif toc_pattern[index-1]!=element:
            cleaned_toc_pattern.append(element)
    print(f"cleaned TOC pattern is:{cleaned_toc_pattern}")
    '''
    encoded_pattern= encode_the_pattern(preprocessed_text_array_3)
    #print(f"TOC pattern is:{encoded_pattern}, len is :{len(encoded_pattern)}, len of text array is:{len(preprocessed_text_array_3)}")
    
    #check the ending element in the cleaned toc pattern. This signifies whether the ending element is string or digit and assumption is that it is correct ie. if its a digit here it means that it is a page number in the pdf as well
    #the last pair of elements is the actual order

    if len(encoded_pattern)>=2:
        actual_order_array=[encoded_pattern[-2], encoded_pattern[-1]]
        #print(actual_order_array)
        return (encoded_pattern,actual_order_array)
    else:
        return None


#10. 
def create_the_toc_dictionary(actual_order_array,preprocessed_text_array_3,toc_pattern):

    '''
    Here we create the dictionary that holds the page number and the heading
    '''
    dict_headings={}
    #create the dictionary
    for index,sentence in enumerate(preprocessed_text_array_3):
        if(index <len(preprocessed_text_array_3)-1):

            #print(f"toc_pattern at current index is:{toc_pattern[index]} and at next index is :{toc_pattern[index+1]}")
        
            if toc_pattern[index]==actual_order_array[0] and toc_pattern[index+1]==actual_order_array[1]:
                #add the TOC heading as the key and the heading as the value
                if actual_order_array[0]==0:
                    dict_headings[preprocessed_text_array_3[index+1]]=preprocessed_text_array_3[index]
                else:
                    
                    dict_headings[preprocessed_text_array_3[index]]=preprocessed_text_array_3[index+1]

    #all_toc_dicts[pdf]=dict_headings
    #print(dict_headings)
    return dict_headings

#11.calculate the offset (pdf page number on which topic is present versus the page number given in the TOC
def calculate_offset(toc_dict_array, doc,toc_page_num):
   #go through each page and then check for the word on that page
   for toc_dict in toc_dict_array:
    all_headings_status_dict={}

    #iterate over the dictionary
    for heading,page_num in toc_dict.items():
        #print(page_num, heading)
        all_headings_status_dict[heading]={"toc_page_num":page_num,"pdf_page_num":[],"offset":0}
        regex_for_current_heading=r''+heading.strip()+'\s*(?![\w\d])'
       # print(f"regex is :{regex_for_current_heading}")
            
        for each_page in range(0,doc.page_count):
            #print(f"toc page num is {toc_page_num_array} and each page is:{each_page}")
            
            if each_page not in toc_page_num_array:
                #print("each page is not equal to toc page num")
                current_page= doc.load_page(each_page)
                current_page_text= current_page.get_text()
                if re.findall(regex_for_current_heading,current_page_text):
                    all_headings_status_dict[heading]["pdf_page_num"].append(each_page)
        #print()
    #print()
    #pprint(all_headings_status_dict)
    #print()

    #calculate the offset
    for heading,page_numbers in all_headings_status_dict.items():
        toc_page_num= page_numbers["toc_page_num"]
        pdf_page_num= page_numbers["pdf_page_num"]
        offset=page_numbers["offset"]
        #if there are multiple pages on which the heading is present, then loop through each page and select the closet one to the page number present in the Table of Contents
        if len(pdf_page_num)>1:
            difference= -1
            selected_pdf_page_num= pdf_page_num[0]
            for each_pdf_page_num in pdf_page_num:
                if int(toc_page_num)> int(each_pdf_page_num):
                    continue
                else:
                    current_difference= int(toc_page_num)- int(each_pdf_page_num)
                    if current_difference >difference:
                        selected_pdf_page_num=each_pdf_page_num
                        difference= current_difference

                    
            #print(f"selected pdf page num is:{selected_pdf_page_num}")
            page_numbers["pdf_page_num"]=[selected_pdf_page_num]

            #calculate the offset and store it
            page_numbers["offset"]=int(selected_pdf_page_num)-int(toc_page_num)

        elif len(pdf_page_num)==0:
            continue
        else:
            offset=int(pdf_page_num[0])-int(toc_page_num)
            #print(f"when only one pdf page num is present, offset is {offset}")
            page_numbers["offset"]=offset

    #print(all_headings_status_dict)
    fixed_offset_dict= fix_offset_issues(all_headings_status_dict)

    #print(f"fixed offset issues {fixed_offset_dict}")
    all_headings_status_dict= fixed_offset_dict
    #print()
    #print(f"after fixing the offsets")
    #print(all_headings_status_dict)   
    return all_headings_status_dict 

#12.
def fix_offset_issues(all_headings_status_dict):
    #find the offset that appears most often
    offset_count_dict={}
    for headings,page_numbers in all_headings_status_dict.items():
        offset=page_numbers["offset"]

        if offset in offset_count_dict.keys():
            offset_count_dict[offset]+=1
        else:
            offset_count_dict[offset]=1
    
    offset_with_max_count=list(offset_count_dict.keys())[0]

    max_count=offset_count_dict[offset_with_max_count]

    #apply the offset that apppears most often
    for offset, count in offset_count_dict.items():
        if count> max_count:
            offset_with_max_count= count
            offset_with_max_count=offset
    
    for headings, page_numbers in all_headings_status_dict.items():
        page_numbers["offset"]=offset_with_max_count

    #when the pdf_page_num_array length is 0, and if toc_page_num and offset is present then fill the pdf_page_num array
    for heading, page_numbers in all_headings_status_dict.items():
        if len(page_numbers["pdf_page_num"])<1:
            all_headings_status_dict[heading]["pdf_page_num"].append(int(page_numbers["toc_page_num"])+int(page_numbers["offset"]))
    
    
    return all_headings_status_dict
    
#13.
def extract_subheadings_and_their_text(doc,all_headings_status_dict):
    modified_all_headings_status_dict= determine_starting_and_ending_page_numbers_for_each_heading(doc, all_headings_status_dict)  

    #now extract subheading
    for heading, page_numbers in modified_all_headings_status_dict.items():
        #["Business","Risk Factors","Unresolved Staff Comments","Properties","Legal Proceedings","Mine Safety Disclosures","Market For Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities","Selected Financial Data","Management’s Discussion and Analysis of Financial Condition and Results of Operations","Quantitative and Qualitative Disclosures About Market Risk","Financial Statements and Supplementary Data","Changes in and Disagreements with Accountants on Accounting and Financial Disclosure","Controls and Procedures","Other Information","Disclosure Regarding Foreign Jurisdictions that Prevent Inspections","Directors, Executive Officers and Corporate Governance","Executive Compensation","Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters","Certain Relationships and Related Transactions, and Director Independence","Principal Accountant Fees and Services","Exhibits and Financial Statement Schedules","Form 10-K Summary"]
        #for testing purposes
        if heading in ["Business","Risk Factors","Unresolved Staff Comments","Properties","Legal Proceedings","Mine Safety Disclosures","Market For Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities","Selected Financial Data","Management’s Discussion and Analysis of Financial Condition and Results of Operations","Quantitative and Qualitative Disclosures About Market Risk","Changes in and Disagreements with Accountants on Accounting and Financial Disclosure","Controls and Procedures","Other Information","Disclosure Regarding Foreign Jurisdictions that Prevent Inspections","Directors, Executive Officers and Corporate Governance","Executive Compensation","Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters","Certain Relationships and Related Transactions, and Director Independence","Principal Accountant Fees and Services","Exhibits and Financial Statement Schedules","Form 10-K Summary"]:
            continue
        
        if(len(page_numbers["pdf_page_num"])>0):
            #print(f"heading:{headings}, starting page number:{page_numbers["starting_page_num"]}, ending page number:{page_numbers["ending_page_num"]}")
            #text_within_subheading=extract_text(doc,page_numbers["starting_page_num"], page_numbers["ending_page_num"])
            #print(f"heading:{headings}, text:{text_within_subheading}")

            #print(f"\n Current heading is :{heading}\n")
            subheadings_within_heading_dict=extract_subheadings(doc, page_numbers["starting_page_num"], page_numbers["ending_page_num"])
            #extract_subheadings(heading,blocks_of_text_within_subheading)
            #pprint(subheadings_within_heading_dict)

            filter_1_possible_subheadings_dict={}
            
            for page_number in list(subheadings_within_heading_dict.keys()):
                filter_1_possible_subheadings_dict[page_number]=[]
                filter_1_possible_subheadings_dict[page_number].extend(remove_toc_headings_from_subheadings(heading,subheadings_within_heading_dict[page_number]))
                
            #print(filter_1_possible_subheadings_dict)
            extract_text_within_subheading(doc,filter_1_possible_subheadings_dict,heading,page_numbers["starting_page_num"])

            #TODO:remove this later
            break

#14.
def determine_starting_and_ending_page_numbers_for_each_heading(doc, all_headings_status_dict):

    modified_all_headings_status_dict= all_headings_status_dict
    #pprint(all_headings_status_dict)
    #go to the page with the headings and extract the text until the next heading
    for index,(headings,page_numbers) in enumerate(all_headings_status_dict.items()):

        #when we reach to the last ending, there is no heading after it hence dont increment the index
        if index < len(list(all_headings_status_dict.keys()))-1:
            next_heading_index=index+1
            next_heading=list(all_headings_status_dict.keys())[next_heading_index]
            current_heading=list(all_headings_status_dict.keys())[index]

            if int(all_headings_status_dict[next_heading]["toc_page_num"]) == int(all_headings_status_dict[current_heading]["toc_page_num"]):
                #that current heading and next heading is on the same page
                #print("\nNext heading and current heading are on the same page\n")
                text_within_heading_starts_at_page= int(page_numbers["toc_page_num"])+ int(page_numbers["offset"])
                text_within_heading_ends_at_page=text_within_heading_starts_at_page
                modified_all_headings_status_dict[headings]["starting_page_num"]=int(text_within_heading_starts_at_page)
                modified_all_headings_status_dict[headings]["ending_page_num"]=int(text_within_heading_ends_at_page)
            
            elif int(all_headings_status_dict[next_heading]["toc_page_num"]) > int(all_headings_status_dict[current_heading]["toc_page_num"]):
                #assumption that each new heading starts at a new page
                text_within_heading_starts_at_page= int(page_numbers["toc_page_num"])+ int(page_numbers["offset"])
                text_within_heading_ends_at_page=int(all_headings_status_dict[next_heading]["toc_page_num"])+ int(page_numbers["offset"])-1
                modified_all_headings_status_dict[headings]["starting_page_num"]=int(text_within_heading_starts_at_page)
                modified_all_headings_status_dict[headings]["ending_page_num"]=int(text_within_heading_ends_at_page)

                #print(f"heading is :{headings}. It starts at page:{text_within_heading_starts_at_page} and ends at Page:{text_within_heading_ends_at_page}")

        else:
            next_heading_index=None
            text_within_heading_starts_at_page= int(page_numbers["toc_page_num"])+ int(page_numbers["offset"])
            text_within_heading_ends_at_page=doc.page_count
            #print(f"heading is :{headings}. It starts at page:{text_within_heading_starts_at_page} and ends at Page:{text_within_heading_ends_at_page}")

            modified_all_headings_status_dict[headings]["starting_page_num"]=int(text_within_heading_starts_at_page)

            modified_all_headings_status_dict[headings]["ending_page_num"]=int(text_within_heading_ends_at_page)
    #print(f"\n added offset, starting page numbers and ending page numbers\n")
    #pprint(modified_all_headings_status_dict)
    return modified_all_headings_status_dict


#15.
def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)


#16.
def extract_text(doc,starting_page_num,ending_page_num):
    all_pages_extracted_text=""
    #print(f"starting page number:{starting_page_num}, ending page number:{ending_page_num}")
    for page_num in range(starting_page_num, ending_page_num):
        #print(page_num)
        current_page=doc.load_page(page_num)
        current_page_extracted_text=current_page.get_text()
        all_pages_extracted_text+=current_page_extracted_text
        
    return all_pages_extracted_text


#17.
def extract_subheadings(doc,starting_page_num,ending_page_num):

    #a dictionary that holds the page number and its blocks and the font properties in that block
    #page_and_its_text_block_dict={}

    #possible subheadings in the heading
    possible_subheadings_array={}
    
    #iterate over each page 
    for each_page_num in range(starting_page_num,ending_page_num+1):
        #print()
        #print(f"current page number within the heading is:{each_page_num}\n")

        #the index of the last page is one less than the page count and hence gives an issue when loading the page. Since the last page of the pdf is already parsed in the previous iteration, current iteration need not be carried out, hence break is used 
        if int(each_page_num)==int(doc.page_count):
            break
        current_page=doc.load_page(each_page_num)

        possible_subheadings_array[each_page_num]=[]

        ###################Analyzing text#####################################

        #get the text on the page as a dictionary and then extract all the blocks from it (blocks are very similar to paragraphs)
        blocks = current_page.get_text("dict", flags=11)["blocks"]
        #pprint(f"Blocks on the Current page is\n")
        #pprint(f"{blocks}")

        #a dictionary that holds the blocks and its font properties for each page
        #each_page_dict={}
        
        #to keep track of the number of blocks in the page
        #index=1
        
        # iterate through the text blocks
        for b in blocks: 

            #a dictionary the font properties of each block
            #each_block_dict={"font_properties":[]}
            #each_block_dict={}
            #subheadings_in_a_block=[]

            #create a key for each block
            #block_key_name="block"+str(index)
            #block_text=""
            
            #print(f"\nNEW BLOCK\nnumber of lines in the block are:{len(b["lines"])}\n")
            #print("the text in the block is\n")
            #to avoid table's column heading being part of the subheading, just check the number of lines in the block. If the number of lines in the block are greater than 2, then it not a subheading block
            if len(b["lines"])<=2:
                # iterate through the text lines in each block
                for l in b["lines"]: 
                    #print(f"the lines are {b["lines"]}")

                    # iterate through the text spans
                    for s in l["spans"]:    

                        font= s["font"]
                        flags=flags_decomposer(s["flags"])
                        #print(font, flags)
                        font_size=s["size"]
                        #font_color=s["color"]
                        text=s["text"]
                        #print(text)
                        #block_text+=text

                        #print(f"\ncurrent span text is {text}hello and font style is {font} and flags are {flags}\n")
                        temp_subheadings= find_possible_subheadings(text.strip(),font,flags)
                        

                        if temp_subheadings!=None:
                            #temp_subheadings.append("Business") #just for testing
                            possible_subheadings_array[each_page_num].extend(temp_subheadings)

                        #keep count of the  the combination of font, its flags and font size in the block
                        '''if (font,flags,font_size) not in list(each_block_dict.keys()):
                            each_block_dict[(font,flags,font_size)]=1
                            #each_block_dict["font_properties"].append({"font":font,"flags":flags, "font_size":font_size, "count":1})
                        else:
                            each_block_dict[(font,flags,font_size)]+=1
                            #each_block_dict["font_properties"]
                        '''
                    
                #after the traversing the whole block , add the block and its font contents dictionary to the page dictionary
                #each_block_dict["text"]=block_text
                #print(f"text in each block is\n {block_text}\n")
                #each_block_dict["no_of_lines"]=len(b["lines"])
                #each_page_dict[block_key_name]=each_block_dict
                
                #index+=1
            

                #after traversing the whole page, add the page and its block contents to the primary dictionary
                #page_and_its_text_block_dict[each_page_num]=each_page_dict

                #break
            #else:
                #print("this is not a subheading")
        

    #pprint(page_and_its_text_block_dict)
    #return page_and_its_text_block_dict
    return possible_subheadings_array
    

#18. extract sub-headings from the given dictionary of the text blocks and their text properties
#def extract_subheadings(toc_heading,text_blocks_dict):
    
    #analyze the pattern of the subheadings (subheadings are usually bold or greater in size or both)
    #pattern_of_subheading= analyze_pattern_of_subheading(toc_heading,text_blocks_dict)

    #find the subheadings


#19
def find_possible_subheadings(current_span_text,font, flags):
    '''
    Steps in analyzing are:
    1. check whether the text is the same as the TOC heading, if yes, then don't consider it
    2. check the font sizes of the text.The largest ones are the subheadings usually
    3. check for keyword "bold" in the font and the flags of each block to determine the subheadings
    '''

    '''
    filter_1_blocks_that_might_contain_subheading={}
    regex_for_toc_heading= r''+toc_heading+'(?![\s\w\d])'
            #regex_for_toc_heading= r''+toc_heading

            if re.findall(regex_for_toc_heading, current_block) and no_of_lines_in_block <=2 :
                #print(f"\n this is a toc heading {text_in_block} and number of lines in block is :{no_of_lines_in_block}\n")
                #blocks_that_might_contain_subheading.append()
                continue
            else:
                filter_1_blocks_that_might_contain_subheading[current_page_number].append(current_block)
                #filter_1_blocks_that_might_contain_subheading["blocks"].append(blocks[block])
    '''

    filter_2_block_that_might_contain_subheading=[]
    all_fonts= font.split(",")
    all_flags=flags.split(",")

    pattern=re.compile(r'italic',re.IGNORECASE)
    for font in all_fonts:
        #print(font)
        if font.strip().lower()=="bold" and not re.findall(pattern,font.strip().lower()) and current_span_text not in filter_2_block_that_might_contain_subheading and not re.findall(r'(?<![\w\d])\s+(?![\w\d])', current_span_text) and current_span_text!="":
            filter_2_block_that_might_contain_subheading.append(current_span_text)
        #else:
            #print(current_span_text, font)

    for flag in all_flags:
        #print(f"\nflag is :{flag} and type is type:{type(flag)}\n")
        if flag.strip().lower()=="bold" and not re.findall(pattern,font.strip().lower()) and current_span_text not in filter_2_block_that_might_contain_subheading and not re.findall(r'(?<![\w\d])\s+(?![\w\d])', current_span_text) and current_span_text!="":
            filter_2_block_that_might_contain_subheading.append(current_span_text)
            
        #else:
            #print(flag,re.findall(pattern,flag.strip().lower()))


    if len(filter_2_block_that_might_contain_subheading)>0:
        #print()
        #print(f"the blocks that might contain the subheading are :\n")
        #pprint(filter_2_block_that_might_contain_subheading)

        return filter_2_block_that_might_contain_subheading
    else:
        return None
    

#20.
def remove_toc_headings_from_subheadings(toc_heading,possible_subheadings_array):

    filtered_subheadings_array=[]
    regex_for_toc_heading= r'(?<=Item\s\w\w\.\s)'+toc_heading+'(?![\s\w\d])'
    another_regex_for_toc_heading=r'(?<=Item\s\w\.\s)'+toc_heading+'(?![\s\w\d])'
    
    #regex_for_toc_heading= r''+toc_heading

    for subheading in possible_subheadings_array:
        if re.findall(regex_for_toc_heading, subheading) or re.findall(another_regex_for_toc_heading,subheading):
            #print(f"\n this is a toc heading {subheading}\n")
            #blocks_that_might_contain_subheading.append()
            continue
        elif "Item" in subheading or "PART" in subheading:
            continue
        else:
            filtered_subheadings_array.append(subheading)
            #filter_1_blocks_that_might_contain_subheading["blocks"].append(blocks[block])
    return filtered_subheadings_array

#21. 
#def analyze_pattern_of_subheading(toc_heading,text_blocks_dict):
    '''
    Steps in analyzing are:
    1. check whether the text is the same as the TOC heading, if yes, then don't consider it
    2. check the font sizes of the text.The largest ones are the subheadings usually
    3. check for keyword "bold" in the font and the flags of each block to determine the subheadings
    '''


    '''
    filter_1_blocks_that_might_contain_subheading={}
    #print(f"{text_blocks_dict}")
    for page_number, blocks in text_blocks_dict.items():
        #print()
        #print(page_number, blocks)
        filter_1_blocks_that_might_contain_subheading[page_number]=[]

        #step 1:
        #print(blocks.keys())
        for block in list(blocks.keys()):
            #print()
            #print(blocks[block]["text"])
            text_in_block= blocks[block]["text"].strip()
            no_of_lines_in_block=blocks[block]["no_of_lines"]
            #print(text_in_block)

            regex_for_toc_heading= r''+toc_heading+'(?![\s\w\d])'
            #regex_for_toc_heading= r''+toc_heading

            if re.findall(regex_for_toc_heading, text_in_block) and no_of_lines_in_block <=2 :
                #print(f"\n this is a toc heading {text_in_block} and number of lines in block is :{no_of_lines_in_block}\n")
                #blocks_that_might_contain_subheading.append()
                continue
            else:
                filter_1_blocks_that_might_contain_subheading[page_number].append(blocks[block])
                #filter_1_blocks_that_might_contain_subheading["blocks"].append(blocks[block])

            
        #step 2:
        font_properties_of_block=[]
        filter_2_block_that_might_contain_subheading=[]
        for page_number,blocks in filter_1_blocks_that_might_contain_subheading.items():
            #print(page_number, blocks)
            for block in blocks:
                all_keys_in_block=list(block.keys())
                for key,count in block.items():
                    if key not in ["text","no_of_lines"]:
                        font_properties_of_block.append({key:count})
                        (font, flags, font_size)=key
                        all_fonts= font.split(",")
                        all_flags=flags.split(",")

                        for font in all_fonts:
                            #print(font)
                            if font.strip().lower()=="bold" and block not in filter_2_block_that_might_contain_subheading:
                                filter_2_block_that_might_contain_subheading.append(block[])
                        
                        for flag in all_flags:
                            #print(f"\nflag is :{flag} and type is type:{type(flag)}\n")
                            if flag.strip().lower()=="bold" and block not in filter_2_block_that_might_contain_subheading:
                                filter_2_block_that_might_contain_subheading.append(block)



            #font_properties_of_block[]=font_properties_of_block
        #break
        pprint(filter_2_block_that_might_contain_subheading)

        #TODO:Need to rerun the flag decomposer function here, and the lines that are bold add it to the list
    '''


#22
def extract_text_within_subheading(doc,subheading_dict,toc_heading,toc_heading_page_num):

    all_page_numbers_array=list(subheading_dict.keys())
    #print(all_page_numbers_array)

    #remove all the keys whose values are empty
    temp_page_array=[]
    for page_number in all_page_numbers_array:
        #print(len(subheading_dict[9]))
        #print(page_number)
        if len(subheading_dict[page_number])>0:
            temp_page_array.append(page_number)
    
    if len(temp_page_array)>0:
        all_page_numbers_array.clear()
        all_page_numbers_array.extend(temp_page_array)

    print(subheading_dict)
    print(all_page_numbers_array)

    #text between the main heading and the first subheading
    regex_for_toc_heading= r''+toc_heading+'(?![\s\w\d])'
    #another_regex_for_toc_heading=r'(?<=Item\s\w\.\s)'+toc_heading+'(?![\s\w\d])'

    first_subheading=subheading_dict[all_page_numbers_array[0]][0]
    first_subheading_page_num=all_page_numbers_array[0]
    #print(first_subheading)
    text_between_main_heading_and_first_subheading=""
    
    #On a page, it might be that there are subheadings for the previous heading. This text shouldn't be recorded in the current heading. Hence this flag is used to tell the program to start recording text only after the current heading is found
    main_heading_found=False
    start_recording_text=False
    all_blocks=[]
    for page_number in range(toc_heading_page_num, first_subheading_page_num+1):
        toc_heading_page= doc.load_page(page_number)
        blocks=toc_heading_page.get_text("dict",flags=11)["blocks"]
        all_blocks.extend(blocks)

    for b in all_blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                text=s["text"]
                if re.findall(regex_for_toc_heading,text.strip()):
                    start_recording_text=True
                    main_heading_found=True
                    continue
                if re.findall(r""+first_subheading,text.strip()):
                    start_recording_text=False

                if start_recording_text:
                    text_between_main_heading_and_first_subheading+=text.strip()+" "
    print()       
    print()   
    print(text_between_main_heading_and_first_subheading)


    if main_heading_found:
        #iterate over the array after removing empty values
        for index,page_number in enumerate(all_page_numbers_array):
            #print(page_number)
            #to avoid index out of range, consider only till the second last subheading
            if index < len (all_page_numbers_array)-1:
                #get the array of subheadings on each page number,to determine whether the next subheading is on the same page or the next page
                current_element_in_dict=subheading_dict[page_number]
                next_element_in_dict=subheading_dict[all_page_numbers_array[index+1]]
                
                #print(current_element_in_dict)
                #print(next_element_in_dict)
                
                #check whether the next element is not the empty or the current element is not empty
                #if len(current_element_in_dict)>0 and len(next_element_in_dict)>0:

                #get the current sub-heading and the next subheading
                for index_subheading,subheading in enumerate(current_element_in_dict):
                    current_heading= subheading
                    next_heading_page_number=all_page_numbers_array[index+1]
                    
                    if index_subheading==len(current_element_in_dict)-1:
                        next_heading=next_element_in_dict[0]
                        
                    else:
                        next_heading=current_element_in_dict[index_subheading+1]
                    
                    print(f"current sub-heading is :{current_heading} and next sub-heading is:{ next_heading}\n and next sub-heading page number is :{next_heading_page_number}")

                    #extract text between the subheadings
                    text_between_subheadings=""
                    #current_subheading_page_text_blocks=doc.load_page(page_number).get_text("dict",flags=11)["blocks"]
                    #print(current_subheading_page_text_blocks)
                    text_blocks=[]
                    for page_number_of_contents_within_subheading in range(page_number,next_heading_page_number+1):
                        current_page_blocks=doc.load_page(page_number_of_contents_within_subheading).get_text("dict",flags=11)["blocks"]
                        text_blocks.extend(current_page_blocks)
                    #next_subheading_page_text_blocks=doc.load_page(next_heading_page_number).get_text("dict",flags=11)["blocks"]
                    #print(next_subheading_page_text_blocks)

                    #combined_text_blocks_of_both_pages=current_subheading_page_text_blocks
                    #combined_text_blocks_of_both_pages.extend(next_subheading_page_text_blocks)
                    #print(combined_text_blocks_of_both_pages)

                    start_recording_text=False
                    for b in text_blocks:
                        for l in b["lines"]:
                            for s in l["spans"]:
                                text=s["text"].strip()
                                if re.findall(r""+current_heading,text):
                                    print(f"found the current subheading: {text}")
                                    start_recording_text=True
                                    continue
                                elif re.findall(r""+next_heading,text):
                                    start_recording_text=False

                                if start_recording_text :
                                    text_between_subheadings+=" "+text
                    print()
                    print(text_between_subheadings)
                    print()
                    #break
            #if the heading is of only one page and there subheadings only on that one page
            elif index==0 and len(all_page_numbers_array)-1==0:
                #get the array of subheadings on each page number,to determine whether the next subheading is on the same page or the next page
                current_element_in_dict=subheading_dict[all_page_numbers_array[index]]
                next_element_in_dict=current_element_in_dict

                #get the current sub-heading and the next subheading
                for index_subheading,subheading in enumerate(current_element_in_dict):
                    current_heading= subheading
                    next_heading_page_number=all_page_numbers_array[index]
                    
                    if index_subheading==len(current_element_in_dict)-1:
                        next_heading=next_element_in_dict[0]
                        
                    else:
                        next_heading=current_element_in_dict[index_subheading+1]
                    
                    print(f"current sub-heading is :{current_heading} and next sub-heading is:{ next_heading}\n and next sub-heading page number is :{next_heading_page_number}")

                    #extract text between the subheadings
                    text_between_subheadings=""
                    #current_subheading_page_text_blocks=doc.load_page(page_number).get_text("dict",flags=11)["blocks"]
                    #print(current_subheading_page_text_blocks)
                    text_blocks=[]
                    for page_number_of_contents_within_subheading in range(page_number,next_heading_page_number+1):
                        current_page_blocks=doc.load_page(page_number_of_contents_within_subheading).get_text("dict",flags=11)["blocks"]
                        text_blocks.extend(current_page_blocks)
                    #next_subheading_page_text_blocks=doc.load_page(next_heading_page_number).get_text("dict",flags=11)["blocks"]
                    #print(next_subheading_page_text_blocks)

                    #combined_text_blocks_of_both_pages=current_subheading_page_text_blocks
                    #combined_text_blocks_of_both_pages.extend(next_subheading_page_text_blocks)
                    #print(combined_text_blocks_of_both_pages)

                    start_recording_text=False
                    for b in text_blocks:
                        for l in b["lines"]:
                            for s in l["spans"]:
                                text=s["text"].strip()
                                if re.findall(r""+current_heading,text):
                                    print(f"found the current subheading: {text}")
                                    start_recording_text=True
                                    continue
                                elif re.findall(r""+next_heading,text):
                                    start_recording_text=False

                                if start_recording_text :
                                    text_between_subheadings+=" "+text
                    print()
                    print(text_between_subheadings)
                    print()
                    #break

            #TODO:last subheading for the heading      
            else:
                print("i am here")
        






        
            
'''
######################################################################################################################################################################
                                                                                    ACTUAL IMPLEMENTATION
######################################################################################################################################################################

'''
directory="../PDFExtraction/pdfs"
all_pdfs=os.listdir(directory)
print(all_pdfs)
all_toc_dicts={}


#Single PDFs testing
doc=fitz.open(os.path.join(directory,all_pdfs[0]))
#doc= fitz.open("../PDFExtraction/pdfs/AnnualReport1.pdf")
#doc= fitz.open("../PDFExtraction/pdfs/abbott_2023_annual_report.pdf")
#for testing, it is a dict of all pdfs and their analyzed table of contents which is in a dict
#doc=fitz.open("../PDFExtraction/pdfs/coca_cola_ar_2023.pdf")
toc_page_num_array=get_table_of_contents_page_number(doc)
dict_for_current_pdf=get_toc_dict_for_pdf(toc_page_num_array,doc)

if(dict_for_current_pdf !=None):
    print("DICTIONARY FOR CURRENT PDF IS\n")
    pprint(dict_for_current_pdf)

    #get the pdf page number along with the Table of Contents Page number
    headings_status_dict=calculate_offset(dict_for_current_pdf,doc,toc_page_num_array)

    #go to the pages with the headings and extract subheadings
    extract_subheadings_and_their_text(doc,headings_status_dict)
else:
    print("no table of contents present for the pdf")

#Calculate the offset
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
