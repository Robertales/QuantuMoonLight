from app.source.utils import addAttribute
from app.source.validazioneDataset import train_testSplit
from app.source.validazioneDataset import kFoldValidation


def valida(userpath: str, userpathTest: str, autosplit: bool, kFold: bool, k: int):
    """
    This function is going to validate a given Dataset with kFoldValidation or train_testSplit

    :param userpath: string that points to the location of the dataset that is going to be validated
    :param userpathTest: string that points to the location of the datasetTest that is going to be
                         validated with kfoldValidation
    :param autosplit: boolean flag that indicated whether the user wants to execute autoSplit or not
    :param kFold: boolean flag that indicated whether the user wants to execute kFoldValidation or not
    :param k: number of groups that a given data sample will be split into
    :return: two validated dataset: 'Data_training.csv', 'Data_testing.csv'
    :rtype: (str,str)
    """

    if k < 2:
        # si dovrebbe anche controllare che k non sia maggiore nel numero di righe del dataset;
        # il design goal della robustezza ha priorità basse, dunque evitiamo il controllo
        print("impossibile eseguire kfold validation se k<2!")
        return 1
    if autosplit and kFold:
        print("impossibile eseguirle entrambe!")
        return 1
    elif autosplit:
        addAttribute.addAttribute(userpath, 'featureDataset.csv')
        train_testSplit.splitDataset('featureDataset.csv')  # crea 'Data_training.csv' e 'Data_testing.csv'
    elif kFold:
        kFoldValidation.cross_fold_validation(userpath, k)
    else:
        addAttribute.addAttribute(userpath, 'Data_training.csv')
        addAttribute.addAttribute(userpathTest, 'Data_testing.csv')

    return 'Data_training.csv', 'Data_testing.csv'
