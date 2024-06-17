## @mainpage Sales prediction project
#
# @section author Authors:
#
# Sadegh Naderi, Raunak Shahare, Deepti Hegde
#
#
# @section intro_sec Introduction
#
# This documentation serves as a comprehensive guide to understand, utilize, and extend the functionality of the sales
# prediction model. The codebase is designed to assist businesses in forecasting sales figures, enabling them to make
# informed decisions and optimize their operations.
#
# The project is done by following the kdd process.
#
# ![KDD process](KDDProcess.jpg)
#
# @subsection loading Data loading:
#
# The codebase loads data from multiple CSV files, including information about stores, items,
# transactions, oil prices, holidays, and historical sales. Each dataset is loaded into a separate Pandas DataFrame,
# facilitating data manipulation and analysis.
#
# @subsection blending Data blending
#
# The codebase provides a function to blend the sales data with additional information from other datasets, such as
# stores, items, holidays, and oil prices. This consolidation enhances the dataset with relevant features for accurate
# sales prediction.Data is merged using the key columns seen in this picture:
#
# ![Data blending](DataBlending.jpg)
#
# @subsection transformation Data transformation Techniques
#
# The codebase applies various data transformation techniques, including one-hot encoding and re-scaling of variables.
# One-hot encoding converts categorical variables into numerical representations, while re-scaling ensures that the
# data is within a consistent range for model training.
#
#
# @subsection fitting Regression model fitting
#
# The codebase trains an XGBoost regression model on the preprocessed sales data.
# It splits the data into training and testing sets, fits the model to the training data, and generates predictions for
# the test data.
#
# @subsection evaluation Model evaluation and visualization
#
# The codebase evaluates the performance of the trained model using evaluation metrics such as R2 score and
# mean squared error (MSE). It also provides visualizations, including a scatter plot comparing true sales values
# with predicted sales values, enabling users to assess the accuracy of the predictions visually.
# This pictures shows the results of the evaluation process:
#
# ![Prediction diagram](Prediction.png)
#
# @subsection monitor Data monitoring
#
# The codebase includes monitoring functionalities to check for missing values in the loaded dataframes.
# It displays the number of missing values for each dataframe, allowing users to identify and handle missing data
# effectively.
#
# @section start Getting Started
#
# To get started with the Sales Prediction codebase, ensure that you have the required packages installed.
# The codebase relies on Pandas, NumPy, Matplotlib, XGBoost, and scikit-learn. Once the dependencies are set up,
# you can proceed with loading the data and following the step-by-step instructions in the codebase.


##
# @file development.py
#
# @brief This code file is created in order to do the development of the sales prediction



# Loading the packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.model_selection import KFold, GridSearchCV, train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import pickle

##
# @var dtypes
# A dictionary that defines the data types of various columns in the sales DataFrame.
dtypes = {'store_nbr': np.dtype('int64'),
          'item_nbr': np.dtype('int64'),
          'unit_sales': np.dtype('float64'),
          'onpromotion': np.dtype('O')}    # each element can have a different data type


# Data Loading

##
# @var stores
# The pandas DataFrame that stores the information about stores.
# @var items
# The pandas DataFrame that stores the information about items.
# @var trans
# The pandas DataFrame that stores the information about transactions.
# @var oil
# The pandas DataFrame that stores the information about oil prices.
# @var holidays
# The pandas DataFrame that stores the information about holidays and events.
# @var sales
# The pandas DataFrame that stores the sales data.
# @var salesdf
# A copy of the sales DataFrame used for test functions.


stores = pd.read_csv('Data/stores.csv')
stores = pd.read_csv('Data/stores.csv')
items = pd.read_csv('Data/items.csv')
trans = pd.read_csv('Data/transactions.csv')
oil = pd.read_csv('Data/oil.csv')
holidays = pd.read_csv('Data/holidays_events.csv')
sales = pd.read_csv('Data/trainnew.csv', dtype=dtypes)
salesdf = sales    # This is done for the ease of use of test functions for the sales object


