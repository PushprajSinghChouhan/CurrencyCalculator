
from django.urls import path
from converter import views

urlpatterns = [
   
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('convert/', views.ConvertCurrency.as_view(), name='convert_currency'),
    path('history/', views.ConversionHistoryView.as_view(), name='conversion_history'),
    path('predict/', views.PredictCurrency.as_view(), name='predict_currency'),
    path('financial-analysis/', views.financial_analysis, name='financial_analysis'),
]
