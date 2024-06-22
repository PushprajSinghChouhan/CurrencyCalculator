import requests
from .models import ConversionHistory
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model


def load_exchange_rate_model():
    return load_model('model/currency_predictor.h5')

def fetch_exchange_rate(source_currency, target_currency):
    api_url = f"https://openexchangerates.org/api/latest.json?app_id=4229ab1419bd4525b0a7db1e14bc1022"
    response = requests.get(api_url).json()
    rates = response['rates']
    return rates[target_currency] / rates[source_currency]

def get_historical_data(source_currency, target_currency):
    api_url = f"https://api.exchangerate.host/timeseries?start_date=2023-01-01&end_date=2023-01-31&base={source_currency}&symbols={target_currency}"
    response = requests.get(api_url).json()
    return response['rates']

def get_financial_news():
    api_url = f"https://newsapi.org/v2/everything?q=currency&apiKey=9db267bc552b4502a7260911d92fc97a"
    response = requests.get(api_url).json()
    return response['articles']

def predict_exchange_rate(source_currency, target_currency):
    model = tf.keras.models.load_model('model/currency_predictor.h5')
    # Example prediction logic
    historical_data = np.array([[1, 2, 3], [4, 5, 6]])  # Dummy data
    predictions = model.predict(historical_data)
    return predictions
