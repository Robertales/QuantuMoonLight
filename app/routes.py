import os.path
import pathlib
from datetime import datetime

from imblearn.over_sampling import SMOTE
import csv as csv
from flask import render_template, request, Response, flash, redirect, url_for

from flask import render_template, request, Response, flash
from flask_login import current_user, login_required
from qiskit import IBMQ
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from app import app, db
from app.source.model.models import User, Dataset, Article, Comment
from app.source.preprocessingDataset.aggId import addId
from app.source.utils import utils
from app.source.utils import addAttribute
from sqlalchemy import func

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def homepage():  # put application's code here
    return render_template("index.html")


@app.route("/LogIn")
def loginPage():
    return render_template("login.html")


@app.route("/SignIn")
def registrationPage():
    return render_template("registration.html")


@app.route("/downloadPage")
def downloadPage():
    return render_template("downloadPage.html")


@app.route("/showList")
def showList():
    return render_template("showList.html")


@app.route("/adminPage")
def adminPage():
    return render_template("adminPage.html")

@app.route("/compareExperiments" , methods=['POST'])
def compareExperiments():

    listDataset = request.form.getlist('selectedDataset')
    datasets = Dataset.query.filter(Dataset.id.in_(listDataset)).all()

    #COMPARISION FOR TOTAL TIME
    maxTotalTime = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.total_time).first()
    minTotalTime = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.total_time.desc()).first()

    # COMPARISION FOR TRAINING TIME
    maxTrainingTime = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.training_time).first()
    minTrainingTime = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.training_time.desc()).first()

    # COMPARISION FOR PRECISION
    maxPrecision = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.precision).first()
    minPrecision = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.precision.desc()).first()

    # COMPARISION FOR ACCURACY
    maxAccuracy = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.accuracy).first()
    minAccuracy = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.accuracy.desc()).first()

    # COMPARISION FOR RECALL
    maxRecall = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.recall).first()
    minRecall = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.recall.desc()).first()

    # COMPARISION FOR MSE
    maxMSE = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.mse).first()
    minMSE = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.mse.desc()).first()

    # COMPARISION FOR MAE
    maxMAE = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.mae).first()
    minMAE = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.mae.desc()).first()

    # COMPARISION FOR RMSE
    maxRMSE = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.rmse).first()
    minRMSE = Dataset.query.filter(Dataset.id.in_(listDataset)).order_by(Dataset.rmse.desc()).first()
    return render_template("compareExperiments.html",
                           datasets=datasets,
                           maxTotalTime=maxTotalTime,
                           minTotalTime=minTotalTime,
                           maxTrainingTime=maxTrainingTime,
                           minTrainingTime=minTrainingTime,
                           maxPrecision=maxPrecision,
                           minPrecision=minPrecision,
                           maxAccuracy=maxAccuracy,
                           minAccuracy=minAccuracy,
                           maxRecall=maxRecall,
                           minRecall=minRecall,
                           maxMSE=maxMSE,
                           minMSE=minMSE,
                           maxMAE=maxMAE,
                           minMAE=minMAE,
                           maxRMSE=maxRMSE,
                           minRMSE=minRMSE
                           )

@app.route("/adminDataset")
def adminDataset():
    datasets = Dataset.query.all()
    rows = Dataset.query.count()
    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0
    v5 = 0
    for dataset in datasets:
        if dataset.simple_split: v1 += 1
        if dataset.k_fold: v2 += 1
        if dataset.ps: v3 += 1
        if dataset.fe: v4 += 1
        if dataset.model: v5 += 1
    p1 = v1 * 100 / rows
    p2 = v2 * 100 / rows
    p3 = v3 * 100 / rows
    p4 = v4 * 100 / rows
    p5 = v5 * 100 / rows
    return render_template("datasetList.html", datasets=datasets, p_ss=p1, p_kf=p2,
                           p_ps=p3, p_fe=p4, p_qv=p5)


@app.route("/userDataset")
def userDataset():
    datasets = Dataset.query.filter_by(email_user=current_user.email)
    rows = Dataset.query.filter_by(email_user=current_user.email).count()
    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0
    v5 = 0
    for dataset in datasets:
        if dataset.simple_split: v1 += 1
        if dataset.k_fold: v2 += 1
        if dataset.ps: v3 += 1
        if dataset.fe: v4 += 1
        if dataset.model: v5 += 1
    p1 = v1 * 100 / rows
    p2 = v2 * 100 / rows
    p3 = v3 * 100 / rows
    p4 = v4 * 100 / rows
    p5 = v5 * 100 / rows
    return render_template("datasetList.html", datasets=datasets, p_ss="{:.2f}".format(p1), p_kf="{:.2f}".format(p2),
                           p_ps="{:.2f}".format(p3), p_fe="{:.2f}".format(p4), p_qv="{:.2f}".format(p5))


