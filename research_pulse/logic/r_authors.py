import pandas as pd
import research_pulse.logic.data_loader as dl

def get_author(author: str, df: pd.DataFrame):
    """
    Get author appearances from the ArXiv dataset by name
    """
    author_processed = author.replace("-", " ").title()
    try :
        lst=df.loc[df['authors'].str.contains(author_processed)].to_dict(orient='records')
        results=[]
        for paper in lst:
            results=results+[{'Title': paper["title"],'Authors': paper["authors"],
                        'Year': str(paper["year"]),'Link': paper["url"],'Abstract': paper["abstract"]}]

        return {f'{i}': d for i, d in enumerate(results)}
    except:
        return {"error": "Author not found"}

if __name__ =='__main__':
    data=dl.load_data()
    get_author(query=str(input('Enter author(s) name: ')), df=data)
