from django.shortcuts import render
from product.models import Product
# Create your views here.
def index(request):
    context = {'products' : Product.objects.all()}
    print(context)
    return render(request , 'home/index.html' , context)

def product_list(request):
    query = request.GET.get("q", "")
    products = Product.objects.all()

    if query:
        products = products.filter(product_name__icontains=query)  # Case-insensitive search

    return render(request, "home/product_list.html", {"products": products, "query": query})
