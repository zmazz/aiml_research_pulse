import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


df = pd.read_csv("data_processed_aiml_arxiv_with_cit.csv")

#Part 1 - Evolution of the number of publications during the years(by Global and Category)

#1 - Preprocessing functions
df_sample = df.sample(n=3000, random_state=42)

#Global creteria - Preprocessing
def get_publications_per_year(dataframe):
    # convert year column to datetime format
    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y')
    # group by year and count number of publications
    publications_per_year = dataframe.groupby(dataframe['year'].dt.year)['id'].count().reset_index()
    # rename columns
    publications_per_year.columns = ['year', 'publications']
    # return dataframe
    return publications_per_year

get_publications_per_year(df_sample)

#Categorical creteria - Preprocessing
def get_publications_per_year_and_category(dataframe):
    # convert year column to datetime format
    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y')
    # group by year and category and count number of publications
    publications_per_year_and_category = dataframe.groupby([dataframe['year'].dt.year, 'category'])['id'].count().reset_index()
    # rename columns
    publications_per_year_and_category.columns = ['year', 'category', 'publications']
    # return dataframe
    return publications_per_year_and_category

#2 - Treatment functions
publications_per_year= get_publications_per_year(df_sample)

#Global creteria - Treatment
def get_publications_by_time_range(dataframe, start_year, end_year):
    # convert year column to datetime format
    dataframe['year'] = pd.to_datetime(dataframe['year'], format='%Y')
    # filter dataframe to specified time range
    time_range = (dataframe['year'] >= pd.Timestamp(str(start_year))) & (dataframe['year'] <= pd.Timestamp(str(end_year)))
    filtered_df = dataframe.loc[time_range]
    # group by year and count number of publications
    publications_by_year = filtered_df.groupby(filtered_df['year'].dt.year)['publications'].sum().reset_index()
    # rename columns
    publications_by_year.columns = ['year', 'publications']
    # return dataframe
    return publications_by_year

get_publications_by_time_range(publications_per_year, 2010, 2019)

#Categorical creteria - Treatment
publications_per_year_and_category= get_publications_per_year_and_category(df_sample)

def get_publications_by_category_and_time_range(dataframe, start_year, category, end_year):
    # filter dataframe by time range and category
    filtered_df = dataframe[(dataframe['year'].between(start_year, end_year)) & (dataframe['category'].str.contains(category))]
    # group by year and count number of publications
    publications_by_year = filtered_df.groupby(['year', 'category'])['publications'].sum().reset_index()
    # return dataframe
    return publications_by_year

publications_by_category_and_time_range = get_publications_by_category_and_time_range(publications_per_year_and_category, 2010, 'math.NA', 2019)
publications_by_category_and_time_range

#3 - Data Visualization

#Global creteria - Data Visualization
publications_per_year_visualization = get_publications_by_time_range(publications_per_year, 2010, 2019)

import seaborn as sns
import matplotlib.pyplot as plt

def plot_publications_per_year(dataframe):
    plt.figure(figsize=(18,10))
    sns.set_style("whitegrid")
    ax = sns.lineplot(data=dataframe, x="year", y="publications", color="blue")
    ax.set_title("Number of Publications per Year", fontsize=18)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Publications", fontsize=14)
    plt.show()

#Graph 1
plot_publications_per_year(publications_per_year_visualization)

#Categorical creteria - Data Visualization

#Let's stock the ouput of the corresponding treatment function in a variable called publications_per_year_visualization
publications_by_category_and_time_range = get_publications_by_category_and_time_range(publications_per_year_and_category, 2010, 'math.NA', 2019)

def scatterplot_publications_by_category_and_size(dataframe):
     # set plot style
    sns.set(style="whitegrid")
    # plot scatter plot
    ax = sns.scatterplot(data=dataframe, x="year", y="publications", size="publications", hue="category", sizes=(20, 400))
    # set x-axis label
    ax.set_xlabel("Year")
    # set y-axis label
    ax.set_ylabel("Number of Publications")
    # set plot title
    ax.set_title("Number of Publications by Year and Category")
    # set legend outside plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # show plot
    plt.show()

#Graph 2
scatterplot_publications_by_category_and_size(publications_by_category_and_time_range)

#Part 2 - Count of publications and citations

#Count of publications and citations
#create me a sample of 3000 rows from df and call it df_sample_2
df_sample_2 = df.sample(n=3000, random_state=42)

#1 - Global creteria - Preprocessing
def get_publications_and_citations_per_year(dataframe):
    """
    Returns a new dataframe with the number of publications and citations per year.

    :param dataframe: pandas dataframe with columns 'year' and 'num_cit'.
    :return: pandas dataframe with columns 'year', 'publications', and 'citations'.
    """
    publications_per_year = dataframe.groupby('year')['id'].count().reset_index()
    citations_per_year = dataframe.groupby('year')['num_cit'].sum().reset_index()
    result = publications_per_year.merge(citations_per_year, on='year')
    result.columns = ['year', 'publications', 'citations']
    return result

