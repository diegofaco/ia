# CB: 1.0 - Import Libraries
import nltk
from textblob import TextBlob
import string
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import argparse
from collections import Counter
from fpdf import FPDF
import datetime

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

# CB: 4.0 - Command Line Arguments
parser = argparse.ArgumentParser(description='Perform sentiment analysis on text files.')
parser.add_argument('Files', metavar='F', type=str, nargs='*', default=['text01.txt'], help='a list of files to analyze')
args = parser.parse_args()
files = args.Files

# CB: 5.0 - Read and Analyze Multiple Files
for file_name in files:
    print(f"★ Starting sentiment analysis for {file_name}...")
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"★ The file '{file_name}' does not exist.")
        text = ""

    # CB: 6.0 - Preprocess Text
    words = preprocess_text(text)

    # CB: 7.0 - Perform Sentiment Analysis
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

    print(f"★ Sentiment analysis completed for {file_name}.")
    print(f"★ Positive sentences: {positive_sentences}")
    print(f"★ Negative sentences: {negative_sentences}")
    print(f"★ Neutral sentences: {neutral_sentences}")

    # CB: 8.0 - Create a PDF with Basic Information
    pdf = FPDF()
    pdf.add_page()

    # Add title
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 10, txt="Sentiment Analysis Report", ln=True, align='C')

    # Add subtitle
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"File: {file_name}", ln=True)

    # Add content
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Positive sentences: {positive_sentences}", ln=True)
    pdf.cell(200,★ My apologies for the cut-off. Here's the continuation and completion of the code:
    pdf.cell(200, 10, txt=f"Negative sentences: {negative_sentences}", ln=True)
    pdf.cell(200, 10, txt=f"Neutral sentences: {neutral_sentences}", ln=True)

    # CB: 9.0 - Add a Pie Chart to the PDF
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive_sentences, negative_sentences, neutral_sentences]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Sentiment Distribution')
    plt.savefig('sentiment_distribution.png')

    # Add the pie chart to the PDF
    pdf.image('sentiment_distribution.png', x=10, y=80, w=100)

    # CB: 10.0 - Add More Detailed Information
    # Calculate total sentences
    total_sentences = positive_sentences + negative_sentences + neutral_sentences

    # Add total sentences to the PDF
    pdf.cell(200, 10, txt=f"Total sentences: {total_sentences}", ln=True)

    # Calculate most common words
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)

    # Add most common words to the PDF
    pdf.cell(200, 10, txt="Most common words:", ln=True)
    for i, (word, count) in enumerate(most_common_words):
        pdf.cell(200, 10, txt=f"{word}: {count}", ln=True)

    # Save the PDF
    pdf.output(f"SentimentAnalysisReport_{file_name}.pdf")

    print(f"★ PDF report saved as 'SentimentAnalysisReport_{file_name}.pdf'.")
