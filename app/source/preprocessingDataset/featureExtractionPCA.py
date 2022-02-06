import pathlib
import warnings
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from app.source.utils import utils

warnings.simplefilter(action="ignore", category=FutureWarning)


def callFeatureExtraction(
        path: pathlib.Path,
        output: pathlib.Path,
        n_components=2
):
    """
    This function executes the Feature Extraction on the given dataset

    :param path: path to the location of the dataset that is going to be reduced with FE
    :param output: path to the location of the dataset preprocessed with FE
    :param n_components: number of new columns
    :return: string that points to the location of the dataset preprocessed with FE
    :rtype: str
    """
    print("Into callFeatureExtraction...")

    # A comma-separated values (csv) file is returned as a DataFrame: two-dimensional data structure with labeled axes.
    df = pd.read_csv(path)
    X = df.drop("labels", 1)  # Dataset senza colonna labels, su cui fare PCA
    Y = df["labels"]  # Solo le label, da reinserire dopo la PCA

    # Feature Scaling
    sc = StandardScaler()
    X = sc.fit_transform(X)
    # print(X)

    # Feature Extraction
    pca = PCA(n_components)
    X = pca.fit_transform(X)
    # print(X)

    # Recupero i nomi delle colonne, i valori delle labels e di queste faccio anche lo scaling
    PCA_df = pd.DataFrame(data=X, columns=utils.createFeatureList(n_components))
    PCA_df = pd.concat([PCA_df, Y], axis=1)
    PCA_df['labels'] = LabelEncoder().fit_transform(PCA_df['labels'])
    # print(PCA_df.head())

    # salvataggio su output in formato csv
    pathFileYourPCA = pathlib.Path(__file__).parent
    pathFileYourPCA = pathFileYourPCA / output
    PCA_df.to_csv(pathFileYourPCA, index=False)

    return pathFileYourPCA.__str__()


def extractFeatureForPrediction(
        path: pathlib.Path, output: pathlib.Path, n_components=2
):
    """
    This function executes the Feature Extraction on the doPrediction

    :param path: path to the location of the dataset that is going to be reduced with FE
    :param output: path to the location of the dataset preprocessed with FE
    :param n_components: number of new columns
    :return: string that points to the location of the dataset preprocessed with FE
    :rtype: str
    """
    print("Into extractFeatureForPrediction...")

    # A comma-separated values (csv) file is returned as a DataFrame: two-dimensional data structure with labeled axes.
    df = pd.read_csv(path)
    X = df.drop("labels", 1)

    # Feature Scaling
    sc = StandardScaler()
    X = sc.fit_transform(X)

    # Feature Extraction
    pca = PCA(n_components)
    X = pca.fit_transform(X)

    PCA_df = pd.DataFrame(data=X)
    # salvataggio su output in formato csv
    pathFileYourPCA = pathlib.Path(__file__).parent
    pathFileYourPCA = pathFileYourPCA / output
    PCA_df.to_csv(pathFileYourPCA, index=False, header=False)

    return pathFileYourPCA.__str__()
