# Loading test train and joining

def load_data(TRAIN_PATH, TEST_PATH):
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TRAIN_PATH) 

def aggregate_data(train_df, test_df):
    all_df = pd.concat([train_df, test_df], axis=0)
    all_df["set"] = "train"
    all_df.loc[all_df.Survived.isna(), "set"] = "test"

    return df
