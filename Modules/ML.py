import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier

class MachineLearning:
    def __init__(self):
        pass


    def prepare_datasets(self, train, valid, predictors, target):
        """
        Prepares the training and validation datasets by extracting the feature columns (predictors) and the target column.

        Parameters:
        train (pd.DataFrame): The training dataset.
        valid (pd.DataFrame): The validation dataset.
        predictors (list of str): List of column names to be used as predictors/features.
        target (str): The column name of the target variable.

        Returns:
        tuple: Returns four datasets: train_X, train_Y, valid_X, valid_Y.
        """
        # Extract feature columns and target columns for training
        train_X = train[predictors]
        train_Y = train[target].values

        # Extract feature columns and target columns for validation
        valid_X = valid[predictors]
        valid_Y = valid[target].values

        return train_X, train_Y, valid_X, valid_Y

    def train_and_predict_random_forest(self, train_X, train_Y, valid_X, random_state=42, n_estimators=100, criterion="gini"):
        """
        Trains a RandomForestClassifier on the training data and returns predictions for both training and validation sets.

        Parameters:
        train_X (pd.DataFrame): Features of the training dataset.
        train_Y (pd.Series or np.array): Target of the training dataset.
        valid_X (pd.DataFrame): Features of the validation dataset.
        random_state (int, optional): Random state for reproducibility. Default is 42.
        n_estimators (int, optional): The number of trees in the forest. Default is 100.
        criterion (str, optional): The function to measure the quality of a split. Default is "gini".

        Returns:
        tuple: Returns predictions for both training and validation sets.
        """
        # Initialize the RandomForestClassifier
        clf = RandomForestClassifier(n_jobs=-1, 
                                    random_state=random_state,
                                    criterion=criterion,
                                    n_estimators=n_estimators,
                                    verbose=False)

        # Fit the classifier to the training data
        clf.fit(train_X, train_Y)

        # Predict on the training and validation data
        preds_train = clf.predict(train_X)
        preds_valid = clf.predict(valid_X)

        return preds_train, preds_valid