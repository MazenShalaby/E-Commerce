from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .models import Category, Product
from cart.forms import CartAddForm

# Create your views here.

@cache_page(60*30)
def product_list(request, category_slug=None):

    categories = Category.objects.prefetch_related("category_products")
    
    if category_slug:
        cache_key = f"products_{category_slug}"
    else:
        cache_key = "products_all"

    products = cache.get(cache_key)
    
    if products is None:
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.select_related('category').filter(category=category)
        else:
            products = Product.objects.select_related('category')

        cache.set(cache_key, products, timeout=60*30) # 30 minutes  

    context = {
        'products': products,
        'categories': categories,
        }
    return render(request, 'inventory/product_list.html', context)


@cache_page(60*30)
def product_detail(request, product_slug):
    
    cache_key = f"product_{product_slug}"
    product = cache.get(cache_key)
    
    if product is None:
        product = get_object_or_404(Product, slug=product_slug)
        cache.set(cache_key, product, timeout=60*30) # 30 minutes 

    cart_add_form = CartAddForm(request.POST)
    
    context = {
        'product': product,
        'cart_add_form': cart_add_form
        }
    return render(request, 'inventory/product_detail.html', context)


@cache_page(60*30)
def product_search(request):
    query = request.GET.get('query', '')
    result = Product.objects.none()
    result_count = 0
    
    if query:
        
        cache_key = f"search_{query}"
        cached_data = cache.get(cache_key)
        
        if cached_data is None: 
        
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
            cache.set(cache_key, {"result": result, "result_count": result_count}, timeout=60 * 15) # 15 min
        else:
            result = cached_data.get("result")
            result_count = cached_data.get("result_count")

    context = {
        'result': result,
        'result_count': result_count,
        }
    return render(request, 'inventory/product_search.html', context)