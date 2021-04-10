"""nessues URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

import nessues_app.views as views
import nessues_app_users.views as users_views
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', users_views.login_view, name='login'),
    path('logout/', users_views.logout_view, name='logout'),
    path('register/', users_views.register_view, name='register'),
    path('account/', users_views.account_view, name='account'),
    path('admin/', admin.site.urls),

    # path('login/', auth_views.LoginView.as_view(template_name='nessues_app_users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='nessues_app_users/logout.html'), name='logout'),
]
