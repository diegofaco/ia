# CB: 1.4 - Load GloVe vectors directly
from gensim.models import KeyedVectors

filename = 'glove.6B.50d.txt'
model = KeyedVectors.load_word2vec_format(filename, binary=False, no_header=True)

# CB: 2.1 - Find similar words
similar_words = model.most_similar('queen', topn=5)
print(similar_words)

# CB: 2.2 - Solve word analogies
result = model.most_similar(positive=['woman', 'king'], negative=['man'])
print(result[0][0])

# CB: 2.3 - Visualize word embeddings
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

words = ['king', 'queen', 'man', 'woman']
vectors = [model[word] for word in words]

pca = PCA(n_components=2)
result = pca.fit_transform(vectors)

plt.scatter(result[:, 0], result[:, 1])
for i, word in enumerate(words):
    plt.annotate(word, xy=(result[i, 0], result[i, 1]))
plt.show()
