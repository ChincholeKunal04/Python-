import numpy as nm
import matplotlib.pyplot as mtp
import pandas as pd

data_set = pd.read_csv('csvFile.csv')

x = data_set.iloc[:, :-1].values
y = data_set.iloc[:, 1].values

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 1/3, random_state= 0)
print(x_test)
print(y_test)

from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
regressor.fit(x_train, y_train)

x_pred = regressor.predict(x_test)

y_test_reshaped = y_test.reshape(-1, 1)
y_pred = regressor.predict(y_test_reshaped)

if len(x_train) != len(y_train):
    raise ValueError("x_train and y_train must have the same length for scatter plot.")

mtp.figure(figsize=(10, 6))

mtp.scatter(x_train[:, 0], y_train, color="green", label="Training Data")
mtp.plot(x_test[:, 0], x_pred, color="red", label="Predicted Values")

mtp.title("Salary Vs Experience")
mtp.xlabel("Experience")
mtp.ylabel("Salary")
mtp.legend()
mtp.show()