
import pathlib
from datetime import datetime
from pathlib import Path

from flask_login import current_user

from app import models
from flask import render_template, request
import subprocess as sp
from app import app, db
from app.source.utils import utils
from app.models import Dataset
from app.models import User
from app.source.utils import getlog as log
from app.source.validazioneDataset.ValidazioneControl import valida
from app.source.preprocessingDataset.PreprocessingControl import preprocessing
from app.source.classificazioneDataset.ClassificazioneControl import classify
from app.source.classificazioneDataset.ClassificazioneControl import getClassifiedDataset


@app.route('/')
@app.route('/home')
def homepage():  # put application's code here
    return render_template('index.html')


@app.route('/LogIn')
def loginPage():
    return render_template('login.html')



@app.route('/formcontrol', methods=['GET', 'POST'])
def smista():
    print('Request send on ')
    ROOT_DIR = pathlib.Path(__file__).cwd()
    # log.log()
    file = request.files.get('userfile')




    ext_ok = ['txt', 'csv', 'data']
    temp = file.filename
    extension = temp.split('.')[-1]
    print(extension)
    if not ext_ok.__contains__(extension):
        return 'Il file ha un estensione non ammessa!'

    if file is None:
        return 'No Train set uploaded'

    # Dataset Train from form
    uploaddir = ROOT_DIR / 'upload_dataset/'
    userfile_name = file.filename
    userpath = uploaddir / userfile_name


    # Dataset Test from form
    userpathTest = ''

    # Dataset to Predict from form
    userpathToPredict = 'app/source/classificazioneDataset/doPrediction1.csv'

    if file.content_length > 80000000:
        return 'Il file è troppo grande!'
    prototypeSelection = request.form.get('reduce1')
    featureExtraction = request.form.get('reduce')
    autosplit = request.form.get('test')

    print("Userpath: ", userpath)
    print("Dataset: ", file.filename)
    # Recupero le impostazioni dell'utente, cioè
    # quali operazioni vuole effettuare e, in caso di QSVM, anche il token
    print("AutoSplit: ", autosplit)
    numRawsPS = 50  # numero di righe dopo la Prototype Selection con GA
    print("Prototype Selection: ", prototypeSelection)
    numColsFE = 3  # numero di colonne dopo la Feature Extraction con PCA
    print("Feature Extraction: ", featureExtraction)
    # kFold= request.form.get('kFold') da inserire nel form
    kFold = False
    k = 10
    # doQSVM= request.form.get('QSVM') da inserire nel form
    doQSVM = True
    # token= request.form.get('token') da inserire nel form
    token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'

    # assert isinstance(current_user, User)
    # salvataggiodatabase = Dataset(email_user=current_user.email, name=file.filename, upload_date=datetime.now(),
    #                               paths=userpath, simple_split=bool(autosplit), ps=bool(prototypeSelection),
    #                               fe=bool(featureExtraction), k_fold=bool(kFold))
    # db.session.add(salvataggiodatabase)
    # db.session.commit()
    # path = Path.cwd().parents[2] / 'upload_dataset' / current_user.email / salvataggiodatabase.id
    # if not path.is_dir():
    #     path.mkdir()

    file.save(userpath)







    numCols = utils.numberOfColumns(userpath)
    features = utils.createFeatureList(numCols - 1)

    valida(userpath, userpathTest, autosplit, kFold, k)
    pathTrain = 'Data_training.csv'
    pathTest = 'Data_testing.csv'
    if kFold:
        return "ora scarica e procedi dalla home specificando quali usare"

    # Preprocessing
    if prototypeSelection or featureExtraction:
        preprocessing(userpath, prototypeSelection, featureExtraction, numRawsPS, numColsFE, doQSVM)
        pathTrain = 'DataSetTrainPreprocessato.csv'
        pathTest = 'DataSetTestPreprocessato.csv'

    # Classificazione
    # backend = request.form.get("backend")
    backend = 'ibmq_jakarta'
    backend = 'ibmq_qasm_simulator'

    if doQSVM:
        if featureExtraction:
            features = utils.createFeatureList(numColsFE)  # lista di features per la qsvm
            userpathToPredict = "doPredictionFE.csv"
        result: dict = classify(pathTrain, pathTest, userpathToPredict, features, token, backend)
        if result != 0:
            getClassifiedDataset(result)

        # if result==0 il token non è valido
        # if result==1 errore su server IBM (comunica errore tramite email)
        # if result["noBackend"]==True il backend selezionato non è attivo per il token oppure non ce ne sono disponibili di default quindi usa il simulatore
        # aggiungere controlli per result["noBackend"]==True e result==0 per mostrare gli errori tramite frontend

    return "ora classifica"
