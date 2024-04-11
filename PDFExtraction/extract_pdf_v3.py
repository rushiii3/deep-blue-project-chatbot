import PyPDF2
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
# Download NLTK resources if not already downloaded
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

# Function for text preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Join tokens back into a string
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text

# Function to extract headings from preprocessed text
def extract_headings(text):
    headings = []
    for sentence in text.split('\n'):
        if len(sentence) > 0 and sentence.isupper():  # Assuming headings are in all uppercase
            headings.append(sentence.strip())
    return headings

# Function to extract headings recursively from preprocessed text
def extract_headings_recursive(text):
    headings = []
    for sentence in text.split('\n'):
        if len(sentence) > 0 and sentence.isupper():  # Assuming headings are in all uppercase
            headings.append(sentence.strip())
            # Extract subheadings recursively
            subheadings = extract_headings_recursive(sentence)
            if subheadings:
                headings.extend(subheadings)
    return headings

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract useful data from headings
def extract_data_from_headings(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    print(text)
    preprocessed_text = preprocess_text(text)
    headings = extract_headings_recursive(preprocessed_text)
    return headings

# Example usage
pdf_path = os.getcwd()+"/pdfs/AnnualReport1.pdf"
headings = extract_data_from_headings(pdf_path)
print(headings)
