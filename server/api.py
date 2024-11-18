# Part 1: Import Libraries and Initial Setup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go
import plotly.express as px
import mysql.connector
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import warnings
warnings.filterwarnings('ignore')


# Step 1: Define function to connect to the MySQL database and load data
def create_connection():
    connection = mysql.connector.connect(
        host="34.100.164.75", 
        user="root",
        password="RahulAbhi@1234",
        database="updated_gold_price_prediction"
    )
    return connection

def load_data_from_db():
    conn = create_connection()
    query = "SELECT * FROM merged_gold_prediction"
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Step 2: Load the data from MySQL database
data = load_data_from_db()

class GoldPricePreprocessing:
    def __init__(self):
        self.scaler = StandardScaler()
        self.price_scaler = MinMaxScaler()

    def create_index(es, index_name):
        mapping = {
        "mappings": {
            "properties": {
                "field1": {"type": "text"},
                "field2": {"type": "integer"},
            }
        }
    }
    
    def load_and_clean_data(self, data):
        # Convert dates and set index
        df = data.copy()
        df['date_id'] = pd.to_datetime(df['date_id'])
        df.set_index('date_id', inplace=True)
        df = self.clean_data(df)
        return df

    def clean_data(self, df):
        df = df.dropna(axis=1)
        return df

preprocessor = GoldPricePreprocessing()
processed_df = preprocessor.load_and_clean_data(data)

class FeatureEngineering1:
    @staticmethod
    def create_features(df):
        # Create technical indicators
        df_features = df.copy()

        # Price related features
        df_features['Price_Return'] = df_features['close'].pct_change()
        df_features['Price_MA5'] = df_features['close'].rolling(window=5, min_periods=1).mean()
        df_features['Price_MA20'] = df_features['close'].rolling(window=20, min_periods=1).mean()
        df_features['Price_MA50'] = df_features['close'].rolling(window=50, min_periods=1).mean()

        # Volume features (if 'volume' column exists)
        if 'volume' in df_features.columns:
            df_features['Volume_MA5'] = df_features['volume'].rolling(window=5, min_periods=1).mean()
            df_features['Volume_MA20'] = df_features['volume'].rolling(window=20, min_periods=1).mean()

        # List of relevant columns for correlation matrix
        relevant_columns = [
            'open', 'high', 'close', 'volume', 
            'sp_open', 'sp_high', 'sp_low', 'sp_close', 'sp_ajclose'
        ]
        relevant_columns = [col for col in relevant_columns if col in df_features.columns]

        # Calculate and visualize the correlation matrix
        if relevant_columns:
            df_relevant = df_features[relevant_columns]
            correlation_matrix = df_relevant.corr()

        # Scatter plots for Gold Price vs other assets
        assets_to_compare = ['sp_close', 'dj_close', 'eu_price', 'of_price', 'plt_price', 'pld_price', 'usdi_price']
        asset_colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink']



        # Remove highly correlated features based on a threshold
        correlation_matrix = df_features.corr()
        threshold = 0.8
        correlated_features = set()

        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                colname = correlation_matrix.columns[i]
                if colname != 'close' and abs(correlation_matrix.iloc[i, j]) > threshold:
                    correlated_features.add(colname)

        remaining_features = [col for col in df_features.columns if col not in correlated_features or col == 'close']
        

        return df_features[remaining_features]

# Example usage
# Assuming processed_df is your pre-processed DataFrame
# processed_df = pd.read_csv("your_data.csv")  # Example for loading the DataFrame
feature_engineer = FeatureEngineering1()
final_df = feature_engineer.create_features(processed_df)  # Replace 'processed_df' with your actual DataFrame

from sklearn.decomposition import PCA

