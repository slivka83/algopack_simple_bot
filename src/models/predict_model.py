import pandas as pd
import lightgbm as lgb
from moexalgo import Ticker
from datetime import datetime


TICKER = 'YNDX'

today = datetime.today().strftime('%Y-%m-%d')

# Загружаем модель
model = lgb.Booster(model_file=f'models/{today.replace("-","")}_model.lgb')

# Загружаем торговую статистику за текущий день
loader = Ticker(TICKER)
df = loader.tradestats(date=today, till_date=today)
df = pd.DataFrame(df)
df['tradedate'] = pd.to_datetime(df['ts']).dt.date
df['tradetime'] = pd.to_datetime(df['ts']).dt.time
df['pr_mean'] = df[['pr_high','pr_low']].mean(axis=1)


def f_ratio(df):
    print('Отношение к последнему часу')
    for i in range(1,11+1):
        df[f'ratio_pr_mean_{i}'] = df['pr_mean'] / df['pr_mean'].shift(i)
    return df

def f_stat_hour(df):
    print('Статистика за прошлый час')
    for a in ['min','max','mean','std']:
        df[f'hour_{a}'] = df.groupby('tradedate')['pr_mean'].transform(
            lambda s: s.shift(1).rolling(11).agg(a))
    return df

def f_stat_ytd_month(df):
    print('Статистики за прошлый час и за прошлый год')
    ytd_month = pd.read_pickle(f'data/interim/{today.replace("-","")}_part.pkl')
    df = df.merge(ytd_month, how='cross')
    return df

# Формируем фичи
df = (df
    .pipe(f_ratio)
    .pipe(f_stat_hour)
    .pipe(f_stat_ytd_month)
)

# Выделяем последнюю строку
last_row = df[model.feature_name()][-1:]
last_row.to_pickle(f"data/processed/{today.replace('-','')}_{TICKER}_predict.pkl")

# Выполняем предсказание
pred = model.predict(last_row).argmax()

# Отправляем запрос брокеру 
def send_to_broker(pred):
    if pred == 0:
        print(TICKER, df['tradetime'].max(), '- Ничего не делаем')
    elif pred == 1:
        print(TICKER, df['tradetime'].max(), '- Пик (продаем)')
    elif pred == 2:
        print(TICKER, df['tradetime'].max(), '- Впадина (покупаем)')

send_to_broker(pred)