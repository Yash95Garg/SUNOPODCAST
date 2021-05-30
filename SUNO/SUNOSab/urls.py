from django.conf.urls import url
from SUNOSab import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^register$',views.registerApi),
    url(r'^register/([0-9]+)$',views.registerApi),
] 