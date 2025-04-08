from pydoc import render_doc
from tkinter import E

from django.http import JsonResponse
from product.models import Product, ProductImage
from django.shortcuts import redirect, get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Product, Cart, Order, OrderItem
from users.models import Address

def add_to_cart(request, product_id):
    print('product_id', product_id)
    product = get_object_or_404(Product, uid=product_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if product is already in cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1  # Increase quantity if already exists
            cart_item.save()

        messages.success(request, "Product added to cart!")
    else:
        messages.error(request, "You need to log in first!")

    return redirect('get_product', slug=product.slug)

def buy_now(request, product_id):
    product = get_object_or_404(Product, uid=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Add product to cart (if not already there)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1  # Increase quantity if already exists
            cart_item.save()

        return redirect('cart:checkout')  # Redirect to checkout
    else:
        messages.error(request, "Please log in to place an order.")

    return redirect('get_product', slug=product.slug)

@login_required
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    addresses = Address.objects.filter(user=request.user)
    selected_address_id = request.POST.get("selected_address")

    # Fetch selected address (if changed)
    selected_address = Address.objects.filter(uid=selected_address_id).first() if selected_address_id else addresses.first()

    if request.method == "POST":
        selected_address_uid = request.POST.get("selected_address")
        selected_address = Address.objects.get(uid=selected_address_uid)
        
    if not cart or not cart.cartitem_set.exists():  # Ensure both cart and items exist
        messages.error(request, "Your cart is empty.")
        return redirect("index")  # Redirect to cart page

    cart_items = cart.cartitem_set.all()  # Fetch CartItem objects
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        if not selected_address:
            messages.error(request, "Please fill all the required fields.")
            return redirect("cart:checkout")

        # Create a new order for the user
        order = Order.objects.create(user=user, status="Pending")

        # Add products to the order using OrderItem
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Clear cart after checkout
        cart.cartitem_set.all().delete()  # Delete cart items instead of clearing products

        messages.success(request, "Your order has been placed successfully!")
        return redirect("cart:order_success") 

    return render(request, "cart/checkout.html", {"cart_items": cart_items, "total_price": total_price, "addresses": addresses, "selected_address": selected_address})

def order_success(request):
    return render(request, "cart/order_success.html")

@login_required
def get_cart_data(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.products.exists():
        return JsonResponse({"cart_items": []})  # Return empty list if cart is empty

    cart_items = []
    for item in cart.products.all():
        first_image = ProductImage.objects.filter(product=item).first()  # Get the first image

        cart_items.append({
            "name": item.product_name,
            "price": item.price,
            "quantity": item.cartitem_set.get(cart=cart).quantity,
            "image": first_image.image.url if first_image else "",  # Use first image if available
        })

    return JsonResponse({"cart_items": cart_items})

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart:checkout")

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity becomes 0

    return redirect("cart:checkout")

@login_required
def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    messages.success(request, "Item removed from cart.")
    return redirect("cart:checkout")

@login_required
def my_orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("orderitem_set__product")
    return render(request, "cart/my_orders.html", {"orders": user_orders})

@login_required
def my_orders(request):
    status_filter = request.GET.get("status", "")  # Get status filter from request
    orders = Order.objects.filter(user=request.user)

    if status_filter:
        orders = orders.filter(status=status_filter)  # Apply filter if selected

    return render(request, "cart/my_orders.html", {"orders": orders})

@login_required
def cancel_order(request, order_uid):
    order = get_object_or_404(Order, uid=order_uid, user=request.user)

    if order.status == "Pending":  # Allow cancel only if Pending
        order.delete()
        messages.success(request, "Your order has been cancelled successfully.")
    else:
        messages.error(request, "You can only cancel pending orders.")

    return redirect("cart:my_orders")