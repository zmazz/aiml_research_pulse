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




    # title_processed = title.replace("-", " ")
    # checker = df['title'].str.contains(title_processed, case=False)
    # index_first_true=checker.idxmax()
    # try :
    #     #return df.loc[df['id']==str(paper_id)].iloc[0].to_dict(orient='records')
    #     #return df.loc[df['id']==str(paper_id)].iloc[0].to_dict()
    #     paper = df.iloc[index_first_true].to_dict()
    #     result={'Title': paper["title"],'Authors': paper["authors"],
    #                     'Year': str(paper["year"]),'Link': paper["url"],'Category(-ies)':paper['category'],
    #                     'Number_citations':paper['num_cit'],'Abstract': paper["abstract"]}
    #     return result
    # except:
    #     return {"error": "Paper not found"}


if __name__ =='__main__':
    data=dl.load_data()
    get_paper(query=str(input('Enter paper id: ')), df=data)
