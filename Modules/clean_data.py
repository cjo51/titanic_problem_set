import pandas as pd
import numpy as np

class DataCleaner:
    # Constructor initialises the classes
    def __init__(self):
        """ 
        Constructor initialises the classes
        Takes a pandas dataframe as an argument
        """    
        pass

    def add_family_size(self, df):
        """
        add_family_size 

        Add a 'Family Size' column to the DataFrame based on the number of siblings/spouses
        and parents/children aboard, plus one for the individual.

        Returns:
        pd.DataFrame: The original DataFrame with an added 'Family Size' column.
        """        
        df["Family Size"] = df['SibSp'] + df['Parch'] + 1

        return df

    def add_age_interval(self, df):
        """
        Add an 'Age Interval' column to the DataFrame, categorizing ages into intervals.

        Returns:
        pd.DataFrame: The original DataFrame with an added 'Age Interval' column.
        """
        # Initialize the 'Age Interval' column with default values
        df["Age Interval"] = 0.0
        
        # Apply conditions to assign age intervals
        df.loc[df['Age'] <= 16, 'Age Interval'] = 0
        df.loc[(df['Age'] > 16) & (df['Age'] <= 32), 'Age Interval'] = 1
        df.loc[(df['Age'] > 32) & (df['Age'] <= 48), 'Age Interval'] = 2
        df.loc[(df['Age'] > 48) & (df['Age'] <= 64), 'Age Interval'] = 3
        df.loc[df['Age'] > 64, 'Age Interval'] = 4

        return df

    def add_fare_interval_column(self, df):
        """
        Add a 'Fare Interval' column to the DataFrame based on fare ranges.

        Returns:
        pd.DataFrame: The DataFrame with the added 'Fare Interval' column.
        """
        df['Fare Interval'] = 0.0
        df.loc[df['Fare'] <= 7.91, 'Fare Interval'] = 0
        df.loc[(df['Fare'] > 7.91) & (df['Fare'] <= 14.454), 'Fare Interval'] = 1
        df.loc[(df['Fare'] > 14.454) & (df['Fare'] <= 31), 'Fare Interval'] = 2
        df.loc[df['Fare'] > 31, 'Fare Interval'] = 3

        return df

    def add_sex_pclass(self, df):
        """
        Add a 'Sex_Pclass' column to the DataFrame, combining the first letter of 'Sex' 
        and the 'Pclass' with a specific format.

        Returns:
        pd.DataFrame: The original DataFrame with an added 'Sex_Pclass' column.
        """
        df["Sex_Pclass"] = df.apply(lambda row: row['Sex'][0].upper() + "_C" + str(row['Pclass']), axis=1)
        return df

    @staticmethod
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
    
    def extract_names(self, df):
        """
        Extract family name, title, given name, and maiden name from the 'Name' column 
        and add them as new columns to the DataFrame.

        Returns:
        pd.DataFrame: The original DataFrame with new columns added for Family Name, Title, 
                    Given Name, and Maiden Name.
        """
        # Apply the parse_names function to extract name components
        df[["Family Name", "Title", "Given Name", "Maiden Name"]] = df.apply(lambda row: DataCleaner.parse_names(row), axis=1)
        return df

    def add_family_type_column(self, df):
        """
        Add a 'Family Type' column based on 'Family Size' to the provided datasets.

        Returns:
        pd.DataFrame: The original DataFrame with 'Family Type' column
        """
        if "Family Size" in df.columns:
            df["Family Type"] = df["Family Size"]
        else:
            print(f"'Family Size' column not found in dataset with shape {df.shape}.")
        
        return df

    def assign_family_type(self, df):
        """
        Assign a 'Family Type' based on 'Family Size' for the provided dataset.

        Returns:
        datasets (list of pd.DataFrame): Dataset to which the 'Family Type' column will be assigned.
        """
        # Assign 'Family Type' based on 'Family Size'
        df.loc[df["Family Size"] == 1, "Family Type"] = "Single"
        df.loc[(df["Family Size"] > 1) & (df["Family Size"] < 5), "Family Type"] = "Small"
        df.loc[df["Family Size"] >= 5, "Family Type"] = "Large"

        return df

    def unify_titles(self, df):
        """
        Standardize titles in the 'Titles' column for the provided datasets.

        Returns:
        datasets (list of pd.DataFrame): DataFrame to which the title unification will be applied.
        """

        # Unify 'Miss'
        df['Titles'] = df['Titles'].replace({'Mlle.': 'Miss.', 'Ms.': 'Miss.'})
        # Unify 'Mrs'
        df['Titles'] = df['Titles'].replace({'Mme.': 'Mrs.'})
        # Unify Rare titles
        rare_titles = ['Lady.', 'the Countess.', 'Capt.', 'Col.', 'Don.', 
                        'Dr.', 'Major.', 'Rev.', 'Sir.', 'Jonkheer.', 'Dona.']
        df['Titles'] = df['Titles'].replace(rare_titles, 'Rare')

    def calculate_survival_rate_by_title_and_sex(self, df):
        """
        Calculate the mean survival rate grouped by 'Titles' and 'Sex'.

        Returns:
        pd.DataFrame: A DataFrame with the mean survival rates grouped by 'Titles' and 'Sex'.
        """
        return df[['Titles', 'Sex', 'Survived']].groupby(['Titles', 'Sex'], as_index=False).mean()

    def map_sex_column(self, df):
        """
        Maps the 'Sex' column to integers, where 'female' is 1 and 'male' is 0.

        Parameters:
        datasets (list of pd.DataFrame): List of DataFrames to apply the transformation.

        Returns:
        None: The function modifies the DataFrames in place.
        """

        df['Sex'] = df['Sex'].map({'female': 1, 'male': 0}).astype(int)

        return df