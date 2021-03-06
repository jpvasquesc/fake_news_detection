# fake_news_detection
A machine learning model built to predict if a piece of text, in the portuguese language, is real or fake.

This project was built in two weeks as the final project for the ['Programing for Biosciences' (CFB017)](https://siga.ufrj.br/sira/repositorio-curriculo/disciplinas/9FF2077D-92A4-F799-307D-EA47BB21E873.html) undergraduate course in the Federal University of Rio de Janeiro, taught by Professor Pedro Henrique Monteiro Torres.

I have taken this oportunity to learn about natural language processing (NLP) in machine learning, an area which I'm very interested but don't have experience in.


## Table of contents
* [Usage](#usage)
* [Making the project](#making-the-project)
  + [Planning](#planning)
  + [Creating a training dataset](#creating-a-training-dataset)
  + [Building the model](#building-the-model)
* [Conclusions](#conclusions)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Usage
This project was built in Python 3.9.7 and therfore may not work in older version of Python.\
All the third-party packages necessary can be found in the 'requirements.txt' file. Use 'pip install requirements.txt' to install them. 

The model can be utilized through the 'main.py' file.\
The input can be given directly through the command line or using one or more '.txt' files.\
All the input files **must** have the '.txt' extension or an error will be raised. 

   **Command line**:\
       python main.py -t "your text here"

   **Text files**:\
       python main.py -f ./your_text.txt\
       python main.py -f ./*.txt


## Making the project
### Planning
To create such a model there are two major factors to be considered:
* The media that contains the 'fake news' (e.g. text, images, videos, etc).
* The vehicle for the dessimination of the 'fake news' (e.g. a specific social media, newspapers, etc).
In this model I have chosen to utilize text media disseminated by digital news articles.


### Creating a training dataset
The [training dataset](https://github.com/jpvasquesc/fake_news_detection/tree/main/training_data) was [collected](https://github.com/jpvasquesc/fake_news_detection/tree/main/news_scrapping) utilizing web scrapping from the following websites:
* [G1](https://g1.globo.com/)
* [Correio Braziliense](https://www.correiobraziliense.com.br/)
* [Carta Capital](https://www.cartacapital.com.br/)
* [Jovem Pan](https://jovempan.com.br/)
* [Folha Politica](https://www.folhapolitica.org/)
* [Diario do Brasil](https://diariodobrasil.org/)
* [Terca Livre](https://tercalivre.com.br/)


### Building the model
I choose to use the ["Bag-of-words"](https://scikit-learn.org/stable/modules/feature_extraction.html#the-bag-of-words-representation) represantation. The text was processed utilizing a pipeline with the NLP following methods:
* [Removal of stopwords](https://scikit-learn.org/stable/modules/feature_extraction.html#using-stop-words)

   Removal of common words and punctuation. I utilized the [NLTK portuguese stopwords](http://www.nltk.org/nltk_data/) collection and the [Python punctuation collection](https://docs.python.org/3/library/string.html#string.punctuation).

* [Tokenazation and word count](https://scikit-learn.org/stable/modules/feature_extraction.html#common-vectorizer-usage)

   Transform words in unique tokens for better processing and count the frequencie of each token.\
   This was done utilizing sklearn's [CountVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html).

* [Normalization with term-frequency](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)

The result of this pipeline is then given as input to a ML estimator. I compared the accuracy of 5 estimators, using GridSearchCV to find their best parameter configuration:
* [Support Vector Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
* [K-Neighbors Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
* [Random Forest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
* [Stochastic Gradient Descent (SGD) Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)
* [Multinomial Naive Bayes](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html)

The best result found, achieving an accuray of 85.7%, was with the SGDClassifier and parameters: alpha=0.01, loss='log', random_state=17.


## Further improvements
This project is not novel and similar projects can be found, such as [FakeCheck](http://nilc-fakenews.herokuapp.com/about) and the [Fake.Br](https://github.com/roneysco/Fake.br-Corpus) corpus.\
As this was my first foray in NLP and an assignment for one of my undegraduate classes, I choose to build both the training dataset and the model from scratch. Here are some considerations that could improve the accuaracy of the model.

* Utilizing a better training dataset

   The training dataset used was fairly small as I had a limited amount of time to collect, clean and manually classify each text. Having a bigger or more refined dataset would probally increase the accuracy of the model. 

   The dataset could also be more diverse and better balanced. Some of the sources had only 'real' or 'fake' classified texts. Considering that different sources will have different writing style, this could lead to an overfitting problem. This could be resolved with the same amount of 'real' and 'fake' texts from each source.
   
* Using other preprocessing techniques

   In this model's pipeline, the only preprocessing in the input is the removal of stopwords, tokenazation and normalization. I've tested using stemming with RSLP but ir resulted in a lower accuracy. Still there are other techinques that could be utilized, such as Lemmatization, which I have not tested.

* Selecting more features from the text

   This model only utilizes the 'Bag-of-words' representation but there are other ways to select features with NLP such as POS Tags, semantic classes, pauses, emotiveness, etc.

* Testing other classification estimators

   As I'm new to the field of NLP and ML, I only tested five different estimators with a limited of parameters permutations. There may be other estimators, such as neural networks, or combinations of parameters that yield a model with an higher accuracy.