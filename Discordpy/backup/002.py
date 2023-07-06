# CB: 1.0 - Import necessary libraries
import random
import nltk
import spacy
import language_tool_python
from enum import Enum
from wonderwords import RandomWord
from gensim.models import KeyedVectors
from nltk.corpus import words, stopwords
from collections import defaultdict, Counter
from nltk.probability import FreqDist
from random import choices

# CB: 2.0 - Load GloVe vectors directly
filename = 'glove.6B.50d.txt'
glove_model = KeyedVectors.load_word2vec_format(filename, binary=False, no_header=True)

# CB: 3.0 - Define a list of highly descriptive words
descriptive_words = ['vibrant', 'luminous', 'dazzling', 'shadowy', 'radiant', 'gloomy', 'vivid', 'colorful', 
                     'sparkling', 'glistening', 'picturesque', 'scenic', 'breathtaking', 'magnificent', 'tranquil', 
                     'serene', 'spectacular', 'majestic', 'grand', 'stunning', 'charming', 'quaint', 'unique', 
                     'mysterious', 'enchanted', 'magical', 'captivating', 'mesmerizing', 'exquisite', 'elegant', 
                     'lavish', 'luxurious', 'opulent', 'rustic', 'ancient', 'historic', 'timeless', 'classic', 
                     'modern', 'innovative', 'sleek', 'stylish', 'chic', 'sophisticated', 'ornate', 'extravagant', 
                     'exotic', 'tropical', 'lush', 'wild', 'untamed', 'remote', 'secluded', 'idyllic', 'paradise', 
                     'heavenly', 'utopia', 'dreamy', 'fantasy', 'fairy-tale', 'legendary', 'mythical', 'epic', 
                     'adventure', 'journey', 'odyssey', 'quest', 'exploration', 'discovery', 'revelation', 'enlightenment']

# CB: 4.0 - Define an enumeration for the parts of speech
class PartOfSpeech(Enum):
    ADJECTIVE = 'JJ'
    NOUN = 'NN'
    VERB = 'VB'
    ADVERB = 'RB'
    PREPOSITION = 'IN'
    CONJUNCTION = 'CC'

# CB: 5.0 - Initialize the English words set
class EnglishWords:
    def __init__(self):
        self.words = self.initialize()

    def initialize(self):
        english_words = set()
        try:
            english_words = set(words.words())
        except LookupError:
            nltk.download('words')
            english_words = set(words.words())
        print(f"Number of words from NLTK corpus: {len(english_words)}")
        r = RandomWord()
        for _ in range(1000): # Add 1000 random words
            english_words.add(r.word())
        print(f"Number of words after adding from WonderWords: {len(english_words)}")
        print(f"Size of english_words set: {len(english_words)}")
        return english_words

# CB: 6.0 - Load stopwords from NLTK
class StopWords:
    def __init__(self):
        self.words = self.load()

    def load(self):
        return set(stopwords.words('english'))

# CB: 7.0 - Categorize words by their part of speech
class WordsByPOS:
    def __init__(self, english_words, chunk_size):
        self.words = self.categorize(english_words, chunk_size)

    def categorize(self, english_words, chunk_size):
        nlp = spacy.load('en_core_web_sm') # Load the spaCy model
        words_by_pos = defaultdict(list)
        def chunked_words(words, chunk_size):
            for i in range(0, len(words), chunk_size):
                yield words[i:i + chunk_size]
        for chunk in chunked_words(list(english_words), chunk_size):
            tagged_words = nlp(' '.join(chunk))
            for token in tagged_words:
                pos = token.tag_[:2] # Get the first two characters of the tag
                if any(pos.startswith(val.value) for val in PartOfSpeech.__members__.values()):
                    words_by_pos[PartOfSpeech(pos)].append(token.text)
            print(f"Words by POS after processing: {words_by_pos}")
        for pos in PartOfSpeech:
            print(f"{pos}: {len(words_by_pos[pos])} words")
        return words_by_pos

