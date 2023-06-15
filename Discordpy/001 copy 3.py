# CB: 1.4 - Load GloVe vectors directly
from gensim.models import KeyedVectors

filename = 'glove.6B.50d.txt'
model = KeyedVectors.load_word2vec_format(filename, binary=False, no_header=True)

# CB: 3.2 - Generate semantically good short sentences with Gensim 4.0.0+
import random
from nltk.corpus import stopwords
import string

# Load the list of stopwords
stop_words = set(stopwords.words('english'))

# List of highly descriptive words
descriptive_words = ['vibrant', 'luminous', 'dazzling', 'shadowy', 'radiant', 'gloomy', 'vivid', 'colorful', 
                     'sparkling', 'glistening', 'picturesque', 'scenic', 'breathtaking', 'magnificent', 'tranquil', 
                     'serene', 'spectacular', 'majestic', 'grand', 'stunning', 'charming', 'quaint', 'unique', 
                     'mysterious', 'enchanted', 'magical', 'captivating', 'mesmerizing', 'exquisite', 'elegant', 
                     'lavish', 'luxurious', 'opulent', 'rustic', 'ancient', 'historic', 'timeless', 'classic', 
                     'modern', 'innovative', 'sleek', 'stylish', 'chic', 'sophisticated', 'ornate', 'extravagant', 
                     'exotic', 'tropical', 'lush', 'wild', 'untamed', 'remote', 'secluded', 'idyllic', 'paradise', 
                     'heavenly', 'utopia', 'dreamy', 'fantasy', 'fairy-tale', 'legendary', 'mythical', 'epic', 
                     'adventure', 'journey', 'odyssey', 'quest', 'exploration', 'discovery', 'revelation', 'enlightenment']

# Generate 50 sentences
for _ in range(50):
    # Select a seed word from the descriptive words
    seed_word = random.choice([word for word in descriptive_words if word in model.index_to_key])

    # Find related words excluding stopwords and punctuation
    related_words = [word for word, _ in model.most_similar(seed_word, topn=100) 
                     if word not in stop_words and word not in string.punctuation]

    # Generate a sentence ensuring no word is repeated
    sentence_words = random.sample(related_words, min(5, len(related_words)))
    sentence = ' '.join(sentence_words)

    print(sentence)
