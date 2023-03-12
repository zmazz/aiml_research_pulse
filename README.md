# aiml_research_pulse
----------------->>> Assistive explorer of AI/ML-related research papers <<<-----------------

## Data
- arXiv database of ~2.2m research papers from 1991 to today.\
- skimmed for AI/ML-related papers: ~774k kept from 2000.


## Project architecture
Dashboard analytics:
- subpages: global views / ranking
- user inputs: aggregate or category {&} last 1y, 5y or 23y
- source & services: GCS then GBQ {&} GCE {&} streamlit
- associated worksheets: app.py (interface), dashboard.py (logic)

Search:
- user inputs: query {&} number (top n) {&} criteria (scoring method)
- source & services: GCS then GBQ {&} GCE {&} streamlit
- associated worksheets: app.py (interface), search.py (logic), fast.py (api)

Research:
- subpages: papers / authors / citations parsers
- user inputs: paper id or author name or category
- sources & services: GCS then GBQ {&} GCE {&} Fast API then GBQ {&} streamlit {&} prefect (for citations)
- associated worksheets: app.py (interface), r_papers.py (logic), r_authors.py (logic), r_citations.py (logic), r_recommend.py (logic)

Tools:
- subpages: translation / summarization / topic alert bot
- user inputs: paper id or category
- sources & services: GCS {&} GCE {&} Fast API {&} streamlit {&} prefect (for bot)
- associated worksheets: app.py (inteface), t_translate.py (logic), t_summarize.py (logic), t_alert.py (logic), fast.py (api)

## Folder tree:
 as of 11.03.2023:

├── Dockerfile\
├── LICENSE\
├── Makefile\
├── README.md\
├── requirements.txt\
├── research_pulse\
│   ├── api\
│   │   └── fast.py\
│   ├── interface\
│   │   ├── app.py\
│   │   └── main.py\
│   ├── logic\
│   │   ├── dashboard.py\
│   │   ├── data_loader.py\
│   │   ├── r_authors.py\
│   │   ├── r_citations.py\
│   │   ├── r_papers.py\
│   │   ├── r_recommendation.py\
│   │   ├── search.py\
│   │   ├── t_alert.py\
│   │   ├── t_summarize.py\
│   │   └── t_translate.py\
│   ├── params.py\
│   └── utils.py\
├── setup.py\
└── tests

## Team
Bene\
Ibra\
Sam\
Ziad

with help from TAs: \
Charlotte, Romain, Adrien, Elizabeth, Charles...

## Roadmap

## Environment preparation

## Bibliography
