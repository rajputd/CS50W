from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

import json
import re

from .forms import *
from .models import *
from .helpers.view_helper import *

# Create your views here.
def index(request):
    context = {'user': request.user}
    return render(request, 'orders/index.html', context)

def menu(request):
    pizzas = getPizzaMenu()
    toppings = Topping.objects.all()
    subs = getSubMenu()
    addons = getSubAddons()
    entrees = getEntrees()
    sizes = Size.objects.all()

    context = {
        'pizzas': pizzas,
        'toppings': toppings,
        'subs': subs,
        'addons': addons,
        'user': request.user,
        'entrees': entrees,
        'sizes': sizes,
    }

    return render(request, 'orders/menu.html', context)

def location(request):
    context = {'user': request.user}
    return render(request, 'orders/location.html', context)

def hours(request):
    context = {'user': request.user}
    return render(request, 'orders/hours.html', context)

def sicilian_v_regular(request):
    context = {'user': request.user}
    return render(request, 'orders/sicilian_v_regular.html', context)

def contact(request):
    context = {'user': request.user}
    return render(request, 'orders/contact.html', context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if not form.is_valid():
            render(request, "orders/login.html", {"error": "Username/Password is too long to be valid"})

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("menu"))
        else:
            return render(request, "orders/login.html", {"error": "Invalid credentials."})
    else:
        return render(request, 'orders/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'orders/login.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if not form.is_valid():
            render(request, "orders/login.html", {"error": "Username/Password is too long to be valid"})

        firstname = form.cleaned_data["firstname"]
        lastname = form.cleaned_data["lastname"]
        email = form.cleaned_data["email"]
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if User.objects.filter(username=username).exists():
            return render(request, 'orders/register.html', {'error': 'the username ' + username + ' is already taken'})

        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        return render(request, 'orders/login.html')
    else:
        return render(request, 'orders/register.html')


def shopping_cart(request):
    #if user is not logged in redirect them to login page
    if not request.user.is_authenticated:
        return reverse("login")

    if request.method == "GET":
        #see if user has a pre-existing order
        order = Order.objects.filter(customer=request.user, status=OrderStatus.objects.get(status="unsubmitted"))

        #create a new order for the user if one doesn't already exist
        if (len(order) == 0):
            order = Order(customer=request.user, status=OrderStatus.objects.get(status="unsubmitted")).save()
            order = Order.objects.filter(customer=request.user, status=OrderStatus.objects.get(status="unsubmitted"))
        else:
            #otherwise use the one found earlier
            order = order[0]

        context = {
            'order': order,
            'toppings': Topping.objects.all(),
            'pizza_types': PizzaType.objects.all(),
            'sizes': Size.objects.all(),
            'pizzas': Pizza.objects.all(),
            'pizza_names': getUniquePizzaNames(),
            'subs': Sub.objects.all(),
            'addons': Addon.objects.all(),
            'entrees': Entree.objects.all(),
            'entree_types': EntreeType.objects.all()
        }

        return render(request, 'orders/shopping_cart.html', context)

def add_pizza_to_cart(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    #parse form fields related to pizza
    pizza_type = PizzaType.objects.get(name=request.POST["pizzaType"])
    size = Size.objects.get(size=request.POST["size"])
    name = request.POST["itemName"]
    quantity = request.POST["quantity"]

    #create a pizza and loop up the order to attach it to.
    pizza = Pizza.objects.get(name=name, pizza_type=pizza_type, size=size)
    main_order = Order.objects.get(pk=request.POST["order"])

    #attach the pizza to the order and save
    pizza_order = PizzaOrder(order=main_order, pizza=pizza, quantity=quantity)
    pizza_order.save()

    #add all of the toppings request to the order
    pattern = re.compile("topping-[0-9]")
    for key, value in enumerate(request.POST):
        if pattern.match(value):
            topping_name = request.POST[value]
            topping = Topping.objects.get(name=topping_name)
            topping_order = ToppingsOrder(pizzaOrder=pizza_order, topping=topping)
            topping_order.save()

    return HttpResponseRedirect(reverse("shopping_cart"))



def add_entree_to_cart(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    #parse form fields related to pizza
    entree_type = EntreeType.objects.get(name=request.POST["entreeType"])
    size = Size.objects.get(size=request.POST["size"])
    name = request.POST["itemName"]
    quantity = request.POST["quantity"]

    #create a pizza and loop up the order to attach it to.
    entree = Entree.objects.get(name=name, entree_type=entree_type, size=size)
    main_order = Order.objects.get(pk=request.POST["order"])

    #attach the pizza to the order and save
    entree_order = EntreeOrder(order=main_order, entree=entree, quantity=quantity)
    entree_order.save()

    return HttpResponseRedirect(reverse("shopping_cart"))

def add_sub_to_cart(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    #parse form fields related to item
    size = Size.objects.get(size=request.POST["size"])
    sub_id = request.POST["subName"]
    quantity = request.POST["quantity"]

    #create a item and loop up the order to attach it to.
    sub = Sub.objects.get(pk=sub_id)
    main_order = Order.objects.get(pk=request.POST["order"])

    #attach the item to the order and save
    sub_order = SubOrder(order=main_order, sub=sub, quantity=quantity)
    sub_order.save()

    #add all of the toppings request to the order
    pattern = re.compile("addon-[0-9]")
    for key, value in enumerate(request.POST):
        if pattern.match(value):
            name = request.POST[value]
            addon = Addon.objects.get(name=name)
            addon_order = AddonOrder(subOrder=sub_order, addon=addon)
            addon_order.save()

    return HttpResponseRedirect(reverse("shopping_cart"))

def remove_order_item(request, order_type, id):
    if order_type == "pizza":
        order = PizzaOrder.objects.get(pk=id)
    elif order_type == "topping":
        order = ToppingsOrder.objects.get(pk=id)
    elif order_type == "sub":
        order = SubOrder.objects.get(pk=id)
    elif order_type == "addon":
        order = AddonOrder.objects.get(pk=id)
    elif order_type == "entree":
        order = EntreeOrder.objects.get(pk=id)
    else:
        return HttpResponseForbidden()

    order.delete()


    return HttpResponseRedirect(reverse("shopping_cart"))

def submit_order(request):
    order = Order.objects.filter(customer=request.user, status=OrderStatus.objects.get(status="unsubmitted"))[0]
    order.status = OrderStatus.objects.get(status="submitted")
    order.save()

    return HttpResponseRedirect(reverse("order_history"))

def order_history(request):

    #if user is not logged in redirect them to login page
    if not request.user.is_authenticated:
        return reverse("login")

    history = Order.objects.filter(customer=request.user).order_by('-date')

    context = {
        'history' : history
    }

    return render(request, 'orders/order_history.html', context)

def reciept(request, order_id):
    order = Order.objects.get(pk=order_id)
    context = {'order' : order}
    return render(request, 'orders/reciept.html', context)

def google_maps_dependency(request):
    return HttpResponseRedirect("https://maps.googleapis.com/maps/api/js?key="  + settings.GOOGLE_MAPS_API_KEY + "&callback=initMap")