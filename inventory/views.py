from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

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


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    context = {'product': product}
    return render(request, 'inventory/product_detail.html', context)


def product_search(request):
    query = request.GET.get('query', '')
    result = Product.objects.none()
    result_count = 0
    
    if query:
        search_vector = SearchVector('name', 'description', 'category__name')
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vector, search_query)
        
        result = Product.objects.annotate(
            search=search_vector,
            rank=search_rank
        ).filter(
            search=search_query,
            quantity__gt=0
        ).order_by('-rank')
        result_count = result.count()
    
    context = {
        'result': result,
        'result_count': result_count,
        }
    return render(request, 'inventory/product_search.html', context)