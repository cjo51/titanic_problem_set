import pandas as pd
import numpy as np

class DataCleaner(self, df):
    # Constructor initialises the classes
    def __init__(self, dataframe):
        self.dataframe = dataframe
        """ 
        Constructor initialises the classes
        Takes a pandas dataframe as an argument
        """    
    def add_family_size(self):
        """
        add_family_size 

        Add a 'Family Size' column to the DataFrame based on the number of siblings/spouses
        and parents/children aboard, plus one for the individual.

        Returns:
        pd.DataFrame: The original DataFrame with an added 'Family Size' column.
        """        
        self.dataframe["Family Size"] = self.dataframe['SibSp'] + self.dataframe['Parch'] + 1

        return self.dataframe


    def add_age_interval(self):
        """
        Add an 'Age Interval' column to the DataFrame, categorizing ages into intervals.

        Returns:
        pd.DataFrame: The original DataFrame with an added 'Age Interval' column.
        """
        # Initialize the 'Age Interval' column with default values
        self.dataframe["Age Interval"] = 0.0
        
        # Apply conditions to assign age intervals
        self.dataframe.loc[self.dataframe['Age'] <= 16, 'Age Interval'] = 0
        self.dataframe.loc[(self.dataframe['Age'] > 16) & (self.dataframe['Age'] <= 32), 'Age Interval'] = 1
        self.dataframe.loc[(self.dataframe['Age'] > 32) & (self.dataframe['Age'] <= 48), 'Age Interval'] = 2
        self.dataframe.loc[(self.dataframe['Age'] > 48) & (self.dataframe['Age'] <= 64), 'Age Interval'] = 3
        self.dataframe.loc[self.dataframe['Age'] > 64, 'Age Interval'] = 4

        return self.dataframe

    def add_fare_interval_column(self):
        """
        Add a 'Fare Interval' column to the DataFrame based on fare ranges.

        Returns:
        pd.DataFrame: The DataFrame with the added 'Fare Interval' column.
        """
        self.dataframe['Fare Interval'] = 0.0
        self.dataframe.loc[self.dataframe['Fare'] <= 7.91, 'Fare Interval'] = 0
        self.dataframe.loc[(self.dataframe['Fare'] > 7.91) & (self.dataframe['Fare'] <= 14.454), 'Fare Interval'] = 1
        self.dataframe.loc[(self.dataframe['Fare'] > 14.454) & (self.dataframe['Fare'] <= 31), 'Fare Interval'] = 2
        self.dataframe.loc[self.dataframe['Fare'] > 31, 'Fare Interval'] = 3

        return self.dataframe

    def add_sex_pclass(self):
        """
        Add a 'Sex_Pclass' column to the DataFrame, combining the first letter of 'Sex' 
        and the 'Pclass' with a specific format.

        Returns:
        pd.DataFrame: The original DataFrame with an added 'Sex_Pclass' column.
        """
        self.dataframe["Sex_Pclass"] = self.dataframe.apply(lambda row: row['Sex'][0].upper() + "_C" + str(row['Pclass']), axis=1)
        return self.dataframe

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
    
    def extract_names(self):
        """
        Extract family name, title, given name, and maiden name from the 'Name' column 
        and add them as new columns to the DataFrame.

        Returns:
        pd.DataFrame: The original DataFrame with new columns added for Family Name, Title, 
                    Given Name, and Maiden Name.
        """
        # Apply the parse_names function to extract name components
        self.dataframe[["Family Name", "Title", "Given Name", "Maiden Name"]] = df.apply(lambda row: parse_names(row), axis=1)
        return self.dataframe

    def add_family_type_column(self):
        """
        Add a 'Family Type' column based on 'Family Size' to the provided datasets.

        Returns:
        pd.DataFrame: The original DataFrame with 'Family Type' column
        """
        if "Family Size" in self.dataframe.columns:
            self.dataframe["Family Type"] = self.dataframe["Family Size"]
        else:
            print(f"'Family Size' column not found in dataset with shape {self.dataframe.shape}.")
        
        return self.dataframe

    def assign_family_type(self):
        """
        Assign a 'Family Type' based on 'Family Size' for the provided dataset.

        Returns:
        datasets (list of pd.DataFrame): Dataset to which the 'Family Type' column will be assigned.
        """
        # Assign 'Family Type' based on 'Family Size'
        self.dataframe.loc[self.dataframe["Family Size"] == 1, "Family Type"] = "Single"
        self.dataframe.loc[(self.dataframe["Family Size"] > 1) & (self.dataframe["Family Size"] < 5), "Family Type"] = "Small"
        self.dataframe.loc[self.dataframe["Family Size"] >= 5, "Family Type"] = "Large"

        return self.dataframe

    def unify_titles(self):
        """
        Standardize titles in the 'Titles' column for the provided datasets.

        Returns:
        datasets (list of pd.DataFrame): DataFrame to which the title unification will be applied.
        """

        # Unify 'Miss'
        self.dataframe['Titles'] = self.dataframe['Titles'].replace({'Mlle.': 'Miss.', 'Ms.': 'Miss.'})
        # Unify 'Mrs'
        self.dataframe['Titles'] = self.dataframe['Titles'].replace({'Mme.': 'Mrs.'})
        # Unify Rare titles
        rare_titles = ['Lady.', 'the Countess.', 'Capt.', 'Col.', 'Don.', 
                        'Dr.', 'Major.', 'Rev.', 'Sir.', 'Jonkheer.', 'Dona.']
        self.dataframe['Titles'] = self.dataframe['Titles'].replace(rare_titles, 'Rare')

    def calculate_survival_rate_by_title_and_sex(self):
        """
        Calculate the mean survival rate grouped by 'Titles' and 'Sex'.

        Returns:
        pd.DataFrame: A DataFrame with the mean survival rates grouped by 'Titles' and 'Sex'.
        """
        return self.dataframe[['Titles', 'Sex', 'Survived']].groupby(['Titles', 'Sex'], as_index=False).mean()

    def map_sex_column(self):
        """
        Maps the 'Sex' column to integers, where 'female' is 1 and 'male' is 0.

        Parameters:
        datasets (list of pd.DataFrame): List of DataFrames to apply the transformation.

        Returns:
        None: The function modifies the DataFrames in place.
        """

        self.dataframe['Sex'] = self.dataframe['Sex'].map({'female': 1, 'male': 0}).astype(int)

        return self.dataframe