from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('about/', views.about, name='about'),
    path('search-customer/', views.search_customer, name='search-customer'),
    path('add-transaction/', views.add_transaction, name='add-transaction'),
]