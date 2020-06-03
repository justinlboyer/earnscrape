import datetime
import json
import logging
from make_db import create_entry_for_ticker, find_missing_quarters, get_all_dates, get_all_entries, human_readable_datetimes, save_dict

logging.basicConfig(filename="update_db.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

def open_metadata(pth = './data/metadata/metadata.json'):
    with open(pth, 'r') as fp:
        data = json.load(fp)
    return data

def normalize_date(date_string):
    date = date_string.replace('_', '-')
    return date

def quarter_missing(ticker, date, metadata):
    today = datetime.datetime.now()
    if type(date) is not str:
        date = normalize_date(date)
    if ticker not in metadata:
        return True
    elif len(metadata[ticker]['missed_quarters'])>0 and date in (metadata[ticker]['missed_quarters']):
        return True
    elif datetime.datetime.strptime(date, '%Y-%m-%d') > today:
        logger.debug(f"Attempting to insert earnings for {date}, which has not occured yet")
    else:
        return False

def check_insert_update(ticker, date, metadata):
    if ticker not in metadata.keys():
        return 'insert'
    elif quarter_missing(ticker, date, metadata):
        return 'update'
    else:
        return None

def find_ticker_dates(all_tickers):
    ticker_dates_dict = {}
    for ticker in all_tickers:
        ticker_dates_dict[ticker] = get_all_dates(ticker)
    return ticker_dates_dict

def upsert_db_given_ticker(ticker, ticker_dict, metadata_db):
    insert_or_update = None
    for date in ticker_dict[ticker]:
        if type(date) is not str:
            date = datetime.datetime.strftime(date, '%Y-%m-%d')
        if insert_or_update != 'skip':
            insert_or_update = check_insert_update(ticker, date, metadata_db)
            if insert_or_update == 'insert':
                metadata_db[ticker] = create_entry_for_ticker(ticker, ticker_dict[ticker])
                insert_or_update = 'skip'
            elif insert_or_update == 'update':
                update_ticker()
                pass
            else:
                pass
    return metadata_db

def update_ticker(ticker, date_to_update):
    pass

if __name__ == '__main__':
    earnings_data_path = './data'
    metadata_save_path = f'{earnings_data_path}/metadata/metadata.json'
    logger.debug(f"Searching: {earnings_data_path}")
    all_tickers = get_all_entries(earnings_data_path)
    ticker_dates_dict = find_ticker_dates(all_tickers)
    metadata_db = open_metadata(metadata_save_path)

    # for ticker in ticker_dates_dict:
        
