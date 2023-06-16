# CB: 1.0 - Import Libraries
from nltk import word_tokenize, sent_tokenize, data, download, ne_chunk, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from string import punctuation
from collections import Counter
from argparse import ArgumentParser, ArgumentTypeError
from matplotlib.pyplot import pie, title, savefig
from fpdf import FPDF
from datetime import datetime
from os.path import splitext
from tqdm import tqdm
from langdetect import detect
from gensim import corpora, models
from summarizer import Summarizer
from wordcloud import WordCloud

# CB: 2.0 - Download NLTK Data
nltk_packages = ['punkt', 'wordnet', 'stopwords', 'maxent_ne_chunker']
for package in nltk_packages:
    try:
        data.find(f'tokenizers/{package}')
    except LookupError:
        print(f"★ Downloading necessary NLTK package: {package}...")
        download(package)

# CB: 3.0 - Define Preprocessing Function
def preprocess_text(text):
    """
    Preprocesses the text by lowercasing, removing punctuation, tokenizing, removing stop words, and lemmatizing.

    Parameters:
    text (str): The text to preprocess.

    Returns:
    words (list): The preprocessed words.
    """
    text = text.lower()
    text = ''.join([char for char in text if char not in punctuation])
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# CB: 4.0 - Command Line Arguments
parser = ArgumentParser(description='Perform sentiment analysis on text files.')
parser.add_argument('Files', metavar='F', type=str, nargs='*', default=['text01.txt'], help='a list of files to analyze')
args = parser.parse_args()
files = args.Files

if not all(splitext(file)[1] == '.txt' for file in files):
    raise ArgumentTypeError("Only text files are allowed.")

# CB: 5.0 - Read and Analyze Multiple Files
for file_name in files:
    print(f"★ Starting sentiment analysis for {file_name}...")
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"★ The file '{file_name}' does not exist.")
        continue

    if not text:
        print(f"★ The file '{file_name}' is empty.")
        continue

    language = detect(text)
    if language != 'en':
        print(f"★ The text is in {language}, not English. Skipping sentiment analysis.")
        continue

    # CB: 6.0 - Preprocess Text
    words = preprocess_text(text)

    # CB: 7.0 - Perform Sentiment Analysis
    positive_sentences = 0
    negative_sentences = 0
    neutral_sentences = 0

    sentences = sent_tokenize(text)

    for sentence in tqdm(sentences, desc="Analyzing sentences"):
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

    # Add timestamp
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Analysis performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    # Add subtitle
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"File: {file_name}", ln=True)

    # Add content
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Positive sentences: {positive_sentences}", ln=True)
    pdf.cell(200, 10, txt=f"Negative sentences: {negative_sentences}", ln=True)
    pdf.cell(200, 10, txt=f"Neutral sentences: {neutral_sentences}", ln=True)

    # CB: 9.0 - Add a Pie Chart to the PDF
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive_sentences, negative_sentences, neutral_sentences]
    pie(sizes, labels=labels, autopct='%1.1f%%')
    title('Sentiment Distribution')
    savefig('sentiment_distribution.png')

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

    # Add most common entities to the PDF
    entities = ne_chunk(pos_tag(word_tokenize(text)))
    entity_names = [str(entity[0]) for entity in entities if hasattr(entity, 'label')]
    entity_freq = Counter(entity_names)
    pdf.cell(200, 10, txt="Most common entities:", ln=True)
    for i, (entity, count) in enumerate(entity_freq.most_common(10)):
        pdf.cell(200, 10, txt=f"{entity}: {count}", ln=True)

    # Add topics to the PDF
    dictionary = corpora.Dictionary([words])
    corpus = [dictionary.doc2bow(text) for text in [words]]
    lda_model = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=2)
    pdf.cell(200, 10, txt="Topics:", ln=True)
    for i, topic in lda_model.print_topics(-1):
        pdf.cell(200, 10, txt=f"Topic {i}: {topic}", ln=True)

    #★ Add word cloud to the PDF
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_freq)
    wordcloud.to_file('wordcloud.png')
    pdf.image('wordcloud.png', x=10, y=80, w=100)

    # Add summary to the PDF
    model = Summarizer()
    summary = model(text)
    pdf.cell(200, 10, txt="Summary:", ln=True)
    pdf.multi_cell(200, 10, txt=summary)

    # Save the PDF
    pdf.output(f"SentimentAnalysisReport_{file_name}.pdf")

    print(f"★ PDF report saved as 'SentimentAnalysisReport_{file_name}.pdf'.")
