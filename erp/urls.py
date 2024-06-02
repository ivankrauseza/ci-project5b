from django.urls import path
from . import views
from .views import product_edit, product_media_delete


urlpatterns = [
    path('erp/', views.erp, name='erp'),
    path('erp/products/', views.erp_products, name='erp_products'),
    path('erp/products/create/', views.product_create, name='erp_product_create'),
    path('erp/products/edit/<int:pk>/', product_edit.as_view(), name='erp_product_edit'),
    path('erp/products/delete/<int:pk>/', views.product_delete, name='erp_product_delete'),
    path('erp/media/delete/<int:pk>/', product_media_delete.as_view(), name='media_delete'),
    path('erp/orders/', views.erp_orders, name='erp_orders'),
    path('erp/order/<str:order_number>/', views.erp_order_detail, name='erp_order_detail'),
    # Company Information
    path('erp/company-information/', views.company, name='erp_company'),
    path('erp/staff/', views.staff, name='erp_staff'),
    path('erp/staff/profilekey/', views.staff, name='erp_staff'),
    # Add other URLs as needed
]
