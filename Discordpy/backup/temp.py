# CB: 1.0 - Import necessary libraries
import random
import time
import nltk
import spacy
import tkinter as tk
import sqlite3
import language_tool_python
from enum import Enum
from tqdm import tqdm
from nltk.corpus import words, stopwords
from collections import defaultdict, Counter
from tkinter import scrolledtext, ttk, messagebox
from wonderwords import RandomWord
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from nltk.probability import FreqDist
from random import choices

# CB: 2.0 - Define an enumeration for the parts of speech
class PartOfSpeech(Enum):
    ADJECTIVE = 'JJ'
    NOUN = 'NN'
    VERB = 'VB'
    ADVERB = 'RB'
    PREPOSITION = 'IN'
    CONJUNCTION = 'CC'

# CB: 3.0 - Initialize the English words set
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

# CB: 4.0 - Load stopwords from NLTK
class StopWords:
    def __init__(self):
        self.words = self.load()

    def load(self):
        return set(stopwords.words('english'))

# CB: 5.0 - Categorize words by their part of speech
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

# CB: 6.0 - Define a larger set of templates
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

# CB: 7.0 - Define a function to generate a sentence
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

    # CB: 7.1 - Define a function to choose a word based on frequency
    def choose_word_based_on_frequency(self, words):
        word_counts = Counter(words)
        word = choices(list(word_counts.keys()), weights=list(word_counts.values()))[0]
        return word

# CB: 7.2 - Add a post-processing step
class SentencePostProcessor:
    def __init__(self, sentence):
        self.sentence = sentence

    def post_process(self):
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(self.sentence)
        corrected_sentence = language_tool_python.correct(self.sentence, matches)
        return corrected_sentence

# CB: 8.0 - Load the Word2Vec model
class WordEmbeddings:
    def __init__(self):
        self.model = self.load()

    def load(self):
        model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
        return model

# CB: 8.1 - Find semantically related words
class RelatedWordFinder:
    def __init__(self, word, model):
        self.word = word
        self.model = model

    def find(self):
        related_words = self.model.most_similar(positive=[self.word], topn=10)
        related_word = random.choice(related_words)[0]
        return related_word

# CB: 8.2 - Use semantically related words in sentence generation
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
            if self.min_length <= len(sentence_str) <= self.max_length and sentence_str not in self.used_sentences:
                self.used_sentences.add(sentence_str)
                return sentence_str
        return None

# CB: 9.0 - Define a function to generate sentences and display them in the GUI
class SentenceDisplay:
    def __init__(self, num_sentences, templates, words_by_pos, progress_bar, text_area):
        self.num_sentences = num_sentences
        self.templates = templates
        self.words_by_pos = words_by_pos
        self.progress_bar = progress_bar
        self.text_area = text_area
        self.sentences = []

    def generate_and_display(self):
        self.progress_bar['value'] = 0
        word_embeddings = WordEmbeddings().model  # Load the Word2Vec model
        for i in tqdm(range(self.num_sentences)):
            template = random.choice(self.templates)
            sentence = SemanticSentenceGenerator(template, self.words_by_pos, word_embeddings).generate()  # Pass the model to SemanticSentenceGenerator
            if sentence is not None: # Only display the sentence if it's not None
                self.text_area.insert(tk.INSERT, sentence + '\n')
                self.sentences.append(sentence)
            self.progress_bar['value'] += 100 / self.num_sentences # Update the progress bar
        self.progress_bar['value'] = 100 # Set the progress bar to 100% when done
        if self.progress_bar['value'] == 100:
            messagebox.showinfo("Information", "Sentence generation completed!")
        SentenceExporter(self.sentences).export_to_db()

# CB: 9.1 - Define a function to export sentences to a★ Continuing from where we left off:
class SentenceExporter:
    def __init__(self, sentences):
        self.sentences = sentences

    def export_to_file(self):
        with open('sentences.txt', 'w') as f:
            for sentence in self.sentences:
                f.write(sentence + '\n')

    # CB: 9.2 - Define a function to export sentences to a database
    def export_to_db(self):
        conn = sqlite3.connect('sentences.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sentences
                     (sentence text)''')
        for sentence in self.sentences:
            c.execute("INSERT INTO sentences VALUES (?)", (sentence,))
        conn.commit()
        conn.close()

# CB: 10.0 - Create the main window
class SentenceGeneratorGUI:
    def __init__(self, templates, words_by_pos):
        self.window = tk.Tk()
        self.window.title("Sentence Generator")
        self.window.configure(bg='lightgray')  # Change the background color
        self.templates = templates
        self.words_by_pos = words_by_pos

        tk.Label(self.window, text="Number of sentences:").pack()
        self.num_sentences_spinbox = tk.Spinbox(self.window, from_=1, to=20)
        self.num_sentences_spinbox.pack()

        self.generate_button = tk.Button(self.window, text="Generate Sentences", command=self.generate_and_display_sentences)
        self.generate_button.pack()

        self.progress_bar = ttk.Progressbar(self.window, length=100, mode='determinate')
        self.progress_bar.pack()

        tk.Label(self.window, text="Generated sentences:").pack()
        self.text_area = scrolledtext.ScrolledText(self.window)
        self.text_area.pack()

    def generate_and_display_sentences(self):
        num_sentences = int(self.num_sentences_spinbox.get()) # Get the number of sentences to generate
        SentenceDisplay(num_sentences, self.templates, self.words_by_pos, self.progress_bar, self.text_area).generate_and_display()

    def start_main_loop(self):
        self.window.mainloop()

    # CB: 10.1 - Add a function to add a new template
    def add_template(self, template):
        self.templates.append(template)

    # CB: 10.2 - Add a function to choose a part of speech
    def choose_pos(self, pos):
        self.pos = pos

if __name__ == "__main__":
    chunk_size = 50000 # Configurable chunk size
    english_words = EnglishWords().words
    stop_words = StopWords().words
    words_by_pos = WordsByPOS(english_words, chunk_size).words
    templates = Templates().templates
    gui = SentenceGeneratorGUI(templates, words_by_pos)
    gui.start_main_loop()

