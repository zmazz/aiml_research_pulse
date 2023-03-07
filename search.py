import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
import pickle

# Load the dataset
data = pd.read_csv('raw_data/aiml_arxiv_with_cit.csv',low_memory=False)
data=data[data['abstract'].notna()]

# Preprocess the data
stop_words = stopwords.words('english')
tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
tfidf_matrix = tfidf_vectorizer.fit_transform(data['abstract'])

## instead of loading dataset and redoing vectorization
#tfidf_vectorizer= pickle.load(open('raw_data/search_tfidf_vectorizer.pk','rb'))
#tfidf_matrix=sp.load_npz('raw_data/search_tfidf_matrix.npz')

# Define the chatbot function
def chatbot():
    # Greet the user
    print('Hi, I am a chatbot that can help you find research papers in machine learning and deep learning. What can I do for you?')

    # Loop until the user says goodbye
    while True:
        # Get the user's query
        query = input('> ')

        # Check if the user wants to quit
        if query.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print('Goodbye!')
            break

        # Preprocess the query
        query_tokens = word_tokenize(query.lower())
        query_tokens = [token for token in query_tokens if token not in stop_words]
        query = ' '.join(query_tokens)

        # Compute the similarity scores between the query and the abstracts
        query_tfidf = tfidf_vectorizer.transform([query])
        scores = cosine_similarity(query_tfidf, tfidf_matrix).flatten()
        ranked_indices = scores.argsort()[::-1]

        # Return the top 5 results
        for i in range(5):
            paper = data.iloc[ranked_indices[i]]
            print(f'Title: {paper["title"]}\nAuthors: {paper["authors"]}\nYear: {paper["year"]}\nLink: {paper["url"]}\nAbstract: {paper["abstract"]}\n')

if __name__ =='__main__':
    chatbot()
