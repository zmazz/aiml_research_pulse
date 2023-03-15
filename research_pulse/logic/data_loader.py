### Imports
import pandas as pd
import json
import dask.bag as db

### Load cleaned and merged  dataset
def load_data():
    """
    Load the dataset from the processed folder
    """
    # data = pd.read_csv('~/deepdipper/data/processed/aiml_arxiv_with_cit.csv', low_memory=False)

    import gcsfs

    fs = gcsfs.GCSFileSystem(project='deepdipper')
    with fs.open('deepdipper_data/data/processed/aiml_arxiv_with_cit.csv') as f:
        data = pd.read_csv(f)

    return data

##########################################
# OR THIS from original dataframe in json format
def dataset_creator_local():

    aiml_category_list=['cond-mat.dis-nn','cond-mat.stat-mech','cond-mat.str-el','cs.AI',
                    'cs.CE','cs.CG','cs.CL','cs.CR','cs.CV','cs.CY','cs.DB','cs.DC',
                    'cs.DL','cs.DM','cs.DS','cs.ET','cs.FL','cs.GL','cs.GT','cs.HC',
                    'cs.IR','cs.IT','cs.LG','cs.LO','cs.MA','cs.MS','cs.NA','cs.NE',
                    'cs.NI','cs.RO','cs.SI','econ.EM','eess.AS','eess.IV','eess.SP',
                    'math.CA','math.CT','math.DS','math.FA','math.GN','math.NA',
                    'math.OC','math.PR','math.RT','math.ST','nlin.AO','nlin.CD',
                    'stat.AP','stat.CO','stat.ME','stat.ML','stat.OT','stat.TH']

    records=db.read_text("~/deepdipper/data/raw/arxiv-metadata-oai-snapshot.json").map(lambda x:json.loads(x))
    ai_docs = (records.filter(lambda x:any(ele in x['categories'] for ele in aiml_category_list)==True))

    get_metadata = lambda x: {'id': x['id'],
                    'title': x['title'],
                    'category':x['categories'],
                    'authors':x['authors'],
                    'url': f"https://arxiv.org/pdf/{x['id']}.pdf",
                    'journal_ref':x['journal-ref'],
                    'abstract':x['abstract'],
                    'version':x['versions'][-1]['created'],
                            'doi':x["doi"],
                            'authors_parsed':x['authors_parsed']}

    data=ai_docs.map(get_metadata).to_dataframe().compute()
    # OR THIS
    #data=pd.read_csv("~/deepdipper/data/raw/AI_ML_ArXiv_Papers.csv",low_memory=False)

    ### Load citation dataset
    with open("/tmp/internal-citations.json") as f:
        citations = json.load(f)

    with open("arxiv-metadata-ext-citation.csv","w+") as f_out :
        f_out.write("id,id_reference\n")
        for i,id in enumerate(citations):
            for k in citations[id]:
                f_out.write(f'{id},{k}\n')

    df_citations = pd.read_csv("~/deepdipper/data/raw/arxiv-metadata-ext-citation.csv",dtype={"id":object,"id_reference":object})

    ##########################################
    ### Data preprocessing
    # extract the Date Time Information
    data['DateTime']=pd.to_datetime(data['version'])
    # convert DateTime column to datetime type
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    # extract date features
    data['year'] = data['DateTime'].dt.year
    data['month'] = data['DateTime'].dt.month
    data['day'] = data['DateTime'].dt.day
    data['hour'] = data['DateTime'].dt.hour
    data['minute'] = data['DateTime'].dt.minute
    # cleaning the authors_parsed column
    data['num_authors']=data['authors_parsed'].apply(lambda x:len(x))
    data['authors']=data['authors_parsed'].apply(lambda authors:[(" ".join(author)).strip() for author in authors])
    # citation aggregation per paper
    df_citcount=pd.DataFrame(df_citations['id'].value_counts())

    ##########################################
    ### Return aggregate dataframe
    df=pd.merge(data,df_citcount,how='left',left_on='id',right_index=True)
    df.rename(columns={'id_x':'id','id_y':'num_cit'},inplace=True)
    df['id']=df['id'].astype(str)
    df['num_cit']=df['num_cit'].fillna(0)
    return df
