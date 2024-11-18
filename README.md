Gold Price Prediction
This project focuses on predicting gold prices using advanced machine learning models, data preprocessing techniques, and a robust deployment setup. It involves data collection, feature reduction, model training, and end-to-end deployment with Docker, GCP, and MySQL.

Table of Contents
Overview
Features
Tech Stack
Data Pipeline
Modeling and Evaluation
Frontend and Backend
Deployment
Setup and Installation
Usage
Acknowledgments
Overview
The project utilizes six years of gold price data scraped from Yahoo Finance. The data undergoes preprocessing, feature extraction, and modeling using state-of-the-art techniques like PCA, XGBoost, LightGBM, Random Forest, ARIMA, SARIMA, and LSTM. It is deployed using a Flask backend and a React frontend with containerization for scalability.

Features
Data Collection: Automated data scraping from Yahoo Finance.
Data Cleaning and Visualization: Handling missing values, outliers, and insightful visualizations.
Feature Engineering: PCA for dimensionality reduction.
Model Training: Multiple models for accurate prediction:
XGBoost
LightGBM
Random Forest
ARIMA
SARIMA
LSTM
Database Integration: MySQL for storing and retrieving cleaned datasets.
Containerization: Dockerized components for ease of deployment.
Cloud Deployment: NGINX as a reverse proxy, GCP for cloud infrastructure.
User Interface: React frontend for visualization and interaction.
Tech Stack
Programming Languages: Python, JavaScript, TypeScript
Frontend: React.js
Backend: Flask
Database: MySQL
Modeling Libraries: Scikit-learn, XGBoost, LightGBM, TensorFlow/Keras, Statsmodels
Visualization Tools: Matplotlib, Seaborn, Plotly
Containerization: Docker
Web Server: NGINX
Cloud Services: Google Cloud Platform (GCP)
Data Pipeline
Data Collection: Scraped six years of historical data using Yahoo Finance API.
Data Cleaning: Removed null values and anomalies, standardized the dataset.
Feature Engineering: Applied PCA for dimensionality reduction.
Database Storage: Inserted cleaned data into MySQL tables for structured storage.
Modeling and Evaluation
Algorithms Used:
Gradient Boosting (XGBoost, LightGBM)
Random Forest
Time Series Models (ARIMA, SARIMA)
Deep Learning (LSTM)
Evaluation Metrics:
Mean Squared Error (MSE)
Root Mean Squared Error (RMSE)
Mean Absolute Error (MAE)
Frontend and Backend
Frontend:

Built using React.js for dynamic and interactive data visualization.
Charts and plots for showcasing predictions and trends.
Backend:

Flask-based API for serving prediction results and handling user requests.
Integrated with MySQL for data retrieval.
Deployment
Containerization: All components (frontend, backend, database, and models) are Dockerized.
Reverse Proxy: NGINX for routing and load balancing.
Cloud Hosting: Deployed on Google Cloud Platform (GCP).
Setup and Installation
Prerequisites
Python 3.8+
Node.js 16+
Docker and Docker Compose
MySQL
GCP Account
Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/abhijantheja/gold-predictor.git
cd gold-price-prediction
Install Python dependencies:

bash
Copy code
pip install -r requirements.txt
Install frontend dependencies:

bash
Copy code
cd frontend
npm install
Build Docker images:

docker-compose build
Run the application:

docker-compose up
Access the app at:
https://gold-predictor.vercel.app/

Usage
Navigate to the frontend application.
Upload a dataset or fetch predictions for specific dates.
Visualize trends and predictions through interactive plots.
Acknowledgments
Yahoo Finance for historical data.
Open-source libraries and tools: Scikit-learn, TensorFlow, Flask, React, and Docker.
Feel free to customize the URLs, repository links, and other specific details.