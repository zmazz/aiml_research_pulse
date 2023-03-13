import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import squarify
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

import nltk
from nltk.corpus import stopwords

#df = pd.read_csv("data_processed_aiml_arxiv_with_cit.csv")
#df.head(5)

#create me a sample of 1000 rows from df and call it df_sample
#df_sample = df.sample(n=3000, random_state=42)

#Part 1 - Top 50 most cited authors

#1 - Preprocessing - Global Criteria
def top_cited_authors_V1(arxiv_df):
    # Group the dataframe by author and sum the number of citations for each author
    author_citations = arxiv_df.groupby('authors')['num_cit'].sum()

    # Sort the authors by the number of citations and return the top 100
    top_authors = author_citations.sort_values(ascending=False)[:100].reset_index()

    return top_authors

def top_cited_authors_V2(arxiv_df):
    # Split the authors by comma and stack them into individual rows
    authors_df = arxiv_df['authors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    authors_df.name = 'author'

    # Combine the new authors dataframe with the original arxiv dataframe
    arxiv_df = arxiv_df.drop('authors', axis=1).join(authors_df)

    # Group the dataframe by author and sum the number of citations for each author
    author_citations = arxiv_df.groupby('author')['num_cit'].sum()

    # Sort the authors by the number of citations and return the top 100
    top_authors = author_citations.reset_index().sort_values(by='num_cit', ascending=False)[:100]

    return top_authors

#top_cited_authors_V1(df_sample)
#top_cited_authors_V2(df_sample)

#2 - Preprocessing - Categorical Criteria
def top_cited_authors_by_category(df, category, k=10):
    # Filter the dataframe by category
    filtered_df = df[df['category'].str.contains(category)]

    # Split the authors by comma and stack them into individual rows
    authors_df = filtered_df['authors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    authors_df.name = 'author'

    # Combine the new authors dataframe with the filtered arxiv dataframe
    filtered_df = filtered_df.drop('authors', axis=1).join(authors_df)

    # Group the filtered dataframe by author and sum the number of citations for each author
    author_citations = filtered_df.groupby(['author', 'category'])['num_cit'].sum()

    # Sort the authors by the number of citations and return the top k
    top_authors = author_citations.reset_index().sort_values(by='num_cit', ascending=False)[:k]

    return top_authors

#top_cited_authors_by_category(df_sample, 'cs.AI')

#Part 2 - Treatment/Logic Function

#1 - Global Criteria
#top_cited_authors= top_cited_authors_V2(df_sample)

def display_top_authors(top_authors, k):
    if k > 100:
        print("Please enter a number less than or equal to 100")
        return None
    else:
        top_authors_bar = top_authors.head(k).set_index('author')
        top_authors_bar = top_authors_bar.reset_index()
        return top_authors_bar

#display_top_authors(top_cited_authors,10)

#2 - Categorical Criteria
def top_cited_authors_by_category(df, category, k=10):
    # Filter the dataframe by category
    filtered_df = df[df['category'].str.contains(category)]

    # Split the authors by comma and stack them into individual rows
    authors_df = filtered_df['authors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    authors_df.name = 'author'

    # Combine the new authors dataframe with the filtered arxiv dataframe
    filtered_df = filtered_df.drop('authors', axis=1).join(authors_df)

    # Group the filtered dataframe by author and sum the number of citations for each author
    author_citations = filtered_df.groupby(['author', 'category'])['num_cit'].sum()

    # Sort the authors by the number of citations and return the top k
    top_authors = author_citations.reset_index().sort_values(by='num_cit', ascending=False)[:k]

    return top_authors

#Part 3 - Visualization Function

#1 - Global Criteria
#top_authors = display_top_authors(top_cited_authors, 50)

def display_bar_chart(df_top_authors):
    df_top_authors = df_top_authors.rename(columns={'num_cit': 'citations'})
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='author', y='citations', data=df_top_authors, ax=ax, palette='viridis')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=10, ha='right')
    ax.set_xlabel('Authors', fontsize=12)
    ax.set_ylabel('Number of citations', fontsize=12)
    ax.set_title('Top cited authors', fontsize=14)
    plt.tight_layout()
    plt.show()

#Graph 1
#display_bar_chart(top_authors)

#2 - Categorical Criteria
#op_authors_by_category = top_cited_authors_by_category(df_sample, 'cs.AI',k=50)

def display_bar_chart(df_top_authors):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='author', y='num_cit', hue='category', data=df_top_authors, ax=ax, palette='viridis')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=10, ha='right')
    ax.set_xlabel('Authors', fontsize=12)
    ax.set_ylabel('Number of citations', fontsize=12)
    ax.set_title('Top cited authors by category', fontsize=14)
    ax.tick_params(axis='x', which='major', pad=15)
    plt.tight_layout()
    plt.show()

