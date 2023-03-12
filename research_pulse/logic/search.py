import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
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

    ## instead of loading dataset and redoing vectorization
    #tfidf_vectorizer= pickle.load(open('/Users/ziadmazzawi/deepdipper/training_outputs/search_tfidf_vectorizer.pk','rb'))
    #tfidf_matrix=sp.load_npz('/Users/ziadmazzawi/deepdipper/training_outputs/search_tfidf_matrix.npz')
    import gcsfs
    fs = gcsfs.GCSFileSystem(project='deepdipper')
    with fs.open('deepdipper_data/training_outputs/search_tfidf_vectorizer.pk', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    with fs.open('deepdipper_data/training_outputs/search_tfidf_matrix.npz') as g:
        tfidf_matrix = sp.load_npz(g)

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
    return {'#1': top20[0], '#2': top20[1], '#3': top20[2], '#4': top20[3], '#5': top20[4],
            '#6': top20[5], '#7': top20[6], '#8': top20[7], '#9': top20[8], '#10': top20[9],
            '#11': top20[10], '#12': top20[11], '#13': top20[12], '#14': top20[13], '#15': top20[14],
            '#16': top20[15], '#17': top20[16], '#18': top20[17], '#19': top20[18], '#20': top20[19]}

    # Return the top 5 resultsgit add .
    #for i in range(5):
    #    paper = data.iloc[ranked_indices[i]]
    #    print(f'Title: {paper["title"]}\nAuthors: {paper["authors"]}\nYear: {paper["year"]}\nLink: {paper["url"]}\nAbstract: {paper["abstract"]}\n')


if __name__ =='__main__':
    data=dl.load_data()
    vector, matrix = vectorizer(data)
    search(query=input('Enter your query: '), vector=vector, matrix=matrix)
