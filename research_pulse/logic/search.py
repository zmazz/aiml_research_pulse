import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
import pickle

# Load the dataset
def load_data():
    """
    Load the dataset from the processed folder
    """
    data = pd.read_csv('~/deepdipper/data/processed/aiml_arxiv_with_cit.csv', low_memory=False)
    return data

def vectorizer(df):
    """
    Vectorize abstracts, and return tfidf_vectorizer and tfidf_matrix to reusage
    """
    #df=df[df['abstract'].notna()]
    # Preprocess the data
    #stop_words = stopwords.words('english')
    #tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    #tfidf_matrix = tfidf_vectorizer.fit_transform(df['abstract'])

    ## instead of loading dataset and redoing vectorization
    tfidf_vectorizer= pickle.load(open('/Users/ziadmazzawi/deepdipper/training_outputs/search_tfidf_vectorizer.pk','rb'))
    tfidf_matrix=sp.load_npz('/Users/ziadmazzawi/deepdipper/training_outputs/search_tfidf_matrix.npz')
    return tfidf_vectorizer,tfidf_matrix

# Define the search function
def search(query, data, vector, matrix):
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

    # Return the top 10 results
    top20=[]
    for i in range(0,20):
        paper = data.iloc[ranked_indices[i]]
        top20=top20+[{'Title': paper["title"],'Authors': paper["authors"],
                    'Year': str(paper["year"]),'Link': paper["url"],'Abstract': paper["abstract"]}]
    return top20

    # Return the top 5 results
    #for i in range(5):
    #    paper = data.iloc[ranked_indices[i]]
    #    print(f'Title: {paper["title"]}\nAuthors: {paper["authors"]}\nYear: {paper["year"]}\nLink: {paper["url"]}\nAbstract: {paper["abstract"]}\n')


if __name__ =='__main__':
    data=load_data()
    vector, matrix = vectorizer(data)
    search(query=input('Enter your query: '), vector=vector, matrix=matrix)
