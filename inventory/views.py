from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product

# Create your views here.


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    categories = Category.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category, quantity__gt=0)
    
    context = {
        'products': products,
        'categories': categories,
        }
    return render(request, 'inventory/product_list.html', context)