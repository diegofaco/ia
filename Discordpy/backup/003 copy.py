# Step 1: Import the necessary libraries
import nltk
from textblob import TextBlob
import string
import matplotlib.pyplot as plt

# Step 2: Download the necessary NLTK data
nltk.download('punkt')

# Step 3: Define a function to preprocess the text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])

    # Tokenize the text
    words = nltk.word_tokenize(text)

    return words

# Step 4: Read the text from the file
with open('text01.txt', 'r', encoding='utf-8') as file:  # Specify the encoding
    text = file.read()

# Step 5: Preprocess the text
words = preprocess_text(text)

# Step 6: Perform sentiment analysis
blob = TextBlob(text)
sentiment = blob.sentiment

# Step 7: Display the results
labels = ['Polarity', 'Subjectivity']
scores = [sentiment.polarity, sentiment.subjectivity]

plt.bar(labels, scores, color=['blue', 'green'])
plt.ylim([-1, 1])  # Set the limits of the y-axis
plt.title('Sentiment Analysis')
plt.show()
