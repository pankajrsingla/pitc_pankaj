from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.list_customers, name='list_customers'),
    # Other URL patterns
]