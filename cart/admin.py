from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__product_name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['order__user__username', 'product__product_name']
