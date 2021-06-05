from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def login(request):
    author = request.data.get('username')
    title = request.data.get('password')
    print(author)
    print(title)
    object = Post.objects.create(author=author,title=title)
    object.save()
    return HttpResponse("success")