from django import http
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage

# Create your views here.
@api_view(['GET'])
def success(request):
    return HttpResponse("hey there")

#@api_view(['POST'])
#def post(request):
#    title = request.data.get('title')
#    description = request.data.get('description')
#    uploaded_file = request.FILES['document']
#    fs = FileSystemStorage()
#    name = fs.save(uploaded_file.name, uploaded_file)
#    url = fs.url(name)
#    print(url)
#    print(author)
#    print(title)
#    object = Post.objects.create(author=author,title=title,description=description,imageurl=url)
#    object.save()
#    return HttpResponse("success")

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user_obj = User.objects.filter(username = username).first()
    if user_obj is None:
        return HttpResponse("Username Not Exists")
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if not profile_obj.is_verified:
        return HttpResponse("Please Verify Your Account")

    user = authenticate(username = username , password = password)
    if user is None:
        return HttpResponse("login Unsuccessful")
    else:
        #login(request , user)
        return HttpResponse("login successful")

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    try:
        if User.objects.filter(username = username).first():
            return HttpResponse("Username Already Exists")

        if User.objects.filter(email = email).first():
            return HttpResponse("Email Already Exists")   
        
        user_obj = User.objects.create_user(username=username, email=email, password=password)     
        user_obj.save()
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
        profile_obj.save()
        send_mail_after_registration(email , auth_token)
        return HttpResponse("Email Sent Successfully")

    except Exception as e:
        print(e)

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
        if profile_obj:
            if profile_obj.is_verified:
                return HttpResponse("Profile Already Verified")
            
            profile_obj.is_verified = True
            profile_obj.save()
            return HttpResponse("Your Account has been verified successfully")
        else:
            return HttpResponse("Error While Verifying")
    except Exception as e:
        print(e)
        return HttpResponse("Not verified Successfully")


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi Click the link to verify your account http://127.0.0.1:8000/api/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


#FORGOT PASSWORD
@api_view(['GET','POST'])
def forgot(request):
    if request.method == 'GET':
        return HttpResponse("Forgot Page")
    if request.method == 'POST':        
        email = request.data.get('email')
        user_obj = User.objects.filter(email = email).first()
        if user_obj is None:
            return HttpResponse("User Not Exists")
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if not profile_obj.is_verified:
            return HttpResponse("Please Verify Your Account")
        auth_token = profile_obj.auth_token
        send_mail_for_forgot(email , auth_token)
        return HttpResponse("Mail Sent Successfully")

@api_view(['GET','POST'])
def change(request , auth_token):
    if request.method == 'GET':
        return HttpResponse("Enter Details")
    
    if request.method == 'POST':
        try:
            profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
            if profile_obj:
                if not profile_obj.is_verified:
                    return HttpResponse("Profile is not verified")
            
                user = profile_obj.user
                password = request.data.get('password')
                user.set_password(password)
                user.save()
                return HttpResponse("Your Password has been changed successfully")
            else:
                return HttpResponse("Error While Changing Password")
        except Exception as e:
            print(e)
            return HttpResponse("Not Changed Successfully")        

def send_mail_for_forgot(email , token):
    subject = 'Request For Password Change'
    message = f'Hi Click the link to change your password http://127.0.0.1:8000/api/password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


@api_view(['GET'])
def ProfilePage(request):
    if request.method == 'GET':
        user = User.objects.filter(username = "suno").first()
        Profile = UserProfile.objects.filter(user = user).first()
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        profileimage = Profile.profileimage
        bio = Profile.bio
        doc = {username : username, first_name : first_name, last_name: last_name, profileimage : profileimage, bio : bio}
        return HttpResponse(doc)


#LOGOUT
def logout_view(request):
    logout(request)


@api_view(['POST'])
def add_blog(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        imageurl = fs.url(name)
        title = request.POST.get('title')
        description = request.POST.get('description')
        user = User.objects.filter(username = "suno").first()
        blog_obj = Blog(
            author = user , title = title, 
            description = description, imageurl = imageurl
            )
        blog_obj.save()
        print(blog_obj)
        return HttpResponse("Added")
    
@api_view(['DELETE'])
def blog_delete(request , id):
    try:
        blog_obj = Blog.objects.get(id = id)
        user = User.objects.filter(username = "suno").first()
        if blog_obj.author == user:
            blog_obj.delete()
            return HttpResponse("Delete")
        
    except Exception as e :
        print(e)


@api_view(['GET'])
def blogHome(request): 
    allPosts=Blog.objects.all()
    context={'allPosts': allPosts} 
    return HttpResponse(allPosts)


@api_view(['POST'])
def add_event(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        imageurl = fs.url(name)
        title = request.data.get('title')
        user = User.objects.filter(username = "suno").first()
        description = request.data.get('description')
        tag = request.data.get('tag')
        event_on = request.data.get('event_on')
        blog_obj = Event(
            author = user , title = title, 
            description = description, imageurl = imageurl,tag=tag,
            event_on = event_on
            )
        blog_obj.save()
        print(blog_obj)
        return HttpResponse("Added")

@api_view(['DELETE'])
def event_delete(request , id):
    try:
        blog_obj = Event.objects.get(id = id)
        user = User.objects.filter(username = "suno").first()
        if blog_obj.author == user:
            blog_obj.delete()
            return HttpResponse("Delete")
        
    except Exception as e :
        print(e)


@api_view(['GET'])
def eventHome(request): 
    allPosts=Event.objects.all()
    context={'allPosts': allPosts} 
    return HttpResponse(allPosts)

            
