from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.utils.text import slugify


class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories/")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Product(BaseModel):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

def product_image_upload_path(instance, filename):
    return f'products/{instance.product.slug}/{filename}'

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to=product_image_upload_path)

    class Meta:
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.product_name}"