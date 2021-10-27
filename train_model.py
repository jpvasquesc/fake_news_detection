"""
This script builds a machine learning model to predict if a news article, in the portuguese language, is real or fake.
To do this it utilizes natual language processing (NLP) methods such as tokenazition and removal of stop-words.
It compares the accuracy of prediction utilizing different classification estimators from the sklearn library and chooses the one with the best score.
Estimators:
    - SVM
    - SGDClassifier
    - MultinomialNB
    - KNeighborsClassifier
    - RandomForestClassifier
"""

import pandas as pd
import numpy as np
from pathlib import Path
from string import punctuation
import nltk
import nltk.corpus as corpus
from sklearn.utils import shuffle
import sklearn.feature_extraction.text as sk_text
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle


def main():
    """
    Test multiple machine model estimators and save the one with the best accuracy
    """
    seed = 17
    download_nltk_corpus()   
     
    # Set up training dataset
    df = get_training_texts()
    df = shuffle(df, random_state=seed)
    df.reset_index(inplace=True, drop=True)
    X = df.text
    y = df.label
    
    # Train model
    best_model = build_best_model(X, y, seed)
    print("Best model: {0}\nAccuracy: {1}".format(best_model["model"], best_model["accuracy"]))
    
    # Save model
    pickle.dump(best_model["model"], open(Path("./model.sav"), 'wb'))


def download_nltk_corpus() -> None:
    """
    Download nltk packages that are required to build the model
    """
    print("Download required nltk packages:")
    nltk.download('stopwords')
    print("\n-------\n")


def get_training_texts() -> pd.DataFrame:
    """
    Get the training text from "./training_data" and classify them as "fake" or "real".

    Raises:
        ValueError: Raise an error if no files are found in the 'train_data/label' directory

    Returns:
        pd.Dataframe: DataFrame with all texts('text' column) and their classification('label' column)
    """
    print("Fetching training data:")
    df = pd.DataFrame(columns={"text": [], "label": []})
        
    for label in ["fake", "real"]:
        articles_dir = Path("./training_data/{0}".format(label))
        articles = articles_dir.glob("*.txt")
        
        if articles:
            print("Extracting {0} texts...".format(label))
            for article in articles:
                with open(article, "r", encoding="UTF-8") as a:
                    text = a.read()
                    df = df.append({'text': text, "label": label}, ignore_index=True)
        
        else:
            raise ValueError("Found no articles at {0}".format(articles_dir))

    print("\n-------\n")
    return df
    

def build_best_model(X_train: pd.DataFrame, y_train: pd.DataFrame, seed: int) -> dict:
    """
    Test different estimators with multiple paremeters and return the one with the highest accuracy

    Args:
        X_train[pd.Dataframe] : Training features 
        y_train[pd.Dataframe] : Training outcome
        seed[int]: random_state seed for reproducibility
        
    Returns:
        dict: A dict of the best model and it's accuracy
    """
    print("Testing best model:")
    best_model= {"accuracy": 0, "model": 0}

    # List of possible estimators and their paramenters
    estimators=[(svm.SVC(random_state=seed), {"kernel": ("poly", "rbf", "sigmoid"),
                                          "gamma": ("scale", "auto"),
                                          "C": [0.01, 0.1, 1, 10, 100],
                                          }),
                (KNeighborsClassifier(), {"n_neighbors": np.arange(1, round(X_train.count()/2))}),
                (RandomForestClassifier(random_state=seed), {"criterion": ["gini", "entropy"]}),
                (SGDClassifier(random_state=seed), {'alpha': 10.0**-np.arange(1,7),
                                                'loss': ["hinge", "log", "perceptron", "modified_huber", "squared_hinge"],
                                                "class_weight": [None, "balanced"]              
                                                }),
                (MultinomialNB(), {"fit_prior": (True, False), "alpha": 10.0**-np.arange(1,7)})]
    
    # Stop words that will be removed from the texts
    stopwords = corpus.stopwords.words("portuguese") + list(punctuation)
    
    # Test each estimator
    for e, params in estimators:
        print("\nEstimator: {0}".format(e))
        
        # Set up model pipeline
        model = Pipeline([('vect', sk_text.CountVectorizer(stop_words=stopwords)),
                          ('tfidf', sk_text.TfidfTransformer()),
                          ('clf', e)])
        
        # Set up estimator's possible parameters
        parameters = {"clf__{0}".format(p): options for p, options in params.items()}
        parameters['vect__ngram_range'] = [(1, 1), (1, 2)]
        parameters['tfidf__use_idf'] = (True, False)
               
        # Test best parameters                 
        gs_clf = GridSearchCV(model, parameters, n_jobs=-1)
        gs_clf = gs_clf.fit(X_train,y_train) 
        print("Score: {0}\nParams: {1}\n".format(gs_clf.best_score_, gs_clf.best_params_))

        # Check if the model has highest accuracy
        if gs_clf.best_score_ > best_model["accuracy"]:
            best_model["accuracy"] = gs_clf.best_score_
            best_model["model"] = gs_clf.best_estimator_
    
    print("\n-------\n")
    return best_model


if __name__ == "__main__":
    main()