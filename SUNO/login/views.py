from django import http
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
@api_view(['GET'])
def success(request):
    return HttpResponse("hey there")

@api_view(['POST'])
def post(request):
    author = request.data.get('username')
    title = request.data.get('password')
    print(author)
    print(title)
    object = Post.objects.create(author=author,title=title)
    object.save()
    return HttpResponse("success")

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return HttpResponse("login successful")
    else:
        return HttpResponse("login unsuccessful")

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    user = User.objects.create_user(username=username, email=email, password=password)
    if user is not None:
        return HttpResponse(user)
    else:
        return HttpResponse("login unsuccessful")        