import pathlib
import warnings
from itertools import cycle

import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from app.source.utils import utils

warnings.simplefilter(action="ignore", category=FutureWarning)


def callFeatureExtraction(
        pathTrain: pathlib.Path,
        pathTest: pathlib.Path,
        pathToPredict: pathlib.Path,
        classification: bool,
        n_components=2
):
    """
    This function executes the Feature Extraction on the given dataset

    :param pathTrain: path to the location of the dataset Train that is going to be reduced with FE
    :param pathTest: path to the location of the dataset Test that is going to be reduced with FE
    :param pathToPredict: path to the location of the dataset to Predict that is going to be reduced with FE
    :param classification: boolean flag that indicated whether the user wants to execute classification or not
    :param n_components: number of new columns
    :return: string that points to the location of the datasets preprocessed with FE
    :rtype: pathlib.Path, pathlib.Path
    """
    print("Into callFeatureExtraction...")
    pathFileYourPCA = pathTrain.parent

    # A comma-separated values (csv) file is returned as a DataFrame: two-dimensional data structure with labeled axes.
    df_train = pd.read_csv(pathTrain)
    X_train = df_train.drop("labels", 1)  # Dataset senza colonna labels, su cui fare PCA
    Y_train = df_train["labels"]  # Solo le label, da reinserire dopo la PCA

    df_test = pd.read_csv(pathTest)
    X_test = df_test.drop("labels", 1)  # Dataset senza colonna labels, su cui fare PCA
    Y_test = df_test["labels"]  # Solo le label, da reinserire dopo la PCA

    # Feature Scaling
    sc = StandardScaler()
    sc.fit(X_train)
    X_train_scaled = sc.transform(X_train)
    X_test_scaled = sc.transform(X_test)

    # Feature Extraction
    pca = PCA(n_components)
    pca.fit(X_train_scaled)
    X_train_PCA = pca.transform(X_train_scaled)
    X_test_PCA = pca.transform(X_test_scaled)

    # Restore columns name for X_train and relative labels from Y_train
    PCA_df_train = pd.DataFrame(data=X_train_PCA, columns=utils.createFeatureList(n_components))
    PCA_df_train = pd.concat([PCA_df_train, Y_train], axis=1)
    # Restore columns name for X_test and relative labels from Y_test
    PCA_df_test = pd.DataFrame(data=X_test_PCA, columns=utils.createFeatureList(n_components))
    PCA_df_test = pd.concat([PCA_df_test, Y_test], axis=1)

    # save output in csv
    pathFileYourPCATrain = pathFileYourPCA / "yourPCA_Train.csv"
    pathFileYourPCATest = pathFileYourPCA / "yourPCA_Test.csv"
    PCA_df_train.to_csv(pathFileYourPCATrain, index=False)
    PCA_df_test.to_csv(pathFileYourPCATest, index=False)

    print("Feature Extraction result for: " + pathTrain.__str__())
    print(PCA_df_train.head())
    print("Feature Extraction result for: " + pathTest.__str__())
    print(PCA_df_test.head())

    if classification:
        df_to_predict = pd.read_csv(pathToPredict, header=None)
        df_to_predict.columns = X_train.columns
        print(df_to_predict)

        # Scaling
        X_to_predict_scaled = sc.transform(df_to_predict)
        # Extraction with PCA
        X_to_predict_PCA = pca.transform(X_to_predict_scaled)

        PCA_df_to_predict = pd.DataFrame(data=X_to_predict_PCA)


        #print("Il valore medio della varianza é: "+pca.explained_variance_ratio_)


        # save output in csv
        pathFileYourPCAToPredict = pathFileYourPCA / "doPredictionFE.csv"
        PCA_df_to_predict.to_csv(pathFileYourPCAToPredict, index=False, header=False)

        print("Feature Extraction result for: " + pathToPredict.__str__())
        print(PCA_df_to_predict.head())

    if n_components == 2 and len(Y_train.unique()) < 7:
        plt.figure(dpi=150, facecolor='w', edgecolor='k')
        classes = Y_train.unique()  # find nique values for labels
        cycol = cycle('rbgcmyk')  # possible colors for labels
        for clas in classes:
            plt.scatter(PCA_df_train.loc[PCA_df_train['labels'] == clas, 'feature1'],
                        PCA_df_train.loc[PCA_df_train['labels'] == clas, 'feature2'],
                        c=next(cycol))

        plt.xlabel('feature1', fontsize=12)
        plt.ylabel('feature2', fontsize=12)
        plt.title('2D PCA', fontsize=15)
        plt.legend(Y_train.unique().data)
        plt.grid()
        plt.savefig(pathFileYourPCA / 'graphFE', dpi=150)
        plt.show()

    if n_components == 3    :

        plt.figure(dpi=150, facecolor='w', edgecolor='k')
        ax = plt.axes(projection='3d')
        classes = Y_train.unique()  # find nique values for labels
        for clas in classes:
            ax.scatter3D(PCA_df_train.loc[PCA_df_train['labels'] == clas, 'feature1'],
                         PCA_df_train.loc[PCA_df_train['labels'] == clas, 'feature2'],
                         PCA_df_train.loc[PCA_df_train['labels'] == clas, 'feature3']
                         )

        ax.set_xlabel('feature1', fontsize=12)
        ax.set_ylabel('feature2', fontsize=12)
        ax.set_zlabel('feature3', fontsize=12)
        plt.title('3D PCA', fontsize=15)
        plt.legend(Y_train.unique().data)
        plt.grid()
        plt.savefig(pathFileYourPCA / 'graphFE', dpi=150)
        plt.show()

    return pathFileYourPCATrain, pathFileYourPCATest
