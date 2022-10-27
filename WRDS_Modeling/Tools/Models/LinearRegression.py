import pandas as pd
import numpy as np
from datetime import date
import math
from sklearn.model_selection import train_test_split
from statistics import mean
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale

class linearRegression:
    def __init__(self,data):
        symbol_data = data[['open','high','low','close']]
        symbol_data.fillna(value=-99999,inplace=True)
        forecast_col = 'close'
        forecast_out = int(math.ceil(0.01 * len(symbol_data)))
        symbol_data['label'] = symbol_data[forecast_col].shift(-forecast_out)
        symbol_data.dropna(inplace=True)

        X = symbol_data.iloc[:,:-1]
        y = symbol_data.label
        
        X_scaled =scale(X)
        X_scaled = pd.DataFrame(X_scaled)

        X_train,X_test,y_train,y_test = train_test_split(X_scaled,y)
        model = LinearRegression()
        model.fit(X_train,y_train)
        y_predict = model.predict(X_test)
        prediction = mean(y_predict)

        self.prediction = prediction
    def score(self):
        return self.prediction
