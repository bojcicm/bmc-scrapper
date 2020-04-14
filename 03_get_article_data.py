import time
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, wait, ThreadPoolExecutor, as_completed
from typing import List

from parsers import process_article_for_soup
from helpers import get_driver, connect_to_base, get_articles_to_process_list, get_processed_articles_list, batch, write_processed_articles_to_file

def run_get_page_articles_process_batch(urls):
    browser = get_driver()
    articles = []
    for url in urls:
        print(f'Parsing article {url}')
        if connect_to_base(browser, url):
            time.sleep(1)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            article = process_article_for_soup(soup, url)
            articles.append(article)
        else:
            print('Error connecting to bmc')

    browser.quit()
    return articles

if __name__ == '__main__':
    futures = []
    article_urls = []

    
    print(f'Loading article urls...')
    article_urls = get_articles_to_process_list()
    total_articles = len(article_urls)
    processed_articles = get_processed_articles_list()
    total_processed = len(processed_articles)
    print()
    print(f'Urls loaded: {total_articles}')
    print(f'Processed:   {total_processed}')
    print()

    urls_to_process = [art['url'] for art in article_urls]
    print(len(urls_to_process))
    for done_art in processed_articles:
        if done_art['url'] in urls_to_process:
            urls_to_process.remove(done_art['url'])

    print(f'Starting reading article...')
    with ProcessPoolExecutor(4) as executor:
        for article_url_batch in batch(urls_to_process, 20):
            urls = [url for url in list(article_url_batch)]
            futures.append(executor.submit(run_get_page_articles_process_batch, urls))
    
        for future in as_completed(futures):
            result = future.result()
            if result is None:
                print('Article process result is None')
            else:
                print(f'Writing {len(result)} articles to articles file')
                total_processed = total_processed + len(result)
                write_processed_articles_to_file(result)
                print(f'Processed {total_processed}/{total_articles} articles...')
                article_urls.extend(result)

    wait(futures)

    print("")
    print("==============================")
    print("          COMPLETED           ")
    print("==============================")
    print("")