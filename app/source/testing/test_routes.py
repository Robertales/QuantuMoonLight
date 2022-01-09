import pathlib


def test_smista():
    path = pathlib.Path(__file__).parent
    pathtrain = path / "testingFiles" / "Data_training.csv"
    pathtest = path / "testingFiles" / "Data_testing.csv"
    pathpred = path / "testingFiles" / "doPrediction.csv"
    dataset_train = open(str(pathtrain))
    dataset_test = open(str(pathtest))
    dataset_prediction = open(str(pathpred))
    print(dataset_prediction.name)
    print(dataset_test.name)
    print(dataset_train.name)
#i tre dataset sono tre file da mandare nella richiesta a smista, diventeranno poi quelli presi dalla funzione e passati ad upload