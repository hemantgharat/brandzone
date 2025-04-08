from pydoc import render_doc
from tkinter import E
from django.shortcuts import render
from product.models import Product
from .models import Product

def get_product(request , slug):
    try:
        product = Product.objects.get(slug=slug)
        return render(request, 'products/product.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, 'base/404.html', status=404)  # Render a custom 404 page
    except Exception as e:
        print("Error", e)
        return render(request, 'base/error.html', {'message': 'Something went wrong'}, status=500)  # Handle other errors
