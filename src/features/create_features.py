import pandas as pd
import glob
from scipy.signal import find_peaks
from datetime import datetime, timedelta

TICKER = 'YNDX'
DIST = 5 # Дистанция между пикам/впадинами


# Считываем все исторические данные
all_files = glob.glob('data/raw/*.pkl')
df = []
for filename in all_files:
    tdf = pd.read_pickle(filename)
    df.append(tdf)
df = pd.concat(df, axis=0, ignore_index=True)
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

def f_stat_yesterday(df):
    print('Статистика за прошлый день')
    agg_temp = df.groupby('tradedate')['pr_mean'].agg(['min','max','mean','std'])
    agg_temp.columns = [f'ytd_{col}' for col in agg_temp.columns]
    agg_temp = agg_temp.reset_index()
    agg_temp['tradedate'] = agg_temp['tradedate'] + timedelta(days=1)
    df = df.merge(agg_temp, on='tradedate', how='left')
    return df

def f_stat_month(df):
    print('Статистика за прошлый месяц')
    month_temp = df['pr_mean'].rolling(3120).agg(['min','max','mean','std'])
    month_temp.columns = [f'month_{col}' for col in month_temp.columns]
    month_temp['tradedate'] = df['tradedate']
    month_temp['tradetime'] = df['tradetime']
    month_temp['tradedate'] = month_temp['tradedate'].shift(-1)
    month_temp = month_temp.groupby('tradedate').nth(0)
    month_temp = month_temp.iloc[:,:-1]
    df = df.merge(month_temp, on='tradedate', how='left')
    return df


def target(df):
    print('Формируем таргет')
    # Считаем пики
    peaks, _ = find_peaks(df['pr_mean'], distance=DIST)
    temp = pd.DataFrame(index=peaks)
    temp['peak'] = 1
    df = df.join(temp)
    df['peak'] = df['peak'].fillna(0).astype(int)

    # Считаем впадины
    peaks, _ = find_peaks(0 - df['pr_mean'], distance=DIST)
    temp = pd.DataFrame(index=peaks)
    temp['trough'] = 2
    df = df.join(temp)
    df['trough'] = df['trough'].fillna(0).astype(int)

    # Формируем таргет
    df['target'] = df[['trough','peak']].max(axis=1)

    return df

df = (df
    .pipe(f_ratio)
    .pipe(f_stat_hour)
    .pipe(f_stat_yesterday)
    .pipe(f_stat_month)
    .pipe(target)
)

# Удаляем лишние и пустые строки
df = df[df['tradetime'].astype(str) > '11']
df = df.dropna(subset=['month_mean','ytd_mean'])

# Сохраняем датасет
today = datetime.today().strftime('%Y-%m-%d')
df.to_pickle(f"data/processed/{today.replace('-','')}_{TICKER}_train.pkl")


# Подготовим статистики за прошлоый день/месяц для предсказания 
agg_temp = df.groupby('tradedate')['pr_mean'].agg(['min','max','mean','std'])
agg_temp.columns = [f'ytd_{col}' for col in agg_temp.columns]
agg_temp = agg_temp[-1:]
agg_temp = agg_temp.reset_index(drop=True)

month_temp = df[:3120][['pr_mean']].agg(['min','max','mean','std']).T
month_temp.columns = [f'month_{col}' for col in month_temp.columns]
month_temp = month_temp.reset_index(drop=True)

ytd_month = pd.concat([agg_temp,month_temp], axis=1)
ytd_month.to_pickle(f'data/interim/{today.replace("-","")}_part.pkl')