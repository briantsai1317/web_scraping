import rank_results
import requests
import search_selenium
import pandas as pd
import time
import random

'''
    Main file that runs the scraping algorithm
'''


def google_rank(search_term, num_results, location, strlen_key, language_code='en'):

    try:
        search_items, search_urls, page, cached = search_selenium.get_results_selenium(search_term,\
                                                        num_results, location, strlen_key, language_code)
        all_rankings = rank_results.rank_targets(search_items, search_urls, page, cached)
        return all_rankings
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("Blocked by Google")


if __name__ == '__main__':

    # Number of results wanted - increment by 10
    num_results = 100
    language_code = 'en'
    filepath = '/Users/chunantsai/Documents/wcd_course/my_scraping/'

    # The file contains search keywords
    search_file = 'search_words_test.csv'
    search_term = pd.read_csv(filepath+search_file,header=None).values[:, 0]


    # The file contains secret key for the uule parameter
    strlen_file = 'strlen_key.csv'
    strlen_key = pd.read_csv(filepath+strlen_file, header=None)

    # The file contains the canonical names of the locations
    location_file = 'canonical_names_test.csv'
    location_lists = pd.read_csv(filepath+location_file, sep=';', header=None).values[:, 0]

    for location in location_lists:
        for term in search_term:
            try:
                data_all = google_rank(term, num_results, language_code,\
                                       location, strlen_key)
                data_all['Keyword'] = term
                data_all['Location'] = location

                all_file = 'rankings.csv'
                with open(filepath+all_file, 'a') as f:
                    data_all.to_csv(f, header=None)
            except Exception as e:
                print(e)
            finally:
                print(f'Appending data of shape {data_all.shape}')

            # Randomized sleep time to avoid blocking(?)
            time.sleep(random.randint(10,20))
    time.sleep(random.randint(25,35))

