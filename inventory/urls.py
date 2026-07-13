from django.urls import path

from .views import product_list

# create your urlpatterns here.


urlpatterns = [
    path('product-list/', product_list, name='product-list'),
    path('product-list/<slug:category_slug>/', product_list, name='categorized-product-list'),
]
