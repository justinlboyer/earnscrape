import datetime
date_list = ['2019_01_29.html'
                , '2019_04_28.html'
                , '2019_10_23.html']

dates = [datetime.date(2019,1,29)
            , datetime.date(2019, 4, 28)
            , datetime.date(2019, 10, 23)]


ticker_fixture = {'ticker': 'NYSE:TLRA', 'date':'2019_11_07'}


metadata_db = {"NASDAQ:AAL": 
                {"created_at": "2020-03-01 09:13:24", "earliest_earnings": "2019-07-25", "missed_quarters": [], "most_recent_earnings": "2020-01-24", "updated_at": "2020-03-01 09:13:24"}
                , "NASDAQ:AAPL": {"created_at": "2020-03-01 09:13:24", "earliest_earnings": "2019-07-30", "missed_quarters": [], "most_recent_earnings": "2020-01-28", "updated_at": "2020-03-01 09:13:24"}
                , "NASDAQ:AAWW": {"created_at": "2020-03-01 09:13:24", "earliest_earnings": "2019-10-31", "missed_quarters": ["2020-01-31"], "most_recent_earnings": "2019-10-31", "updated_at": "2020-03-01 09:13:24"}
                , "update_ticker": {"created_at": "2020-03-01 09:13:24", "earliest_earnings": "2019-10-31", "missed_quarters": [], "most_recent_earnings": "2019-10-31", "updated_at": "2020-03-01 09:13:24"}
                , "NASDAQ:AAXN": {"created_at": "2020-03-01 09:13:24", "earliest_earnings": "2020-02-28", "missed_quarters": [], "most_recent_earnings": "2020-02-28", "updated_at": "2020-03-01 09:13:24"}}