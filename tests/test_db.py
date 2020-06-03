import datetime
import make_db
import update_db
import pytest
import tests.fixtures as tf

def test_update_ticker():
    # test more recent out of quarter
    data = tf.metadata_db
    data = update_db.upsert_db_given_ticker('NASDAQ:AAL',  {'NASDAQ:AAL':['2020-03-01']}, data)
    assert len(data['NASDAQ:AAL']['missed_quarters'])== 0
    assert data['NASDAQ:AAL']['most_recent_earnings'] == '2020-03-01'
    assert data['NASDAQ:AAL']['created_at'] == '2020-03-01 09:13:24'
    assert data['NASDAQ:AAL']['updated_at'] != '2020-03-01 09:13:24'

    # test add missing
    data = update_db.upsert_db_given_ticker('update_ticker',  {'update_ticker':['2020-03-01']}, data)
    assert len(data['update_ticker']['missed_quarters']) > 0
    assert data['update_ticker']['most_recent_earnings'] == '2020-03-01'
    assert data['update_ticker']['created_at'] == '2020-03-01 09:13:24'
    assert data['update_ticker']['updated_at'] != '2020-03-01 09:13:24'
    
    # test add earlier
    data = update_db.upsert_db_given_ticker('update_ticker1',  {'update_ticker1':['2019-07-28']}, data)
    assert len(data['update_ticker1']['missed_quarters']) > 0
    assert data['update_ticker1']['most_recent_earnings'] == '2019-10-31'
    assert data['update_ticker1']['earliest_earnings'] == '2019-07-28'
    assert data['update_ticker1']['created_at'] == '2020-03-01 09:13:24'
    assert data['update_ticker1']['updated_at'] != '2020-03-01 09:13:24'


def test_insert_ticker():
    data = tf.metadata_db
    data = update_db.upsert_db_given_ticker('test_ticker',  {'test_ticker':['2019-01-01', '2019-04-01']}, data)
    assert len(data['test_ticker']['missed_quarters'])>= 2
    assert data['test_ticker']['most_recent_earnings'] == '2019-04-01'

def test_convert_dates():
    assert type(make_db.covert_dates_datetimes(['2019-01-01'])[0]) is datetime.date


def test_find_ticker_dates():
    dic = update_db.find_ticker_dates(['NASDAQ:AAL', 'TSX:ECA'])
    assert len(dic) == 2
    assert len(dic['NASDAQ:AAL']) >=3

# def test_open_metadata():
#     data = tf.metadata_db
#     assert type(data) == dict
#     assert len(data) >= 4

def test_check_db():
    data = tf.metadata_db
    assert update_db.quarter_missing('NASDAQ:AAL', '2020-01-24', data) is False
    assert update_db.quarter_missing('NASDAQ:AAWW', '2020-01-31', data) is True
    assert update_db.quarter_missing('NASDAQ:AAWW', '2100-01-31', data) is None
    
def test_normalize_date():
    assert update_db.normalize_date('2019_02_01') == '2019-02-01'


def test_readable_dates():
    one_datetime = datetime.datetime(2020,1,12)
    assert make_db.human_readable_datetimes(one_datetime) == '2020-01-12 00:00:00'
    one_date = datetime.date(2020,1,12)
    assert make_db.human_readable_datetimes(one_date) == '2020-01-12'
    dates = [one_date, one_datetime]
    assert all([a == b for a, b in zip(make_db.human_readable_datetimes(dates)
                , ['2020-01-12', '2020-01-12'])])

def test_parse_dates():
    dates = make_db.parse_dates(tf.date_list)
    assert dates[0] == datetime.date(2019, 1, 29)
    
def test_find_missing_quarters():
    missing = make_db.find_missing_quarters(tf.dates)
    assert missing[0] == datetime.date(2019, 7, 31)
    # need to also assert that october is not missing

def test_last_day():
    last = make_db.last_day_of_month(datetime.date(2019, 10, 23))
    assert last == datetime.date(2019, 10, 31)