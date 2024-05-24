from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.ContactPage, name='contact'),
    path('privacy-policy/', views.PrivacyPage, name='privacy'),
    path('cookie-policy/', views.CookiePage, name='cookie'),
    path('customer-support/', views.SupportPage, name='support'),
    path('search/', views.ProductSearch, name='search'),
    path('products/', views.ProductList, name='products'),
    path('products/<str:sku>/', views.ProductDetail, name='product_detail'),
    path('products/collection/', views.ProductCategories, name='collection'),
    path('product/', views.ProductDetail, name='product-detail'),
    path('basket/', views.Basket, name='basket'),
    path('basket_quantity_update/<int:transaction_id>/', views.basket_quantity_update, name='basket_quantity_update'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('order-confirmation/<str:order_number>/', views.OrderConfirmation, name='confirm'),
    # PROFILE
    path('profile/', views.profile, name='profile'),
    path('profile/update_billing/', views.update_billing, name='update_billing'),
    path('profile/update_shipping/', views.update_shipping, name='update_shipping'),
    path('orders/', views.orders, name='orders'),
    path('orders/<str:order_number>/', views.OrderDetail, name='order_detail'),
    # Stripe
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
    # ADMIN
    path('dashboard/', views.Dashboard, name='Dashboard'),
]
