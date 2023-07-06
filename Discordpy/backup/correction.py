import os
import numpy as np
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load the GloVe model
def load_glove_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    glove_path = os.path.join(current_dir, "glove.6B.50d.word2vec.txt")
    return KeyedVectors.load_word2vec_format(glove_path, binary=False)

# Generate embeddings for the items
def generate_embeddings(items, glove_model):
    embeddings = []
    for item in items:
        words = [word for word in item.split(" ::")[0].split() if word in glove_model]
        if words:
            embedding = np.mean([glove_model[word] for word in words], axis=0)
            embeddings.append(embedding)
        else:
            print(f"Skipping item '{item}' because it doesn't contain any recognized words")
    return embeddings

# Plot the reduced embeddings
def plot_embeddings(embeddings, items):
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)
    plt.figure(figsize=(10, 10))
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])
    for i, item in enumerate(items):
        plt.annotate(item, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))
    plt.show()

def main():
    # Load the GloVe model
    glove_model = load_glove_model()

    # Specify the output directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "output")

    # Loop over the files in the output directory
    for filename in os.listdir(output_dir):
        # Only process .txt files
        if filename.endswith(".txt"):
            with open(os.path.join(output_dir, filename), "r") as file:
                # Create a list of items from the file
                items = [line.strip() for line in file if "::" in line]
                
                # Generate embeddings for the items
                embeddings = generate_embeddings(items, glove_model)
                
                # Plot the reduced embeddings
                plot_embeddings(embeddings, items)

if __name__ == "__main__":
    main()
