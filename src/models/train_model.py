import lightgbm as lgb
import pandas as pd
from datetime import datetime
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import classification_report

import warnings
warnings.filterwarnings('ignore')


TICKER = 'YNDX'

today = datetime.today().strftime('%Y-%m-%d')
df = pd.read_pickle(f"data/processed/{today.replace('-','')}_{TICKER}.pkl")
df = df.fillna(0)

drop_cols = ['ticker','secid','ts','tradedate','tradetime','systime','peak','trough','target']
f_cols = [col for col in df.columns if col not in drop_cols]

last_day = str(df['tradedate'].max())
train = df[df['tradedate'].astype('str') < last_day]
test = df[df['tradedate'].astype('str') == last_day]

X_train, y_train = train[f_cols], train['target']
X_test, y_test = test[f_cols], test['target']

print(X_train.shape, X_test.shape)
print(y_train.mean() * 100, y_test.mean() * 100)



params = {
    #'n_estimators ': [100],
    #'learning_rate ': [0.9, 0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1],
    'max_depth ': [2,3,4,5,6],
    #'subsample ': [0.3],
    #'colsample_bytree ': [0.3]
}

clf = lgb.LGBMClassifier(verbosity=-1)
model = GridSearchCV(
    clf,
    params,
    scoring='precision_macro',
    cv=TimeSeriesSplit(n_splits=5))
model.fit(X_train, y_train)

print(model.best_score_)
print(model.best_params_)


y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))


today = datetime.today().strftime('%Y-%m-%d')
model.best_estimator_.booster_.save_model(f'models/{today.replace("-","")}_model.lgb')