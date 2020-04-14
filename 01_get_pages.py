import time
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, wait, ThreadPoolExecutor, as_completed
from typing import List

from parsers import get_section_urls_from_section_soup, get_2019_volume_number, get_number_of_pages
from helpers import get_driver, connect_to_base, write_pages_to_file, batch

BMC_JOURNAL_A_Z_URL = 'https://www.biomedcentral.com/journals-a-z'

def get_section_urls():
    browser = get_driver()
    section_page_urls = []
    if connect_to_base(browser, BMC_JOURNAL_A_Z_URL):
        print('Parsing sections')
        time.sleep(1)
        html = browser.page_source
        section_soup = BeautifulSoup(html, 'html.parser')
        section_page_urls = get_section_urls_from_section_soup(section_soup)
    else:
        print('Error connecting to BMC - Sections read')

    browser.quit()
    return section_page_urls

def get_page_urls_from_section_batch(urls:list):
    browser = get_driver()
    page_urls = []
    for section_url in urls:
        print(f'Parsing 2019 volume from section {section_url}')
        volume_number = None
        if connect_to_base(browser, section_url + "/articles"):
            time.sleep(1)
            html = browser.page_source
            section_soup = BeautifulSoup(html, 'html.parser')
            volume_number = get_2019_volume_number(section_soup)
        else:
            print(f'Error connectin to BMC - Volume read for {section_urls}')
            continue

        if connect_to_base(browser, section_url + '/articles'+ f'?tab=keyword&volume={volume_number}&sort=PubDateAscending'):
            time.sleep(1)
            html = browser.page_source
            first_page_soup = BeautifulSoup(html, 'html.parser')
            number_of_pages = get_number_of_pages(first_page_soup)
            if number_of_pages is None:
                print(f'Error reading number of pages for {section_urls} volume {volume_number}')
                print(f'Retry!!!')
                break
            section_pages_urls = [
                {
                    'section_url': section_url,
                    'volume': {volume_number},
                    'page_number': {page_num}
                }
                for page_num 
                in range(1, number_of_pages+1)
            ]
            page_urls.extend(section_pages_urls)
        else:
            print(f'Error connectin to BMC - Page number read for {section_urls} volume {volume_number}')
            continue

    browser.quit()
    return page_urls


if __name__ == '__main__':
    futures = []
    total_pages = []
    print(f'Loading sections urls...')
    section_urls = get_section_urls()
    total_sections = len(section_urls)
    print(f'Sections loaded ({total_sections}).')

    print(f'Generating section page URLS...')
    with ProcessPoolExecutor(4) as executor:
        for section_url_batch in batch(section_urls, 20):
            urls = [url for url in list(section_url_batch)]
            futures.append(executor.submit(get_page_urls_from_section_batch, urls))
        
        for future in as_completed(futures):
            result = future.result()
            if result is None:
                print('Page reading result is None')
            else:
                print(f'Writing {len(result)} pages to pages file')
                write_pages_to_file(result)
                total_pages.extend(result)

    wait(futures)

    print("")
    print("==============================")
    print("          COMPLETED           ")
    print(f"       Total pages {len(total_pages)}           ")
    print("==============================")
    print("")