# Monitoring:
if __name__ == "__main__":
    ##
    # @var dataframes
    # A dictionary that stores the various dataframes used in the code for monitoring purposes.
    dataframes = {
        'stores': stores,
        'items': items,
        'trans': trans,
        'oil': oil,
        'holidays': holidays,
        'sales': sales
    }

    for name, df in dataframes.items():
        na_counts = df.isnull().sum()
        na_columns = na_counts[na_counts > 0]
        if not na_columns.empty:
            print("NA counts for '{}' dataframe:".format(name))
            print(na_columns)
            print()


    print(salesdf.head(3))


# Monitoring: Print the shape of loaded dataframes
if __name__ == "__main__":
    for name, df in dataframes.items():
        print("Shape of '{}' dataframe: {}".format(name, df.shape))
    # Monitoring:
    print(sales.info())


# Data Blending


def process_sales_data(inputdfr, stores=stores, items=items, holidays=holidays, oil=oil):
    """! Merges all the datasets.
    @brief Processes the sales data by merging it with additional information from other datasets.
    @param inputdfr: The input DataFrame containing the sales data.
    @param stores: The pandas DataFrame that stores the information about stores (default: stores).
    @param items: The pandas DataFrame that stores the information about items (default: items).
    @param holidays: The pandas DataFrame that stores the information about holidays and events (default: holidays).
    @param oil: The pandas DataFrame that stores the information about oil prices (default: oil).
    @return the merged dataset
    """
    blendeddf = inputdfr.drop('id', axis=1)
    blendeddf = blendeddf.merge(stores, left_on='store_nbr', right_on='store_nbr', how='left')
    blendeddf = blendeddf.merge(items, left_on='item_nbr', right_on='item_nbr', how='left')
    blendeddf = blendeddf.merge(holidays, left_on='date', right_on='date', how='left')
    blendeddf = blendeddf.merge(oil, left_on='date', right_on='date', how='left')
    blendeddf = blendeddf.drop(['description', 'state', 'locale_name', 'class'], axis=1)
    return blendeddf


salesdf = process_sales_data(inputdfr=salesdf)

# Monitoring:
if __name__ == "__main__":
    print(salesdf.head(3))
    print(salesdf.columns)

# Monitoring:
if __name__ == "__main__":
    print(salesdf.info())
    print(salesdf.isnull().sum())
    print(salesdf.head(3))



salesdf_filtered = salesdf

# Fill in cells if there is no holiday by the value : "no_holyday"
salesdf_filtered.loc[salesdf_filtered['type_y'].isnull(), 'type_y'] = "no_holyday"
salesdf_filtered.loc[salesdf_filtered['locale'].isnull(), 'locale'] = "no_locale"
salesdf_filtered.loc[salesdf_filtered['transferred'].isnull(), 'transferred'] = "no_holyday"


def get_month_year(df):
    """! Maps a number from one range to another.
    @brief Extract month and year from the date
    @param df: The input dataframe
    @return The dataframe with added 'month' and 'year' columns
    """

    df['month'] = df.date.apply(lambda x: x.split('-')[1])
    df['year'] = df.date.apply(lambda x: x.split('-')[0])

    return df


get_month_year(salesdf_filtered)

salesdf_filtered['date'] = pd.to_datetime(salesdf_filtered['date'])
salesdf_filtered['day'] = salesdf_filtered['date'].dt.day_name()
salesdf_filtered = salesdf_filtered.drop('date', axis=1)


# Monitoring: count the NAs
if __name__ == "__main__":
    print(salesdf_filtered.isnull().sum())

salesdf_filtered['dcoilwtico'] = salesdf_filtered['dcoilwtico'].fillna(salesdf_filtered['dcoilwtico'].mean())


salesdf_clean = salesdf_filtered.copy()

# Monitoring: count the NAs
if __name__ == "__main__":
    print(salesdf_filtered.isnull().sum())

# Data Transformation Techniques
# One hot Encoding

##
# @var dummy_variables
# A list of variables used for one-hot encoding.
dummy_variables = ['onpromotion', 'city', 'type_x', 'cluster', 'store_nbr', 'item_nbr',
                   'family', 'perishable', 'type_y', 'locale', 'transferred', 'month', 'day']

