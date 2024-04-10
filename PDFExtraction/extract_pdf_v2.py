import PyPDF2
import os
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text
def preprocess_text(text):
    # Remove newline characters and extra whitespaces
    text = text.replace('\n', ' ').strip()
    # Remove non-breaking spaces
    text = text.replace('\xa0', ' ')
    return text

def extract_financial_figures(text):
    # Define regular expressions to match financial figures
    regex_currency = r'\$\s?\d+(?:,\d+)*(?:\.\d+)?'  # Matches currency amounts ($X,XXX.XX)
    regex_percentage = r'\d+(?:\.\d+)?\s?%'  # Matches percentage values (X.XX%)
    regex_numbers = r'\d+(?:,\d+)*(?:\.\d+)?'  # Matches numbers with optional commas and decimals

    # Find all matches of currency amounts, percentages, and numbers
    currencies = re.findall(regex_currency, text)
    percentages = re.findall(regex_percentage, text)
    numbers = re.findall(regex_numbers, text)

    return currencies, percentages, numbers



directory= os.getcwd()+"/pdfs/AnnualReport1.pdf"
# Example usage:
pdf_path = directory  # Replace 'example.pdf' with the path to your PDF file
pdf_text = extract_text_from_pdf(pdf_path)
# Example usage:
preprocessed_text = preprocess_text(pdf_text)
print(preprocessed_text)

# currencies, percentages, numbers = extract_financial_figures(preprocessed_text)

# print("Currencies:", currencies)
# print("Percentages:", percentages)
# print("Numbers:", numbers)

