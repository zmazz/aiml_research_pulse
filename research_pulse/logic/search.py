import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
import pickle
import research_pulse.logic.data_loader as dl

def vectorizer(df):
    """
    Vectorize abstracts, and return tfidf_vectorizer and tfidf_matrix to reusage
    """
    #df=df[df['abstract'].notna()]
    # Preprocess the data
    #stop_words = stopwords.words('english')
    #tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    #tfidf_matrix = tfidf_vectorizer.fit_transform(df['abstract'])

    tfidf_vectorizer= pickle.load(open('/Users/ziadmazzawi/deepdipper/training_outputs/search_tfidf_vectorizer.pk','rb'))
    tfidf_matrix=sp.load_npz('/Users/ziadmazzawi/deepdipper/training_outputs/search_tfidf_matrix.npz')

    # import gcsfs
    # fs = gcsfs.GCSFileSystem(project='deepdipper')
    # with fs.open('deepdipper_data/training_outputs/search_tfidf_vectorizer.pk', 'rb') as f:
    #     tfidf_vectorizer = pickle.load(f)
    # with fs.open('deepdipper_data/training_outputs/search_tfidf_matrix.npz') as g:
    #     tfidf_matrix = sp.load_npz(g)

    return tfidf_vectorizer,tfidf_matrix

# Define the search function
def search(query, data, vector, matrix):
    """
    Compare query to vectorized abstracts, and return top 20 results based on scoring.
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

    # Return the top 20 results
    top20=[]
    for i in range(0,20):
        paper = data.iloc[ranked_indices[i]]
        top20=top20+[{'Title': paper["title"],'Authors': paper["authors"],'Id': paper["id"],
                        'Year': str(paper["year"]),'Link': paper["url"],'Category':paper['category'],
                        'Number_citations':str(paper['num_cit']),'Abstract': paper["abstract"]}]

    return {f'{i}': d for i, d in enumerate(top20)}

    # Return the top 5 resultsgit add .
    #for i in range(5):
    #    paper = data.iloc[ranked_indices[i]]
    #    print(f'Title: {paper["title"]}\nAuthors: {paper["authors"]}\nYear: {paper["year"]}\nLink: {paper["url"]}\nAbstract: {paper["abstract"]}\n')


if __name__ =='__main__':
    data=dl.load_data()
    vector, matrix = vectorizer(data)
    search(query=input('Enter your query: '), vector=vector, matrix=matrix)
