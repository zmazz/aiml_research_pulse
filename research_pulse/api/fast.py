import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    import research_pulse.logic.search as ls
    data=ls.load_data()
    vector, matrix = ls.vectorizer(data)
    top20=ls.search(query.lower(), data, vector, matrix)
    return top20


@app.get("/")
def root():
    return {'greeting':'Hello'}
