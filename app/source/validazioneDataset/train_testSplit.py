# Split the dataset in training set and testing set in order to be consistent on the comparisons
import pandas as pd
from sklearn.model_selection import train_test_split

def splitDataset(filename):
    #df = pd.read_csv(filename, index_col=0)

    #SEED = 1

    # 80/20 holdout split
    #train, test = train_test_split(df, stratify=df['Species'], test_size=20, random_state=SEED)

    #return train.to_csv('Data_training.csv'), test.to_csv('Data_testing.csv')

    data = pd.read_csv(filename)
    X = data

    X_train, X_test = train_test_split(X, test_size=20)

    print("\nX_train:\n")
    print(X_train.head())
    print(X_train.shape)

    print("\nX_test:\n")
    print(X_test.head())
    print(X_test.shape)



    return X_train.to_csv('Data_training.csv', index=False), X_test.to_csv('Data_testing.csv',index=False)



