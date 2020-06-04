"""shopnewark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from users.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('register/', user_views.register, name='register'),
    path('terms-conditions/', user_views.terms_conditions, name='terms_conditions'),
    path('logout/', user_views.logout_view, name='logout'),
    path('login/', user_views.login_view, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('tax-bank/', user_views.tax_bank, name="tax-bank"),
    path('transaction-data/', user_views.transaction_data, name='transaction_data'),
    path('special/', user_views.special, name='special'),
    path('advanced/', user_views.UserView.as_view(), name='advanced'),
    path('user/<int:pk>/update', user_views.UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/', user_views.UserDetailView.as_view(), name='user-detail'),
    ##reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]

handler404 = 'users.views.error_view_400'
handler500 = 'users.views.error_view'
handler403 = 'users.views.error_view_400'
handler400 = 'users.views.error_view_400'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
