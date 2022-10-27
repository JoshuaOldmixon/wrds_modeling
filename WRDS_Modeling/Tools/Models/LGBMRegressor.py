import pandas as pd
import numpy as np
from datetime import date
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import scale
from lightgbm import LGBMRegressor
import optuna
pd.options.mode.chained_assignment = None

class lightGBMRegressor:
    def __init__(self,data):
        prices = data[['open','high','low','close']]
        prices.fillna(value=-99999,inplace=True)
        forecast_col = 'close'
        forecast_out = int(math.ceil(0.01 * len(prices)))
        prices['label'] = prices[forecast_col].shift(-forecast_out)
        prices.dropna(inplace=True)

        X = prices.iloc[:,:-1]
        y = prices.label

        def objective(trial,data=data):
        
            X_train,X_test,y_train,y_test = train_test_split(X,y)

            params = {
            'metric': 'rmse', 
            'random_state': 48,
            'n_estimators': 20000,
            'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-3, 10.0),
            'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-3, 10.0),
            'colsample_bytree': trial.suggest_categorical('colsample_bytree', [0.3,0.4,0.5,0.6,0.7,0.8,0.9, 1.0]),
            'subsample': trial.suggest_categorical('subsample', [0.4,0.5,0.6,0.7,0.8,1.0]),
            'learning_rate': trial.suggest_categorical('learning_rate', [0.006,0.008,0.01,0.014,0.017,0.02]),
            'max_depth': trial.suggest_categorical('max_depth', [10,20,100]),
            'num_leaves' : trial.suggest_int('num_leaves', 7, 1000),
            'min_child_samples': trial.suggest_int('min_child_samples', 1, 300),
            'cat_smooth' : trial.suggest_int('min_data_per_groups', 1, 100)
            }

            model = LGBMRegressor(**params)
            model.fit(X_train,y_train)
            prediction = model.predict(X_test)
            pred = (mean_squared_error(prediction,y_test))
            return pred

        
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=5)

        prediction = study.best_value

        self.prediction = prediction
    def score(self):
        return self.prediction