get_publications_and_citations_per_year(df_sample_2)

#2 - Categorical creteria - Preprocessing
def get_publications_and_citations_by_year_and_category(dataframe):
    pubs_cits_by_year_and_cat = dataframe.groupby(['year', 'category']).agg({'id': 'count', 'num_cit': 'sum'})
    pubs_cits_by_year_and_cat = pubs_cits_by_year_and_cat.reset_index()
    pubs_cits_by_year_and_cat.columns = ['year', 'category', 'publications', 'citations']
    return pubs_cits_by_year_and_cat

get_publications_and_citations_by_year_and_category(df_sample_2)

#Part 3 - Treatment/Logic Functions

#1 - Global creteria - Treatment
publications_and_citations_per_year = get_publications_and_citations_per_year(df_sample_2)

def get_publications_and_citations_by_time_range(dataframe, start_year, end_year):
    filtered_df = dataframe[(dataframe['year'] >= start_year) & (dataframe['year'] <= end_year)]
    publications_by_year = filtered_df.groupby('year')['publications'].sum()
    citations_by_year = filtered_df.groupby('year')['citations'].sum()
    result_df = pd.concat([publications_by_year, citations_by_year], axis=1).reset_index()
    return result_df

get_publications_and_citations_by_time_range(publications_and_citations_per_year,2010,2019)

#2 - Categorical creteria - Treatment
publications_and_citations_per_year_and_category = get_publications_and_citations_by_year_and_category(df_sample_2)

def get_publications_and_citations_by_category_and_time_range(dataframe, start_year, end_year, category):
    mask = (dataframe['year'] >= start_year) & (dataframe['year'] <= end_year) & (dataframe['category'].str.contains(category))
    filtered_df = dataframe[mask]
    grouped_df = filtered_df.groupby(['category', 'year']).agg({'publications': 'sum', 'citations': 'sum'}).reset_index()
    return grouped_df

get_publications_and_citations_by_category_and_time_range(publications_and_citations_per_year_and_category, 2010, 2019, 'cs.AI')

#Part 4 - Data Visualization

#Global creteria - Data Visualization
publications_and_citations_by_year_time_range = get_publications_and_citations_by_time_range(publications_and_citations_per_year,2010,2019)

import seaborn as sns

def scatterplot_citations_vs_publications(df):
    plt.figure(figsize=(16, 12))
    sns.scatterplot(x='citations', y='publications', hue='year', data=df, palette='deep', s=300)
    plt.title('Citations vs Publications', fontsize=18)
    plt.xlabel('Citations', fontsize=14)
    plt.ylabel('Publications', fontsize=14)
    plt.show()

#Graph 3
scatterplot_citations_vs_publications(publications_and_citations_by_year_time_range)

#Categorical creteria - Data Visualization
publications_and_citations_by_category_year_time_range = get_publications_and_citations_by_category_and_time_range(publications_and_citations_per_year_and_category, 2010, 2019, 'cs.AI')



def scatterplot_by_category_year_shape(publications_and_citations_by_category_year):
    # Create a dictionary to map category to color
    category_color_map = {}
    categories = publications_and_citations_by_category_year["category"].unique()
    num_categories = len(categories)
    color_map = plt.get_cmap("Set1")
    for i in range(num_categories):
        category_color_map[categories[i]] = color_map(i / num_categories)

    # Create a dictionary to map year to shape marker
    year_marker_map = {}
    years = publications_and_citations_by_category_year["year"].unique()
    num_years = len(years)
    marker_map = ["o", "s", "d", "^", "v", ">", "<", "P", "X", "H"]
    for i in range(num_years):
        year_marker_map[years[i]] = marker_map[i % len(marker_map)]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Iterate over each row of the dataframe and plot the point
    for index, row in publications_and_citations_by_category_year.iterrows():
        category = row["category"]
        x = row["citations"]
        y = row["publications"]
        year = row["year"]
        marker = year_marker_map[year]
        color = category_color_map[category]
        ax.scatter(x, y, s=150, marker=marker, color=color)

    # Set the axis labels and title
    ax.set_xlabel("Citations")
    ax.set_ylabel("Publications")
    ax.set_title("Publications and Citations by Category and Year")

    # Create a legend for category color and year marker mapping
    handles = []
    labels = []
    for category in categories:
        color = category_color_map[category]
        handles.append(plt.Line2D([], [], linestyle="", marker="o", color=color))
        labels.append(category)
    for year in years:
        marker = year_marker_map[year]
        handles.append(plt.Line2D([], [], linestyle="", marker=marker, color="black"))
        labels.append(year)
    ax.legend(handles, labels, loc="center left", bbox_to_anchor=(1, 0.5))

    # Show the plot
    plt.show()

#Graph 4
scatterplot_by_category_year_shape(publications_and_citations_by_category_year_time_range)
