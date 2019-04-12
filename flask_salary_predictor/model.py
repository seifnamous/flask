# coding: utf-8

# Linear Regression to predict salary from number of years of experience

# Import libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

# Import data
df = pd.read_csv('~/ai/webdev/deployMLflask/salaries/flask_salary_pred/Salary_Data.csv')
X = np.array(df.YearsExperience).reshape(-1,1)
y = np.array(df.Salary).reshape(-1,1)

# Splitt data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

# Fitting model to training set
reg = LinearRegression(fit_intercept=True)
reg.fit(X_train, y_train)

# Use fitted model to predict
y_test_pred = reg.predict(X_test)


# Saving model to disk
pickle.dump(reg, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load( open('model.pkl','rb'))
print(model.predict([[1.8]]))




