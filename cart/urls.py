"""brandzone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from cart.views import add_to_cart,buy_now, cancel_order,checkout, decrease_quantity, increase_quantity,order_success, get_cart_data, remove_item, my_orders
from django.urls import path
app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<str:product_id>/', add_to_cart, name='add_to_cart'),
    path('buy-now/<str:product_id>/', buy_now, name='buy_now'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('data/', get_cart_data, name='get_cart_data'),
    path("decrease_quantity/<int:item_id>/", decrease_quantity, name="decrease_quantity"),
    path("increase_quantity/<int:item_id>/", increase_quantity, name="increase_quantity"),
    path("remove_item/<int:item_id>/", remove_item, name="remove_item"),
    path("my-orders/", my_orders, name="my_orders"),
    path("cancel-order/<uuid:order_uid>/", cancel_order, name="cancel_order"),
]
