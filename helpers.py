import csv
from time import sleep
from selenium import webdriver


def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage') 

    driver = webdriver.Chrome(chrome_options=options)
    return driver

def connect_to_base(browser, url):
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(url)
            return True
        except Exception as ex:
            connection_attempts += 1
            sleep(2)
            print(f'Error connecting to {url}.')
            print(f'Exception:  {ex}')
            print(f'Attempt #{connection_attempts}.')
    return False


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def write_to_article_urls_file(output_list):
    with open('urls.csv', 'a') as csvfile:
        fieldnames = ['a', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in output_list:
            d = {
                'a': '1',
                'url': row
            }
            writer.writerow(d)

def get_articles_to_process_list():
    data = []
    with open('urls.csv', 'r') as csvfile:
        fieldnames = ['a', 'url']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        data = list(reader)
    return data


def write_pages_to_file(pages):
    with open('pages.csv', 'a') as csvfile:
        fieldnames = ['section_url', 'volume', 'page_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in pages:
            writer.writerow(row)

def load_pages_from_file():
    data = []
    with open('pages.csv', 'r') as csvfile:
        fieldnames = ['section_url', 'volume', 'page_number']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        data = list(reader)
    return data


def write_processed_articles_to_file(articles):
    with open('articles.csv', 'a', newline='') as csvfile:
        fieldnames = ['url', 'title', 'journal_name', 'publish_date', 'data_available']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in articles:
            writer.writerow(row)

def get_processed_articles_list():
    data = []
    with open('articles.csv', 'r') as csvfile:
        fieldnames = ['url', 'title', 'journal_name', 'publish_date', 'data_available']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        data = list(reader)
    return data
