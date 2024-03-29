import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import research_pulse.logic.search as ls
import research_pulse.logic.data_loader as ldl
import research_pulse.logic.r_papers as lrp
import research_pulse.logic.r_authors as lra
import research_pulse.logic.t_translate as ltt
import research_pulse.logic.t_summarize as lts

app = FastAPI()

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

df,df_cit=ldl.load_data()
vector, matrix = ls.vectorizer(df)
marian_tokenizer, marian_model = ltt.load_marian_model()
bart_tokenizer,bart_model,bart_config=lts.load_bart_model()


# http://deepdipper-rp6v7d7m4q-ew.a.run.app/search?query=bayesian-neural-networks
@app.get("/search")
def search(query: str,result_type: str):  # "bayesian neural networks" / "adam optimizers" / ...
    """
    Calls search function from logic/search.py and returns the top 50 results in list of str format.
    """
    # Search for the query
    top50=ls.search(query.lower(), result_type, df, vector, matrix)
    # Return the top 50 results
    return top50

# http://deepdipper-rp6v7d7m4q-ew.a.run.app/papers?query=704-0019
@app.get("/papers")
def get_paper(query: str):
    """
    Get a row from the ArXiv dataset by ID (with - instead of .)
    """
    paper_details = lrp.get_paper(query, df)
    return paper_details

# http://deepdipper-rp6v7d7m4q-ew.a.run.app/authors?query=theran-louis
@app.get("/citations")
def get_citations(query: str):
    """
    Get author appearances from the ArXiv dataset by name
    """
    citing_papers=lrp.get_citations(query, df_cit, df)
    return citing_papers

# http://deepdipper-rp6v7d7m4q-ew.a.run.app/authors?query=theran-louis
@app.get("/authors")
def get_author(query: str):
    """
    Get author appearances from the ArXiv dataset by name
    """
    author_occ=lra.get_author(query, df)
    return author_occ

# http://deepdipper-rp6v7d7m4q-ew.a.run.app/translatefr?query=704-0019
@app.get("/translatefr")
def translate_fr(query: str):
    """
    Get author appearances from the ArXiv dataset by name
    """
    text_translated=ltt.translate_fra(query, df, marian_tokenizer, marian_model)
    return text_translated

@app.get("/translatees")
def translate_es(query: str):
    """
    Get author appearances from the ArXiv dataset by name
    """
    text_translated=ltt.translate_esp(query, df, marian_tokenizer, marian_model)
    return text_translated

@app.get("/translatepo")
def translate_po(query: str):
    """
    Get author appearances from the ArXiv dataset by name
    """
    text_translated=ltt.translate_por(query, df, marian_tokenizer, marian_model)
    return text_translated

# http://deepdipper-rp6v7d7m4q-ew.a.run.app/summarize?query=704-0019
@app.get("/summarize")
def summarize(query: str):
    """
    Get abstract summary from the ArXiv dataset by ID
    """
    text_translated=lts.summarizer(query, df, bart_tokenizer, bart_model,bart_config)
    return text_translated

@app.get("/")
def root():
    return {'greeting':'Hello, welcome to the DeepDipper API!'}
