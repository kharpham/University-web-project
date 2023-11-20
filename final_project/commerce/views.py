from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Item
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    # Get index page
    # Set up Pagination
    p = Paginator(Item.objects.all(), 12)
    page = request.GET.get('page')
    items = p.get_page(page)

    # if request.user.is_authenticated:
    return render(request,'commerce/index.html', {
        "items": items,
    }) 
    # else:
    #     return HttpResponseRedirect(reverse('login'))

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


@login_required
def view_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        shopping_cart = request.user.shopping_cart.all()
    except Item.DoesNotExist:
        return HttpResponse("Item not found")
    return render(request, "commerce/view_item.html", {
        "item": item,
        "shopping_cart": shopping_cart,
    })

@login_required
def shopping_cart(request):
    items = request.user.shopping_cart.all()
    return render(request, 'commerce/shopping_cart.html', {
        "items": items,
    })

@login_required
def add_item(request, item_id):
    try: 
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return HttpResponse("Item not found")
    request.user.shopping_cart.add(item)
    request.user.save()
    return HttpResponseRedirect(reverse('view_item', args=[item.id]))

@login_required
def remove_item(request, item_id):
    try: 
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return HttpResponse("Item not found")
    request.user.shopping_cart.remove(item)
    request.user.save()
    return HttpResponseRedirect(reverse('view_item', args=[item.id]))

def loi_login(request):
    return render(request,'commerce/loi_login.html')

def loi_aboutus(request):
    return render(request, 'commerce/loi_aboutus.html')

def loi_register(request):
    return render(request, 'commerce/loi_register.html')
