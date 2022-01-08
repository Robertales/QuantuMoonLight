import pathlib
from flask import render_template, request
from app import app
from app.source.utils import utils
from distutils.util import strtobool
from flask_login import current_user


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
def smista():


    # if not current_user.is_authenticated:
    #     return render_template('login.html')

    print("\nIn smista carico le richieste dal form...")
    dataset_train = request.files.get('dataset_train')
    dataset_test = request.files.get('dataset_test')
    dataset_prediction = request.files.get('dataset_prediction')
    paths = upload(dataset_train, dataset_test, dataset_prediction)
    userpath = paths[0]
    userpathTest = paths[1]
    userpathToPredict = paths[2]
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
    numRawsPS = request.form.get('nrRows', type=int)  # numero di righe dopo la Prototype Selection con GA
    print("numRawsPS:  ", numRawsPS)
    numColsFE = request.form.get('nrColumns', type=int)  # numero di colonne dopo la Feature Extraction con PCA
    print("numColsFE: ", numColsFE)


    # assert isinstance(current_user, User)
    # salvataggiodatabase = Dataset(email_user=current_user.email, name=file.filename, upload_date=datetime.now(),
    #                               path=userpath, simple_split=bool(autosplit), ps=bool(prototypeSelection),
    #                               fe=bool(featureExtraction), k_fold=bool(kFold), doQSVM=bool(doQSVM))
    # db.session.add(salvataggiodatabase)
    # db.session.commit()
    # path = Path.cwd()/ 'upload_dataset' / current_user.email / str(salvataggiodatabase.id)
    # if not path.exists():
    #     path.mkdir()

    # Validazione
    print("\nIn validazione...")
    if autosplit and not kFold and not simpleSplit:
        # se l'utente vuole fare autosplit ma non seleziona opzioni avanzate, di dafault faccio simpleSplit
        simpleSplit = True
    if not autosplit:
        kFold = None
        simpleSplit = None
    app.test_client().post("/validazioneControl", data=dict(userpath=userpath, userpathTest=userpathTest,
                                                            simpleSplit=simpleSplit, kFold=kFold, k=k))
    if kFold:
        return "ora scarica e procedi dalla home specificando quali usare"

    # Preprocessing
    print("\nIn preprocessing...")
    app.test_client().post("/preprocessingControl", data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                                              prototypeSelection=prototypeSelection,
                                                              featureExtraction=featureExtraction,
                                                              numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
    pathTrain = 'DataSetTrainPreprocessato.csv'  # DataSet Train ready to be classified
    pathTest = 'DataSetTestPreprocessato.csv'  # DataSet Test ready to be classified

    # Classificazione
    if doQSVM:
        print("\nIn classificazione...")
        backend = request.form.get("backend")
        backend = "ibmq_qasm_simulator"
        # token= request.form.get('token') da inserire nel form
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        if featureExtraction:
            features = utils.createFeatureList(numColsFE)  # lista di features per la qsvm
        else:
            features = utils.createFeatureList(utils.numberOfColumns(userpath) - 1)
        app.test_client().post("/classificazioneControl", data=dict(pathTrain=pathTrain, pathTest=pathTest, #dataset=salvataggiodatabase,
                                                                    userpathToPredict=userpathToPredict,
                                                                    features=features, token=token, backend=backend))

    print("\n\nSmista ha finito! To the Moon!")

    return "ora classifica"


def upload(file, file1, file2):
    print('Request send on ')
    ROOT_DIR = pathlib.Path(__file__).cwd()
    ext_ok = ['txt', 'csv', 'data']
    # log.log()

    # Dataset Train from form

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
    temp = file1.filename
    extension = temp.split('.')[-1]
    userpathTest = ''
    if file1.filename != "" and not ext_ok.__contains__(extension):
        # print(file1.filename)
        return 'Il file Dataset Test ha un estensione non ammessa!'
    if file1.filename != "":
        userpathTest = uploaddir / file1.filename
        file1.save(userpathTest)
    if file1.content_length > 80000000:
        return 'Il file è troppo grande!'

    # Dataset to Predict from form
    # userpathToPredict = 'app/source/classificazioneDataset/doPrediction.csv'
    temp = file2.filename
    # print("TempDataToPredict: ", temp)
    # print("file2: ", file2)
    extension = temp.split('.')[-1]
    userpathToPredict = ''
    if file2.filename != "" and not ext_ok.__contains__(extension):
        return 'Il file to Predict ha un estensione non ammessa!'
    if file2.filename != "" != 0:
        userpathToPredict = uploaddir / file2.filename
        file2.save(userpathToPredict)
    if file2.content_length > 80000000:
        return 'Il file è troppo grande!'
    print("UserpathTrain: ", userpath)
    # print("DatasetTrain: ", file.filename)
    print("UserpathTest: ", userpathTest)
    # print("DatasetTest: ", file1.filename)
    print("UserpathToPredict: ", userpathToPredict)
    # print("DatasetToPredict: ", file2.filename)
    paths = [userpath, userpathTest, userpathToPredict]
    return paths