@app.route("/modifyUserPage")
def modifyUserPage():
    return render_template("modifyUserByAdmin.html")


@app.route("/modifyUser")
def modifyUser():
    return render_template("modifyUser.html")


@app.route("/sendEmail")
def sendEmail():
    return render_template("sendEmail.html")


@app.route("/blog")
def blog():
    posts = Article.query.order_by(Article.data.desc()).all()

    return render_template("blog.html", posts=posts)


@app.route("/ArticleApproval")
def ArticleApproval():
    posts = Article.query.order_by(Article.data.desc()).all()

    return render_template("ArticleApproval.html", posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Article.query.filter_by(id=post_id).one()
    comments = Comment.query.filter_by(id_article=post_id).all()
    return render_template('post.html', post=post, comments=comments)


@app.route('/add')
@login_required
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
@login_required
def addpost():
    title = request.form['title']
    author = current_user.username
    email = current_user.email
    body = request.form['content']

    post = Article(title=title, author=author, body=body, data=datetime.now(), email_user=email)

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('blog'))


@app.route('/enableArticle/<int:article_id>', methods=['POST','GET'])
def enableArticle(article_id):
    article = Article.query.filter_by(id=article_id).one()
    article.authorized = True
    db.session.commit()

    return redirect(url_for('blog'))


@app.route('/enableComment/<int:comment_id>', methods=['POST'])
def enableComment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).one()
    comment.authorized = True
    db.session.commit()

    return redirect(url_for('blog'))

@app.route('/addcomment', methods=['POST'])
@login_required
def addcomment():
    author = current_user.username
    email = current_user.email
    body = request.form['content']
    id = request.form['artId']

    comment = Comment(email_user=email, author=author, body=body, data=datetime.now(), id_article=id)

    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('post', post_id=id))


@app.route("/userPage")
def userPage():
    return render_template("userPage.html")


@app.route("/formPage")
def formPage():
    return render_template("formDataset.html")


@app.route("/preprocessingPage")
def preprocessingPage():
    return render_template("preprocessing.html")


@app.route("/aboutUs")
def aboutUs():
    return render_template("aboutus.html")


