import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import urllib.request
from PIL import Image

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, LinearSVC

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV, RepeatedKFold

from sklearn.decomposition import PCA



def modeling(df):
    # Variables
    X = np.array(df.iloc[:, :-1])

    y = np.array(df.iloc[:, -1])

    # Train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state = 42)

    # Cross validation
    kfold = RepeatedKFold(n_splits = 3, n_repeats = 1, random_state = 42)

    pipe = Pipeline(steps=[
        ("pca", PCA()),           
        ("reglog", LogisticRegression())        
    ])

    logistic_params = {
        'classifier': [LogisticRegression()],
        'classifier__penalty': ['l1', 'l2'],
        "classifier__C": [0.01, 0.1, 0.5, 1]
    }

    random_forest_params = {
        'classifier': [RandomForestClassifier()],
        'classifier__n_estimators': [10, 100, 1000],
        'classifier__max_features': [1,2,3]
    }

    svm_params = {
        'classifier': [SVC()],
        'classifier__kernel': ('linear', 'rbf', 'sigmoid'),
        'classifier__C': [0.001, 0.1, 0.5, 1, 5, 10],
        'classifier__gamma': ('scale', 'auto')
        
    }

    search_space = [
        logistic_params,
        random_forest_params,
        svm_params
    ]

    clf = GridSearchCV(estimator = pipe,
                    param_grid = search_space,
                    cv = 10,
                    verbose=1,
                    n_jobs=-1)

    clf.fit(X_train, y_train)

    return clf.best_estimator_.predict(X)
