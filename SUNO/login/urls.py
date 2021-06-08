from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('here', views.success),
    path('verify/<auth_token>' , views.verify),
    path('blog', views.add_blog),
    path('blog_delete/<str:id>',views.blog_delete),
    path('blog_get', views.blogHome),
    path('forgot', views.forgot),
    path('password/<auth_token>' , views.change),
    path('logout', views.logout_view),
    path('profile', views.ProfilePage),
    path('add_event', views.add_event),
    path('event_delete/<str:id>',views.event_delete),
    path('event_get', views.eventHome),
]
