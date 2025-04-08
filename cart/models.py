from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.utils.text import slugify
from product.models import Product

class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(Product, through="CartItem")

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in {self.cart.user.username}'s cart"


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through="OrderItem")
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.uid} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.uid}"
