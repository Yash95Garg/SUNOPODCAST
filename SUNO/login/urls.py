from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('here', views.success),
    path('verify/<auth_token>' , views.verify),
]
