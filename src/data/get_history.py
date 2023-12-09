from moexalgo import Ticker
from datetime import date, timedelta
import pandas as pd
import time

TICKER='YNDX'
loader = Ticker(TICKER)

load_date = date(2023, 1, 1)
end_date = date(2023, 12, 8)

while load_date <= end_date:
    date_str = load_date.strftime("%Y-%m-%d")

    one_day_df = loader.tradestats(date=date_str, till_date=date_str)
    one_day_df = pd.DataFrame(one_day_df)

    if one_day_df.shape[0] > 0:
        print(date_str, TICKER, one_day_df.shape)
        one_day_df.to_pickle(f"data/raw/{date_str.replace('-','')}_{TICKER}.pkl")
    else:
        print(load_date, TICKER, 'Данных нет')
        
    load_date += timedelta(days=1)
    time.sleep(3)