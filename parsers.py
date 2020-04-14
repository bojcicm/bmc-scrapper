import re
from typing import List
from bs4 import BeautifulSoup


def get_section_urls_from_section_soup(section_soup: BeautifulSoup)->List[str]:
    sections = section_soup.findAll("li", class_='u-mb-24-at-md')
    urls = []
    for section in sections:
        section_a_tags = section.findAll("a", class_='u-ml-8')
        for a_tag in section_a_tags:
            urls.append("https:" + a_tag['href'])

    return urls


def get_2019_volume_number(section_soup: BeautifulSoup) -> str:
    pattern = re.compile(r"2019")
    
    volumes_select = section_soup.find("select", attrs={
        'name': 'volume'
        }).find("option", text=(pattern))['value']

    return volumes_select


def get_number_of_pages(soup: BeautifulSoup) -> int:
    pattern = re.compile(r'Page 1 of')
    pages = soup.find("p", text=(pattern))
    if pages is None:
        return None
    pages_string=pages.getText()
    
    numbers = []
    for word in pages_string.split():
        if word.isdigit():
            numbers.append(int(word))

    return numbers[-1]


def get_entry_aricle_a_tags_from_soup(soup:BeautifulSoup) -> List:
    return soup.findAll("a", attrs={
        'data-test': 'title-link'
    })


def process_article_for_soup(article_soup, url):
    publish_date = ''
    publish_date_div = article_soup.find('time', attrs={'itemprop':'datePublished'})
    if publish_date_div is not None:
        publish_date = publish_date_div['datetime']

    title = ""
    title_h1 = article_soup.find('h1')
    if title_h1 is not None:
        title = title_h1.getText()

    journal_name = ""
    journal_i_tag = article_soup.find('i', attrs={'data-test': 'journal-title'}) 
    if journal_i_tag is not None: 
        journal_name = journal_i_tag.getText()

    data_text = ""
    availability_div = article_soup.find('div', id='availability-of-data-and-materials-content')
    if availability_div is not None:
        data_text = availability_div.find('p').getText()
    else:
        availability_h3 = article_soup.find('h3', text='Availability of data and materials')
        if availability_h3 is not None and \
            availability_h3.next_sibling is not None and \
            availability_h3.next_sibling.next_sibling is not None:
                data_text = availability_h3.next_sibling.next_sibling.getText()

    article = {
        'url': url,
        'title': title,
        'journal_name': journal_name,
        'publish_date': publish_date,
        'data_available': data_text
    }
    return article