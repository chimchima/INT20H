from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
#from django.contrib.auth.views import login, logout
from django.contrib.auth.views import LoginView, PasswordResetView
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'parsing'

urlpatterns = [
    path('', views.index, name='index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)