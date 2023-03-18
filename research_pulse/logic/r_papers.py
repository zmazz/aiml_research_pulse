import pandas as pd
import research_pulse.logic.data_loader as dl

def get_paper(query: str, df: pd.DataFrame):
    """
    Get a row from the ArXiv dataset by ID
    """

    try :
        lst=df.loc[df['id']==query].to_dict(orient='records')
        results=[]
        for paper in lst:
            results=results+[{'Title': paper["title"],'Authors': paper["authors"],'Id': paper["id"],
                        'Year': str(paper["year"]),'Link': paper["url"],'Category':paper['category'],
                        'Number_citations':str(paper['num_cit']),'Abstract': paper["abstract"]}]

        return {f'{i}': d for i, d in enumerate(results)}
    except:
        return {"error": "Paper not found with this ID"}


def get_citations(paper_id: str, df_cit: pd.DataFrame, df: pd.DataFrame):
    """
    Get citing papers ids from the ArXiv dataset by paper id
    """

    try :
        citing_ids=df_cit[df_cit['id'].str.contains(paper_id)]['id_reference'].tolist()
        lst=[]
        for citing_id in citing_ids:
            lst.append(df.loc[df['id']==citing_id].to_dict(orient='records'))
        results=[]
        for citing_paper in lst:
            results=results+[{'Title': citing_paper[0]["title"],'Authors': citing_paper[0]["authors"],'Id': citing_paper[0]["id"],
                        'Year': str(citing_paper[0]["year"]),'Link': citing_paper[0]["url"],'Category':citing_paper[0]['category'],
                        'Number_citations':str(citing_paper[0]['num_cit']),'Abstract': citing_paper[0]["abstract"]}]
        return {f'{i}': d for i, d in enumerate(results)}

    except:
        return {"error": "No citing paper found"}



if __name__ =='__main__':
    data=dl.load_data()
    get_paper(query=str(input('Enter paper id: ')), df=data)
