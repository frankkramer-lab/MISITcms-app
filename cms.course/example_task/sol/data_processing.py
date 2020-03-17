# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split

# Read data set in csv function
def read_dataset(path):
    data_set = pd.read_csv(path)
    return data_set

# Data exploration
def exploration(data_set):
    # Colnames with first 5 lines
    print("Data Set:" + "\n" + str(data_set.head()) + "\n")
    # Any abnormalities in the Age data?
    outlier = data_set["Age"].sort_values()[448]
    print("Age data abnormalities:" + "\n" + str(outlier) + "\n")
    # Categories of Entry_Person
    entry_person_categories = data_set["Entry_Person"].unique()
    print("Categories of Entry_Person:" + "\n" + str(entry_person_categories) + "\n")
    # Number of patients in which age_range
    age_range_dist = data_set["Age_Range"].value_counts()
    print("Age range distribution:" + "\n" + str(age_range_dist) + "\n")

# Preprocess data
def preprocessing(data_set, categorical_variables, binary_variables,
                  numeric_variables):
    # Remove all incomplete cases
    ds_proc = data_set.dropna(axis=0, how="any", inplace=False)

    # One-hot-encode categorical variables
    ds_proc = pd.get_dummies(data=ds_proc, prefix ="OHE",
                               columns=categorical_variables)

    # Convert binary variables to 0/1
    mapping = {"no": 0, "yes": 1,
               "NO": 0, "YES": 1,
               "f": 0, "m": 1,}
    for col in binary_variables:
        ds_proc[col] = ds_proc[col].map(mapping)

    # Normalize continous & discrete variables
    for col in numeric_variables:
        ds_proc[col] = (ds_proc[col] - ds_proc[col].min()) / \
                       (ds_proc[col].max() - ds_proc[col].min())

    # Return normalized data set
    return ds_proc

# Split data set
def split_dataset(data_set, y_var, test_size=0.2):
    y = data_set.pop(y_var)
    return train_test_split(data_set, y, test_size=test_size)
