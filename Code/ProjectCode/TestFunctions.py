# Test functions for Sales prediction project
# Authors:
# Deepti Hegde
# intro_sec Introduction TestFuctions
# The test functions behave to confirm the data’s integrity and evaluate the prediction model’s performance.
# They provide useful feedback on the data reading process, missing values, and model accuracy,
# which aids in the detection and resolution of potential code errors.


# Loading the packages
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor
import pytest
from sklearn.model_selection import train_test_split
from development import stores, items, trans, oil, holidays, sales, salesdf_clean, y_test, y_pred
from deployment import inputdf, inputdfTest, inputdfTestRead

# A class for performing data validation tests.
class TestDataValidation:

    # Test function to verify CSV file reading and column presence.
    def test_csv_read(self):
        # Assert that the DataFrames are not empty
        assert not stores.empty, "Failed to read 'stores.csv'"
        assert not items.empty, "Failed to read 'items.csv'"
        assert not trans.empty, "Failed to read 'transactions.csv'"
        assert not oil.empty, "Failed to read 'oil.csv'"
        assert not holidays.empty, "Failed to read 'holidays_events.csv'"
        assert not sales.empty, "Failed to read 'train.csv'"
        assert not inputdf.empty, "Failed to read 'train.csv'"

        # Assert that the necessary columns are present
        expected_columns = ['id', 'date', 'store_nbr', 'item_nbr', 'unit_sales', 'onpromotion']
        assert all(col in sales.columns for col in expected_columns), "Missing columns in 'train.csv'"

        expected_columns_input = ['date', 'store_nbr', 'item_nbr', 'onpromotion', 'city', 'type_x', 'cluster','family', 'perishable', 'type_y', 'locale', 'transferred', 'dcoilwtico']
        assert all(col in inputdfTestRead.columns for col in expected_columns_input), "Missing columns in 'input.csv'"

        print("CSV files read successfully.")

    # Test function to check for missing values in salesdf_clean DataFrame.
    def test_missing_values(self):
        # Assuming salesdf_clean is already defined and contains the DataFrame

        # Check for missing values in salesdf_clean
        has_missing_values = salesdf_clean.isnull().values.any()
        has_missing_values_input = inputdfTest.isnull().values.any()

        # Assert that there are no missing values
        assert not has_missing_values, "salesdf_clean contains missing values (NaN or NA)"
        assert not has_missing_values_input, "salesdf_clean contains missing values (NaN or NA)"

        print("No missing values found in salesdf_clean.")

    # Test function to evaluate the model's performance.
    def test_prediction_function(self):
        # Evaluate the model's performance
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        # Perform assertions on the performance metrics
        assert r2 == pytest.approx(0.033, abs=0.15)
        assert mse == pytest.approx(0.00013, abs=0.0001)

    def run_tests(self):
        self.test_csv_read()
        self.test_missing_values()
        self.test_prediction_function()

if __name__ == '__main__':
    data_validation = TestDataValidation()
    data_validation.run_tests()
