# fake_news_detection
A machine learning model built to predict if a piece of text, in the portuguese language, is real or fake.

This project was built in two weeks as the final project for the 'Programing for Biosciences' (CFB017) undergraduate course in the Federal University of Rio de Janeiro, taught by Professor Pedro Henrique Monteiro Torres.

I have taken this oportunity to learn about natural language processing (NLP) in machine learning, an area which I'm very interested but don't have experience in.

## Index

## Usage
This project was built in Python 3.9.7 and therfore may not work in older version of Python.\
All the third-party packages necessary can be found in the 'requirements.txt' file. Use 'pip install requirements.txt' to install them. 

The model can be utilized through the 'main.py' file.\
The input can be given directly through the command line or using one or more '.txt' files.\
All the input files **must** have the '.txt' extension or an error will be raised. 

Command line:\
python main.py -t "your text here"

Text files:\
python main.py -f ./your_text.txt\
python main.py -f ./*.txt

## Making the project
### Planning
To create such a model there are two major factors to be considered:
* The media that contains the 'fake news' (e.g. text, images, videos, etc).
* The vehicle for the dessimination of the 'fake news' (e.g. a specific social media, newspapers, etc).
In this model I have chosen to utilize text media disseminated by digital news articles.

### Creating a training dataset
The training dataset was collected, utilizing web scrapping, from the following websites:
* G1
* Correio Braziliense
* Carta Capital
* Jovem Pan
* Folha Politica
* Diario do Brasil
* Terca Livre

### Building the model
I choose to use the "Bag-of-words" model. The text was processed utilizing a pipeline with the NLP following methods:
* Removal of stopwords:

 Removal of common words and punctuation. I utilized the NLTK portuguese stopwords collection and the Python punctuation collection.

* Tokenazation and word count

 Transform words in unique tokens for better processing and count the frequencie of each token. This was done utilizing sklearn.feature_extraction.text.CountVectorizer.

* Frequency weighting: 

The result of this pipeline is then given as input to a ML estimator. I compared the accuracy of 5 estimators, using GridSearchCV to find their best parameter configuration:
* Support Vector Classifier
* K-Neighbors Classifier
* Random Forest Classifier
* Stochastic Gradient Descent (SGD) Classifier
* Multinomial Naive BayeS

The best result found, achieving an accuray of 85.7%, was with the SGDClassifier and parameters: alpha=0.01, loss='log', random_state=17.

## Conclusions
