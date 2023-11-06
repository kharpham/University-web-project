from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("item/<int:item_id>", views.view_item, name="view_item"),
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("item/<int:item_id>/add_item", views.add_item, name="add_item"),
    path("item/<int:item_id>/remove_item", views.remove_item, name="remove_item"),
]
