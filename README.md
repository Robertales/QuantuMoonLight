<h1>QuantuMoonLight</h1>

QuantuMoonLight is the major user-friendly web platform aimed at quantum computation and machine learning enthusiasts, industry professionals, students and researchers.

The main function of the system is to allow registered users to perform common operation as validation, preprocessing, classifications, regression and more on datasets uploaded by users.

Quantum Machine Learning is a little-known area and therefore we want to extend the interested community, trying to offer a product simple, reliable and useful, using the solutions made available by new Quantum Computing technologies.

The goal of the project is to observe the variation of the metrics of a quantum classification algorithm by applying preprocessing techniques that decrease the dimensionality of a dataset in favor of execution time.

The purpose of this project is to present, in detail, the algorithms of the Machine Learning pipeline algorithms used in the QML platform: from validation and feature engineering methods to the creation and use of the quantum classification model.

<h2>Local Installation</h2>
The following prerequisites must be used to install such a platform locally:
Python >= vers. 3.7
Anaconda >= vers. 2021.11
Editor to set up the code (example PyCharm)
MySql vers. >= 7.0
Client MySQL (example HeidiSQL)

After verifying that you have these prerequisites you will need to proceed in this order:

   IF YOU WANT TO RUN ON IDE:
1) Import repository on you IDE (ex. using https://github.com/Robertales/QuantuMoonLight.git)
2) Open Anaconda Prompt and install the environment.yml using this commanad (download from env/yourOS/environment.yml)
   "conda env create -f environment.yml"
   next
   "conda activate name-environment"
3) Set-up the interpreter and the environment on your IDE as a Flask Application
4) Run the code
5) The home page will be shown on your browser

   ELSE IF YOU WANT TO RUN ON PROMPT:
1) clone the github repository
2) Open Anaconda Prompt and install the environment.yml using this commnad 
   "conda env create -f environment.yml"
   next
   "conda activate name-environment"
3) cd into the QuantuMoonLight folder of the local copy of the repository
4)  type in "flask run" command and run it
5)  open the link provided by the cli interface to access your local copy

![immagine](https://user-images.githubusercontent.com/21276583/174491339-711adce9-8439-4193-a237-af916d82056d.png)
