from django.urls import path
from . import views
from .views import ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('api/products/', ProductListAPIView.as_view(), name='api_product_list'),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
]