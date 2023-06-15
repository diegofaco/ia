import random
import nltk
from nltk.corpus import words, stopwords
from enum import Enum
from tqdm import tqdm
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from collections import defaultdict
from wonderwords import RandomWord
import spacy
import time
import sqlite3

# CB: 1.0 - Define an enumeration for the parts of speech
class PartOfSpeech(Enum):
    ADJECTIVE = 'JJ'
    NOUN = 'NN'
    VERB = 'VB'
    ADVERB = 'RB'
    PREPOSITION = 'IN'
    CONJUNCTION = 'CC'

# CB: 2.0 - Initialize the English words set
def initialize_english_words():
    english_words = set()
    try:
        english_words = set(words.words())
    except LookupError:
        nltk.download('words')
        english_words = set(words.words())
    print(f"Number of words from NLTK corpus: {len(english_words)}")
    # CB: 2.1 - Add random words from wonderwords
    r = RandomWord()
    for _ in range(1000): # Add 1000 random words
        english_words.add(r.word())
    print(f"Number of words after adding from WonderWords: {len(english_words)}")
    # CB: 2.2 - Print the size of the english_words set
    print(f"Size of english_words set: {len(english_words)}")
    return english_words

# CB: 3.0 - Load stopwords from NLTK
def load_stop_words():
    return set(stopwords.words('english'))

# CB: 4.0 - Categorize words by their part of speech
def categorize_words_by_pos(english_words, chunk_size):
    nlp = spacy.load('en_core_web_sm') # Load the spaCy model
    words_by_pos = defaultdict(list)
    # CB: 4.1 - Define a function to divide words into chunks
    def chunked_words(words, chunk_size):
        for i in range(0, len(words), chunk_size):
            yield words[i:i + chunk_size]
    # CB: 4.2 - Process words in chunks
    for chunk in chunked_words(list(english_words), chunk_size):
        tagged_words = nlp(' '.join(chunk))
        for token in tagged_words:
            pos = token.tag_[:2] # Get the first two characters of the tag
            if any(pos.startswith(val.value) for val in PartOfSpeech.__members__.values()):
                words_by_pos[PartOfSpeech(pos)].append(token.text)
        print(f"Words by POS after processing: {words_by_pos}")
    # CB: 4.3 - Print the count of words for each part of speech
    for pos in PartOfSpeech:
        print(f"{pos}: {len(words_by_pos[pos])} words")
    return words_by_pos

# CB: 5.0 - Define sentence templates
def define_templates():
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
        [PartOfSpeech.ADVERB, PartOfSpeech.CONJUNCTION, PartOfSpeech.NOUN, PartOfSpeech.VERB]
    ]

# CB: 6.0 - Define a function to generate a sentence
def generate_sentence(template, words_by_pos, min_length=0, max_length=float('inf'), used_sentences=set(), timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        sentence = []
        for pos in template:
            if words_by_pos[pos]: # Check if the list is not empty
                word = choose_word_based_on_frequency(words_by_pos[pos])
                sentence.append(word)
        sentence_str = " ".join(sentence)
        print(f"Template: {template}, Sentence: {sentence_str}") # Print the template and the sentence
        if min_length <= len(sentence_str) <= max_length and sentence_str not in used_sentences:
            used_sentences.add(sentence_str)
            return sentence_str
    return None # Return None if no valid sentence could be generated after timeout

# CB: 6.1 - Define a function to choose a word based on frequency
def choose_word_based_on_frequency(words):
    # Choose a word based on its frequency (assumed to be inversely proportional to its length)
    words.sort(key=len) # Sort words by length
    return random.choice(words) # Choose a random word (shorter words are more likely to be chosen)


# CB: 7.0 - Define a function to generate sentences and display them in the GUI
def generate_and_display_sentences(num_sentences_spinbox, text_area, progress_bar, templates, words_by_pos):
    num_sentences = int(num_sentences_spinbox.get()) # Get the number of sentences to generate
    progress_bar['value'] = 0
    sentences = []
    for i in tqdm(range(num_sentences)):
        template = random.choice(templates)
        sentence = generate_sentence(template, words_by_pos)
        if sentence is not None: # Only display the sentence if it's not None
            text_area.insert(tk.INSERT, sentence + '\n')
            sentences.append(sentence)
        progress_bar['value'] += 100 / num_sentences # Update the progress bar
    progress_bar['value'] = 100 # Set the progress bar to 100% when done
    if progress_bar['value'] == 100:
        messagebox.showinfo("Information", "Sentence generation completed!")
    # Export the sentences to a file
    export_sentences_to_file(sentences)

# CB: 7.1 - Define a function to export sentences to a file
def export_sentences_to_file(sentences):
    with open('sentences.txt', 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')

# CB: 7.2 - Define a function to export sentences to a database
def export_sentences_to_db(sentences):
    conn = sqlite3.connect('sentences.txt')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sentences
                 (sentence text)''')
    for sentence in sentences:
        c.execute("INSERT INTO sentences VALUES (?)", (sentence,))
    conn.commit()
    conn.close()
    
# CB: 8.0 - Create the main window
class SentenceGeneratorGUI:
    def __init__(self, templates, words_by_pos):
        self.window = tk.Tk()
        self.window.title("Sentence Generator")
        self.templates = templates
        self.words_by_pos = words_by_pos

        # Add a label for the spinbox
        tk.Label(self.window, text="Number of sentences:").pack()
        self.num_sentences_spinbox = tk.Spinbox(self.window, from_=1, to=20)
        self.num_sentences_spinbox.pack()

        self.generate_button = tk.Button(self.window, text="Generate Sentences", command=self.generate_and_display_sentences)
        self.generate_button.pack()

        self.progress_bar = ttk.Progressbar(self.window, length=100, mode='determinate')
        self.progress_bar.pack()

        # Add a label for the text area
        tk.Label(self.window, text="Generated sentences:").pack()
        self.text_area = scrolledtext.ScrolledText(self.window)
        self.text_area.pack()

    def generate_and_display_sentences(self):
        num_sentences = int(self.num_sentences_spinbox.get()) # Get the number of sentences to generate
        self.progress_bar['value'] = 0
        sentences = []
        for i in tqdm(range(num_sentences)):
            template = random.choice(self.templates)
            sentence = generate_sentence(template, self.words_by_pos)
            if sentence is not None: # Only display the sentence if it's not None
                self.text_area.insert(tk.INSERT, sentence + '\n')
                sentences.append(sentence)
            self.progress_bar['value'] += 100 / num_sentences # Update the progress bar
        self.progress_bar['value'] = 100 # Set the progress bar to 100% when done
        if self.progress_bar['value'] == 100:
            messagebox.showinfo("Information", "Sentence generation completed!")
        # Export the sentences to a file
        export_sentences_to_db(sentences)

    def start_main_loop(self):
        self.window.mainloop()
        
    # CB: 8.1 - Add a function to add a new template
    def add_template(self, template):
        self.templates.append(template)
        
    # CB: 8.2 - Add a function to choose a part of speech
    def choose_pos(self, pos):
        self.pos = pos

if __name__ == "__main__":
    chunk_size = 50000 # Configurable chunk size
    english_words = initialize_english_words()
    stop_words = load_stop_words()
    words_by_pos = categorize_words_by_pos(english_words, chunk_size)
    templates = define_templates()
    gui = SentenceGeneratorGUI(templates, words_by_pos)
    gui.start_main_loop()
