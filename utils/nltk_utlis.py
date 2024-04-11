import nltk  # Importing the Natural Language Toolkit library
from nltk.stem.porter import PorterStemmer  # Importing the Porter Stemmer algorithm
import numpy as np  # Importing NumPy library for numerical computations

# Initialize the Porter Stemmer
stemmer = PorterStemmer()

# Download necessary NLTK data (word tokenizer) for tokenization
nltk.download('punkt')

# Tokenization Function: Splits a sentence into a list of words
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Stemming Function: Reduce each word to its word stem or root form
def stem(word):
    # Convert word to lowercase and stem it using Porter Stemmer
    return stemmer.stem(word.lower())

# Bag of Words Function: Generates a binary vector representing presence/absence of words
def bag_of_words(tokenized_sentence, words):
    # Stem each word in the tokenized sentence
    stemmed = [stem(word) for word in tokenized_sentence]
    
    # Initialize bag of words vector with zeros
    bag = np.zeros(len(words), dtype=np.float32)
    
    # Iterate through each word in the vocabulary
    for idx, w in enumerate(words):
        # Check if stemmed word is present in the tokenized sentence
        if w in stemmed:
            # If present, set the corresponding index in bag to 1
            bag[idx] = 1
    
    return bag


# Example data
sentence = "The quick brown fox jumps over the lazy dog"
words = ["quick", "brown", "fox", "jumps", "over", "lazy", "dog", "apple", "banana", "cherry"]

# Tokenize the sentence
tokenized_sentence = tokenize(sentence)
print("Tokenized sentence:", tokenized_sentence)

# Stem each word in the tokenized sentence
stemmed_words = [stem(word) for word in tokenized_sentence]
print("Stemmed words:", stemmed_words)

# Generate bag-of-words representation
bag_of_words_vector = bag_of_words(tokenized_sentence, words)
print("Bag of words vector:", bag_of_words_vector)
