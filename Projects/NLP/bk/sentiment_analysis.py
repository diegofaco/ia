# sentiment_analysis.py

from keras.datasets import imdb
from gensim.models import KeyedVectors
from sklearn.linear_model import LogisticRegression
import numpy as np

class SentimentAnalysis:
    def __init__(self):
        self.model = LogisticRegression()
        self.glove_model = KeyedVectors.load_word2vec_format('glove.6B.50d.word2vec.txt', binary=False)
        self.train()

    def get_word_index(self):
        word_index = imdb.get_word_index()
        reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
        return reverse_word_index

    def decode_review(self, text, reverse_word_index):
        return ' '.join([reverse_word_index.get(i, '?') for i in text])

    def text_to_vector(self, text):
        words = text.split()
        word_vecs = [self.glove_model.get_vector(word) for word in words if word in self.glove_model.vocab]
        return np.mean(word_vecs, axis=0)

    def train(self):
        (train_data, train_labels), (test_data, test_labels) = imdb.load_data()
        reverse_word_index = self.get_word_index()

        train_data = [self.decode_review(text, reverse_word_index) for text in train_data]
        test_data = [self.decode_review(text, reverse_word_index) for text in test_data]

        train_vectors = np.array([self.text_to_vector(text) for text in train_data])
        test_vectors = np.array([self.text_to_vector(text) for text in test_data])

        self.model.fit(train_vectors, train_labels)

    def predict(self, text):
        vector = self.text_to_vector(text)
        prediction = self.model.predict([vector])
        return "Positive" if prediction[0] == 1 else "Negative"
