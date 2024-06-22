from django import forms

class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    currency_pair = forms.CharField(label='Currency Pair', max_length=6)

class ConversionForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    source_currency = forms.CharField(label='Source Currency', max_length=3)
    target_currency = forms.CharField(label='Target Currency', max_length=3)