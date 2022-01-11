import pathlib
from datetime import datetime

from flask import render_template, request, Response
from app import app, db
from app.models import User, Dataset
from app.source.utils import utils
from flask_login import current_user, login_required
from flask import session


@app.route('/')
@app.route('/home')
def homepage():  # put application's code here
    return render_template('index.html')


@app.route('/LogIn')
def loginPage():
    return render_template('login.html')


@app.route('/SignIn')
def registrationPage():
    return render_template('registration.html')


@app.route('/formPage')
def formPage():
    return render_template('formDataset.html')


@app.route('/preprocessingPage')
def preprocessingPage():
    return render_template('preprocessing.html')


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutus.html')


@app.route('/formcontrol', methods=['GET', 'POST'])
@login_required
def smista():
    print("\nIn smista carico le richieste dal form...")
    dataset_train = request.files.get('dataset_train')
    dataset_test = request.files.get('dataset_test')
    dataset_prediction = request.files.get('dataset_prediction')

    autosplit = request.form.get('splitDataset')
    print("AutoSplit: ", autosplit)
    prototypeSelection = request.form.get('reducePS')
    print("Prototype Selection: ", prototypeSelection)
    featureExtraction = request.form.get('reduceFE')
    print("Feature Extraction: ", featureExtraction)
    doQSVM = request.form.get('doQSVM')
    print("doQSVM: ", doQSVM)

    # Advanced option
    simpleSplit = request.form.get('simpleSplit')
    print("simpleSplit: ", simpleSplit)
    kFold = request.form.get('kFold')
    print("kFold: ", kFold)
    k = request.form.get('kFoldValue', type=int)
    print("kFoldValue: ", k)
    # numero di righe dopo la Prototype Selection con GA
    numRawsPS = request.form.get('nrRows', type=int)
    print("numRawsPS:  ", numRawsPS)
    # numero di colonne dopo la Feature Extraction con PCA
    numColsFE = request.form.get('nrColumns', type=int)
    print("numColsFE: ", numColsFE)

    assert isinstance(current_user, User)
    salvataggiodatabase = Dataset(
        email_user=current_user.email,
        name=dataset_train.filename,
        upload_date=datetime.now(),
        simple_split=bool(autosplit),
        ps=bool(prototypeSelection),
        fe=bool(featureExtraction),
        k_fold=bool(kFold),
        doQSVM=bool(doQSVM))
    db.session.add(salvataggiodatabase)
    db.session.commit()
    paths = upload(dataset_train, dataset_test,
                   dataset_prediction, str(salvataggiodatabase.id))
    if paths == (-1):
        print("Estensione non valida")
        return Response(status=400)
    userpathTrain = paths[0]
    userpathTest = paths[1]
    userpathToPredict = paths[2]
    dataPath = userpathTrain.parent

    # Validazione
    print("\nIn validazione...")
    if autosplit and not kFold and not simpleSplit:
        # se l'utente vuole fare autosplit ma non seleziona opzioni avanzate,
        # di dafault faccio simpleSplit
        simpleSplit = True
    if not autosplit:
        kFold = None
        simpleSplit = None
    app.test_client().post(
        "/validazioneControl",
        data=dict(
            userpath=userpathTrain,
            userpathTest=userpathTest,
            simpleSplit=simpleSplit,
            kFold=kFold,
            k=k))
    if kFold:
        return "ora scarica e procedi dalla home specificando quali usare"

    # Preprocessing
    print("\nIn preprocessing...")
    app.test_client().post(
        "/preprocessingControl",
        data=dict(
            userpath=userpathTrain,
            userpathToPredict=userpathToPredict,
            prototypeSelection=prototypeSelection,
            featureExtraction=featureExtraction,
            numRawsPS=numRawsPS,
            numColsFE=numColsFE,
            doQSVM=doQSVM))
    # DataSet Train ready to be classified
    pathTrain = dataPath / 'DataSetTrainPreprocessato.csv'
    # DataSet Test ready to be classified
    pathTest = dataPath / 'DataSetTestPreprocessato.csv'

    # Classificazione
    if doQSVM:
        print("\nIn classificazione...")
        backend = request.form.get("backend")
        #backend = "ibmq_qasm_simulator"
        if request.form.get('token'):
            token = request.form.get('token')
        else:
            token = current_user.token
        if request.form.get('email'):
            email = request.form.get('email')
        else:
            email = current_user.email

        if featureExtraction:
            features = utils.createFeatureList(
                numColsFE)  # lista di features per la qsvm
        else:
            features = utils.createFeatureList(
                utils.numberOfColumns(userpathTrain) - 1)
        app.test_client().post(
            "/classificazioneControl",
            data=dict(
                pathTrain=pathTrain,
                pathTest=pathTest,
                email=email,
                userpathToPredict=userpathToPredict,
                features=features,
                token=token,
                backend=backend))

    print("\n\nSmista ha finito! To the Moon!")

    return "ora classifica"


def upload(file, file1, file2, idTrainSet):
    print('Request send on ')
    ext_ok = ['txt', 'csv', 'data']
    # log.log()

    # Dataset Train from form

    temp = file.filename
    extension = temp.split('.')[-1]
    if not ext_ok.__contains__(extension):
        return -1
    if file is None:
        return -1
    uploaddir = pathlib.Path(
        __file__).parents[1] / 'upload_dataset' / current_user.email / str(idTrainSet)
    if not uploaddir.exists():
        uploaddir.mkdir()
    userfile_name = file.filename
    userpath = uploaddir / userfile_name
    file.save(userpath)
    if file.content_length > 80000000:
        return -1

    # Dataset Test from form
    temp = file1.filename
    extension = temp.split('.')[-1]
    userpathTest = ''
    if file1.filename != "" and not ext_ok.__contains__(extension):
        # print(file1.filename)
        return -1
    if file1.filename != "":
        userpathTest = uploaddir / file1.filename
        file1.save(userpathTest)
    if file1.content_length > 80000000:
        return -1

    # Dataset to Predict from form
    # userpathToPredict = 'app/source/classificazioneDataset/doPrediction.csv'
    temp = file2.filename
    # print("TempDataToPredict: ", temp)
    # print("file2: ", file2)
    extension = temp.split('.')[-1]
    userpathToPredict = ''
    if file2.filename != "" and not ext_ok.__contains__(extension):
        return -1
    if file2.filename != "" != 0:
        userpathToPredict = uploaddir / file2.filename
        file2.save(userpathToPredict)
    if file2.content_length > 80000000:
        return -1
    print("UserpathTrain: ", userpath)
    # print("DatasetTrain: ", file.filename)
    print("UserpathTest: ", userpathTest)
    # print("DatasetTest: ", file1.filename)
    print("UserpathToPredict: ", userpathToPredict)
    # print("DatasetToPredict: ", file2.filename)
    paths = [userpath, userpathTest, userpathToPredict]
    return paths
