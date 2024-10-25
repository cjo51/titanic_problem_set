def missing_data(df):
    total = df.isnull().sum()
    percent = (total/df.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    df_missing = np.transpose(tt)
    return df_missing

def most_frequent_data(df):
    total = df.count()
    tt = pd.DataFrame(total)
    tt.columns = ['Total']
    items = []
    vals = []
    for col in train_df.columns:
        try:
            itm = train_df[col].value_counts().index[0]
            val = train_df[col].value_counts().values[0]
            items.append(itm)
            vals.append(val)
        except Exception as ex:
            print(ex)
            items.append(0)
            vals.append(0)
            continue
    tt['Most frequent item'] = items
    tt['Frequence'] = vals
    tt['Percent from total'] = np.round(vals / total * 100, 3)
    np.transpose(tt)

    return tt

def unique_values(df):
    total = df.count()
    tt = pd.DataFrame(total)
    tt.columns = ['Total']
    uniques = []
    for col in train_df.columns:
        unique = train_df[col].nunique()
        uniques.append(unique)
    tt['Uniques'] = uniques
    np.transpose(tt)

    return tt