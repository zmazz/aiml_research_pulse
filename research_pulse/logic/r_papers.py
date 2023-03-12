import pandas as pd
import research_pulse.logic.data_loader as dl

def get_paper(query, df):
    row_paper = df[df['id'] == str(query)]
    if not row_paper.empty:
        return {
            'id': row_paper.iloc[0]['id'],
            'title': row_paper.iloc[0]['title'],
            'authors': row_paper.iloc[0]['authors'],
            'abstract': row_paper.iloc[0]['abstract'],
            'year': row_paper.iloc[0]['year'],
            'month': row_paper.iloc[0]['month'],
            'num_cit': row_paper.iloc[0]['num_cit'],
            'category': row_paper.iloc[0]['category'],
            'url': row_paper.iloc[0]['url'],
            'journal_ref': row_paper.iloc[0]['journal_ref'],
            'doi': row_paper.iloc[0]['doi']
        }
    else:
        return {
            'error': 'Paper not found'
        }

if __name__ =='__main__':
    data=dl.load_data()
    get_paper(query=str(input('Enter paper id: ')), df=data)
