# CB: 1.0 - Import Libraries
import nltk
from textblob import TextBlob
import string
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# CB: 2.0 - Download NLTK Data
nltk_packages = ['punkt', 'wordnet', 'stopwords']
for package in nltk_packages:
    try:
        nltk.data.find(f'tokenizers/{package}')
    except LookupError:
        nltk.download(package)

# CB: 3.0 - Define Preprocessing Function
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])

    # Tokenize the text
    words = nltk.word_tokenize(text)

    # Remove stop words
    words = [word for word in words if word not in stopwords.words('english')]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return words

# CB: 4.0 - Read and Analyze Multiple Files
files = ['text01.txt', 'text02.txt', 'text03.txt']

for file_name in files:
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        text = ""

    # CB: 5.0 - Preprocess Text
    words = preprocess_text(text)

    # CB: 6.0 - Perform Sentiment Analysis
    positive_sentences = 0
    negative_sentences = 0
    neutral_sentences = 0

    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        sentiment = TextBlob(sentence).sentiment.polarity
        if sentiment > 0:
            positive_sentences += 1
        elif sentiment < 0:
            negative_sentences += 1
        else:
            neutral_sentences += 1

    # CB: 7.0 - Display Results
    labels = ['Positive', 'Negative', 'Neutral']
    scores = [positive_sentences, negative_sentences, neutral_sentences]

    plt.bar(labels, scores, color=['blue', 'green', 'red'])
    plt.title(f'Sentiment Analysis for {file_name}')
    plt.show()
