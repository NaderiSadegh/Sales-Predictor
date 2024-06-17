# Code developers: Deepti Hegde, Raunak Shahare, Sadegh Naderi

## @file
# @brief Deployment script for the machine learning model
# @details This script loads a trained XGBoost model and uses it to make predictions on input data.
# Code developers: Deepti Hegde, Raunak Shahare, Sadegh Naderi


import development as dv
import pandas as pd
import numpy as np
import os
import pickle

## @var model_filename
# @brief The filename of the saved XGBoost model
model_filename = 'xgboost_model.pkl'

# Load the saved model from file
## @var loaded_model
# @brief The loaded XGBoost model
loaded_model = pickle.load(open(model_filename, 'rb'))

## @var dtypes
# @brief Dictionary specifying the data types of columns in the input data
dtypes = {'store_nbr': np.dtype('int64'),
          'item_nbr': np.dtype('int64'),
          'onpromotion': np.dtype('O')}


# Data Loading for input

# Read the input data file path from input_data_path.txt
with open('input_data_path.txt', 'r') as file:
    file_path = file.read().strip()

## @var inputdf
# @brief DataFrame for storing the input data
inputdf = pd.read_csv(file_path, dtype=dtypes)
inputdfout = inputdf.copy()

print('inputdf shape before merging:', inputdf.shape)

# Data Blending
## @fn process_sales_data(inputdfr)
# @brief Process sales data by performing data blending
# @param inputdfr Input DataFrame containing sales data
# @return Processed DataFrame


# Fill in cells if there is no holiday by the value : "no_holyday"
inputdf.loc[inputdf['type_y'].isnull(), 'type_y'] = "no_holyday"
inputdf.loc[inputdf['locale'].isnull(), 'locale'] = "no_locale"
inputdf.loc[inputdf['transferred'].isnull(), 'transferred'] = "no_holyday"


## @fn get_month_year(inputdfr)
# @brief Extract month and year information from the date column of the input DataFrame
# @param inputdfr Input DataFrame containing the date column
# @return Updated DataFrame with additional columns for month and year
def get_month_year(df):
    """! Maps a number from one range to another.
    @brief Extract month and year from the date
    @param df: The input dataframe
    @return The dataframe with added 'month' and 'year' columns
    """

    df['month'] = df.date.apply(lambda x: x.split('-')[1])
    df['year'] = df.date.apply(lambda x: x.split('-')[0])

    return df

get_month_year(inputdf)

inputdf['date'] = pd.to_datetime(inputdf['date'])
inputdf['day'] = inputdf['date'].dt.day_name()
inputdf = inputdf.drop('date', axis=1)

inputdf['dcoilwtico'] = inputdf['dcoilwtico'].fillna(inputdf['dcoilwtico'].mean())

inputdfTest = inputdf.copy()

print('inputdf after replacing dcoilwtico with means', inputdf.shape)

# One hot Encoding
## @var dummy_variables
# @brief List of variables to be one hot encoded
dummy_variables = ['onpromotion', 'city', 'type_x', 'cluster', 'store_nbr', 'item_nbr',
                   'family', 'perishable', 'type_y', 'locale', 'transferred', 'month', 'day']

for var in dummy_variables:
    dummy = pd.get_dummies(inputdf[var], prefix=var, drop_first=False)
    inputdf = pd.concat([inputdf, dummy], axis=1)

inputdf = inputdf.drop(dummy_variables, axis=1)
inputdf = inputdf.drop(['year'], axis=1)

min_oil, max_oil = inputdf['dcoilwtico'].min(), inputdf['dcoilwtico'].max()

# Re-scale
## @var scalable_variables
# @brief List of variables to be rescaled

## @var mini
# @brief The minimum value of the current variable
## @var maxi
# @brief The maximum value of the current variable


inputdf.loc[:, 'dcoilwtico'] = (inputdf['dcoilwtico'] - dv.min_oil) / (dv.max_oil - dv.min_oil)


print('inputdf after replacing onehot and rescaling', inputdf.shape)

## @var extra_columns
# @brief List of column names present in salesdf_filtered but not in inputdf
extra_columns = list(set(dv.salesdf_filtered.columns) - set(inputdf.columns))

# Create a new dataframe with the extra columns from df2 and fill them with 0
inputdf = pd.concat([inputdf] + [pd.DataFrame(False, index=inputdf.index, columns=[col]) for col in extra_columns], axis=1)

inputdf = inputdf.reindex(columns=dv.salesdf_filtered.columns)
inputdf = inputdf.drop(['unit_sales'], axis=1)

#inputdf.loc[:, inputdf.columns != 'dcoilwtico'].replace(0, False, inplace=True)

print('inputdf after adding columns', inputdf.shape)
print('dv.salesdf_filtered', dv.salesdf_filtered.shape)
print(inputdf)
print(dv.salesdf_filtered)

## @var y_pred
# @brief Predicted unit sales values
y_pred = loaded_model.predict(inputdf)


# Undoing the rescaling:
## @fn undo_rescaling(y_pred)
# @brief Undo the rescaling applied to the predicted values
# @param y_pred Predicted unit sales values
# @return Undo-scaled predicted values
y_pred = y_pred * (dv.max_train - dv.min_train) + dv.min_train
# min_oil, max_oil
print(y_pred.shape)
inputdfout['unitsales_pred'] = y_pred

# Read the output directory path from output_directory_path.txt
with open('output_directory_path.txt', 'r') as file:
    output_directory = file.read().strip()

# Save the output dataframe to the specified output directory
output_file_path = os.path.join(output_directory, 'output.csv')
inputdfout.to_csv(output_file_path, index=False)

print(inputdfout['unitsales_pred'].max())
print(inputdfout['unitsales_pred'].min())
