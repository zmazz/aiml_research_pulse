import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import research_pulse.logic.search as ls
import research_pulse.logic.data_loader as dl
import research_pulse.logic.r_papers as lrp
import research_pulse.logic.data_loader as dl

app = FastAPI()

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/search?query=bayesian-neural-networks
@app.get("/search")
def search(query: str):  # "bayesian neural networks" / "adam optimizers" / ...
    """
    Calls search function from logic/search.py and returns the top 20 results in list of str format.
    """

    data=dl.load_data()

    vector, matrix = ls.vectorizer(data)
    top20=ls.search(query.lower(), data, vector, matrix)

    return top20

# https://deepdipper-rp6v7d7m4q-ew.a.run.app/research_paper?query=0704%2E0672%2F
@app.get("/research_paper")
def research_paper(query: float):  # 704.0193/ / ...
    """
    Calls research_paper function from logic/r_papers.py and returns line in dataset of paper.
    """

    data=dl.load_data()

    paper_info=lrp.get_paper(str(query), data)

    return paper_info



@app.get("/")
def root():
    return {'greeting':'Hello'}
