from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('privacy-policy/', views.Privacy, name='privacy'),
    path('customer-support/', views.Support, name='support'),
    path('search/', views.ProductSearch, name='search'),
    path('products/', views.ProductList, name='products'),
    path('products/<str:sku>/', views.ProductDetail, name='product_detail'),
    path('products/collection/', views.ProductCategories, name='collection'),
    path('product/', views.ProductDetail, name='product-detail'),
    path('basket/', views.Basket, name='basket'),
    path('order-confirmation/', views.OrderConfirmation, name='confirm'),
    path('dashboard/', views.Dashboard, name='Dashboard'),
]
