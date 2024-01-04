# Import libraries
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load housing data
housing = pd.read_csv('data/source/housing.csv')

# Handle missing values
housing_num = housing.drop('ocean_proximity', axis=1)
imputer = SimpleImputer(strategy='mean')  
imputer.fit(housing_num)
housing_num = imputer.transform(housing_num)

# Encode categorical data
housing_cat = housing['ocean_proximity'].values.reshape(-1,1)
encoder = OrdinalEncoder() 
housing_cat = encoder.fit_transform(housing_cat)

# Split data 
X = np.hstack((housing_num, housing_cat))
y = housing['median_house_value'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize data
std_scaler = StandardScaler()
X_train = std_scaler.fit_transform(X_train)
X_test = std_scaler.transform(X_test)

# Linear Regression
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
y_pred_lr = lin_reg.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr) 
rmse_lr = np.sqrt(mse_lr)
print(f"Linear Regression RMSE: {rmse_lr: .2f}")

# Decision Tree Regression 
dt_reg = DecisionTreeRegressor()
dt_reg.fit(X_train, y_train)
y_pred_dt = dt_reg.predict(X_test)
mse_dt = mean_squared_error(y_test, y_pred_dt)
rmse_dt = np.sqrt(mse_dt) 
print(f"Decision Tree Regression RMSE: {rmse_dt: .2f}")

# Random Forest Regression
rf_reg = RandomForestRegressor() 
rf_reg.fit(X_train, y_train)  
y_pred_rf = rf_reg.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
print(f"Random Forest Regression RMSE: {rmse_rf: .2f}")

# Simple Linear Regression
X_train_income = X_train[:,7].reshape(-1,1) 
X_test_income = X_test[:,7].reshape(-1,1)

sl_reg = LinearRegression()
sl_reg.fit(X_train_income, y_train)

y_pred_sl_train = sl_reg.predict(X_train_income)
y_pred_sl_test = sl_reg.predict(X_test_income)

plt.scatter(X_train_income, y_train, color='blue')
plt.plot(X_train_income, y_pred_sl_train, color='black')
plt.scatter(X_test_income, y_test, color='red')
plt.plot(X_test_income, y_pred_sl_test, color='green')  
plt.show()