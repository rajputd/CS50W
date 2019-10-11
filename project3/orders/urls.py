from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("location", views.location, name="location"),
    path("hours", views.hours, name="hours"),
    path("sicilian_v_regular", views.sicilian_v_regular, name="sicilian_v_regular"),
    path("contact", views.contact, name="contact"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("shopping_cart", views.shopping_cart, name="shopping_cart"),
    path("add_pizza_to_cart", views.add_pizza_to_cart, name="add_pizza_to_cart"),
    path("add_sub_to_cart", views.add_sub_to_cart, name="add_sub_to_cart"),
    path("add_entree_to_cart", views.add_entree_to_cart, name="add_entree_to_cart"),
    path("remove_order_item/<slug:order_type>/<int:id>", views.remove_order_item, name="remove_order_item"),
    path("order_history", views.order_history, name="order_history"),
    path("submit_order", views.submit_order, name="submit_order"),
    path("reciept/<int:order_id>", views.reciept, name="reciept"),
    path("google_maps_dependency", views.google_maps_dependency, name="google_maps_dependency")
]