# CB: 8.0 - Define a larger set of templates
class Templates:
    def __init__(self):
        self.templates = self.define()

    def define(self):
        return [
            [PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADJECTIVE, PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN],
            [PartOfSpeech.ADJECTIVE, PartOfSpeech.VERB],
            [PartOfSpeech.NOUN, PartOfSpeech.ADJECTIVE],
            [PartOfSpeech.VERB, PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN],
            [PartOfSpeech.ADJECTIVE, PartOfSpeech.VERB, PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN],
            [PartOfSpeech.NOUN, PartOfSpeech.VERB, PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN],
            [PartOfSpeech.ADVERB, PartOfSpeech.VERB, PartOfSpeech.NOUN],
            [PartOfSpeech.NOUN, PartOfSpeech.ADVERB, PartOfSpeech.VERB],
            [PartOfSpeech.PREPOSITION, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.CONJUNCTION, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADJECTIVE, PartOfSpeech.PREPOSITION, PartOfSpeech.NOUN],
            [PartOfSpeech.ADVERB, PartOfSpeech.CONJUNCTION, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADVERB, PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADVERB, PartOfSpeech.PREPOSITION, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADVERB, PartOfSpeech.CONJUNCTION, PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADVERB, PartOfSpeech.ADJECTIVE, PartOfSpeech.PREPOSITION, PartOfSpeech.NOUN, PartOfSpeech.VERB],
            [PartOfSpeech.ADVERB, PartOfSpeech.ADJECTIVE, PartOfSpeech.CONJUNCTION, PartOfSpeech.NOUN, PartOfSpeech.VERB]
        ]

# CB: 9.0 - Define a function to generate a sentence
class SentenceGenerator:
    def __init__(self, template, words_by_pos, min_length=0, max_length=float('inf'), used_sentences=set(), timeout=5):
        self.template = template
        self.words_by_pos = words_by_pos
        self.min_length = min_length
        self.max_length = max_length
        self.used_sentences = used_sentences
        self.timeout = timeout

    def generate(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            sentence = []
            for pos in self.template:
                if self.words_by_pos[pos]: # Check if the list is not empty
                    word = self.choose_word_based_on_frequency(self.words_by_pos[pos])
                    sentence.append(word)
            sentence_str = " ".join(sentence)
            print(f"Template: {self.template}, Sentence: {sentence_str}") # Print the template and the sentence
            if self.min_length <= len(sentence_str) <= self.max_length and sentence_str not in self.used_sentences:
                self.used_sentences.add(sentence_str)
                return sentence_str
        return None # Return None if no valid sentence could be generated after timeout

    # CB: 9.1 - Define a function to choose a word based on frequency
    def choose_word_based_on_frequency(self, words):
        word_counts = Counter(words)
        word = choices(list(word_counts.keys()), weights=list(word_counts.values()))[0]
        return word

# CB: 9.2 - Add a post-processing step
class SentencePostProcessor:
    def __init__(self, sentence):
        self.sentence = sentence

    def post_process(self):
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(self.sentence)
        corrected_sentence = language_tool_python.correct(self.sentence, matches)
        return corrected_sentence

# CB: 10.0 - Find semantically related words
class RelatedWordFinder:
    def __init__(self, word, model):
        self.word = word
        self.model = model

    def find(self):
        related_words = self.model.most_similar(positive=[self.word], topn=10)
        related_word = random.choice(related_words)[0]
        return related_word

# CB: 11.0 - Use semantically related words in sentence generation
class SemanticSentenceGenerator(SentenceGenerator):
    def __init__(self, template, words_by_pos, model, min_length=0, max_length=float('inf'), used_sentences=set(), max_tries=1000):
        super().__init__(template, words_by_pos, min_length, max_length, used_sentences)
        self.model = model
        self.max_tries = max_tries

    def generate(self):
        for _ in range(self.max_tries):
            sentence = []
            for pos in self.template:
                if self.words_by_pos[pos]: # Check if the list is not empty
                    word = self.choose_word_based_on_frequency(self.words_by_pos[pos])
                    related_word = RelatedWordFinder(word, self.model).find()
                    sentence.append(related_word)
            sentence_str = " ".join(sentence)
            if self.min_length <= len(sentence_str) <= self.max_length and
            sentence_str not in self.used_sentences:
                self.used_sentences.add(sentence_str)
                return sentence_str
        return None

# CB: 12.0 - Generate 50 sentences
for _ in range(50):
    # Select a seed word from the descriptive words
    seed_word = random.choice([word for word in descriptive_words if word in glove_model.index_to_key])

    # Find related words
    related_words = [word for word, _ in glove_model.most_similar(seed_word, topn=100)]

    # Separate related words by part of speech
    adjectives = [word for word in related_words if get_wordnet_pos(word) == wordnet.ADJ]
    nouns = [word for word in related_words if get_wordnet_pos(word) == wordnet.NOUN]
    verbs = [word for word in related_words if get_wordnet_pos(word) == wordnet.VERB]
    adverbs = [word for word in related_words if get_wordnet_pos(word) == wordnet.ADV]

    # Generate a sentence
    if adjectives and nouns and verbs and adverbs:
        sentence = [random.choice(adjectives), random.choice(nouns), random.choice(verbs), random.choice(adverbs)]
        sentence_str = " ".join(sentence)
        print(f"Generated Sentence: {sentence_str}")
