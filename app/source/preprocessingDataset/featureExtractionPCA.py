import csv
import numpy as np
import os
import pandas as pd


#filename = 'Iris_testing.csv'

def featureExtractionPCA2(filename, features):
    f = pd.read_csv(filename)
    keep_col = features
    new_f = f[keep_col]
    new_f.to_csv("tempPCA.csv", index=False)

    dataset = pd.read_csv('tempPCA.csv')

    #X1 = dataset.drop('Id', 1)
    X = dataset.drop('labels', 1)

    y = dataset['labels']
    print(dataset.head())
    #print(y)

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    from sklearn.preprocessing import StandardScaler

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    explained_variance = pca.explained_variance_ratio_
    # print(explained_variance)

    z = np.concatenate((X_train, X_test))
    # write csv data
    if not os.path.exists('C:/xampp/htdocs/quantumKNN/python/yourPCA.csv'):
        np.savetxt('C:/xampp/htdocs/quantumKNN/python/yourPCA.csv', z, delimiter=",", fmt='%s')
    else:
        np.savetxt('C:/xampp/htdocs/quantumKNN/python/yourPCA1.csv', z, delimiter=",", fmt='%s')

    # print(z)

    return z

#print(featureExtractionPCA2(filename))

"""""
#prediction
from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(max_depth=2, random_state=0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

#Performance Evaluation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y_test, y_pred)
print(cm)
print('Accuracy' + accuracy_score(y_test, y_pred))"""

