from django.urls import path

from .views import product_list, product_detail, product_search

# create your urlpatterns here.


urlpatterns = [
    path('product-list/', product_list, name='product-list'),
    path('product-list/<slug:category_slug>/', product_list, name='categorized-product-list'),
    path('product-detail/<slug:product_slug>/', product_detail, name='product-detail'),
    path('search/', product_search, name='product-search'),
]
