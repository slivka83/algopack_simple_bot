from moexalgo import Ticker
from datetime import datetime, timedelta
import pandas as pd

TICKER = 'YNDX'

yesterday = datetime.today() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')

loader = Ticker(TICKER)
one_day_df = loader.tradestats(date=yesterday, till_date=yesterday)
one_day_df = pd.DataFrame(one_day_df)

if one_day_df.shape[0] > 0:
    print(yesterday, TICKER, one_day_df.shape)
    one_day_df.to_pickle(f"data/raw/{yesterday.replace('-','')}_{TICKER}.pkl")
else:
    print(yesterday, TICKER, 'Данных нет')