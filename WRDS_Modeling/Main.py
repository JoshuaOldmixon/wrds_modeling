from Tools.Research import wrdsData
from Tools.Models.LinearRegression import linearRegression
from Tools.Models.LGBMRegressor import lightGBMRegressor
#from Tools.Models.H2OXGBoost import H2OXGBoost
from datetime import date
from dateutil.relativedelta import relativedelta


start = (date.today()- relativedelta(years=1)).strftime("%m/%d/%Y")

data = wrdsData('AAPL',start).table
linReg = linearRegression(data)
#h2oboost = H2OXGBoost(data)
lgbmreg = lightGBMRegressor(data)

print ('Linear Regression:',linReg.score())
#print ('H2O XGBoost:',h2oboost.score())
print ('Light GBM Regressor:',lgbmreg.score())
