from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # admin dashboard URLs
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_account/', views.create_account, name='create_account'),
    path('edit_account/<int:account_id>/', views.edit_account, name='edit_account'),
    path('view_account/<int:account_id>/', views.view_account, name='view_account'),
    path('close_account/<int:account_id>/', views.close_account, name='close_account'),
    
    
    # customer dashboard URLS
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('deposit/<int:account_id>/', views.deposit, name='deposit'),
    path('withdraw/<int:account_id>/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('view_account/<int:account_id>/', views.view_account, name='view_account'),
    path('request_checkbook/<int:account_id>/', views.request_checkbook, name='request_checkbook'),
    path('close_account/<int:account_id>/', views.close_account, name='close_account'),
    
    
]
