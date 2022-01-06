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


@app.route('/formPage')
def formPage():
    return render_template('formDataset.html')


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutus.html')


@app.route('/formcontrol', methods=['GET', 'POST'])
def smista():
    print('Request send on ')
    ROOT_DIR = pathlib.Path(__file__).cwd()
    ext_ok = ['txt', 'csv', 'data']
    # log.log()

    # Dataset Train from form
    file = request.files.get('userfile')
    temp = file.filename
    extension = temp.split('.')[-1]
    if not ext_ok.__contains__(extension):
        return 'Il file Dataset Train ha un estensione non ammessa!'
    if file is None:
        return 'No Train set uploaded'
    uploaddir = ROOT_DIR / 'upload_dataset/'
    userfile_name = file.filename
    userpath = uploaddir / userfile_name
    file.save(userpath)
    if file.content_length > 80000000:
        return 'Il file è troppo grande!'

    # Dataset Test from form
    file1 = request.files.get('userfile1')
    temp = file1.filename
    extension = temp.split('.')[-1]
    userpathTest = ''
    if file1.__sizeof__() != 0 and not ext_ok.__contains__(extension):
        return 'Il file Dataset Test ha un estensione non ammessa!'
    if file1.__sizeof__() != 0:
        userpathTest = uploaddir / file1.filename
        file1.save(userpathTest)
    if file1.content_length > 80000000:
        return 'Il file è troppo grande!'


    # Dataset to Predict from form
    # userpathToPredict = 'app/source/classificazioneDataset/doPrediction1.csv'
    file2 = request.files.get('userfile2')
    temp = file2.filename
    print("TempDataToPredict: ", temp)
    print("file2: ", file2)
    extension = temp.split('.')[-1]
    userpathToPredict = ''
    if file2.__sizeof__() != 0 and not ext_ok.__contains__(extension):
        return 'Il file to Predict ha un estensione non ammessa!'
    if file2.__sizeof__() != 0:
        userpathToPredict = uploaddir / file2.filename
        file2.save(userpathToPredict)
    if file2.content_length > 80000000:
        return 'Il file è troppo grande!'

    prototypeSelection = request.form.get('reduce1')
    featureExtraction = request.form.get('reduce')
    autosplit = request.form.get('test')

    print("Userpath: ", userpath)
    print("Dataset: ", file.filename)
    print("UserpathTest: ", userpathTest)
    print("DatasetTest: ", file1.filename)
    print("UserpathToPredict: ", userpathToPredict)
    print("DatasetToPredict: ", file2.filename)
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
    doQSVM = False
    # token= request.form.get('token') da inserire nel form
    token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
    # assert isinstance(current_user, User)
    # salvataggiodatabase = Dataset(email_user=current_user.email, name=file.filename, upload_date=datetime.now(),
    #                               paths=userpath, simple_split=bool(autosplit), ps=bool(prototypeSelection),
    #                               fe=bool(featureExtraction), k_fold=bool(kFold),doQSVM=bool(doQSVM))
    # db.session.add(salvataggiodatabase)
    # db.session.commit()
    # path = Path.cwd().parents[2] / 'upload_dataset' / current_user.email / salvataggiodatabase.id
    # if not path.is_dir():
    #     path.mkdir()

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
