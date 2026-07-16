from django.urls import path

from .views import order_create

# create your urlpatterns here.


urlpatterns = [
    path('create/', order_create, name='order-create'),
]
