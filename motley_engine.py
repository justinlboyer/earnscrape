#!/usr/bin/env python3
import datetime
import logging 

logging.basicConfig(filename="./logs/motley_engine.log", 
                format='%(asctime)s %(message)s', 
                filemode='w')
logger = logging.getLogger() 
logger.setLevel(logging.INFO) 

from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
import requests
import os
from shutil import move
import time
from tqdm import tqdm

import update_db




def get_links_on_page(url):
    contents = requests.get(url)
    soup = BeautifulSoup(contents.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        ln = link.get('href')
        if ln is not None:
            if '/earnings/call-transcripts/' in ln:
                links.append(ln.strip())
    return links

def get_url_info(url):
    i=0
    while i<5:
        try:
            contents = requests.get(url)
            soup = BeautifulSoup(contents.text, 'html.parser')
            # would be good to use link to find ticker (speed improvement)
            text = soup.find('span', {'class':"article-content"})
            ticker = text.find('span', {'class': "ticker"}).find('a').get_text()
            cleaned_url = url.replace('https://www.fool.com/earnings/call-transcripts/','')
            # need to check for valid dates
            date = '_'.join(cleaned_url.split('/')[:3])
            return text, ticker, date
        except:
            i += 1
            if i < 3:
                wait_time = 1.5**i
                logger.debug(f"failed, waiting {wait_time} seconds for {url}")
                time.sleep(wait_time)
            else:
                logger.error(f"failed at {url}")
                break

def write_html(text, ticker, date):
    base_path = './data/'
    pth = base_path + ticker
    if not os.path.isdir(pth):
        os.mkdir(pth)
    file_path = f'{pth}/{date}.html'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as fil:
            fil.write(str(text))

def remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

def get_all_links():
    links = []
    print(f"Getting all links for {NUM_PAGES_TO_CRAWL} pages monitor progress below")
    for num in tqdm(range(NUM_PAGES_TO_CRAWL)):
        link_url = f'https://www.fool.com/earnings-call-transcripts/?page={num}'
        try:
            temp_links = get_links_on_page(link_url)
        except:
            logger.exception(f"Exception on: {link_url} | {get_links_on_page(link_url)}")
            pass
        links.extend(temp_links)
    link_list = remove(links)
    return link_list

def write_links_to_disk(links, path='./temp/link_list'):
    with open(path, 'w') as f:
        for line in links:
            f.write(f"{line}\n")
    logger.info(f"Wrote links to {path}")

def read_link_list(path='./temp/link_list'):
    link_list = []
    with open(path, 'r') as f:
        for line in f:
            link_list.append(line[:-1])
    logger.info(f"Saved off link list to: {path}")
    return link_list

def read_and_write(link):
    url = base_url + link
    text, ticker, date = get_url_info(url)

    metadata_db = update_db.open_metadata(metadata_path)

    date_dashes = date.replace('_', '-')
    data_missing = update_db.quarter_missing(ticker, date_dashes, metadata_db)
    if data_missing:
        write_html(text, ticker, date)
    else:
        logger.debug(f"Data already exists for {ticker} and {date}")

def clear_temp(pth='./temp/'):
    for filename in os.listdir(pth):
        file_path = os.path.join(pth, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.debug('Failed to delete %s. Reason: %s' % (file_path, e))


def move_link_list(linkpth='./temp/link_list'):
    move(linkpth, linkpth+'.bak')
    logger.info(f"Moved link list")

if __name__ == '__main__':
    global NUM_PAGES_TO_CRAWL
    NUM_PAGES_TO_CRAWL = 100
    num_processes = 1
    base_url = 'https://www.fool.com'
    metadata_path = './data/metadata/metadata.json'
    link_path = './temp/link_list'
    logger.info(f"Starting motley fool scraper, pwd: {os.getcwd()}".center(50, '~'))

    if os.path.exists(link_path):
        links = read_link_list()
        logger.info(f"reading in list from {link_path}")
    else:
        logger.info("Scraping links".center(75, '~'))
        links = get_all_links()
    
    logger.debug(f"Found {len(links)} links, now writing") 
    write_links_to_disk(links)

    with Pool(processes=num_processes) as pool:
        logger.info(f"Using {num_processes} process, monitor progress below:")
        r = list(tqdm(pool.map(read_and_write, links)))
    move_link_list()
    logger.info(f"Finished scraping Motley Fool".center(50, '~'))
