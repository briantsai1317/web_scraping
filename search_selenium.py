from selenium import webdriver
import time
from bs4 import BeautifulSoup
import random
from selenium.webdriver.chrome.options import Options
from base64 import b64encode


def get_results_selenium(search_term, num_results, location, strlen_key, language_code='en'):

    '''
    Give the rankings of the searched websites and the rankings of specified targets

    Args:
        search_term (str): keyword to search for
        num_results (int): number of results wanted (increment by 10)
        location (str): geographic location to search from
        strlen_key (str): secret key in the uule parameter
        language_code (str): language code to search, default to 'en'

    Return:
        search_items_all (list): list of all scraped site names
        search_urls_all (list): list of URLs corresponding to the sites
        page_all (list): list of page numbers
        cached (list): list of 1's and 0's identifying whether the site is cached

    '''

    # Initialize the lists to store information
    search_items_all = []
    search_urls_all = []
    page_all = []
    cached = []

    # Convert number to pages, roughly 10 results per page
    num_page = num_results//10

    # Settings for the chromedriver
    options = Options()
    options.headless = True

    # Replace spaces with "+"
    search_term_format = search_term.replace(' ', '+')

    # Set up the components for the uule parameter
    ask_canonical = 'w+CAIQICI'
    secret_key = strlen_key.loc[strlen_key[0]==len(location),1].to_string(index=False).strip()
    encode_byte = b64encode(bytes(location,'utf-8'))
    encode_str = str(encode_byte,'ascii','ignore')
    uule = ask_canonical + secret_key + encode_str

    print(f'Searching {search_term} from {location}')

    driver = webdriver.Chrome('/Users/chunantsai/Documents/wcd_course/my_scraping/chromedriver', \
                              options=options)

    counter = 0
    while counter < num_page:

        # Constructing the URL
        # The &start controls the result page, so we don't need to click the 'next' button
        url = f'https://www.google.com/search?q={search_term_format}&hl={language_code}' \
            f'&start={counter*10}&uule={uule}'

        driver.get(url)
        time.sleep(random.randint(2, 6))

        print(f'Scraping Page {counter+1} of {num_page}')
        time.sleep(random.randint(3, 7))

        # Change search settings to correspondong country
        if counter == 0:
            time.sleep(random.randint(2,5))
            settings = driver.find_element_by_id('abar_button_opt')
            settings.click()
            time.sleep(random.randint(1, 3))

            country = '"' + location.split(',')[-1] + '"'
            xpaths = [
                '//*[@id="lb"]/div/a[1]',
                '//*[@id="regionanchormore"]/span[1]',
                f'//*[contains(text(), {country})]',
                '//*[@id="form-buttons"]/div[1]'
            ]
            for xpath in xpaths:
                button = driver.find_element_by_xpath(xpath)
                button.click()
                time.sleep(random.randint(1, 5))

            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(random.randint(2,4))

        time.sleep(random.randint(2,5))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        result_div = soup.find_all('div', attrs={'class': 'r'})

        for tag in result_div:
            search_items_all.append(tag.find('h3').get_text())
            search_urls_all.append(tag.find('a', href=True)['href'])
            print(counter)
            page_all.append(counter + 1)

            # Determine if the sites are hidden (distinguish by keyword 'Cached' in the html)
            if 'Cached' in tag.get_text():
                cached.append(1)
            else:
                cached.append(0)


        # button = driver.find_element_by_id("pnnext")
        # button.click()
        counter += 1
    driver.quit()

    # Return the names, urls, and page of the websites
    return search_items_all, search_urls_all, page_all, cached