@app.route("/formcontrol", methods=["GET", "POST"])
@login_required
def smista():
    print("\nIn smista carico le richieste dal form...")
    dataset_train = request.files.get("dataset_train")
    dataset_test = request.files.get("dataset_test")
    dataset_prediction = request.files.get("dataset_prediction")

    autosplit = request.form.get("splitDataset")
    print("AutoSplit: ", autosplit)
    prototypeSelection = request.form.get("reducePS")
    print("Prototype Selection: ", prototypeSelection)
    featureExtraction = request.form.get("reduceFE")
    print("Feature Extraction: ", featureExtraction)
    model = request.form.get("model")
    print("model: ", model)
    loss = request.form.get("loss")
    print("loss: ", loss)
    optimizer = request.form.get("optimizer")
    print("optimizer: ", optimizer)
    C = request.form.get("C")
    print("C: ", C)
    tau = request.form.get("tau")
    print("tau: ", tau)
    max_iter = request.form.get("max_iter")
    print("max_iter: ", max_iter)
    data_imputation = request.form.get("imputation")
    print("imputation: ", data_imputation)
    scaling = request.form.get("scaling")
    print("scaling: ", scaling)
    balancing = request.form.get("balancing")
    print("balancing: ", balancing)

    # Advanced option
    print(request.form["Radio"])
    if request.form["Radio"] == "simpleSplit":
        simpleSplit = "simpleSplit"
        kFold = None
    elif request.form["Radio"] == "kFold":
        simpleSplit = None
        kFold = "kFold"

    # simpleSplit = request.form.get("simpleSplit")
    print("simpleSplit: ", simpleSplit)
    # kFold = request.form.get("kFold")
    print("kFold: ", kFold)
    k = request.form.get("kFoldValue", type=int)
    print("kFoldValue: ", k)
    # numero di righe dopo la Prototype Selection con GA
    numRawsPS = request.form.get("nrRows", type=int)
    print("numRawsPS:  ", numRawsPS)
    # numero di colonne dopo la Feature Extraction con PCA
    numColsFE = request.form.get("nrColumns", type=int)
    print("numColsFE: ", numColsFE)

    assert isinstance(current_user, User)
    salvataggiodatabase = Dataset(
        email_user=current_user.email,
        name=dataset_train.filename,
        upload_date=datetime.now(),
        simple_split=bool(simpleSplit),
        ps=bool(prototypeSelection),
        fe=bool(featureExtraction),
        k_fold=bool(kFold),
        model=model,
    )
    db.session.add(salvataggiodatabase)
    db.session.commit()
    paths = upload(
        dataset_train,
        dataset_test,
        dataset_prediction,
        str(salvataggiodatabase.id),
    )
    if paths == (-1):
        print("Estensione non valida")
        return Response(status=400)
    userpathTrain = paths[0]
    userpathTest = paths[1]
    userpathToPredict = paths[2]
    dataPath = userpathTrain.parent

    if data_imputation:
        # Data Imputation
        print("DATA IMPUTATION")
        missing_values = ["n/n", "na", "--", "nan", "NaN"]
        if os.path.exists(userpathTrain):
            addAttribute.addAttribute(userpathTrain, userpathTrain.parent / "TrainImputation.csv")
            train = pd.read_csv(userpathTrain.parent / "TrainImputation.csv", na_values=missing_values)
            for column in train:
                train[column] = train[column].fillna(train[column].mean())
            train.to_csv(userpathTrain, index=False, header=False)
            os.remove(userpathTrain.parent / "TrainImputation.csv")
        if os.path.exists(userpathTest):
            addAttribute.addAttribute(userpathTest, userpathTest.parent / "TestImputation.csv")
            test = pd.read_csv(userpathTest.parent / "TestImputation.csv", na_values=missing_values)
            for column in test:
                test[column] = test[column].fillna(test[column].mean())
            test.to_csv(userpathTest, index=False, header=False)
            os.remove(userpathTest.parent / "TestImputation.csv")
        if os.path.exists(userpathToPredict):
            addAttribute.addAttribute(userpathToPredict, userpathToPredict.parent / "PredictImputation.csv")
            predict = pd.read_csv(userpathToPredict.parent / "PredictImputation.csv", na_values=missing_values)
            for column in predict:
                predict[column] = predict[column].fillna(predict[column].mean())
            predict.to_csv(userpathToPredict, index=False, header=False)
            os.remove(userpathToPredict.parent / "PredictImputation.csv")


    if scaling == "MinMax":
        #Scaling normalization
        scaler = MinMaxScaler()
        print("MINMAX SCALING")
        if os.path.exists(userpathTrain):
            addAttribute.addAttribute(userpathTrain, userpathTrain.parent / "TrainScaled.csv")
            data = pd.read_csv(userpathTrain.parent / "TrainScaled.csv")
            train = data.drop("labels", axis=1)
            train_scaled = scaler.fit_transform(train)
            df = pd.DataFrame(train_scaled)
            df.insert(loc=len(df.columns), column="labels", value=data["labels"].values)
            df.to_csv(userpathTrain, index=False, header=False)
            os.remove(userpathTrain.parent / "TrainScaled.csv")
        if os.path.exists(userpathTest):
            addAttribute.addAttribute(userpathTest, userpathTest.parent / "TestScaled.csv")
            data = pd.read_csv(userpathTest.parent / "TestScaled.csv")
            test = data.drop("labels", axis=1)
            test_scaled = scaler.fit_transform(test)
            df = pd.DataFrame(test_scaled)
            df.insert(loc=len(df.columns), column="labels", value=data["labels"].values)
            df.to_csv(userpathTest, index=False, header=False)
            os.remove(userpathTest.parent / "TestScaled.csv")
        if os.path.exists(userpathToPredict):
            addAttribute.addAttribute(userpathToPredict, userpathToPredict.parent / "PredictScaled.csv")
            predict = pd.read_csv(userpathToPredict.parent / "PredictScaled.csv")
            predict_scaled = scaler.fit_transform(predict)
            df = pd.DataFrame(predict_scaled)
            df.to_csv(userpathToPredict, index=False, header=False)
            os.remove(userpathToPredict.parent / "PredictScaled.csv")
    elif scaling == "Standard":
        # Scaling standardization z-score
        scaler = StandardScaler()
        print("STANDARD SCALING")
        if os.path.exists(userpathTrain):
            addAttribute.addAttribute(userpathTrain, userpathTrain.parent / "TrainScaled.csv")
            data = pd.read_csv(userpathTrain.parent / "TrainScaled.csv")
            train = data.drop("labels", axis=1)
            train_scaled = scaler.fit_transform(train)
            df = pd.DataFrame(train_scaled)
            df.insert(loc=len(df.columns), column="labels", value=data["labels"].values)
            df.to_csv(userpathTrain, index=False, header=False)
            os.remove(userpathTrain.parent / "TrainScaled.csv")
        if os.path.exists(userpathTest):
            addAttribute.addAttribute(userpathTest, userpathTest.parent / "TestScaled.csv")
            data = pd.read_csv(userpathTest.parent / "TestScaled.csv")
            test = data.drop("labels", axis=1)
            test_scaled = scaler.fit_transform(test)
            df = pd.DataFrame(test_scaled)
            df.insert(loc=len(df.columns), column="labels", value=data["labels"].values)
            df.to_csv(userpathTest, index=False, header=False)
            os.remove(userpathTest.parent / "TestScaled.csv")
        if os.path.exists(userpathToPredict):
            addAttribute.addAttribute(userpathToPredict, userpathToPredict.parent / "PredictScaled.csv")
            predict = pd.read_csv(userpathToPredict.parent / "PredictScaled.csv")
            predict_scaled = scaler.fit_transform(predict)
            df = pd.DataFrame(predict_scaled)
            df.to_csv(userpathToPredict, index=False, header=False)
            os.remove(userpathToPredict.parent / "PredictScaled.csv")

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
            k=k,
        ),
    )
    if kFold:
        return render_template(
            "downloadPage.html",
            ID=salvataggiodatabase.id)
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
            doQSVM=True,
        ),
    )
    # DataSet Train ready to be classified
    pathTrain = dataPath / "DataSetTrainPreprocessato.csv"
    # DataSet Test ready to be classified
    pathTest = dataPath / "DataSetTestPreprocessato.csv"

    if balancing:
        # Data Balancing
        x_train = pd.read_csv(pathTrain)
        y_train = x_train["labels"].values
        x_train = x_train.drop("labels", axis=1)
        x_train = x_train.drop("Id", axis=1)
        columns = x_train.columns
        print("DATA BALANCING")
        x_train_array = x_train.to_numpy()
        sm = SMOTE()
        x_train_array_bal, y_train_bal = sm.fit_resample(x_train_array, y_train)
        df = pd.DataFrame(x_train_array_bal)
        #df = df.iloc[:, 1:]
        df.columns = columns
        df.insert(loc=len(df.columns), column="labels", value=y_train_bal)
        df.to_csv(pathTrain, index=False)
        addId(pathTrain, pathTrain)

    # Classificazione
    if model != "None":
        print("\nClassification...")
        backend = request.form.get("backend")
        if request.form.get("token"):
            token = request.form.get("token")
        else:
            token = current_user.token

        # check if the token is valid
        try:
            IBMQ.enable_account(token)
            IBMQ.disable_account()
        except BaseException:
            flash("Token not valid, the classification will not occur", "error")

        if request.form.get("email"):
            email = request.form.get("email")
        else:
            email = current_user.email

        if featureExtraction:
            userpathToPredict = dataPath / "doPredictionFE.csv"
            features = utils.createFeatureList(
                numColsFE
            )  # lista di features per la qsvm
        else:
            features = utils.createFeatureList(
                utils.numberOfColumns(userpathTrain) - 1
            )

        app.test_client().post(
            "/classify_control",
            data=dict(
                pathTrain=pathTrain,
                pathTest=pathTest,
                email=email,
                userpathToPredict=userpathToPredict,
                features=features,
                token=token,
                backend=backend,
                model=model,
                C=C,
                tau=tau,
                optimizer=optimizer,
                loss=loss,
                max_iter=max_iter,
                id_dataset=salvataggiodatabase.id
            ),
        )

    print("\n\nSmista ha finito! To the Moon!")

    return render_template(
        "downloadPage.html",
        ID=salvataggiodatabase.id)


