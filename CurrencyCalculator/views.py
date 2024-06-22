from django.shortcuts import render , redirect
from django.http import JsonResponse
import numpy as np
import tensorflow as tf


# Load the trained model
model = tf.keras.models.load_model('model/currency_predictor.h5')

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def convert_currency(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        from_currency = request.POST['from_currency']
        to_currency = request.POST['to_currency']

        # Dummy data for example; in practice, use real data
        example_data = np.random.rand(60, 10)  # Example data

        prediction = model.predict(np.array([example_data]))
        converted_amount = prediction[0][0] * amount

        # Save conversion to history
        ConversionHistory.objects.create(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
            converted_amount=converted_amount
        )

        return JsonResponse({'converted_amount': converted_amount})

    return render(request, 'converter/home.html')
