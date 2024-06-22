import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ConversionHistory, CurrencyRate
from .forms import CurrencyConverterForm, ConversionForm
from .serializers import ConversionHistorySerializer
from .utils import fetch_exchange_rate, get_historical_data, get_financial_news, predict_exchange_rate, load_exchange_rate_model
import requests

# Load the trained model
model = tf.keras.models.load_model('model/currency_predictor.h5')
scaler = MinMaxScaler(feature_range=(0, 1))


def home(request):
    form = CurrencyConverterForm(request.POST or None)
    converted_amount = None

    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data['amount']
            currency_pair = form.cleaned_data['currency_pair']
            model = load_exchange_rate_model()
            predicted_rate = model.predict(currency_pair)
            converted_amount = amount * predicted_rate

    return render(request, 'converter/home.html', {'form': form, 'converted_amount': converted_amount})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        return redirect('login')
    return render(request, 'converter/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'converter/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def trend_analysis(request):
    pass

def predictive_insights(request):
    pass


class ConvertCurrency(APIView):
    def get(self, request):
        # Dummy implementation, replace with actual model predictions
        amount = float(request.query_params.get('amount', 1))
        source_currency = request.query_params.get('source_currency', 'USD')
        target_currency = request.query_params.get('target_currency', 'EUR')
        
        # Fetch exchange rate from an API
        response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id=4229ab1419bd4525b0a7db1e14bc1022")
        data = response.json()
        
        exchange_rate = data['rates'][target_currency] / data['rates'][source_currency]
        converted_amount = amount * exchange_rate
        
        # Save to history
        history = ConversionHistory(
            amount=amount,
            source_currency=source_currency,
            target_currency=target_currency,
            converted_amount=converted_amount,
            exchange_rate=exchange_rate
        )
        history.save()
        
        return Response({
            'amount': amount,
            'source_currency': source_currency,
            'target_currency': target_currency,
            'converted_amount': converted_amount,
            'exchange_rate': exchange_rate
        })

class ConversionHistoryView(APIView):
    def get(self, request):
        history = ConversionHistory.objects.all()
        serializer = ConversionHistorySerializer(history, many=True)
        return Response(serializer.data)

class PredictCurrency(APIView):
    def get(self, request):
        amount = float(request.query_params.get('amount', 1))
        source_currency = request.query_params.get('source_currency', 'USD')
        target_currency = request.query_params.get('target_currency', 'EUR')

        # Fetch exchange rate data (this should be replaced with actual historical data)
        response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id=4229ab1419bd4525b0a7db1e14bc1022")
        data = response.json()
        
        historical_rates = [data['rates'][source_currency], data['rates'][target_currency]]  # Example data
        historical_data = np.array(historical_rates).reshape(-1, 1)
        scaled_data = scaler.fit_transform(historical_data)

        seq_length = 60
        x_input = scaled_data[-seq_length:]
        x_input = x_input.reshape((1, seq_length, 1))

        predicted_rate = model.predict(x_input)[0][0]
        predicted_rate = scaler.inverse_transform([[predicted_rate]])[0][0]
        converted_amount = amount * predicted_rate

        return Response({
            'amount': amount,
            'source_currency': source_currency,
            'target_currency': target_currency,
            'predicted_rate': predicted_rate,
            'converted_amount': converted_amount
        })
    

def plot_to_html(fig):
    from io import BytesIO
    import base64

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return 'data:image/png;base64,' + string.decode('utf-8')

def financial_analysis(request):
    if request.method == 'POST':
        currency = request.POST['currency']
        data = pd.read_csv('exchange_rates.csv')
        fig, ax = plt.subplots()
        ax.plot(data['date'], data[currency], label=f'{currency} Exchange Rate')
        ax.set_xlabel('Date')
        ax.set_ylabel('Exchange Rate')
        ax.set_title(f'{currency} Exchange Rate Over Time')
        ax.legend()
        chart = plot_to_html(fig)
        
        return render(request, 'converter/analysis.html', {'chart': chart})
    return render(request, 'converter/analysis.html')


