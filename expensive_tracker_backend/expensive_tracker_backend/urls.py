"""expensive_tracker_backend URL Configuration

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
from django.urls import path, include, re_path
from transactions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('transactions.urls')),
    # api/v1/auth/users : register a new user
    # api/v1/auth/me: retrieve/update the currently logged in user
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    # api/v1/accounts/profiles/: get all user profiles and create a new one
    # api/v1/accounts/profiles/id: detail view of a user's profile
    path('api/v1/users/', include('users.urls')),
    path('', views.HomePage.as_view())
    # path('/login', views.home)
]
