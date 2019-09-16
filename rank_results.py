import pandas as pd
from datetime import datetime

def rank_targets(searches, search_urls, page, cached):
    '''
    Give the rankings of the searched websites and the rankings of specified targets

    Args:
        searches (list): list of searched items from scraping
        search_urls (list): list of corresponding urls
        page (list): list of page numbers
        cached (list): list of 1's and 0's identifying whether the link is cached

    Return:
        all_rankings (dataframe): ranking of each target in searched item in 'searches'

    '''

    # Rankings = index + 1 for all items
    all_rankings = list(range(1,len(searches)+1))

    # Clean '... 'from the dictionaries
    searches = [s.strip('... ') for s in searches]

    # Construct the dataframe from the results
    data_all = {'Name': searches,
                'Rank': all_rankings,
                'Page': page,
                'URL': search_urls,
                'Cached': cached
    }
    data_all['Date'] = datetime.now().now()

    df_all = pd.DataFrame.from_dict(data_all)

    return df_all
