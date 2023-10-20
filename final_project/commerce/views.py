from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from .models import User
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,'commerce/index.html') 
    else:
        return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.method == "POST":
        # Sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "commerce/login.html", {
                "message": "Invalid username/password.",
            })
    return render(request, 'commerce/login.html')

def register_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if confirmation != password:
            return render(request, "commerce/register.html", {
                'message': 'Confirmation must match password.',
            })

        # Create new user
        try: 
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "commerce/register.html", {
                "message": "Email or Username already taken.", 
            })
        login(request, user)

    return render(request, 'commerce/register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

