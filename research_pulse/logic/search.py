import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
import pickle

# Load the dataset
data = pd.read_csv('~/deepdipper/data/processed/aiml_arxiv_with_cit.csv', low_memory=False)

def vectorizer(df):
    """
    Vectorize abstracts, and return tfidf_vectorizer and tfidf_matrix to reusage
    """
    df=df[df['abstract'].notna()]
    # Preprocess the data
    stop_words = stopwords.words('english')
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['abstract'])

    ## instead of loading dataset and redoing vectorization
    #tfidf_vectorizer= pickle.load(open('raw_data/search_tfidf_vectorizer.pk','rb'))
    #tfidf_matrix=sp.load_npz('raw_data/search_tfidf_matrix.npz')
    return tfidf_vectorizer,tfidf_matrix



# Define the search function
def search(query, vector, matrix):
    """
    Compare query to vectorized abstracts, and return top 5 results based on scoring.
    """
    stop_words = stopwords.words('english')

    # Preprocess the query
    query_tokens = word_tokenize(query.lower())
    query_tokens = [token for token in query_tokens if token not in stop_words]
    query = ' '.join(query_tokens)

    # Compute the similarity scores between the query and the abstracts
    query_tfidf = vector.transform([query])
    scores = cosine_similarity(query_tfidf, matrix).flatten()
    ranked_indices = scores.argsort()[::-1]

    # Return the top 5 results
    for i in range(5):
        top5=[]
        paper = data.iloc[ranked_indices[i]]
        top5.append(f'Title: {paper["title"]}\nAuthors: {paper["authors"]}\nYear: {paper["year"]}\nLink: {paper["url"]}\nAbstract: {paper["abstract"]}\n')

    return top5


if __name__ =='__main__':
    vector, matrix = vectorizer(data)
    search(query=input('Enter your query: '), vector=vector, matrix=matrix)
