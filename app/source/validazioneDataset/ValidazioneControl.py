from flask import request
from app import app
from app.source.utils import addAttribute
from app.source.validazioneDataset import train_testSplit
from app.source.validazioneDataset import kFoldValidation
from distutils.util import strtobool


@app.route('/validazioneControl', methods=['POST'])
#@login_required
def validazioneControl():
    userpath = request.form.get('userpath')
    userpathTest = request.form.get('userpathTest')
    simpleSplit = request.form.get('simpleSplit')
    kFold = request.form.get('kFold')
    k = request.form.get('k', type=int)
    print("simpleSplit in VC: ", simpleSplit)
    print("kFold in VC: ", kFold)
    print("k in VC: ", k)

    if kFold and k < 2:
        # si dovrebbe anche controllare che k non sia maggiore nel numero di righe del dataset;
        # il design goal della robustezza ha priorità basse, dunque evitiamo il controllo
        return "impossibile eseguire kfold validation se k<2!"

    if simpleSplit and kFold:
        return "impossibile eseguirle entrambe!"

    if not simpleSplit and not kFold:
        if not userpathTest:
            return "Inserire dataset di Test"
        addAttribute.addAttribute(userpath, 'Data_training.csv')
        addAttribute.addAttribute(userpathTest, 'Data_testing.csv')
        return 'Data_training.csv', 'Data_testing.csv'

    valida(userpath, simpleSplit, kFold, k)

    return "Exiting from validazioneControl"


def valida(userpath: str, simpleSplit: bool, kFold: bool, k: int):
    """
    This function is going to validate a given Dataset with kFoldValidation or train_testSplit

    :param userpath: string that points to the location of the dataset that is going to be validated
    :param simpleSplit: boolean flag that indicated whether the user wants to execute simpleSplit or not
    :param kFold: boolean flag that indicated whether the user wants to execute kFoldValidation or not
    :param k: number of groups that a given data sample will be split into
    :return: two validated dataset: 'Data_training.csv', 'Data_testing.csv'
    :rtype: (str,str)
    """

    if simpleSplit:
        addAttribute.addAttribute(userpath, 'featureDataset.csv')
        train_testSplit.splitDataset('featureDataset.csv')  # crea 'Data_training.csv' e 'Data_testing.csv'
    elif kFold:
        kFoldValidation.cross_fold_validation(userpath, k)

    return 'Data_training.csv', 'Data_testing.csv'
