import pandas as pd
import numpy as np

class DataStudyr:
    def __init__(self, df):
        self.df = df

    def missing_data(self):
        total = self.df.isnull().sum()
        percent = (total / len(self.df) * 100)
        missing_summary = pd.DataFrame({
            'Total': total,
            'Percent': percent,
            'Types': self.df.dtypes
        })
        return missing_summary

    def most_frequent_data(self):
        total = self.df.count()
        tt = pd.DataFrame(total)
        tt.columns = ['Total']
        items = []
        vals = []
        for col in self.df.columns:
            try:
                itm = self.df[col].value_counts().index[0]
                val = self.df[col].value_counts().values[0]
                items.append(itm)
                vals.append(val)
            except Exception as ex:
                print(ex)
                items.append(0)
                vals.append(0)
                continue
        tt['Most frequent item'] = items
        tt['Frequency'] = vals
        tt['Percent from total'] = np.round(vals / total * 100, 3)

        return tt.transpose()

    def unique_values(self):
        total = self.df.count()
        tt = pd.DataFrame(total)
        tt.columns = ['Total']
        uniques = []
        for col in self.df.columns:
            unique = self.df[col].nunique()
            uniques.append(unique)
        tt['Uniques'] = uniques
        np.transpose(tt)

        return tt

    def unique_values_summary(self):
        total = self.df.count()
        tt = pd.DataFrame(total)
        tt.columns = ['Total']
        uniques = []
        for col in self.df.columns:
            unique = self.df[col].nunique()
            uniques.append(unique)
        tt['Uniques'] = uniques
        unique_summary=np.transpose(tt)
        return unique_summary