def upload(file, file1, file2, idTrainSet):
    print("Request send on ")
    ext_ok = ["txt", "csv", "data"]
    # log.log()

    # Dataset Train from form

    temp = file.filename
    extension = temp.split(".")[-1]
    if not ext_ok.__contains__(extension):
        return -1
    if file is None:
        return -1
    uploaddir = (
            pathlib.Path(__file__).parents[1]
            / "upload_dataset"
            / current_user.email
            / str(idTrainSet)
    )
    if not uploaddir.exists():
        uploaddir.mkdir()
    userpath = uploaddir / os.path.basename(pathlib.Path(file.filename))
    file.save(userpath)
    if file.content_length > 80000000:
        return -1

    # Dataset Test from form
    temp = file1.filename
    extension = temp.split(".")[-1]
    userpathTest = ""
    if file1.filename != "" and not ext_ok.__contains__(extension):
        # print(file1.filename)
        return -1
    if file1.filename != "":
        userpathTest = uploaddir / os.path.basename(pathlib.Path(file1.filename))
        file1.save(userpathTest)
    if file1.content_length > 80000000:
        return -1

    # Dataset to Predict from form
    # user_path_to_predict = 'app/source/classificazioneDataset/doPrediction.csv'
    temp = file2.filename
    # print("TempDataToPredict: ", temp)
    # print("file2: ", file2)
    extension = temp.split(".")[-1]
    userpathToPredict = ""
    if file2.filename != "" and not ext_ok.__contains__(extension):
        return -1
    if file2.filename != "" != 0:
        userpathToPredict = uploaddir / os.path.basename(pathlib.Path(file2.filename))
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