## @var mini
# @brief The minimum value of the current variable
## @var maxi
# @brief The maximum value of the current variable
for var in dummy_variables:
    dummy = pd.get_dummies(salesdf_filtered[var], prefix=var, drop_first=False)
    salesdf_filtered = pd.concat([salesdf_filtered, dummy], axis=1)

salesdf_filtered = salesdf_filtered.drop(dummy_variables, axis=1)
salesdf_filtered = salesdf_filtered.drop(['year'], axis=1)

# Monitoring:
if __name__ == "__main__":
    print(salesdf_filtered.dtypes)

# Re-scale
# We keep this value to re-scale the predicted unit_sales values in the following lines of code.

##
# @var min_train
# The minimum value of the 'unit_sales' column in the salesdf_filtered DataFrame.
# @var max_train
# The maximum value of the 'unit_sales' column in the salesdf_filtered DataFrame.
min_train, max_train = salesdf_filtered['unit_sales'].min(), salesdf_filtered['unit_sales'].max()
min_oil, max_oil = salesdf_filtered['dcoilwtico'].min(), salesdf_filtered['dcoilwtico'].max()

##
# @var scalable_variables
# A list of variables to be re-scaled.
scalable_variables = ['unit_sales', 'dcoilwtico']

for var in scalable_variables:
    mini, maxi = salesdf_filtered[var].min(), salesdf_filtered[var].max()
    salesdf_filtered.loc[:, var] = (salesdf_filtered[var] - mini) / (maxi - mini)


# Monitoring:
if __name__ == "__main__":
    print(salesdf_filtered.head(3))

# train database without unit_sales
salesdf_filtered = salesdf_filtered.reset_index(drop=True)  # we reset the index
columns_dev = salesdf_filtered.columns

##
# @var y
# The target variable 'unit_sales' from the salesdf_filtered DataFrame.
# @var X
# The input features DataFrame obtained by dropping the 'unit_sales' column from salesdf_filtered.
y = salesdf_filtered['unit_sales']
X = salesdf_filtered.drop(['unit_sales'], axis=1)

##
# @var num_test
# The proportion of the dataset to include in the test split.
# @var X_train
# The training input features obtained after splitting the data.
# @var X_test
# The testing input features obtained after splitting the data.
# @var y_train
# The training target variable obtained after splitting the data.
# @var y_test
# The testing target variable obtained after splitting the data.
# @var col_X_test
# The column names of the X_test DataFrame.
num_test = 0.20    # the proportion of the dataset to include in the test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=num_test, random_state=15)
col_X_test = X_test.columns

if __name__ == "__main__":
    print("Number of columns:", X_train.shape[1])

##
# @var model
# The XGBoost regression model.
# Regression Model fitting
# @var y_pred
# The predicted values of the target variable obtained from the model.
if __name__ == "__main__":
    model = XGBRegressor(max_depth=5)
    model.fit(X_train, y_train)

    # Save the trained model to a file
    model_filename = 'xgboost_model.pkl'
    pickle.dump(model, open(model_filename, 'wb'))

model_filename = 'xgboost_model.pkl'
loaded_model = pickle.load(open(model_filename, 'rb'))
y_pred = loaded_model.predict(X_test)

# Monitoring:
if __name__ == "__main__":
    print('R2 score using XG Boost= ', r2_score(y_test, y_pred), '/ 1.0')
    print('MSE score using XG Boost= ', mean_squared_error(y_test, y_pred), '/ 0.0')

    plt.plot(y_test.values[:50], '+', color='blue', alpha=0.7, label='True Sales')
    plt.plot(y_pred[:50], 'ro', alpha=0.5, label='Predicted Sales')
    plt.xlabel('Sample Index')
    plt.ylabel('Sales')
    plt.title('True Sales vs Predicted Sales')
    plt.legend()
    plt.savefig('Figure_Output/TrueSalesvsPredicted.png', dpi=300, bbox_inches='tight')
    plt.show()

