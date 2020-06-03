import datetime
from dateutil.relativedelta import relativedelta
import json
import logging
import os
from tqdm import tqdm

logging.basicConfig(filename="instantiate_db.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

def get_all_entries(earnings_data_path):
    get_all = os.listdir(earnings_data_path)
    logger.debug(f"Retrieved {len(get_all)} tickers")
    return get_all

def instatiate_db(earnings_data_path):
    get_all = get_all_entries(earnings_data_path)
    scape_dict = {}
    for ticker in tqdm(get_all):
        if ticker != 'metadata':
            dates = get_all_dates(ticker)
            scape_dict[ticker] = create_entry_for_ticker(ticker, dates)
        else:
            logger.debug(f"Removed {ticker} from db")
    return scape_dict

def get_all_dates(ticker, earnings_data_path='./data'):
    get_dates = os.listdir(f'{earnings_data_path}/{ticker}')
    datetime_list = parse_dates(get_dates)
    return datetime_list

def create_entry_for_ticker(ticker, dates):
    missing_dates = find_missing_quarters(dates)

    ticker_dict = {
                    'earliest_earnings': human_readable_datetimes(min(dates))
                    , 'most_recent_earnings': human_readable_datetimes(max(dates))
                    ,'missed_quarters': human_readable_datetimes(missing_dates)
                    , 'created_at': human_readable_datetimes(datetime.datetime.now())
                    , 'updated_at': human_readable_datetimes(datetime.datetime.now())
    }
    return ticker_dict

def human_readable_datetimes(dates):
    if type(dates) is datetime.datetime:
        return dates.strftime('%Y-%m-%d %H:%M:%S')
    elif  type(dates) is datetime.date:
        return dates.strftime('%Y-%m-%d')
    elif type(dates) is list:
        return [dte.strftime('%Y-%m-%d') for dte in dates]
    elif type(dates) is str:
        return dates


def save_dict(scrape_dict, path):
    with open(path, 'w') as fp:
        json.dump(scrape_dict, fp, sort_keys=True)

def parse_dates(date_list):
    dates = [datetime.datetime.strptime(dte[:-5], '%Y_%m_%d').date() for dte in date_list]
    return dates

def covert_dates_datetimes(date_list):
    if type(date_list) is datetime.date or type(date_list) is datetime.datetime:
        return date_list
    else:
        if type(date_list) is list:
            if '-' in date_list[0]:
                date_list = [datetime.datetime.strptime(dte, '%Y-%m-%d').date() for dte in date_list]
            elif '_' in date_list[0]:
                date_list = [datetime.datetime.strptime(dte, '%Y-%m-%d').date() for dte in date_list]
            return date_list
        elif type(date_list) is str:
            if '-' in date_list:
                return datetime.datetime.strptime(date_list, '%Y-%m-%d').date()
            elif '_' in date_list:
                return datetime.datetime.strptime(date_list, '%Y_%m_%d').date()
        else:
            return date_list
                

def find_missing_quarters(dates):
    now = datetime.datetime.now().date()
    three_mon_rel = relativedelta(months=3)

    last_day_date_list = [last_day_of_month(dte) for dte in dates]
    on_date = min(last_day_date_list)
    three_months_from_on = on_date + three_mon_rel

    missing_dates = []
    while three_months_from_on <= now:
        test = any([three_months_from_on==dte for dte in last_day_date_list])
        if test is False:
            missing_dates.append(three_months_from_on)
        three_months_from_on = last_day_of_month(three_months_from_on + three_mon_rel)
    
    return missing_dates

def last_day_of_month(datetime_date):
    datetime_date = covert_dates_datetimes(datetime_date)
    next_month = datetime_date.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

if __name__ == '__main__':
    earnings_data_path = './data'
    metadata_save_path = f'{earnings_data_path}/metadata/metadata.json'
    logger.debug(f"Searching: {earnings_data_path}")

    db_dict = instatiate_db(earnings_data_path)
    logger.debug(f"Generated {len(db_dict)} entries for db")
    logger.debug(f"Saving to {metadata_save_path}")
    save_dict(db_dict, metadata_save_path)

