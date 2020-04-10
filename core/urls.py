from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('about/', views.about, name='about'),
    path('search-customer/', views.search_customer, name='search-customer'),
    path('add-transaction/', views.add_transaction, name='add-transaction'),
    path('user/<int:pk>/update', user_views.UserUpdateView.as_view(), name='user_update'),
]