#Graph 2
#display_bar_chart(top_authors_by_category)

#Part 4 - Top 50 most keywords

#1 - Preprocessing - Both for Global Criteria and Categorical Criteria
#df_abstract_and_category = df_sample[['category', 'abstract']].copy()
#df_abstract_and_category.reset_index(inplace=True)
#df_abstract_and_category.set_index('index', inplace=True)
#df_abstract_and_category

#2 - Treatment/Logic Function - Global Criteria
def get_top_words_in_general(df, n=10):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['using', 'also', 'results', 'problem', 'paper', 'show'])
    corpus = ' '.join(df['abstract'].fillna('').str.lower())
    tokens = nltk.word_tokenize(corpus)
    filtered_tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    word_freq = nltk.FreqDist(filtered_tokens)
    return word_freq.most_common(n)

#Display the 10 most frequents keywords in the abstracts
#get_top_words_in_general(df_abstract_and_category)

#3 - Treatment/Logic Function - Categorical Criteria
def get_top_words_by_category(df, category=None,k=10):
    # Combine all abstracts into a single string
    if category is None:
        abstracts = ' '.join(df['abstract'].dropna())
    else:
        abstracts = ' '.join(df[df['category'].str.contains(category, na=False)]['abstract'].dropna())

    # Tokenize the string
    tokens = nltk.word_tokenize(abstracts)

    # Filter out stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]

    # Filter out specific words
    filtered_words = ['using', 'also', 'results', 'problem', 'paper', 'show']
    tokens = [token for token in tokens if token not in filtered_words]

    # Get the most common words and their frequencies
    word_freq = Counter(tokens).most_common(k)

    return word_freq

#get_top_words_by_category(df_abstract_and_category,'math.CO cs.CG',50)

#4 - Visualization Function - Categorical Criteria
#top50_keywords_by_global = get_top_words_in_general(df_abstract_and_category,50)
#top50_keywords_by_category = get_top_words_by_category(df_abstract_and_category,'math.CO cs.CG',50)

def display_treemap(top_words):
    word_freq = [x[1] for x in top_words]
    labels = [x[0] for x in top_words]
    colors = [plt.cm.Purples(i/float(len(word_freq))) for i in range(len(word_freq))]

    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    squarify.plot(sizes=word_freq, label=labels, alpha=1, color=colors, text_kwargs={'fontsize':10,'fontweight':'bold'},pad = 0.2, ax=ax)
    plt.axis('off')
    plt.subplots_adjust(left=0.05, right=0.85, top=1, bottom=0.05)

    # create a legend with color mapping to frequency
    freqs = sorted(set(word_freq), reverse=True)
    # create a color map for the frequencies
    cmap = plt.cm.Purples
    normalize = plt.Normalize(vmin=min(freqs), vmax=max(freqs))
    colors = [cmap(normalize(value)) for value in freqs]
    handles = [mpatches.Patch(color=colors[i], label='{0} occurrences'.format(freq)) for i, freq in enumerate(freqs)]

    # create a second axes for the legend
    ax2 = fig.add_axes([0.9, 0.1, 0.05, 0.8])
    ax2.axis('off')
    for i, handle in enumerate(handles):
        rect = mpatches.Rectangle((0, i/len(freqs)), 0.3, 0.8/len(freqs), color=colors[i])
        ax2.add_patch(rect)
        ax2.text(0.35, i/len(freqs)+0.4/len(freqs), handle.get_label(), fontsize=12, transform=ax2.transAxes)

#Graph 3
#display_treemap(top50_keywords_by_category)
