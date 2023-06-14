import random
import nltk
from nltk.corpus import words, stopwords
from nltk.tokenize import word_tokenize

# Download the words corpus if it hasn't been downloaded yet
try:
    english_words = set(words.words())
except LookupError:
    nltk.download('words')
    english_words = set(words.words())

# Load stopwords from NLTK
stop_words = set(stopwords.words('english'))

# Define lists of words for each part of speech
adjectives = [word for word in english_words if nltk.pos_tag([word])[0][1] == 'JJ']
nouns = [word for word in english_words if nltk.pos_tag([word])[0][1] == 'NN']
verbs = [word for word in english_words if nltk.pos_tag([word])[0][1] == 'VB']

# Define sentence templates
templates = [
    ["adjective", "noun", "verb"],
    ["noun", "verb"],
    ["adjective", "adjective", "noun", "verb"],
    ["adjective", "noun"],
    ["verb", "noun"],
    ["adjective", "verb"],
    ["noun", "adjective"],
    ["verb", "adjective", "noun"],
    ["adjective", "verb", "adjective", "noun"],
    ["noun", "verb", "adjective", "noun"]
]

# Generate a sentence
for _ in range(5):
    template = random.choice(templates)
    sentence = []
    used_words = []
    for part_of_speech in template:
        if part_of_speech == "adjective":
            word = random.choice(adjectives)
        elif part_of_speech == "noun":
            word = random.choice(nouns)
        elif part_of_speech == "verb":
            word = random.choice(verbs)
        while word in used_words:
            if part_of_speech == "adjective":
                word = random.choice(adjectives)
            elif part_of_speech == "noun":
                word = random.choice(nouns)
            elif part_of_speech == "verb":
                word = random.choice(verbs)
        sentence.append(word)
        used_words.append(word)
    print(" ".join(sentence))
