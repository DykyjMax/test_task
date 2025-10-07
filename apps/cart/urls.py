from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart', views.cart_detail, name='detail'),
    path('cart/add/', views.add_to_cart, name='add'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_item'),
]