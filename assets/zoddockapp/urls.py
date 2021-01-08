"""zoddock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    home_page,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    AddCouponView,
    Menshoes,
    RequestRefundView,
    #Shoes
)
#from zoddockapp import views



urlpatterns = [
    path('women_jeans_page/',HomeView.as_view(), name='women_jeans_page'),
    path('', home_page, name="home_page"),
    path('menshoes/', Menshoes, name="menshoes"),
    path('product/<slug>/', ItemDetailView.as_view(), name = 'product_detail'),
    path('add-to-cart/<slug>/', add_to_cart, name = "add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name = "remove-from-cart"),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name = "remove-single-item-from-cart"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary" ),
    path('check_out/',CheckoutView.as_view(), name='check_out'),
    path('payment/<payment_option>/', PaymentView.as_view(),name="payment" ),
    path('add-coupon/', AddCouponView.as_view(), name = 'add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name="request-refund")
    
]

# urlpatterns = [
#     path('', views.home_page,name="home_page"),
#     path('item_list',HomeView.as_view(),name='women_jeans_page'),
#     path('add_to_cart_page',views.add_to_cart_page,name='add_to_cart_page'),
#     path('cart',views.cart,name='cart'),
#     path('check_out',check_out.as_view(),name='check_out'),
#     path('product/<slug>/',ItemDetailView.as_view(),name='product'),
#     path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
#     path('add-coupon/', AddCouponView.as_view(), name='add_coupon'),
#     path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
#     path('remove_from_cart/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_form_cart'),
#     path('order-summary/',OrderSummaryView.as_view(), name='cart'),
#     path('payment/<payment_option>/',PaymentView.as_view(), name='payment')',
#     path('request-refund/', RequestRefundReview.as_view(), name='request-refund')
    
# ]


# urlpatterns = [
    # path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    # path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    # path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    # # path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    # # path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    # path('cart', views.cart, name='cart'),
    # path('check_out', views.check_out, name='check_out'),
    # path('', views.home_page,name="home_page"),
    # path('women_jeans_page',views.women_jeans_page,name='women_jeans_page'),
# ]
