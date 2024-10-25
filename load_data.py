# Loading test train and joining

import pandas as pd

def load_data(PATH):
    df = pd.read_csv(PATH)

    return df


def combine_train_test(train_df, test_df, target_col):
    """
    Combine the train and test DataFrames, and label the rows based on the dataset they belong to.

    Parameters:
    train_df (pd.DataFrame): The training DataFrame.
    test_df (pd.DataFrame): The testing DataFrame.
    target_col (str): The target column that indicates the training label (e.g., 'Survived').

    Returns:
    pd.DataFrame: A DataFrame combining both train and test data, with an additional 'set' column.
    """
    # Concatenate train and test DataFrames
    all_df = pd.concat([train_df, test_df], axis=0)
    
    # Label all rows as 'train'
    all_df["set"] = "train"
    
    # Label rows as 'test' where the target column is NaN (i.e., they belong to the test set)
    all_df.loc[all_df[target_col].isna(), "set"] = "test"
    
    return all_df
