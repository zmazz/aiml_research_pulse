import pandas as pd 
import numpy as np 
from datetime import datetime
import sys
import ast

import plotly_express as px

import nltk
from nltk.corpus import stopwords
import spacy

import matplotlib.pyplot as plt
import seaborn as sns

import json
import dask.bag as db
import utils

df = pd.read_csv('/Users/benedictvonbismarck-osten/code/benedict007/zmazz/Project/toto.csv')
df = df.sample(n = 1000)

#Most cited authors
def most_cited_df(number):
    try:
        return df.sort_values('num_cit', ascending=False).head(number)
    except:
        print('Please enter a valid number')
most_cited_df(50)

# Growth in Field of ML AI 
def growth_of_ai_ml_over_years():
    
    papers_over_years=df.groupby(['year']).size().reset_index().rename(columns={0:'Number Of Papers Published'})
    return px.line(x="year",y="Number Of Papers Published",data_frame=papers_over_years,title="Growth of AI ML over the Years")

#Graph 1
growth_of_ai_ml_over_years()

# Papers Published Over the Month
def papers_published_over_the_month():
    papers_published_over_days=df.groupby(['day']).size().reset_index().rename(columns={0:'Papers Published over the Month'})
    return px.line(x="day",y="Papers Published over the Month",data_frame=papers_published_over_days,title="Average Papers Published Over the Month")

#Graph 2   
papers_published_over_the_month()

def papers_published_over_the_year():
    papers_published_over_days=df.groupby(['month']).size().reset_index().rename(columns={0:'Number of Papers Published over the Year'})
    return px.line(x="month",y="Number of Papers Published over the Year",data_frame=papers_published_over_days,title="Average Papers Published Over the Year")
    
#Graph 3
papers_published_over_the_year()

def papers_published_over_the_day():
    papers_published_over_days=df.groupby(['hour']).size().reset_index().rename(columns={0:'Number of Papers Published over the Day'})
    return px.line(x="hour",y="Number of Papers Published over the Day",data_frame=papers_published_over_days,title="Average Papers Published Over the Day")
    
#Graph 4
papers_published_over_the_day()