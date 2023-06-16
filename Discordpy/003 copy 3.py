# CB: 1.0 - Import Libraries
import nltk
from textblob import TextBlob
import string
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import argparse
from reportlab.pdfgen import canvas
from collections import Counter

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
    c = canvas.Canvas("SentimentAnalysisReport.pdf")

    # Add title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "Sentiment Analysis Report")

    # Add subtitle
    c.setFont("Helvetica", 16)
    c.drawString(50, 700, f"File: {file_name}")

    # Add content
    c.setFont("Helvetica", 12)
    c.drawString(50, 650, f"Positive sentences: {positive_sentences}")
    c.drawString(50, 625, f"Negative sentences: {negative_sentences}")
    c.drawString(50, 600, f"Neutral sentences: {neutral_sentences}")

    # CB: 9.0 - Add a Pie Chart to the PDF
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive_sentences, negative_sentences, neutral_sentences]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Sentiment Distribution')
    plt.savefig('sentiment_distribution.png')

    # Add the pie chart to the PDF
    c.drawImage('sentiment_distribution.png', 50, 400, width=500, height=300)

    # CB: 10.0 - Add More Detailed Information
    # Calculate total sentences
    total_sentences = positive_sentences + negative_sentences + neutral_sentences

    # Add total sentences to the PDF
    c.drawString(50, 575, f"Total sentences: {total_sentences}")

    # Calculate most common words
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)

    # Add most common words to the PDF
    c.drawString(50, 550, "Most common words:")
    for i, (word, count) in enumerate(most_common_words):
        c.drawString(70, 525 - i*25, f"{word}: {count}")

    # Save the PDF
    c.save()

    print(f"★ PDF report saved as 'SentimentAnalysisReport.pdf'.")
