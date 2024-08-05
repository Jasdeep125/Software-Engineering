from django.urls import path
from . import views


urlpatterns = [
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('details/', views.account_details, name='account_details'),
    path('register/', views.register, name='register'),
]
