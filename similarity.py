import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Caricamento del file CSV
file_path = 'cleaned_arxiv_data_with_babelnet.csv'
data = pd.read_csv(file_path)

# Estrazione dei synset
synsets = data['babelnet_synset'].fillna('')

# Creazione del vettore TF-IDF per i synset
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(synsets)

# Calcolo della similarità del coseno tra i paper
cosine_similarities = cosine_similarity(tfidf_matrix)

# Creazione di un DataFrame per mostrare le similarità
similarity_df = pd.DataFrame(cosine_similarities, index=data['id'], columns=data['id'])

# Funzione per creare relazioni di similarità basate su una soglia
def create_similarity_edges(similarity_df, threshold=0.5):
    edges = []
    for i, row in similarity_df.iterrows():
        for j, similarity in row.items():
            if i != j and similarity >= threshold:
                edges.append((i, j, similarity))
    return edges

# Creazione delle relazioni di similarità
edges = create_similarity_edges(similarity_df, threshold=0.5)

# Creazione di un file CSV per le relazioni di similarità
edges_df = pd.DataFrame(edges, columns=['Paper1', 'Paper2', 'Similarity'])
edges_df.to_csv('similarity_edges.csv', index=False)

print("Relazioni di similarità create e salvate in 'similarity_edges.csv'.")
