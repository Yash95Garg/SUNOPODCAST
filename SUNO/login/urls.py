from django.urls import path
from . import views

urlpatterns = [
    path('post', views.post),
    path('login', views.login),
    path('register', views.register),
    path('here', views.success),
]
