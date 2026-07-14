from django.urls import path

from .views import product_add, product_remove, cart_detail

# create your urlpatterns here.


urlpatterns = [
    path("", cart_detail, name="cart-detail"),
    path("add/<slug:product_slug>/", product_add, name="product-add"),
    path("remove/<slug:product_slug>/", product_remove, name="product-remove"),
]
