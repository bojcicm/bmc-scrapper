import time
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, wait, ThreadPoolExecutor, as_completed
from typing import List

from parsers import get_entry_aricle_a_tags_from_soup
from helpers import get_driver, connect_to_base, load_pages_from_file, write_to_article_urls_file, batch


def get_article_urls_from_page_batch(urls:list):
    browser = get_driver()
    article_urls = []
    for page in urls:
        section_url = page['section_url']
        volume_number = page['volume']
        page_number = page['page_number']
        page_url = section_url + '/articles' + f'?tab=keyword&volume={volume_number}&sort=PubDateAscending&page={page_number}'
        print(f'Parsing page for articles {page_url}')
        if connect_to_base(browser, page_url):
            time.sleep(1)
            html = browser.page_source
            page_soup = BeautifulSoup(html, 'html.parser')
            article_tags = get_entry_aricle_a_tags_from_soup(page_soup)
            found_urls = [
                section_url + a['href']
                for a in article_tags
            ]
            article_urls.extend(found_urls)
        else:
            print(f'Error connectin to BMC - Article URL read for {page_url}')
            continue

    browser.quit()
    return article_urls


if __name__ == '__main__':
    futures = []
    article_urls = []

    print(f'Loading pages from CSV...')
    page_urls = load_pages_from_file()
    total_pages = len(page_urls)
    print(f'Pages loaded ({total_pages}).')

    print(f'Loading article URLS from pages...')
    with ProcessPoolExecutor(4) as executor:
        for page_urls_batch in batch(page_urls, 20):
            urls = [url for url in list(page_urls_batch)]
            futures.append(executor.submit(get_article_urls_from_page_batch, urls))
        
        for future in as_completed(futures):
            result = future.result()
            if result is None:
                print('Article URL reading result is None')
            else:
                print(f'Writing {len(result)} article URLs to urls file')
                write_to_article_urls_file(result)
                article_urls.extend(result)
    
    wait(futures)

    print("")
    print("==============================")
    print("          COMPLETED           ")
    print(f"     Total articles {len(article_urls)}           ")
    print("==============================")
    print("")