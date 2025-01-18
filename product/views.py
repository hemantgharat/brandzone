from pydoc import render_doc
from tkinter import E
from django.shortcuts import render
from product.models import Product




def get_product(request , slug):
    try:
        products = Product.objects.get(slug =slug)
        return render(request  , 'product/product.html' , context = {'product' : products})

    except Exception as e:
        print(e)