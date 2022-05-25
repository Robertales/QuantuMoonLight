import csv
import math
import time
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from sklearn.svm import SVR

from app.source.utils import utils


class classicRegressor:
    def classify(pathTrain, pathTest, path_predict, model_name, kernelSVR, C_SVR):

        print(pathTrain, pathTest, path_predict)
        data_train = pd.read_csv(pathTrain)
        data_train = data_train.drop(columns='Id') #QSVM richiede l'id e Pegasos no
        train_features = data_train.drop(columns='labels')
        train_labels = data_train["labels"].values
        data_test = pd.read_csv(pathTest)
        data_test = data_test.drop(columns='Id')
        test_features = data_test.drop(columns='labels')
        test_labels = data_test["labels"].values

        toAdd = ""
        num_col = utils.numberOfColumns(path_predict)
        for j in range(1, num_col + 1):
            if j == num_col:
                toAdd += "feature" + str(j) + "\n"
                continue
            toAdd += "feature" + str(j) + ","

        with open(path_predict, "r") as f:
            contents = f.readlines()

        contents.insert(0, toAdd)

        with open(path_predict, "w") as f:
            contents = "".join(contents)
            f.write(contents)

        prediction_data = np.genfromtxt(path_predict, delimiter=',')
        prediction_data = np.delete(prediction_data, 0, axis=0)

        test_features = test_features.to_numpy() #Pegasos.fit accetta numpy array e non dataframe
        train_features = train_features.to_numpy()

        result = {}

        model = SVR(kernel=str(kernelSVR), C=int(C_SVR))
        if model_name == "Linear Regression":
            model = LinearRegression()

        try:
            # training
            print("Running...")
            start_time = time.time()
            model.fit(train_features, train_labels)
            training_time = time.time() - start_time
            print("Train effettuato in " + str(training_time))

            # test
            start_time = time.time()
            test_prediction = model.predict(test_features)
            testing_time = time.time() - start_time

            score = r2_score(test_labels, test_prediction)
            mse = mean_squared_error(test_labels, test_prediction)
            mae = mean_absolute_error(test_labels, test_prediction)
            result["regression_score"] = score
            result["mse"] = mse
            result["mae"] = mae
            rmse = math.sqrt(mse)
            result["regression_score"] = score
            result["rmse"] = rmse

            # prediction
            start_time = time.time()
            if utils.numberOfColumns(path_predict) == 1:
                prediction_data = prediction_data.reshape(-1, 1)
            if utils.numberOfRows(path_predict) == 1:
                prediction_data = prediction_data.reshape(1, -1)
            predicted_labels = model.predict(prediction_data)
            print(predicted_labels)
            total_time = time.time() - start_time
            print("Prediction effettuata in " + str(total_time))
            result["predicted_labels"] = np.array(predicted_labels)

            result["total_time"] = str(testing_time + training_time)[0:6]
            result["training_time"] = str(training_time)[0:6]
        except Exception as e:
            print(e)
            result["error"] = 1
            result["exception"] = e
        return result
