import pandas as pd
import numpy as np


def add_family_size(df, sibsp_col='SibSp', parch_col='Parch'):
    """
    Add a 'Family Size' column to the DataFrame based on the number of siblings/spouses
    and parents/children aboard, plus one for the individual.

    Parameters:
    df (pd.DataFrame): The DataFrame to add the 'Family Size' column to.
    sibsp_col (str): The name of the column representing siblings/spouses aboard. Default is 'SibSp'.
    parch_col (str): The name of the column representing parents/children aboard. Default is 'Parch'.

    Returns:
    pd.DataFrame: The original DataFrame with an added 'Family Size' column.
    """
    df["Family Size"] = df[sibsp_col] + df[parch_col] + 1
    return df

def add_age_interval(df, age_col='Age'):
    """
    Add an 'Age Interval' column to the DataFrame, categorizing ages into intervals.

    Parameters:
    df (pd.DataFrame): The DataFrame to add the 'Age Interval' column to.
    age_col (str): The name of the column representing age. Default is 'Age'.

    Returns:
    pd.DataFrame: The original DataFrame with an added 'Age Interval' column.
    """
    # Initialize the 'Age Interval' column with default values
    df["Age Interval"] = 0.0
    
    # Apply conditions to assign age intervals
    df.loc[df[age_col] <= 16, 'Age Interval'] = 0
    df.loc[(df[age_col] > 16) & (df[age_col] <= 32), 'Age Interval'] = 1
    df.loc[(df[age_col] > 32) & (df[age_col] <= 48), 'Age Interval'] = 2
    df.loc[(df[age_col] > 48) & (df[age_col] <= 64), 'Age Interval'] = 3
    df.loc[df[age_col] > 64, 'Age Interval'] = 4

    return df

def add_fare_interval_column(df):
    """
    Add a 'Fare Interval' column to the DataFrame based on fare ranges.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the 'Fare' column.

    Returns:
    pd.DataFrame: The DataFrame with the added 'Fare Interval' column.
    """
    df['Fare Interval'] = 0.0
    df.loc[df['Fare'] <= 7.91, 'Fare Interval'] = 0
    df.loc[(df['Fare'] > 7.91) & (df['Fare'] <= 14.454), 'Fare Interval'] = 1
    df.loc[(df['Fare'] > 14.454) & (df['Fare'] <= 31), 'Fare Interval'] = 2
    df.loc[df['Fare'] > 31, 'Fare Interval'] = 3
    return df


def add_sex_pclass(df, sex_col='Sex', pclass_col='Pclass'):
    """
    Add a 'Sex_Pclass' column to the DataFrame, combining the first letter of 'Sex' 
    and the 'Pclass' with a specific format.

    Parameters:
    df (pd.DataFrame): The DataFrame to add the 'Sex_Pclass' column to.
    sex_col (str): The name of the column representing sex. Default is 'Sex'.
    pclass_col (str): The name of the column representing passenger class. Default is 'Pclass'.

    Returns:
    pd.DataFrame: The original DataFrame with an added 'Sex_Pclass' column.
    """
    df["Sex_Pclass"] = df.apply(lambda row: row[sex_col][0].upper() + "_C" + str(row[pclass_col]), axis=1)
    return df

def parse_names(row):
    """
    Parse the 'Name' field of a DataFrame row to extract family name, title,
    given name, and maiden name.

    Parameters:
    row (pd.Series): A row of the DataFrame containing the 'Name' column.

    Returns:
    pd.Series: A Series containing family name, title, given name, and maiden name.
    """
    try:
        text = row["Name"]
        split_text = text.split(",")
        family_name = split_text[0].strip()
        next_text = split_text[1]
        split_text = next_text.split(".")
        title = (split_text[0] + ".").strip()
        next_text = split_text[1].strip()

        if "(" in next_text:
            split_text = next_text.split("(")
            given_name = split_text[0].strip()
            maiden_name = split_text[1].rstrip(")").strip()
            return pd.Series([family_name, title, given_name, maiden_name])
        else:
            given_name = next_text
            return pd.Series([family_name, title, given_name, None])
    except Exception as ex:
        print(f"Exception: {ex}")
        return pd.Series([None, None, None, None])
    
def extract_names(df):
    """
    Extract family name, title, given name, and maiden name from the 'Name' column 
    and add them as new columns to the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the 'Name' column.

    Returns:
    pd.DataFrame: The original DataFrame with new columns added for Family Name, Title, 
                  Given Name, and Maiden Name.
    """
    # Apply the parse_names function to extract name components
    df[["Family Name", "Title", "Given Name", "Maiden Name"]] = df.apply(lambda row: parse_names(row), axis=1)
    return df

def add_family_type_column(datasets):
    """
    Add a 'Family Type' column based on 'Family Size' to the provided datasets.

    Parameters:
    datasets (list of pd.DataFrame): List containing DataFrames to which the 'Family Type' column will be added.
    """
    for dataset in datasets:
        # Check if 'Family Size' exists in the dataset
        if "Family Size" in dataset.columns:
            dataset["Family Type"] = dataset["Family Size"]
        else:
            print(f"'Family Size' column not found in dataset with shape {dataset.shape}.")

def assign_family_type(datasets):
    """
    Assign a 'Family Type' based on 'Family Size' for the provided datasets.

    Parameters:
    datasets (list of pd.DataFrame): List containing DataFrames to which the 'Family Type' will be assigned.
    """
    for dataset in datasets:
        # Assign 'Family Type' based on 'Family Size'
        dataset.loc[dataset["Family Size"] == 1, "Family Type"] = "Single"
        dataset.loc[(dataset["Family Size"] > 1) & (dataset["Family Size"] < 5), "Family Type"] = "Small"
        dataset.loc[dataset["Family Size"] >= 5, "Family Type"] = "Large"

def unify_titles(datasets):
    """
    Standardize titles in the 'Titles' column for the provided datasets.

    Parameters:
    datasets (list of pd.DataFrame): List containing DataFrames to which the title unification will be applied.
    """
    for dataset in datasets:
        # Unify 'Miss'
        dataset['Titles'] = dataset['Titles'].replace({'Mlle.': 'Miss.', 'Ms.': 'Miss.'})
        # Unify 'Mrs'
        dataset['Titles'] = dataset['Titles'].replace({'Mme.': 'Mrs.'})
        # Unify Rare titles
        rare_titles = ['Lady.', 'the Countess.', 'Capt.', 'Col.', 'Don.', 
                       'Dr.', 'Major.', 'Rev.', 'Sir.', 'Jonkheer.', 'Dona.']
        dataset['Titles'] = dataset['Titles'].replace(rare_titles, 'Rare')

def calculate_survival_rate_by_title_and_sex(dataset):
    """
    Calculate the mean survival rate grouped by 'Titles' and 'Sex'.

    Parameters:
    dataset (pd.DataFrame): The DataFrame containing the relevant columns.

    Returns:
    pd.DataFrame: A DataFrame with the mean survival rates grouped by 'Titles' and 'Sex'.
    """
    return dataset[['Titles', 'Sex', 'Survived']].groupby(['Titles', 'Sex'], as_index=False).mean()

def map_sex_column(datasets):
    """
    Maps the 'Sex' column to integers, where 'female' is 1 and 'male' is 0.

    Parameters:
    datasets (list of pd.DataFrame): List of DataFrames to apply the transformation.

    Returns:
    None: The function modifies the DataFrames in place.
    """
    for dataset in datasets:
        dataset['Sex'] = dataset['Sex'].map({'female': 1, 'male': 0}).astype(int)