class ModelTrainer:
    def __init__(self, n_components=None):
        self.scaler = StandardScaler()
        self.correct_classification_threshold = 0.05  # 5% threshold for "correct" predictions
        self.pca = PCA(n_components=n_components)

    def prepare_data(self, df):
        # Prepare features and target
        feature_columns = [col for col in df.columns if col != 'close']
        X = df[feature_columns]
        y = df['close'].shift(-1)  # Next day's closing price

        # Remove rows with NaN
        valid_rows = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[valid_rows]
        y = y[valid_rows]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Apply PCA
        X_train_pca = self.pca.fit_transform(X_train_scaled)
        X_test_pca = self.pca.transform(X_test_scaled)

        return pd.DataFrame(X_train_pca), pd.DataFrame(X_test_pca), y_train.reset_index(drop=True), y_test.reset_index(drop=True)

    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        models = {
            'XGBoost': xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
            'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
            
        }

        results = {}
        predictions = {}
        correct_classifications = {}

        for name, model in models.items():
                if name == 'LSTM':
                    y_pred = self.predict_lstm(model, X_test)
                elif name == 'HMM':
                    y_pred = self.predict_hmm(model, X_test)
                elif name in ['ARIMA', 'SARIMA']:
                    y_pred = model.predict(start=len(y_train), end=len(y_train) + len(y_test) - 1)
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)

                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)

                correct_predictions = np.abs((y_test - y_pred) / y_test) <= self.correct_classification_threshold
                correct_classifications[name] = correct_predictions.sum()

                results[name] = {'MSE': mse, 'RMSE': rmse, 'R2': r2, 'MAE': mae}
                predictions[name] = y_pred
        
        return results, predictions


# Usage
trainer = ModelTrainer(n_components=5)  # Specify the number of PCA components
X_train, X_test, y_train, y_test = trainer.prepare_data(final_df)
results, predictions = trainer.train_and_evaluate(X_train, X_test, y_train, y_test)



class DatePredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.correct_classification_threshold = 0.05  # 5% threshold for "correct" predictions
        self.models = {}  # Store trained models for later use
       
    def prepare_data(self, df):
        # Prepare features and target
        feature_columns = [col for col in df.columns if col != 'close']
        X = df[feature_columns]
        y = df['close'].shift(-1)  

        # Remove rows with NaN
        valid_rows = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[valid_rows]
        y = y[valid_rows]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )
        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )
        
        return X_train_scaled, X_test_scaled, y_train, y_test, X, y

    def train_and_store_models(self, X_train, y_train):
        # Define traditional models
        self.models = {
            'XGBoost': xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
           
            'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        }

        # Train traditional models
        for name, model in self.models.items():
           
            model.fit(X_train, y_train)



    def predict_for_date(self, input_date, df):


        # Extract the feature data for the given date
        input_data = df.loc[input_date].drop('close')
        input_data_scaled = self.scaler.transform(input_data.values.reshape(1, -1))

        # Generate predictions using each model
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(input_data_scaled)[0]


        return predictions

# Usage
# Assuming final_df is your prepared DataFrame with a 'close' column
trainer = DatePredictor()
X_train, X_test, y_train, y_test, X, y = trainer.prepare_data(final_df)
trainer.train_and_store_models(X_train, y_train)
# Flask app
app = Flask(__name__)
CORS(app)

def create_merged_table(connection, date_of_interest):
    print("Fetching neighbor data...")
    query = f"""
        SELECT date_id, close
        FROM merged_gold_prediction
        WHERE date_id BETWEEN DATE_SUB('{date_of_interest}', INTERVAL 7 DAY)
                          AND DATE_ADD('{date_of_interest}', INTERVAL 7 DAY)
           OR date_id = '{date_of_interest}';
    """
    # Fetch data into a DataFrame
    merged_query_data = pd.read_sql(query, connection)
    
    # Ensure 'close' column is converted to native float
    merged_query_data['close'] = merged_query_data['close'].astype(float)
    
    # Create dictionary with string keys and string values
    date_close_dict = {
        str(row['date_id']): f"{row['close']:.2f}"  # Explicit conversion to float and formatting
        for _, row in merged_query_data.iterrows()
    }
    
    # Convert the dictionary to JSON-compatible string
    total_data_json = json.dumps(date_close_dict)
    
    print("Data in JSON format:", total_data_json)  # Debugging statement
    return total_data_json

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_date = request.json.get('date')  # Extract 'date' from the POST request
        print(f"Received date: {input_date}")  # Debugging statement

        # Get the merged data in JSON format
        total_data_json = create_merged_table(create_connection(), input_date)
        
        # Predictions logic remains the same
        predictions = trainer.predict_for_date(input_date, final_df)
        print("Predictions:", predictions)  # Debugging statement

        # Find the best model with the maximum prediction value
        best_model, best_prediction = max(predictions.items(), key=lambda x: x[1])

        # Return the best model, its prediction, and the total value in JSON format
        return jsonify({
            "best_model": best_model,
            "prediction": float(best_prediction),  # Convert to float for JSON compatibility
            "total_data": total_data_json  # Include the total data as a JSON-compatible string
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8080)

# Run the Flask app
