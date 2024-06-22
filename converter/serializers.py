from rest_framework import serializers
from .models import ConversionHistory

class ConversionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistory
        fields = '__all__'
