from django.urls import path

from .views import order_create, order_payment, success_payment

# create your urlpatterns here.


urlpatterns = [
    path('create/', order_create, name='order-create'),
    path('payment/<int:order_id>/', order_payment, name='order-payment'),
    path('success/<int:order_id>/', success_payment, name='success-payment'),
]
