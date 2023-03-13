import pandas as pd
import research_pulse.logic.data_loader as dl

def get_paper(paper_id: str, df: pd.DataFrame):
    """
    Get a row from the ArXiv dataset by ID
    """
    try :
        #return df.loc[df['id']==str(paper_id)].iloc[0].to_dict(orient='records')
        #return df.loc[df['id']==str(paper_id)].iloc[0].to_dict()
        paper=df[df['id'] == str(paper_id)].to_dict('records')[0]
        result={'Title': paper["title"],'Authors': paper["authors"],'Year': str(paper["year"]),'Link': paper["url"],'Abstract': paper["abstract"]}
        return result
    except:
        return {"error": "Paper not found"}


if __name__ =='__main__':
    data=dl.load_data()
    get_paper(query=str(input('Enter paper id: ')), df=data)
