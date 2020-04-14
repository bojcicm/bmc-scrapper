# BiomedCentral scrapper

Python 3 with Headless Chrome scrapper for loading article data from https://www.biomedcentral.com/

### Install and run:
**NOTE !!!** 
Make sure you have headless Chrome on your system and in $PATH variable
https://sites.google.com/a/chromium.org/chromedriver/getting-started

#### Setup:
1. Install virtaulenv
    ```sh
    $ pip install virtualenv
    ```
2. Create virtualenv in scrapper folder
    ```sh
    $ cd bmc-scrapper
    $ virtualenv venv
    $ source venv/bin/activate
    ```
3. Install pip packages
    ```sh
    $ pip install -r requirements.txt
    ```
4. Run programs in order
    ```sh
    $ python 01_get_pages.py
    $ python 02_get_article_urls.py
    $ python 03_get_article_data.py
    ```
    
### Runtime note:
Sometimes programs crashes because page was not loaded or BMC is down. In that case just re-run program that failed.

### Todo:
- Make it more robust so it can easily recover from unexpected crashes